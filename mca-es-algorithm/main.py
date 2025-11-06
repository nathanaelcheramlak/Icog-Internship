from hyperon import MeTTa
import numpy as np
from utils import *

def cma_es(fitness_function, dimension=5, max_iterations=200, random_seed=42):
    """CMA-ES optimizer.

    Parameters
    - fitness_function: callable that maps a candidate vector -> scalar loss
    - dimension: int, problem dimensionality
    - max_iterations: int, number of generations to run
    - random_seed: int, RNG seed for reproducibility
    """
    np.random.seed(random_seed)

    # --- Strategy parameters ---
    offspring_count = 10  # λ, number of offspring per generation
    parent_count = 5      # μ, number of selected parents
    recombination_weights = np.array([0.35, 0.25, 0.20, 0.15, 0.05])  # weights for parent combination
    effective_parent_count = 1 / np.sum(recombination_weights ** 2)  # μ_eff

    # --- Adaptation parameters ---
    cumulation_time_constant_cov = (4 + effective_parent_count / dimension) / (
        dimension + 4 + 2 * effective_parent_count / dimension
    )
    cumulation_time_constant_sigma = (effective_parent_count + 2) / (
        dimension + effective_parent_count + 5
    )
    learning_rate_rank1 = 2 / ((dimension + 1.3) ** 2 + effective_parent_count)  # c1
    learning_rate_rank_mu = min(
        1 - learning_rate_rank1,
        2 * (effective_parent_count - 2 + 1 / effective_parent_count)
        / ((dimension + 2) ** 2 + effective_parent_count),
    )  # cmu
    damping_sigma = (
        1
        + 2 * max(0, np.sqrt((effective_parent_count - 1) / (dimension + 1)) - 1)
        + cumulation_time_constant_sigma
    )  # damping for sigma updates

    # --- Initialize dynamic variables ---
    mean_vector = np.random.randn(dimension)  # Center of the sampling distribution; CMA-ES "belief" about optimum location
    step_size = 1.3  # Global exploration scale σ; multiplies all sampling directions equally
    evolution_path_cov = np.zeros(dimension)  # pc: cumulative search direction used to shape (elongate/rotate) the covariance
    evolution_path_sigma = np.zeros(dimension)  # ps: cumulative step-length signal used to adapt σ (long if steps align)
    covariance_matrix = np.eye(dimension)  # C: shape of the search distribution (axes lengths/orientations)
    eigenvectors = np.eye(dimension)  # B: columns are principal directions (eigenvectors) of C
    sqrt_eigenvalues = np.ones(dimension)  # D^{1/2}: square roots of eigenvalues; axis scales before applying σ
    inv_sqrt_covariance = np.eye(dimension)  # C^{-1/2}: whitening transform used in path calculations

    expected_norm = np.sqrt(dimension) * (1 - 1 / (4 * dimension) + 1 / (21 * dimension ** 2))  # E||N(0,I)||
    last_eigendecomposition_iter = -1  # index of last eigendecomposition (force initial)
    
    # Initial eigendecomposition
    sqrt_eigenvalues, eigenvectors, inv_sqrt_covariance = update_eigendecomposition(covariance_matrix)  # init eig
    
    # Track global best across generations (monotonic)
    global_best_fitness = float("inf")  # best loss seen so far
    global_best_vector = mean_vector.copy()  # argmin for best loss
    
    # --- Optimization loop ---
    for generation in range(max_iterations):
        # Generate candidate solutions
        random_vectors = np.random.randn(dimension, offspring_count)  # Z ~ N(0, I)
        # Use proper matrix multiplication: eigenvectors @ diag(sqrt_eigenvalues) @ random_vectors
        scaled_random = np.diag(sqrt_eigenvalues) @ random_vectors  # D^{1/2} Z
        candidate_solutions = mean_vector[:, None] + step_size * (eigenvectors @ scaled_random)  # X = m + σ B D^{1/2} Z

        fitness_values = np.array([fitness_function(individual) for individual in candidate_solutions.T])  # losses

        # Select best μ individuals
        sorted_indices = np.argsort(fitness_values)  # ascending by loss
        selected_solutions = candidate_solutions[:, sorted_indices[:parent_count]]  # top-μ solutions
        selected_random_vectors = random_vectors[:, sorted_indices[:parent_count]]  # corresponding Z
        previous_mean = mean_vector.copy()  # m_t

        # --- Update parameters ---
        mean_vector = np.array(update_mean(selected_solutions, recombination_weights))  # m_{t+1}
        weighted_random_mean = selected_random_vectors @ recombination_weights  # Σ w_i z_i

        evolution_path_sigma, evolution_path_cov, hsig_condition = update_evolution_paths(
            evolution_path_sigma, evolution_path_cov, eigenvectors, weighted_random_mean,
            mean_vector, previous_mean, cumulation_time_constant_sigma, cumulation_time_constant_cov,
            effective_parent_count, step_size, expected_norm, dimension, generation
        )

        covariance_matrix = update_covariance_matrix(
            covariance_matrix, evolution_path_cov, selected_solutions, previous_mean,
            recombination_weights, step_size, learning_rate_rank1, learning_rate_rank_mu,
            cumulation_time_constant_cov, hsig_condition
        )

        step_size = update_step_size(
            step_size, evolution_path_sigma, cumulation_time_constant_sigma, damping_sigma, expected_norm
        )

        # --- Occasionally update eigendecomposition ---
        if generation - last_eigendecomposition_iter > offspring_count / (
            learning_rate_rank1 + learning_rate_rank_mu
        ) / dimension / 10:
            last_eigendecomposition_iter = generation  # refresh marker
            sqrt_eigenvalues, eigenvectors, inv_sqrt_covariance = update_eigendecomposition(covariance_matrix)  # refresh eig

        # --- Logging ---
        gen_best_fitness = fitness_values[sorted_indices[0]]  # best loss this generation
        if gen_best_fitness < global_best_fitness:
            global_best_fitness = float(gen_best_fitness)  # update global best loss
            global_best_vector = candidate_solutions[:, sorted_indices[0]].copy()  # corresponding vector
        # Log global best to avoid apparent regressions
        print(f"Iter {generation:03d}: best={global_best_fitness:.6f}, sigma={step_size:.4f}, mean_norm={np.linalg.norm(mean_vector):.4f}")

    return global_best_vector, global_best_fitness