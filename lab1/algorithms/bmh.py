def forming_d(W):
    """ Формируем массив d."""
    d = [len(W) for i in range(1105)]  # символы до буквы ё
    new_p = W[::-1]

    for i in range(len(new_p)):
        if d[ord(new_p[i])] != len(new_p):
            continue
        else:
            d[ord(new_p[i])] = i
    return d


def boyer_mur_horspul_algorithm(T: str, W: str) -> tuple:
    """
    T - текст, W - образец. \n
    Возвращаем либо None, либо позицию первого вхождения W в T
    вместе с количеством операций сравнения.
    """
    d = forming_d(W)
    comparisons = 0  # количество операций сравнения
    # x - начало прохода по T
    # j - проход по W
    # k - проход по T
    len_p = x = j = k = len(W)
    while x <= len(T) and j > 0:
        comparisons += 1
        if W[j - 1] == T[k - 1]:
            j -= 1
            k -= 1
        else:
            x += d[ord(T[k - 1])]
            k = x
            j = len_p
    if j <= 0:
        return k, comparisons
    else:
        return None, comparisons
