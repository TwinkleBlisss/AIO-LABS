import tsplib95
import pandas as pd
import numpy as np


# problem = tsplib95.load('benchmarks/tsp/a280.tsp')
# problem = tsplib95.load('benchmarks/tsp/bays29.tsp')
problem = tsplib95.load('benchmarks/tsp/gr17.tsp')

print(problem.as_name_dict())
print(list(problem.get_nodes()))
print(list(problem.get_edges())[:5])

edge = 1, 2
weight = problem.get_weight(*edge)
print(f'The driving distance from node {edge[0]} to node {edge[1]} is {weight}.\n')


def lower_diag_to_full_matrix(matrix: list[list]) -> list[list]:
    # записываем матрицу в список
    lower_diag_matrix_list = [
        matrix[i][j] for i in range(len(matrix))
                     for j in range(len(matrix[i]))
    ]

    # приводим в нижне диагональную форму
    lower_diag_matrix = []
    row = []
    for i in range(len(lower_diag_matrix_list)):
        row.append(lower_diag_matrix_list[i])
        if lower_diag_matrix_list[i] == 0:
            lower_diag_matrix.append(row)
            row = []

    # делаем из неё симметричную матрицу
    tmp = pd.DataFrame(lower_diag_matrix)
    tmp = tmp.combine_first(tmp.T).values.tolist()
    # возвращаем нужный тип
    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            tmp[i][j] = int(tmp[i][j])
    return tmp


edges = problem.edge_weights
print(lower_diag_to_full_matrix(edges))

print(problem.edge_weight_format)