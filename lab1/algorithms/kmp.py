def prefix_function(string: str):
    pi = [0] * len(string)
    count_of_comp = 0
    for i in range(1, len(string)):
        j = pi[i - 1]
        while j > 0 and string[i] != string[j]:
            count_of_comp += 2
            j = pi[j - 1]
        count_of_comp += 3
        if string[i] == string[j]:
            j += 1
        pi[i] = j
    return pi, count_of_comp


def knutt_moris_pratt_algorithm(text: str, sample: str):
    count_of_comp = 0
    common_string = sample + "~" + text
    answer = prefix_function(common_string)
    pi = answer[0]
    count_of_comp += answer[1]
    for i in range(len(sample), len(pi)):
        count_of_comp += 1
        if len(sample) == pi[i]:
            return i - len(sample) * 2, count_of_comp
    return -1, count_of_comp
