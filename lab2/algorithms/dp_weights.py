from algorithms.base import Base


class DP_weights(Base):
    def __init__(self, weights: list, prices: list, capacity: int):
        super().__init__(weights, prices, capacity)
        self.dp = [[0] * (self.capacity + 1) for _ in range(len(self.weights) + 1)]

    def solve(self) -> None:
        for i in range(len(self.dp) - 1):
            for j in range(self.capacity + 1):
                if self.weights[i] <= j:
                    self.dp[i][j] = max(self.dp[i - 1][j], self.prices[i] + self.dp[i - 1][j - self.weights[i]])
                else:
                    self.dp[i][j] = self.dp[i - 1][j]
        # for i in range(len(self.dp)):
        #     print(*self.dp[i])
        self.__find_items(len(self.weights) - 1, self.capacity)
        items = [0] * len(self.weights)
        for i in self.items:
            items[i] = 1
        self.items = items
        self.solution_number = len(self.dp) * len(self.dp[0])
        self.answer = self.dp[-1][-1]

    def __find_items(self, pos: int, weight: int):
        if self.dp[pos][weight] == 0:
            return 0
        if self.dp[pos - 1][weight] == self.dp[pos][weight]:
            self.__find_items(pos - 1, weight)
        else:
            self.__find_items(pos - 1, weight - self.weights[pos])
            self.items.append(pos)

