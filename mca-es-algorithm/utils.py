import numpy as np
from hyperon import MeTTa

def create_metta_instance():
    metta = MeTTa()

    # Load utility functions and load to Metta instance
    with open("metta/util.metta") as f:
        util = f.read()

    util_atoms = metta.parse_all(util)
    for atom in util_atoms:
        metta.space().add_atom(atom)

    # Load update-mean function and load to Metta instance
    with open("metta/update-mean.metta") as f:
        update_mean = f.read()
    # print(update_mean)
    update_mean_atoms = metta.parse_all(update_mean)
    for atom in update_mean_atoms:
        metta.space().add_atom(atom)

    # Load update covariance function and load to Metta instance
    with open("metta/update-covariance.metta") as f:
        update_covariance = f.read()

    update_covariance_atoms = metta.parse_all(update_covariance)
    for atom in update_covariance_atoms:
        metta.space().add_atom(atom)

    # Load update step size function and load to Metta instance
    with open("metta/update-step-size.metta") as f:
        update_step_size = f.read()
    update_step_size_atoms = metta.parse_all(update_step_size)
    for atom in update_step_size_atoms:
        metta.space().add_atom(atom)
    
    return metta

def update_eigendecomposition(covariance_matrix):
    """Recompute eigen decomposition of covariance matrix."""
    covariance_matrix = np.triu(covariance_matrix) + np.triu(covariance_matrix, 1).T
    sqrt_eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    sqrt_eigenvalues = np.sqrt(np.maximum(sqrt_eigenvalues, 1e-30))
    inv_sqrt_covariance = eigenvectors @ np.diag(1 / sqrt_eigenvalues) @ eigenvectors.T
    return sqrt_eigenvalues, eigenvectors, inv_sqrt_covariance

def update_evolution_paths(
    evolution_path_sigma,
    evolution_path_cov,
    eigenvectors,
    weighted_random_mean,
    mean_vector,
    previous_mean,
    cumulation_time_constant_sigma,
    cumulation_time_constant_cov,
    effective_parent_count,
    step_size,
    expected_norm,
    dimension,
    generation,
):
    """Update evolution paths for sigma and covariance."""
    new_ps = (
        (1 - cumulation_time_constant_sigma) * evolution_path_sigma
        + np.sqrt(
            cumulation_time_constant_sigma
            * (2 - cumulation_time_constant_sigma)
            * effective_parent_count
        )
        * (eigenvectors @ weighted_random_mean)
    )

    hsig_condition = int(
        (np.linalg.norm(new_ps)
         / np.sqrt(1 - (1 - cumulation_time_constant_sigma) ** (2 * (generation + 1)))
         / expected_norm)
        < (1.4 + 2 / (dimension + 1))
    )

    new_pc = (
        (1 - cumulation_time_constant_cov) * evolution_path_cov
        + hsig_condition
        * np.sqrt(cumulation_time_constant_cov * (2 - cumulation_time_constant_cov) * effective_parent_count)
        * ((mean_vector - previous_mean) / step_size)
    )

    return new_ps, new_pc, hsig_condition

def update_step_size(step_size, evolution_path_sigma, cumulation_time_constant_sigma, damping_sigma, expected_norm):
    metta = create_metta_instance()
    # print(f"Current Step Size: {step_size} | Evolution Path Sigma: {evolution_path_sigma} | Cumulation Time Constant Sigma: {cumulation_time_constant_sigma} | Damping Sigma: {damping_sigma} | Expected Norm: {expected_norm}")
    # Parse Parameters
    evolution_path_sigma_atom = parse_list(evolution_path_sigma)

    updated_step_size = metta.run(f"!(update-step-size {step_size} {evolution_path_sigma_atom} {cumulation_time_constant_sigma} {damping_sigma} {expected_norm})")
    # print(f"Updated Step Size: {updated_step_size}")
    updated_step_size = float(str(updated_step_size[0][0]))
    # print(f"Formatted Step Size: {updated_step_size}")
    return updated_step_size

