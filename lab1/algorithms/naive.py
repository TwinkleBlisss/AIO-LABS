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
