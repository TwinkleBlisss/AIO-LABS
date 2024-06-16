"""
Метод имитации отжига
"""

import numpy as np
import random
import math


# Функция для вычисления показателя подобия
def similarity_score(matrix, i, j):
    a_ij = sum(1 for k in range(len(matrix[0])) if matrix[k][i] == 1 and matrix[k][j] == 1)
    b_ij = sum(1 for k in range(len(matrix[0])) if matrix[k][i] == 1 and matrix[k][j] == 0)
    c_ij = sum(1 for k in range(len(matrix[0])) if matrix[k][i] == 0 and matrix[k][j] == 1)
    # print(a_ij)
    # print(b_ij)
    # print(c_ij)
    score = a_ij / (a_ij + b_ij + c_ij)
    return score


def objective_function(solution, matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    n_1 = 0
    n_1_out = 0
    n_0_in = 0

    # Подсчет n_1, n_1_out и n_0_in
    for i in range(num_rows):
        for j in range(num_cols):
            if solution[i][j] == 1:
                n_1 += 1
                if matrix[i][j] == 0:  # Если 1 не попала ни в один кластер
                    n_1_out += 1
            elif solution[i][j] == 0 and matrix[i][j] == 0:  # Нули внутри кластера
                n_0_in += 1

    # Вычисление значения функции
    if n_1 + n_0_in == 0:
        return float('inf')  # Чтобы избежать деления на ноль
    else:
        return (n_1 - n_1_out) / (n_1 + n_0_in)


# Генерация начального решения на основе изначальной матрицы
def generate_initial_solution_from_matrix(matrix):
    return [[random.randint(0, 1) for _ in range(len(matrix[0]))] for _ in range(len(matrix))]


# Генерация соседнего решения
def generate_neighbor(solution):
    new_solution = [row.copy() for row in solution]
    i = random.randint(0, len(new_solution) - 1)
    j = random.randint(0, len(new_solution[0]) - 1)
    new_solution[i][j] = 1 if new_solution[i][j] == 0 else 0
    return new_solution


# Модифицированная функция simulated_annealing с остановкой по достижении минимальной температуры
def simulated_annealing(matrix, initial_temperature=500, cooling_rate=0.8, min_temperature=200):
    current_solution = generate_initial_solution_from_matrix(matrix)
    current_energy = objective_function(current_solution, matrix)  # Используйте objective_function для оценки текущего решения
    best_solution = current_solution
    best_energy = current_energy

    temperature = initial_temperature
    while temperature > min_temperature:
        new_solution = generate_neighbor(current_solution)
        new_energy = objective_function(new_solution, matrix)  # Используйте objective_function для оценки нового решения

        if new_energy < current_energy or random.random() < math.exp((current_energy - new_energy) / temperature):
            current_solution = new_solution
            current_energy = new_energy
            if new_energy < best_energy:
                best_solution = new_solution
                best_energy = new_energy

        temperature *= cooling_rate

    return best_solution, best_energy



# Пример входных данных
# m = 3  # количество станков
# p = 4  # количество деталей

# input_matrix = np.random.randint(2, size=(m, p))  # пример случайной матрицы 0 и 1
input_matrix = np.array([
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0]
])


# # Применяем метод имитации отжига к входным данным
# best_groups = simulated_annealing(input_matrix)
#
# print("Лучшие группы:", best_groups)
# print("Целевая функция:", objective_function(best_groups, input_matrix))


"""
def similarity_scores_matrix(input_matrix):
    res = np.zeros(input_matrix.shape)
    for i in range(res.shape[0]):
        for j in range(i + 1, res.shape[1]):
            res[i][j] = similarity_score(input_matrix, i, j)
    return res
print(similarity_scores_matrix(input_matrix))

def similarity_mas(data):
    m, p = data.shape
    similarity = []

    for i in range(0, p - 1):
        for j in range(i + 1, p):
            a_ij = 0
            b_ij = 0
            c_ij = 0
            for num in range(m):
                p1 = data[num][i]
                p2 = data[num][j]
                if p1 == 1 and p2 == 1:
                    a_ij += 1
                elif p1 == 1 and p2 == 0:
                    b_ij += p1
                elif p1 == 0 and p2 == 1:
                    c_ij += p2
            S = a_ij / (a_ij + b_ij + c_ij)
            if S != 0:
                similarity.append(([i, j], S))

    similarity.sort(key=lambda i: i[1], reverse=True)
    return (similarity)
print(similarity_mas(input_matrix))
"""


from lab5.main import tests_values
tests = tests_values(path="../benchmarks/")

matrix_20x20 = tests["20x20"]["matrix"]
print(matrix_20x20)

# Применяем метод имитации отжига к входным данным
best_groups = simulated_annealing(matrix_20x20)
print("Лучшие группы:", best_groups)
print("Целевая функция:", objective_function(best_groups, matrix_20x20))