def update_covariance_matrix(
    covariance_matrix,
    evolution_path_cov,
    selected_solutions,
    previous_mean,
    recombination_weights,
    step_size,
    learning_rate_rank1,
    learning_rate_rank_mu,
    cumulation_time_constant_cov,
    hsig_condition,
):
    metta = create_metta_instance()

    # Parse Parameters
    covariance_matrix_atoms = parse_two_dim_list(covariance_matrix)
    evolution_path_cov_atoms = parse_list(evolution_path_cov)
    selected_solutions_atoms = parse_two_dim_list(selected_solutions)
    previous_mean_atoms = parse_list(previous_mean)
    recombination_weights_atoms = parse_list(recombination_weights)

    delta_mean_atom = metta.run(f"!(calculate-delta-mean {selected_solutions_atoms} {previous_mean_atoms} {step_size})")
    # print(f"Delta Mean Atom: {delta_mean}")
    delta_mean = convert_to_2d_list(str(delta_mean_atom[0][0]))
    # print(f"Delta Mean List: {delta_mean}")

    rank_one_update_atom = metta.run(f"!(rank-one-update {evolution_path_cov_atoms})")
    # print(f"Rank One: {rank_one_update}")
    rank_one_update = convert_to_2d_list(str(rank_one_update_atom[0][0]))
    # print(f"Rank One Done: {rank_one_update}")

    rank_mu_update_atom = metta.run(f"!(updateRankMu {recombination_weights_atoms} {delta_mean_atom[0][0]} {len(recombination_weights)})")
    # print(f"Rank MU: {rank_mu_update_atom}")
    rank_mu_update = convert_to_2d_list(str(rank_mu_update_atom[0][0]))
    # print(f"Formatted Rank Mu: {rank_mu_update}")

    updated_covariance_atom = metta.run(f"!(updateCov {learning_rate_rank1} {learning_rate_rank_mu} {rank_mu_update_atom[0][0]} {covariance_matrix_atoms} {rank_one_update_atom[0][0]} {hsig_condition} {cumulation_time_constant_cov})")
    # print(f"Updated Covariance Atom: {updated_covariance_atom}")
    updated_covariance = convert_to_2d_list(str(updated_covariance_atom[0][0]))
    # print(f"Updated Covariance Matrix: {updated_covariance}")
    
    # Ensure we have a square matrix with correct dimensions
    expected_dim = covariance_matrix.shape[0]
    
    try:
        updated_covariance_array = np.array(updated_covariance, dtype=float)
        
        # If dimensions don't match, pad or truncate
        if updated_covariance_array.ndim != 2:
            # If not 2D, try to reshape or return identity
            if updated_covariance_array.ndim == 1 and len(updated_covariance_array) == expected_dim * expected_dim:
                updated_covariance_array = updated_covariance_array.reshape(expected_dim, expected_dim)
            else:
                # Fallback to identity
                return np.eye(expected_dim) * np.mean(np.diag(covariance_matrix))
        
        # Ensure square and correct size
        if updated_covariance_array.shape[0] != expected_dim or updated_covariance_array.shape[1] != expected_dim:
            if updated_covariance_array.shape[0] >= expected_dim and updated_covariance_array.shape[1] >= expected_dim:
                updated_covariance_array = updated_covariance_array[:expected_dim, :expected_dim]
            else:
                # Pad with identity matrix
                padded = np.eye(expected_dim) * np.mean(np.diag(covariance_matrix))
                min_rows = min(updated_covariance_array.shape[0], expected_dim)
                min_cols = min(updated_covariance_array.shape[1], expected_dim)
                padded[:min_rows, :min_cols] = updated_covariance_array[:min_rows, :min_cols]
                updated_covariance_array = padded
                
    except (ValueError, TypeError) as e:
        # Fallback to original covariance matrix if parsing fails
        print(f"Warning: Failed to parse covariance matrix from meTTa: {e}")
        return covariance_matrix.copy()
 
    return updated_covariance_array

def parse_list(arr):
    return "(" + " ".join(map(str, arr)) + ")"

def parse_two_dim_list(arr):
    atoms = []
    for row in arr:
        atoms.append(parse_list(row))
    return "(" + " ".join(atoms) + ")"

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def convert_to_list(atom):
    atom_str = str(atom).strip("()")
    return [float(x) for x in atom_str.split()]

def convert_to_2d_list(atom):
    """Convert meTTa atom string to 2D list, ensuring consistent dimensions."""
    # Remove outer parentheses and clean up
    atom_str = str(atom).strip()
    if atom_str.startswith("(") and atom_str.endswith(")"):
        atom_str = atom_str[1:-1].strip()

    if ") (" in atom_str:
        rows_str = atom_str.split(") (")
        rows_str[0] = rows_str[0].lstrip("(").strip()
        rows_str[-1] = rows_str[-1].rstrip(")").strip()
    else:
        rows_str = [atom_str.strip("()")]
    
    res = []
    for row_str in rows_str:
        # Split by spaces and filter for floats
        row_list = row_str.split()
        row_acc = []
        for item in row_list:
            item_clean = item.strip().strip("()")
            if is_float(item_clean):
                row_acc.append(float(item_clean))
        if row_acc:  # Only add non-empty rows
            res.append(row_acc)
    
    # Ensure all rows have the same length (pad with zeros if needed)
    if res:
        max_len = max(len(row) for row in res)
        for row in res:
            while len(row) < max_len:
                row.append(0.0)
    
    return res

def update_mean(selected_solutions, recombination_weights):
    """Update the mean vector."""
    metta = create_metta_instance()
    recombination_weights_atoms = parse_list(recombination_weights)
    selected_solutions_atoms = parse_two_dim_list(selected_solutions)
    updated_mean = metta.run(f"!(update-mean {selected_solutions_atoms} {recombination_weights_atoms})")
    updated_mean = str(updated_mean[0][0]).strip("()")
    updated_mean=  [float(x) for x in updated_mean.split()] # TODO: use the function
    return updated_mean
