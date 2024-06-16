import random
from collections import defaultdict

import numpy as np


def parts_similarity_scores(matrix) -> list[tuple[list, float]]:
    """

    :param matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
    :return: Возвращает список кортежей (пара деталей, коэффициент похожести).
    """
    m, p = matrix.shape
    scores = []

    for i in range(0, p - 1):
        for j in range(i + 1, p):
            a_ij = 0  # кол-во машин, которые обрабатывают детали i и j
            b_ij = 0  # кол-во машин, которые обрабатывают деталь i, но не j
            c_ij = 0  # кол-во машин, которые обрабатывают деталь j, но не i
            for machine in range(m):
                part_1 = matrix[machine][i]
                part_2 = matrix[machine][j]
                if part_1 == 1 and part_2 == 1:
                    a_ij += 1
                elif part_1 == 1 and part_2 == 0:
                    b_ij += part_1
                elif part_1 == 0 and part_2 == 1:
                    c_ij += part_2
            S = a_ij / (a_ij + b_ij + c_ij)
            if S != 0:
                scores.append(([i, j], S))
    scores.sort(key=lambda i: i[1], reverse=True)
    return scores


# TODO: удалить после проверки
def create_interval(t):
    n = 100
    ret = []
    for i in range(t-1):
            ret.append(((int)((i+1)*(n-1)/t))/100)
    ret.append(1)
    return ret


def intervals(num_of_intervals):
    """
    :param num_of_intervals: число интервалов
    :return: границы интервалов в пределах [0, 1]
    """

    # TODO: удалить комментарии

    # t = 100
    # print(len(create_interval(t)))
    # print(create_interval(t))
    # print(np.linspace(1, 0, num=t, endpoint=False, dtype=float)[::-1])
    # print(list(map(lambda x: round(x, 2), np.linspace(1, 0, num=t, endpoint=False, dtype=float)))[::-1])

    return np.linspace(1, 0, num=num_of_intervals, endpoint=False, dtype=float)[::-1]


def split_by_parts(matrix, sim_scores, num_of_intervals=2):
    m, p = matrix.shape

    # создаём пороги похожестей по которым будем объединять
    intervals_list = intervals(num_of_intervals)

    # сюда будем сохранять номера деталей и их группу
    parts_groups = {}

    # рассматриваем все существующие (ненулевые!) похожести
    for score in sim_scores:
        # сравниваем с каждым интервалом
        for i in range(num_of_intervals):
            # если коэффициент похожести лежит до границы интервала
            # и такой детали нет в списке, то для этой детали
            # сохраняем номер этого интервала
            if score[1] < intervals_list[i]:
                part_1 = score[0][0]
                part_2 = score[0][1]
                if part_1 not in parts_groups.keys():
                    parts_groups[part_1] = i
                if part_2 not in parts_groups.keys():
                    parts_groups[part_2] = i

    # записываем номера деталей группировано
    cells = [[] for _ in range(num_of_intervals)]
    for part, group in parts_groups.items():
        cells[group].append(part)

    # если существуют настолько уникальные детали, которые никуда не попали,
    # назначим им группу рандомно
    if len(parts_groups) != p:
        # потеряшки
        missing = list(set(range(p)) - set(parts_groups.keys()))
        for miss in missing:
            # номер ячейки выбирается случайно!
            cells[random.randint(0, num_of_intervals - 1)].append(miss)
    # оставляем только непустые ячейки
    cells = [cell for cell in cells if cell != []]

    return cells


input_matrix = np.array([
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0]
])
m, p = input_matrix.shape

print(parts_similarity_scores(input_matrix))

print(split_by_parts(input_matrix, parts_similarity_scores(input_matrix), num_of_intervals=2))

"""Другой пример"""
from lab5.main import tests_values
tests = tests_values(path="../benchmarks/")

matrix_20x20 = tests["20x20"]["matrix"]
# print(matrix_20x20)
print(parts_similarity_scores(matrix_20x20))
print(split_by_parts(matrix_20x20, parts_similarity_scores(matrix_20x20), num_of_intervals=2))
