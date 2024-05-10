from lab2.algorithms.base import Base


class DP_weights(Base):
    def __init__(self, weights: list, prices: list, capacity: int):
        super().__init__(weights, prices, capacity)
        self.dp = [[0] * (self.capacity + 1)] * len(self.weights)
        self.items = []

    def solve(self) -> None:
        for i in range(1, len(self.dp)):
            for j in range(self.capacity + 1):
                if self.weights[i] <= j:
                    self.dp[i][j] = max(self.dp[i - 1][j], self.prices[i] + self.dp[i - 1][j - self.weights[i]])
                else:
                    self.dp[i][j] = self.dp[i - 1][j]
        self.__find_items(len(self.weights) - 1, self.capacity)

    def __find_items(self, pos: int, weight: int) -> None:
        if self.dp[pos][weight] == 0:
            return None
        if self.dp[pos - 1][weight] == self.dp[pos][weight]:
            self.__find_items(pos - 1, weight)
        else:
            self.__find_items(pos - 1, weight - self.weights[pos])
            self.items.append(pos)

    def get_answer(self) -> int:
        return self.dp[-1][-1]

    def get_items(self) -> list:
        return self.items
