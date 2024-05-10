from algorithms.base import Base


class Thing:
    def __init__(self, position, weight, profit):
        self.position = position
        self.weight = weight
        self.profit = profit
        self.quality = self.profit / self.weight



class BranchAndBound(Base):
    def __init__(self, weights: list, prices: list, capacity: int):
        super().__init__(weights, prices, capacity)
        self.things = [Thing(i, weights[i], prices[i]) for i in range(len(weights))]
        self.things.sort(key=lambda x: x.quality, reverse=True)
        self.answer = 0
        self.items = [0] * len(prices)

    def relaxed_greed(self, k, weight, profit):
        """
        Жадный нецелый алгоритм.
        """
        # print("sorted_things", self.things)
        knapsack = [0 for _ in range(len(self.things))]
        remaining_capacity = self.capacity - weight
        for i in range(k + 1, len(self.things)):
            if self.things[i].weight <= remaining_capacity:
                profit += self.things[i].profit
                knapsack[self.things[i].position] = 1
                remaining_capacity -= self.things[i].weight
            else:
                profit += (remaining_capacity / self.things[i].weight) * self.things[i].profit
                knapsack[self.things[i].position] = remaining_capacity / self.things[i].weight
                remaining_capacity = 0
        return profit

    def branching(self, k, profit, weight, knapsack):
        if weight < self.capacity and profit > self.answer:
            self.answer = profit
            self.items[:] = knapsack[:]
        if k == len(self.things):
            return 0
        self.solution_number += 1
        if weight + self.things[k].weight <= self.capacity:
            knapsack[k] = 1
            self.branching(k + 1, profit + self.things[k].profit, weight + self.things[k].weight, knapsack)
            knapsack[k] = 0
        if self.relaxed_greed(k, weight, profit) > self.answer:
            self.branching(k + 1, profit, weight, knapsack)

    def solve(self):
        self.branching(0, 0, 0, [0] * len(self.things))
        items = self.items
        self.items = [0] * len(self.things)
        for i in range(len(items)):
            if items[i] == 1:
                self.items[self.things[i].position] = 1



    # def knapsack_recursive(i, value, weight, selected_items):
    #     print("i", i, "value", value, "weight", weight, "selected_items", selected_items)
    #     nonlocal max_value
    #     if weight <= capacity and value > max_value:
    #         max_value = value
    #         final_items[:] = selected_items[:]
    #
    #     if i == n:
    #         return
    #
    #     if weight + items[i].weight <= capacity:
    #         new_selected_items = selected_items[:]
    #         new_selected_items[i] = 1
    #         knapsack_recursive(i + 1, value + items[i].value, weight + items[i].weight, new_selected_items)
    #
    #     if bound(i, weight, value) > max_value:
    #         knapsack_recursive(i + 1, value, weight, selected_items)


if __name__ == '__main__':
    w = [3, 2, 1, 4]
    p = [3, 4, 2, 3]
    q = [1, 2, 2, 0.75]
    c = 6
    s = [0, 1, 1, 1, 0]  # оптимум = 51 против 47 от этого алгоритма
    algo = BranchAndBound(w, p, c)
    print(algo.relaxed_greed())
    # algo.solve()
    # print(algo.get_answer())
    # print(algo.get_items())
