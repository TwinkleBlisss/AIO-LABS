import os
import time
import shutil
import numpy as np
import pandas as pd

from algorithms.simulated_annealing_class import SimulatedAnnealing


def tests_values(path: str = "benchmarks/") -> dict:
    values = {}
    tests_names = os.listdir(path)
    for test_name in tests_names:
        # убираем расширение файла из имени теста
        no_ext_name = test_name.rstrip(".txt")

        values[no_ext_name] = {}
        with open(path + test_name, "r", encoding="utf-8") as f:
            # считываем количество станков и деталей
            m, p = map(int, f.readline().split())
            values[no_ext_name]["m"], values[no_ext_name]["p"] = m, p

            # считываем матрицу, обозначающую, где производится каждая деталь
            matrix = np.zeros((m, p))
            for i in range(m):
                m_i, *row = list(map(int, f.readline().split()))
                for j in range(len(row)):
                    matrix[m_i - 1][row[j] - 1] = 1
            values[no_ext_name]["matrix"] = matrix  # .tolist()
    return values


def make_directory(path):
    """
    Создание ПУСТОЙ директории и переход в неё.
    """
    # удаляем файлы, если они есть
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    os.chdir(path)


def get_output_and_time(algorithm, D, F):
    """
    Функция для получения решения теста и времени работы алгоритма.
    """
    start = time.time()
    algo_class = algorithm(F, D)
    sol, cost = algo_class.solve()
    end = time.time()
    return sol, cost, (end - start) * 10 ** 3


def show_results(delete_answers: bool = False):
    """

    :return: Пандас датафрейм с названиями тестов (столбцы - название теста,
    target_function, time)
    """
    # загружаем тестовые данные
    tests = tests_values()

    # создаём директорию для ответов и ПЕРЕХОДИМ В НЕЁ
    root = os.getcwd()  # исходная директория
    ans_path = "answers"
    make_directory(ans_path)
    ans = os.getcwd()  # директория с ответами

    if delete_answers:
        return

    # results = pd.DataFrame(columns=['Test_name', 'f', 'time'])
    tmp = {}
    for test_name, test_value in tests.items():
        start = time.time()
        algo_class = SimulatedAnnealing(test_value['matrix'])
        sol, f = algo_class.solve()
        end = time.time()
        tmp[test_name] = sol, f
    print(tmp)


def main():
    show_results()


if __name__ == "__main__":
    main()
