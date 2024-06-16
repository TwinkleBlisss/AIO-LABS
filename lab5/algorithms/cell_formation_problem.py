import random
import numpy as np


class CFP:
    def __init__(self, matrix, num_of_intervals=2):
        self.matrix = matrix
        self.num_of_intervals = num_of_intervals

    def parts_similarity_scores(self) -> list[tuple[list, float]]:
        """

        :param self.matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
        :return: Возвращает список кортежей (пара деталей, коэффициент похожести).
        """
        m, p = self.matrix.shape
        scores = []

        for i in range(0, p - 1):
            for j in range(i + 1, p):
                a_ij = 0  # кол-во машин, которые обрабатывают детали i и j
                b_ij = 0  # кол-во машин, которые обрабатывают деталь i, но не j
                c_ij = 0  # кол-во машин, которые обрабатывают деталь j, но не i
                for machine in range(m):
                    part_1 = self.matrix[machine][i]
                    part_2 = self.matrix[machine][j]
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

    def intervals(self):
        """
        :return: границы интервалов в пределах [0, 1]
        """
        return np.linspace(1, 0, num=self.num_of_intervals, endpoint=False, dtype=float)[::-1]

    def split_by_parts(self, sim_scores) -> list[list]:
        """
        :param self.matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
        :param sim_scores: список кортежей (пара деталей, коэффициент похожести).
        :param num_of_intervals: количество групп, на которые разобьём детали.
        :return: список с группами деталей, попавших в один интервал.
        """
        m, p = self.matrix.shape

        # создаём пороги похожестей по которым будем объединять
        intervals_list = self.intervals()

        # сюда будем сохранять номера деталей и их группу
        parts_groups = {}

        # рассматриваем все существующие (ненулевые!) похожести
        for score in sim_scores:
            # сравниваем с каждым интервалом
            for i in range(self.num_of_intervals):
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
        cells = [[] for _ in range(self.num_of_intervals)]
        for part, group in parts_groups.items():
            cells[group].append(part)

        # если существуют настолько уникальные детали, которые никуда не попали,
        # назначим им группу рандомно
        if len(parts_groups) != p:
            # потеряшки
            missing = list(set(range(p)) - set(parts_groups.keys()))
            for miss in missing:
                # номер ячейки выбирается случайно!
                cells[random.randint(0, self.num_of_intervals - 1)].append(miss)
        # оставляем только непустые ячейки
        cells = [cell for cell in cells if cell != []]

        return cells

    def split_by_machines(self, cells_parts):
        """
        :param self.matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
        :param cells_parts: список с группами деталей, попавших в один интервал.
        :return: список с группами машин, попавших в один cell деталей.
        """
        m, p = self.matrix.shape

        sum_details_for_machines = list(map(sum, self.matrix))  # количество деталей, которое производит каждая машина
        ve_all_machines_and_cells = []  # список для сохранения информации о том, насколько ячейка подходит машине

        # рассматриваем каждую машину
        for machine in range(m):
            sum_ve_for_machine_per_cell = []
            # считаем отдельно для каждого кластера
            for cell in cells_parts:
                voids = 0  # нули, входящие в кластер для данной машины
                ones = 0  # единицы, входящие в кластер для данной машины
                for part in cell:
                    if self.matrix[machine][part] == 0:
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

    def initial_solution(self, num_of_intervals=2):
        """
        :param self.matrix: матрица, где строка - машина, столбец - деталь (1 значит машина i производит деталь j).
        :param num_of_intervals: количество групп, на которые разобьём детали b машины соответственно
        :return: два списка с распределением деталей и машин по группам.
        """
        sim_scores = self.parts_similarity_scores()
        cells_parts = self.split_by_parts(sim_scores)
        cells_machines = self.split_by_machines(cells_parts)
        return cells_parts, cells_machines

    def target_function(self, cells_parts, cells_machines):
        """
        :param self.matrix:
        :param cells_parts:
        :param cells_machines:
        :return: групповая эффективность -> max
        """
        n_1 = 0  # количество единиц в кластере
        n_1_out = 0  # количество единиц, которые никуда не попали
        n_0_in = 0  # количество нулей в кластере

        # количество деталей, которое производит каждая машина
        sum_details_for_machines = list(map(sum, self.matrix))

        # рассматриваем кластеры
        for i in range(len(cells_machines)):
            for machine in cells_machines[i]:
                sum_1_per_machine_in_cluster = 0  # сумма единиц в кластере для
                for part in cells_parts[i]:
                    if self.matrix[machine][part] == 1:
                        sum_1_per_machine_in_cluster += 1
                    else:
                        n_0_in += 1
                n_1 += sum_1_per_machine_in_cluster
                n_1_out += sum_details_for_machines[i] - sum_1_per_machine_in_cluster

        f = (n_1 - n_1_out) / (n_1 + n_0_in)
        return f
