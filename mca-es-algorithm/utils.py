import numpy as np
from hyperon import MeTTa

def create_metta_instance():
    metta = MeTTa()  # meTTa interpreter instance

    # Load utility functions and load to Metta instance
    with open("metta/util.metta") as f:
        util = f.read()  # contents of util.metta

    util_atoms = metta.parse_all(util)  # parsed atoms from util.metta
    for atom in util_atoms:
        metta.space().add_atom(atom)

    # Load update-mean function and load to Metta instance
    with open("metta/update-mean.metta") as f:
        update_mean = f.read()  # contents of update-mean.metta
    # print(update_mean)
    update_mean_atoms = metta.parse_all(update_mean)  # parsed atoms for update-mean
    for atom in update_mean_atoms:
        metta.space().add_atom(atom)

    # Load update covariance function and load to Metta instance
    with open("metta/update-covariance.metta") as f:
        update_covariance = f.read()  # contents of update-covariance.metta

    update_covariance_atoms = metta.parse_all(update_covariance)  # parsed atoms for covariance update
    for atom in update_covariance_atoms:
        metta.space().add_atom(atom)

    # Load update step size function and load to Metta instance
    with open("metta/update-step-size.metta") as f:
        update_step_size = f.read()  # contents of update-step-size.metta
    update_step_size_atoms = metta.parse_all(update_step_size)  # parsed atoms for step size update
    for atom in update_step_size_atoms:
        metta.space().add_atom(atom)
    
    return metta

def update_eigendecomposition(covariance_matrix):
    """Recompute eigen decomposition of covariance matrix."""
    covariance_matrix = np.triu(covariance_matrix) + np.triu(covariance_matrix, 1).T  # symmetrized C
    sqrt_eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)  # eigen-decomposition of C
    sqrt_eigenvalues = np.sqrt(np.maximum(sqrt_eigenvalues, 1e-30))  # sqrt of eigenvalues (clipped)
    inv_sqrt_covariance = eigenvectors @ np.diag(1 / sqrt_eigenvalues) @ eigenvectors.T  # C^{-1/2}
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
    metta = create_metta_instance()  # meTTa runtime
    # print(f"Current Step Size: {step_size} | Evolution Path Sigma: {evolution_path_sigma} | Cumulation Time Constant Sigma: {cumulation_time_constant_sigma} | Damping Sigma: {damping_sigma} | Expected Norm: {expected_norm}")
    # Parse Parameters
    evolution_path_sigma_atom = parse_list(evolution_path_sigma)  # meTTa atom for ps

    updated_step_size = metta.run(f"!(update-step-size {step_size} {evolution_path_sigma_atom} {cumulation_time_constant_sigma} {damping_sigma} {expected_norm})")  # call meTTa
    # print(f"Updated Step Size: {updated_step_size}")
    updated_step_size = float(str(updated_step_size[0][0]))  # parse result to float
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
    metta = create_metta_instance()  # meTTa runtime

    # Parse Parameters
    covariance_matrix_atoms = parse_two_dim_list(covariance_matrix)  # C as meTTa atoms
    evolution_path_cov_atoms = parse_list(evolution_path_cov)  # pc as meTTa atoms
    selected_solutions_atoms = parse_two_dim_list(selected_solutions)  # selected X
    previous_mean_atoms = parse_list(previous_mean)  # previous mean m_t
    recombination_weights_atoms = parse_list(recombination_weights)  # weights w

    delta_mean_atom = metta.run(f"!(calculate-delta-mean {selected_solutions_atoms} {previous_mean_atoms} {step_size})")  # Δm/σ
    # print(f"Delta Mean Atom: {delta_mean}")
    delta_mean = convert_to_2d_list(str(delta_mean_atom[0][0]))  # parsed Δm matrix
    # print(f"Delta Mean List: {delta_mean}")

    rank_one_update_atom = metta.run(f"!(rank-one-update {evolution_path_cov_atoms})")  # pc pc^T
    # print(f"Rank One: {rank_one_update}")
    rank_one_update = convert_to_2d_list(str(rank_one_update_atom[0][0]))  # parsed rank-1 matrix
    # print(f"Rank One Done: {rank_one_update}")

    rank_mu_update_atom = metta.run(f"!(updateRankMu {recombination_weights_atoms} {delta_mean_atom[0][0]} {len(recombination_weights)})")  # Σ w_i y_i y_i^T
    # print(f"Rank MU: {rank_mu_update_atom}")
    rank_mu_update = convert_to_2d_list(str(rank_mu_update_atom[0][0]))  # parsed rank-μ matrix
    # print(f"Formatted Rank Mu: {rank_mu_update}")

    updated_covariance_atom = metta.run(f"!(updateCov {learning_rate_rank1} {learning_rate_rank_mu} {rank_mu_update_atom[0][0]} {covariance_matrix_atoms} {rank_one_update_atom[0][0]} {hsig_condition} {cumulation_time_constant_cov})")  # updated C
    # print(f"Updated Covariance Atom: {updated_covariance_atom}")
    updated_covariance = convert_to_2d_list(str(updated_covariance_atom[0][0]))  # parsed updated C
    # print(f"Updated Covariance Matrix: {updated_covariance}")
    
    # Ensure we have a square matrix with correct dimensions
    expected_dim = covariance_matrix.shape[0]  # expected square dimension
    
    try:
        updated_covariance_array = np.array(updated_covariance, dtype=float)  # to numpy array
        
        # If dimensions don't match, pad or truncate
        if updated_covariance_array.ndim != 2:
            # If not 2D, try to reshape or return identity
            if updated_covariance_array.ndim == 1 and len(updated_covariance_array) == expected_dim * expected_dim:
                updated_covariance_array = updated_covariance_array.reshape(expected_dim, expected_dim)  # reshape flat
            else:
                # Fallback to identity
                return np.eye(expected_dim) * np.mean(np.diag(covariance_matrix))  # scaled identity
        
        # Ensure square and correct size
        if updated_covariance_array.shape[0] != expected_dim or updated_covariance_array.shape[1] != expected_dim:
            if updated_covariance_array.shape[0] >= expected_dim and updated_covariance_array.shape[1] >= expected_dim:
                updated_covariance_array = updated_covariance_array[:expected_dim, :expected_dim]  # crop
            else:
                # Pad with identity matrix
                padded = np.eye(expected_dim) * np.mean(np.diag(covariance_matrix))  # base padding
                min_rows = min(updated_covariance_array.shape[0], expected_dim)
                min_cols = min(updated_covariance_array.shape[1], expected_dim)
                padded[:min_rows, :min_cols] = updated_covariance_array[:min_rows, :min_cols]
                updated_covariance_array = padded  # padded to expected size
                
    except (ValueError, TypeError) as e:
        # Fallback to original covariance matrix if parsing fails
        print(f"Warning: Failed to parse covariance matrix from meTTa: {e}")
        return covariance_matrix.copy()
 
    return updated_covariance_array

