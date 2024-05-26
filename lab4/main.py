# TODO: write tests load like in lab3
import os
import time
import shutil

from algorithms.local_search import LocalSearch
from algorithms.iterated_local_search import IteratedLocalSearch

# algorithm classes
ALGORITHMS = [LocalSearch, IteratedLocalSearch]


def tests_values(path: str = "benchmarks/") -> dict:
    values = {}
    tests_names = os.listdir(path)
    # сортируем тесты по порядку (20, ..., 100)
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
            f.readline()
            F_matrix = []
            for i in range(values[test_name]["n"]):
                # построчно считываем матрицу потоков F
                F_matrix.append(list(map(int, f.readline().split())))
            values[test_name]["F"] = F_matrix
    return values


def get_output_and_time(algorithm, D, F):
    """
    Функция для получения решения теста и времени работы алгоритма.
    :param algorithm: Класс алгоритма
    :param args: Параметры теста в формате (Distances, Flows)
    :return: Решение, минимальная стоимость потока
    """
    start = time.time()
    # TODO: Класс в конструктор принимает такие параметры
    algo_class = algorithm(F, D)
    # TODO: Тут ЕвГений добавит правильный метод вместо solve # Нет будет solve
    sol, cost = algo_class.solve()
    end = time.time()
    return sol, cost, (end - start) * 10 ** 3


def make_directory(path):
    """
    Создание ПУСТОЙ директории и переход в неё.
    """
    # удаляем файлы, если они есть
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    os.chdir(path)


def show_results(delete_answers: bool = False):
    """
    Функция для вывода таблицы результатов алгоритмов на всех тестах.
    При delete_answers == True очищается папка "answers" и функция прекращает свою работу.
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

    for algorithm in ALGORITHMS:
        # создаём директорию с ответами конкретного алгоритма и ПЕРЕХОДИМ В НЕЁ
        os.chdir(ans)  # возвращаемся в директорию с ответами
        make_directory(algorithm.__name__)

        print(f"{algorithm.__name__}:")

        # определяем формат заголовка
        print('| {:^15} | {:^15} | {:^16} |'
              .format('Test name', 'Best cost', 'Time in ms'))

        # определяем формат результатов теста
        fmt = '| {:15} | {:15} | {:4.13f} |'

        for test_name, test_value in tests.items():
            # решение алгоритма
            solution, cost, algo_time = get_output_and_time(
                algorithm,
                test_value['D'],
                test_value['F']
            )


            # сохраняем solution в файлик "Testname.sol"
            with open(f"{test_name.capitalize()}.sol", "w", encoding="utf-8") as f:
                f.write(" ".join(map(str, solution)))

            # вывод результата
            print(fmt.format(test_name, cost, algo_time))
        print("\n\n")
    os.chdir(root)  # возвращаемся в исходную директорию


def main():
    # path = "benchmarks/"
    # tests_names = os.listdir(path)
    show_results(delete_answers=False)


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    main()
