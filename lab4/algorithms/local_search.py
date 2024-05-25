# TODO: now it doesn't work correct

import numpy as np


def calculate_cost(D, F):
    return np.sum(np.multiply(np.dot(F, D), F))


def swap_elements(F, i, j):
    F_new = np.copy(F)
    F_new[i], F_new[j] = F_new[j], F_new[i]
    return F_new


def local_search(D, F, max_iterations=1000, best_improvement=True):
    n = len(F)
    current_cost = calculate_cost(D, F)
    print("Посчитали поток:", current_cost)

    for _ in range(max_iterations):
        if best_improvement:
            best_cost = current_cost
            best_F = np.copy(F)

        for i in range(n):
            for j in range(i + 1, n):
                F_new = swap_elements(F, i, j)
                new_cost = calculate_cost(D, F_new)

                if new_cost < current_cost:
                    F = np.copy(F_new)
                    current_cost = new_cost

                    if not best_improvement:
                        break

        if best_improvement and best_cost < current_cost:
            break

    return F, current_cost


def print_matrix(matrix: list[list[int]], matrix_name: str):
    print(f"Matrix {matrix_name}")
    for row in matrix:
        print(*row)
    print()


# Пример использования
n = 4
# D = np.random.randint(1, 10, (n, n))
# F = np.random.permutation(np.eye(n))
D = [
    [0, 22, 53, 0],
    [22, 0, 40, 0],
    [53, 40, 0, 55],
    [0, 0, 55, 0]
]
F = [
    [0, 3, 0, 2],
    [3, 0, 0, 1],
    [0, 0, 0, 4],
    [2, 1, 4, 0]
]
# print_matrix(D, "D")
# print_matrix(F, "F")

# result_F, cost = local_search(D, F, best_improvement=False)
# print("Матрица потока после локального поиска:")
# print_matrix(result_F, "result_F")
# print("Лучшая стоимость:", cost)
print(
    np.dot(F, D)
)
print(
    np.array(F)
)
print(
    np.multiply(np.dot(F, D), F)
)
