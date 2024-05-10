class Base:
    def __init__(self, weights: list, prices: list, capacity: int):
        self.weights = weights
        self.prices = prices
        self.capacity = capacity
        self.solution_number = 0
        self.answer = 0
        self.items = []

    def solve(self):
        pass

    def get_answer(self) -> int:
        return self.answer

    def get_items(self) -> list:
        return self.items

    def get_solution_number(self) -> int:
        return self.solution_number