import random
from collections import defaultdict

import numpy as np


def similarity_scores(matrix) -> list[tuple[list, float]]:
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


def intervals(t):
    """
    :param t: число интервалов
    :return: границы интервалов в пределах [0, 1]
    """

    # TODO: удалить комментарии

    # t = 100
    # print(len(create_interval(t)))
    # print(create_interval(t))
    # print(np.linspace(1, 0, num=t, endpoint=False, dtype=float)[::-1])
    # print(list(map(lambda x: round(x, 2), np.linspace(1, 0, num=t, endpoint=False, dtype=float)))[::-1])

    return np.linspace(1, 0, num=t, endpoint=False, dtype=float)[::-1]


def divide_parts(matrix, similarity, n):  # n - количество интервалов
    m, p = matrix.shape

    interval = intervals(n)
    parts_in_work = defaultdict(list)
    list_sim = similarity

    for i in list_sim:
        for j in range(n):  # пробегаем по всем интервалам
            if i[1] <= interval[j]:
                if i[0][0] not in parts_in_work:
                    parts_in_work[(i[0][0])] = j

                if i[0][1] not in parts_in_work:
                    parts_in_work[(i[0][1])] = j

    div_parts = []
    for i in range(n):
        div_parts.append([])

    for part in parts_in_work:
        div_parts[parts_in_work[part]].append(part)  # заносим результат в кластеры

    if len(parts_in_work) != p:  # если есть детали, не вошедшие ни в 1 кластер
        missing = list(set(i for i in range(p)) - set(key for key in parts_in_work))
        for mis in missing:
            a = random.randint(0, n - 1)  # рандомно помещаем их в кластеры
            div_parts[a].append(mis)

    div_parts = [value for value in div_parts if len(value) != 0]  # убираем все пустые кластеры

    return div_parts


input_matrix = np.array([
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0]
])

print(similarity_scores(input_matrix))