def parse_list(arr):
    return "(" + " ".join(map(str, arr)) + ")"  # convert 1D array to meTTa list string

def parse_two_dim_list(arr):
    atoms = []  # rows as strings
    for row in arr:
        atoms.append(parse_list(row))  # stringify row
    return "(" + " ".join(atoms) + ")"  # wrap as matrix

def is_float(value):
    try:
        float(value)
        return True  # is numeric
    except ValueError:
        return False  # not numeric
    
def convert_to_list(atom):
    atom_str = str(atom).strip("()")  # strip outer parens
    return [float(x) for x in atom_str.split()]  # parse numbers

def convert_to_2d_list(atom):
    """Convert meTTa atom string to 2D list, ensuring consistent dimensions."""
    # Remove outer parentheses and clean up
    atom_str = str(atom).strip()  # string form
    if atom_str.startswith("(") and atom_str.endswith(")"):
        atom_str = atom_str[1:-1].strip()  # drop surrounding parens

    if ") (" in atom_str:
        rows_str = atom_str.split(") (")  # split rows
        rows_str[0] = rows_str[0].lstrip("(").strip()
        rows_str[-1] = rows_str[-1].rstrip(")").strip()
    else:
        rows_str = [atom_str.strip("()")]
    
    res = []  # accumulate rows
    for row_str in rows_str:
        # Split by spaces and filter for floats
        row_list = row_str.split()  # tokens
        row_acc = []  # numeric row
        for item in row_list:
            item_clean = item.strip().strip("()")  # clean token
            if is_float(item_clean):
                row_acc.append(float(item_clean))
        if row_acc:  # Only add non-empty rows
            res.append(row_acc)
    
    # Ensure all rows have the same length (pad with zeros if needed)
    if res:
        max_len = max(len(row) for row in res)  # widest row length
        for row in res:
            while len(row) < max_len:
                row.append(0.0)  # right-pad with zeros
    
    return res

def update_mean(selected_solutions, recombination_weights):
    """Update the mean vector."""
    metta = create_metta_instance()  # meTTa runtime
    recombination_weights_atoms = parse_list(recombination_weights)  # weights as atoms
    selected_solutions_atoms = parse_two_dim_list(selected_solutions)  # selected X as atoms
    updated_mean = metta.run(f"!(update-mean {selected_solutions_atoms} {recombination_weights_atoms})")  # call meTTa
    updated_mean = str(updated_mean[0][0]).strip("()")  # get list string
    updated_mean=  [float(x) for x in updated_mean.split()]  # parse to floats
    return updated_mean
