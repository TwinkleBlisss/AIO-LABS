def rabin_carp_algorithm(text, sample):
    count_of_comp = 0
    P = 53
    mod = 2 ** 15
    powers = [1]
    for i in range(1, len(text)):
        powers.append(powers[i - 1] * P % mod)

    hash_prefix_text = []
    for i in range(len(text)):
        hash_prefix_text.append(ord(text[i]) * powers[i] % mod)
        if i > 0:
            hash_prefix_text[i] += hash_prefix_text[i - 1]
            hash_prefix_text[i] %= mod

    hash_sample = 0
    for i in range(len(sample)):
        hash_sample += ord(sample[i]) * powers[i] % mod

    for i in range(len(text) - len(sample) + 1):
        count_of_comp += 2
        current_hash = hash_prefix_text[i + len(sample) - 1]
        if i > 0:
            current_hash -= hash_prefix_text[i - 1]
            current_hash %= mod
        if current_hash == hash_sample * powers[i] % mod:
            equals = True
            for j in range(len(sample)):
                if sample[j] != text[i + j]:
                    equals = False
                    break
            if equals:
                return i, count_of_comp
    return -1, count_of_comp
