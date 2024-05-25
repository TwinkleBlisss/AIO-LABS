# TODO: write tests load like in lab3
import os
import time
import numpy


def tests_values(path: str = "benchmarks/") -> dict:
    values = {}
    tests_names = os.listdir(path)
    tests_names = sorted(tests_names, key=lambda test_num: int(test_num[3:-1]))
    for test_name in tests_names:
        values[test_name] = {}
        with open(path + test_name, "r", encoding="utf-8") as f:
            values[test_name]["n"] = int(f.readline())
            D_matrix = []
            for i in range(values[test_name]["n"]):
                # построчно считываем матрицу расстояний D
                D_matrix.append(list(map(int, f.readline().split())))
            values[test_name]["D"] = D_matrix
            F_matrix = []
            for i in range(values[test_name]["n"]):
                # построчно считываем матрицу потоков F
                F_matrix.append(list(map(int, f.readline().split())))
            values[test_name]["F"] = F_matrix
    return values


def get_output_and_time(algorithm, n, D, F):
    """
    Функция для получения решения теста и времени работы алгоритма.
    :param algorithm: Класс алгоритма
    :param args: Параметры теста в формате (n - размерность, Distances, Flows)
    :return: Решение, минимальная стоимость потока
    """
    start = time.time()
    # TODO: Класс в конструктор принимает такие параметры
    algo_class = algorithm(n, D, F)
    algo_class.solve()
    # TODO: Тут ЕвГений добавит правильный метод вместо solve
    sol, cost = algo_class.solve()
    end = time.time()
    return sol, cost, (end - start) * 10**3


# TODO: Функция для вывода таблицы результатов конкретного алгоритма на всех тестах

def main():
    # path = "benchmarks/"
    # tests_names = os.listdir(path)


    tests = tests_values()
    for test_name, test_value in tests.items():
        print(test_name)
        print(test_value)


if __name__ == "__main__":
    main()
