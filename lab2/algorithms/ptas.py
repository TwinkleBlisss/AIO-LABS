import itertools

from base import Base


class PTAS(Base):
    def __init__(self, weights: list, prices: list, capacity: int):
        super().__init__(weights, prices, capacity)
        self.items = {}
        self.answer = 0

    def __generate_set(self, k: int):
        source = list(range(len(self.prices)))
        for i in range(k + 1):
            permutations = itertools.permutations(source, i)
            for permutation in permutations:
                yield permutation

    def __greed_search(self, M: set):
        common_price = 0
        capacity = self.capacity - sum([self.prices[i] for i in M])
        X = set()
        for j in range(len(self.prices)):
            if j not in M and self.weights[j] < capacity:
                common_price += self.prices[j]
                capacity -= self.weights[j]
                X.add(j)
        return X, common_price


    def solve(self):
        k = 9  # для 90% точности алгоритма
        for M_array in self.__generate_set(k):
            M = set(M_array)
            common_weight = sum(self.weights[i] for i in M)
            if common_weight > self.capacity:
                continue
            M_price = sum(self.prices[i] for i in M)
            X, X_price = self.__greed_search(M)
            if M_price + X_price > self.answer:
                self.answer = M_price + X_price
                self.items = M | X


    def get_answer(self) -> int:
        return self.answer

    def get_items(self) -> list:
        return list(self.items)