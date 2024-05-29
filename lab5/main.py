import os
import time
import shutil
import numpy as np


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
            values[no_ext_name]["matrix"] = matrix.tolist()
    return values


def main():
    # path = "benchmarks/"
    # tests_names = os.listdir(path)
    # print(tests_names)
    # print(tests_names[1].rstrip(".txt"))
    #
    # m_i, *row = [1, 9, 17, 19, 31, 33]
    # print(m_i, row)
    tests = tests_values()
    print(tests)


if __name__ == "__main__":
    main()
