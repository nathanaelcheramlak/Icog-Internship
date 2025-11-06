from hyperon import MeTTa
import numpy as np
from utils import *

metta = MeTTa()

def cma_es(fitness_function, dimension=5, max_iterations=200, random_seed=42):
    np.random.seed(random_seed)

    # --- Strategy parameters ---
    offspring_count = 10  # λ
    parent_count = 5      # μ
    recombination_weights = np.array([0.35, 0.25, 0.20, 0.15, 0.05])
    effective_parent_count = 1 / np.sum(recombination_weights ** 2)

    # --- Adaptation parameters ---
    cumulation_time_constant_cov = (4 + effective_parent_count / dimension) / (
        dimension + 4 + 2 * effective_parent_count / dimension
    )
    cumulation_time_constant_sigma = (effective_parent_count + 2) / (
        dimension + effective_parent_count + 5
    )
    learning_rate_rank1 = 2 / ((dimension + 1.3) ** 2 + effective_parent_count)
    learning_rate_rank_mu = min(
        1 - learning_rate_rank1,
        2 * (effective_parent_count - 2 + 1 / effective_parent_count)
        / ((dimension + 2) ** 2 + effective_parent_count),
    )
    damping_sigma = (
        1
        + 2 * max(0, np.sqrt((effective_parent_count - 1) / (dimension + 1)) - 1)
        + cumulation_time_constant_sigma
    )

    # --- Initialize dynamic variables ---
    mean_vector = np.random.randn(dimension)
    step_size = 1.3
    evolution_path_cov = np.zeros(dimension)
    evolution_path_sigma = np.zeros(dimension)
    covariance_matrix = np.eye(dimension)
    eigenvectors = np.eye(dimension)
    sqrt_eigenvalues = np.ones(dimension)
    inv_sqrt_covariance = np.eye(dimension)

    expected_norm = np.sqrt(dimension) * (1 - 1 / (4 * dimension) + 1 / (21 * dimension ** 2))
    last_eigendecomposition_iter = -1  # Force initial eigendecomposition
    
    # Initial eigendecomposition
    sqrt_eigenvalues, eigenvectors, inv_sqrt_covariance = update_eigendecomposition(covariance_matrix)
    
    # Track global best across generations (monotonic)
    global_best_fitness = float("inf")
    global_best_vector = mean_vector.copy()
    
    # --- Optimization loop ---
    for generation in range(max_iterations):
        # Generate candidate solutions
        random_vectors = np.random.randn(dimension, offspring_count)
        # Use proper matrix multiplication: eigenvectors @ diag(sqrt_eigenvalues) @ random_vectors
        scaled_random = np.diag(sqrt_eigenvalues) @ random_vectors
        candidate_solutions = mean_vector[:, None] + step_size * (eigenvectors @ scaled_random)

        fitness_values = np.array([fitness_function(individual) for individual in candidate_solutions.T])

        # Select best μ individuals
        sorted_indices = np.argsort(fitness_values)
        selected_solutions = candidate_solutions[:, sorted_indices[:parent_count]]
        selected_random_vectors = random_vectors[:, sorted_indices[:parent_count]]
        previous_mean = mean_vector.copy()

        # --- Update parameters ---
        mean_vector = np.array(update_mean(selected_solutions, recombination_weights))
        weighted_random_mean = selected_random_vectors @ recombination_weights

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
            last_eigendecomposition_iter = generation
            sqrt_eigenvalues, eigenvectors, inv_sqrt_covariance = update_eigendecomposition(covariance_matrix)

        # --- Logging ---
        gen_best_fitness = fitness_values[sorted_indices[0]]
        if gen_best_fitness < global_best_fitness:
            global_best_fitness = float(gen_best_fitness)
            global_best_vector = candidate_solutions[:, sorted_indices[0]].copy()
        # Log global best to avoid apparent regressions
        print(f"Iter {generation:03d}: best={global_best_fitness:.6f}, sigma={step_size:.4f}, mean_norm={np.linalg.norm(mean_vector):.4f}")

    return global_best_vector, global_best_fitness

