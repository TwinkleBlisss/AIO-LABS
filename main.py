"""
Ваша первая лабораторная работа будет заключаться в реализации и сравнении алгоритмов поиска подстроки
в строке.
Вам нужно будет реализовать следующие алгоритмы, которые мы разбирали на паре:

1) Наивный алгоритм
2) Алгоритм Рабина-Карпа ИЛИ Алгоритм Бойера-Мура-Хорспула
3) Алгоритм Кнутта-Мориса-Пратта ИЛИ Алгоритм Ахо-Карасика

Реализовать нужно на Python (если вам прям вот хочется, вот прям мочи нет, то можно на С++ или Джаве).

Также нужно будет сравнить время работы алгоритма и количество операций сравнения. Не забываем,
что скорость работы нужно сравнивать, используя информацию о множестве прогонов алгоритма на
одном наборе данных.
"""
import os
import time


def naive_algorithm(T: str, W: str) -> tuple:
    """
    T - текст, W - образец. \n
    Возвращаем либо None, либо позицию первого вхождения W в T
    вместе с количеством операций сравнения.
    """
    # print(f'В строке "{T}" будем искать подстроку "{W}".')
    N = len(T)
    M = len(W)
    comparisons = 0  # количество операций сравнения
    for i in range(N - M + 1):
        # print(f'Возьмём срез с индексами {i}-{i + M - 1} =', T[i: i + M])
        comparisons += M
        if T[i: i + M] == W:
            return i, comparisons
    return None, comparisons


def rabin_carp_algorithm():
    pass


def boyer_mur_horspul_algorithm():
    pass


def knutt_moris_pratt_algorithm():
    pass


def aho_karasik_algorithm():
    pass


def tests_files(path: str = 'benchmarks/') -> list:
    """
    Функция возвращает список кортежей вида (T, W) с входными данными для проверки алгоритмов.
    """
    try:
        filenames = os.listdir(path)
        bad_tests = filenames[:len(filenames) // 2]
        good_tests = filenames[len(filenames) // 2:]
        bad_tests = list(zip(bad_tests[: len(bad_tests) // 2], bad_tests[len(bad_tests) // 2:]))
        good_tests = list(zip(good_tests[: len(good_tests) // 2], good_tests[len(good_tests) // 2:]))

        return bad_tests + good_tests
    except FileNotFoundError:
        raise FileNotFoundError("No tests found. Try to change path.")


def tests_values(pairs: list) -> dict:
    """
    Функция для записи в словарь вида {'имя теста': (T, W)}
    входных данных из текстовых файлов.
    """
    os.chdir('benchmarks/')
    values = {}
    for pair in pairs:
        name_of_test = f"{'bad' if pair[0].startswith('bad') else 'good'}_{pair[0].removesuffix('.txt')[-1]}"
        # print(f"Тест '{name_of_test}'")
        with open(pair[0], 'r', encoding="utf8") as f:
            # print('читаем ', pair[0])
            T = f.read()
        with open(pair[1], 'r', encoding="utf8") as f:
            # print('читаем ', pair[1])
            W = f.read()
        values[name_of_test] = (T, W)
    return values


def count_operations_and_time(algorithm, tests: dict) -> None:
    """
    Функция для вывода информации о работе алгоритма
    (результата, количества операций сравнения и времени выполнения).
    """
    print('{:10} | {:7} | {:7} | {:^7} | {:^12} | {:^12}'
          .format('Test name', 'len(T)', 'len(W)', 'result', 'num_of_comp', 'time in ms'))
    fmt = '{:10} | {:7} | {:7} | {:7} | {:12} | {:.10f}'
    for test_name, test_value in tests.items():
        T, W = test_value[0], test_value[1]
        start = time.time()
        result, comparisons = algorithm(T, W)
        end = time.time()
        print(fmt.format(test_name, len(T), len(W), result, comparisons, (end - start) * 10 ** 3))
    return None


def main():
    tests = tests_values(tests_files())
    # for key, value in tests.items():
    #     print(key, value)

    print("Naive algorithm:")
    count_operations_and_time(naive_algorithm, tests)


if __name__ == '__main__':
    main()
