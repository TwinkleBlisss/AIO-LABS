from lab2.algorithms.base import Base


class TwoApprox(Base):
    def __init__(self, weights: list, prices: list, capacity: int):
        super().__init__(weights, prices, capacity)
        self.items = []
        self.answer = 0

    def __count_arg_sort(self, arr: list[int]) -> list[int]:
        """
        Сортировка подсчетом.
        Выбрана именно она, так как позволяет не сортировать одновременно все массивы.
        :return: Индексы, на которых должны стоять элементы.
        """
        length = len(arr)
        counting_array = [0 for _ in range(max(arr) + 1)]
        result_indices = [0 for _ in range(length)]
        indices = [i for i in range(length)]
        for num in arr:
            counting_array[num] += 1
        for i in range(1, len(counting_array)):
            counting_array[i] += counting_array[i - 1]
        i = length - 1
        while i >= 0:
            pos = counting_array[arr[i]] - 1
            result_indices[pos] = indices[i]
            counting_array[arr[i]] -= 1
            i -= 1
        return result_indices

    def __greed(self):
        """
        Жадный алгоритм, в котором мы кладём в рюкзак самые дорогие предметы.
        """
        sorted_indices = self.__count_arg_sort(self.prices)
        knapsack = [0 for _ in range(len(self.prices))]
        remaining_capacity = self.capacity
        profit = 0
        for i in reversed(sorted_indices):
            if self.weights[i] <= remaining_capacity:
                profit += self.prices[i]
                knapsack[i] = 1
                remaining_capacity -= self.weights[i]
        return profit, knapsack

    def __quality_greed(self):
        """
        Жадный алгоритм, в котором мы кладём в рюкзак предметы, основываясь на качестве (цена/вес).
        """
        quality = [round(self.prices[i] / self.weights[i]) for i in range(len(self.prices))]
        sorted_indices = self.__count_arg_sort(quality)
        knapsack = [0 for _ in range(len(self.prices))]
        remaining_capacity = self.capacity
        profit = 0
        for i in reversed(sorted_indices):
            if self.weights[i] <= remaining_capacity:
                profit += self.prices[i]
                knapsack[i] = 1
                remaining_capacity -= self.weights[i]
        return profit, knapsack

    def solve(self):
        g_cost, g_knapsack = self.__greed()
        qg_cost, qg_knapsack = self.__quality_greed()
        if g_cost > qg_cost:
            self.items = g_knapsack
            self.answer = g_cost
        else:
            self.items = qg_knapsack
            self.answer = qg_cost

    def get_answer(self):
        return self.answer

    def get_items(self):
        return self.items


if __name__ == '__main__':
    w = [12, 7, 11, 8, 9]
    p = [24, 13, 23, 15, 16]
    c = 26
    s = [0, 1, 1, 1, 0]  # оптимум = 51 против 47 от этого алгоритма
    two_approx = TwoApprox(w, p, c)
    two_approx.solve()
    print(two_approx.get_answer())
    print(two_approx.get_items())
