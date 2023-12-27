"""Module with functions for working with the ant algorithm"""

import numpy as np
from concurrent.futures import ThreadPoolExecutor


def construct_path(ant: int, main_point: int, num_cities: int, probability_matrix: np.array) -> list:
    """
    Creating the path of a single ant
    :param ant: number by ant
    :param main_point: Start and end point
    :param num_cities: Number of cities
    :param probability_matrix: Probability matrix
    :return: The path traveled
    """
    print(f'Ant: {ant}')
    visited_cities = [main_point]
    for i in range(num_cities - 1):
        unvisited_cities = list(set(range(num_cities)) - set(visited_cities))
        probabilities = probability_matrix[visited_cities[i], unvisited_cities]
        probabilities = probabilities / sum(probabilities)
        next_city = np.random.choice(unvisited_cities, p=probabilities)
        visited_cities.append(next_city)
    return visited_cities


def aco_tsp(distance_matrix: np.array, num_ants: int, num_iterations: int, main_point: int, alpha: int = 1,
            beta: int = 21, evaporation_rate: float = 0.1) -> (list, float):
    """
    Ant algorithm for solving the traveling salesman problem
    :param distance_matrix: Distance matrix
    :param num_ants: Number of ants in the iteration
    :param num_iterations: Number of iterations
    :param main_point: Start and end point
    :param alpha: Degree of regulation of the significance of the pheromone matrix
    :param beta: Degree of regulation of the significance of the matrix is the inverse of the distance matrix
    :param evaporation_rate: Pheromone drying rate
    :return: The best found path and its distance
    """
    num_cities = len(distance_matrix)
    pheromone_matrix = np.ones((num_cities, num_cities))
    itr_best_paths, itr_best_distances = [], []
    distance_matrix += np.eye(num_cities, num_cities)
    reverse_matrix_dist = (1 / np.array(distance_matrix))
    reverse_matrix_dist -= np.eye(num_cities, num_cities)
    distance_matrix -= np.eye(num_cities, num_cities)
    for iteration in range(num_iterations):
        print(f'Iteration: {iteration}')
        probability_matrix = (pheromone_matrix ** alpha) * (reverse_matrix_dist ** beta)
        ant_paths = []
        args_for_path = [(ants, main_point, num_cities, probability_matrix) for ants in range(num_ants)]
        with ThreadPoolExecutor(6) as pool:
            paths = pool.map(construct_path, *zip(*args_for_path))
            for path in paths:
                ant_paths.append(path)

        distances_itr = []
        for path in ant_paths:
            distance = 0
            for i in range(num_cities - 1):
                distance += distance_matrix[path[i], path[i + 1]]
            distance += distance_matrix[path[-1], path[0]]
            distances_itr.append(distance)
        min_distance_itr = min(distances_itr)
        itr_best_distances.append(min_distance_itr)
        print(itr_best_distances[-1])
        itr_best_paths.append(ant_paths[distances_itr.index(min_distance_itr)])

        pheromone_matrix *= (1 - evaporation_rate)
        for i in range(num_ants):
            for j in range(num_cities - 1):
                city_prev, city_next = ant_paths[i][j], ant_paths[i][j]
                pheromone_matrix[city_prev][city_next] += 1 / distances_itr[i]
            pheromone_matrix[ant_paths[i][-1], ant_paths[i][0]] += 1 / distances_itr[i]

    best_itr = itr_best_distances.index(min(itr_best_distances))
    best_path = itr_best_paths[best_itr]
    best_distance = itr_best_distances[best_itr]
    return best_path, best_distance
