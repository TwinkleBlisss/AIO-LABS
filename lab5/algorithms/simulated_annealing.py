"""
Метод имитации отжига
"""

import random
import math


def calculate_cost(cells, matrix):
    cost = 0
    for cell in cells:
        for i in range(len(cell)):
            for j in range(i + 1, len(cell)):
                cost += matrix[cell[i] - 1][cell[j] - 1]
    return cost


def generate_initial_solution(m, p):
    cells = [[] for _ in range(m)]
    parts = list(range(1, p + 1))
    random.shuffle(parts)
    for i, part in enumerate(parts):
        cells[i % m].append(part)
    return cells


def generate_neighbour(cells):
    neighbour = [list(cell) for cell in cells]
    cell_idx = random.randint(0, len(cells)-1)
    if len(neighbour[cell_idx]) > 0:
        part_idx = random.randint(0, len(neighbour[cell_idx])-1)
        part = neighbour[cell_idx].pop(part_idx)
        target_cell_idx = random.randint(0, len(cells)-1)
        neighbour[target_cell_idx].append(part)
    return neighbour



def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)


def simulated_annealing(matrix, m, p, initial_temperature, cooling_rate, max_iterations):
    current_solution = generate_initial_solution(m, p)
    best_solution = current_solution
    current_cost = calculate_cost(current_solution, matrix)
    best_cost = current_cost
    temperature = initial_temperature

    for iteration in range(max_iterations):
        new_solution = generate_neighbour(current_solution)
        new_cost = calculate_cost(new_solution, matrix)

        if acceptance_probability(current_cost, new_cost, temperature) > random.random():
            current_solution = new_solution
            current_cost = new_cost

        if new_cost < best_cost:
            best_solution = new_solution
            best_cost = new_cost

        temperature *= cooling_rate

    return best_solution, best_cost


# Пример использования
matrix = [
    [0, 2, 3, 4],
    [2, 0, 5, 6],
    [3, 5, 0, 7],
    [4, 6, 7, 0]
]
m = 2
p = 4
initial_temperature = 100.0
cooling_rate = 0.99
max_iterations = 1000

best_solution, best_cost = simulated_annealing(matrix, m, p, initial_temperature, cooling_rate, max_iterations)

print("Best Solution:", best_solution)
print("Best Cost:", best_cost)
