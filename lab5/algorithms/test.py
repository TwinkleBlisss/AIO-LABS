import random
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


def split_by_parts(matrix, sim_scores, num_of_intervals=2) -> list[list]:
    """
    :param matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
    :param sim_scores: список кортежей (пара деталей, коэффициент похожести).
    :param num_of_intervals: количество групп, на которые разобьём детали.
    :return: список с группами деталей, попавших в один интервал.
    """
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


def split_by_machines(matrix, cells_parts):
    """
    :param matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
    :param cells_parts: список с группами деталей, попавших в один интервал.
    :return: список с группами машин, попавших в один cell деталей.
    """
    m, p = matrix.shape

    sum_details_for_machines = list(map(sum, matrix))  # количество деталей, которое производит каждая машина
    ve_all_machines_and_cells = [] # список для сохранения информации о том, насколько ячейка подходит машине

    # рассматриваем каждую машину
    for machine in range(m):
        sum_ve_for_machine_per_cell = []
        # считаем отдельно для каждого кластера
        for cell in cells_parts:
            voids = 0  # нули, входящие в кластер для данной машины
            ones = 0  # единицы, входящие в кластер для данной машины
            for part in cell:
                if matrix[machine][part] == 0:
                    voids += 1
                else:
                    ones += 1
            # единицы, не входящие в кластер для данной машины
            exceptionals = sum_details_for_machines[machine] - ones
            # сохраняем сумму (это число означает как много мы упускаем при назначении ячейки для машины;
            # т.е. в идеале 0)
            sum_ve_for_machine_per_cell.append((voids, exceptionals))
        ve_all_machines_and_cells.append(sum_ve_for_machine_per_cell)

    # количество групп деталей
    cells_num = len(cells_parts)
    # записываем номера машин группировано
    cells_machines = [[] for _ in range(cells_num)]

    for i in range(len(ve_all_machines_and_cells)):
        # минимальное значение v+e для каждой машины
        minimum = min(ve_all_machines_and_cells[i], key=lambda x: sum(x))
        minimum = min(x[0] + x[1] for x in ve_all_machines_and_cells[i])

        # потенциальные кластеры для машины
        positions = [j for j, x in enumerate(ve_all_machines_and_cells[i]) if x[0] + x[1] == minimum]
        if len(positions) == 1:
            # если потенциальный кластер всего один, то можно туда и пихать
            cells_machines[positions[0]].append(i)
        else:
            # иначе ищем кластер с минимальным voids
            minimum = min([ve_all_machines_and_cells[i][j][0] for j in positions])
            for position in positions:
                if ve_all_machines_and_cells[i][position][0] == minimum:
                    cells_machines[position].append(i)
                    break

    return cells_machines


def initial_solution(matrix, num_of_intervals=2):
    """
    :param matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
    :param num_of_intervals: количество групп, на которые разобьём детали b машины соответственно
    :return: два списка с распределением деталей и машин по группам.
    """
    sim_scores = parts_similarity_scores(matrix)
    cells_parts = split_by_parts(matrix, sim_scores, num_of_intervals)
    cells_machines = split_by_machines(matrix, cells_parts)
    return cells_parts, cells_machines


def target_function(matrix, cells_parts, cells_machines):
    """
    :param matrix:
    :param cells_parts:
    :param cells_machines:
    :return: групповая эффективность -> max
    """
    n_1 = 0  # количество единиц в кластере
    n_1_out = 0  # количество единиц, которые никуда не попали
    n_0_in = 0  # количество нулей в кластере

    # количество деталей, которое производит каждая машина
    sum_details_for_machines = list(map(sum, matrix))

    # рассматриваем кластеры
    for i in range(len(cells_machines)):
        for machine in cells_machines[i]:
            sum_1_per_machine_in_cluster = 0  # сумма единиц в кластере для
            for part in cells_parts[i]:
                if matrix[machine][part] == 1:
                    sum_1_per_machine_in_cluster += 1
                else:
                    n_0_in += 1
            n_1 += sum_1_per_machine_in_cluster
            n_1_out += sum_details_for_machines[i] - sum_1_per_machine_in_cluster

    f = (n_1 - n_1_out) / (n_1 + n_0_in)
    return f


input_matrix = np.array([
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0]
])
m, p = input_matrix.shape

# print(parts_similarity_scores(input_matrix))

init_sol = initial_solution(input_matrix)
# print(init_sol[0])
# print(init_sol[1])

print(target_function(input_matrix, *init_sol))

# """Другой пример"""
print("\n\n")

from lab5.main import tests_values
tests = tests_values(path="../benchmarks/")

matrix_20x20 = tests["20x20"]["matrix"]
# print(matrix_20x20)
init_sol = initial_solution(matrix_20x20)
print(init_sol[0])
print(init_sol[1])

print(target_function(matrix_20x20, *init_sol))
