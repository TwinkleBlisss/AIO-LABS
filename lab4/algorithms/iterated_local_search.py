from algorithms.base import Base
import random

class IteratedLocalSearch(Base):
    def __init__(self, flows, distances, iter_num=10):
        super().__init__(flows, distances, iter_num)

    def __perturbation(self):
        city1, city2 = random.sample(self.positions, 2)
        city1, city2 = min(city1, city2), max(city1, city2)
        self.positions = self.positions[:city1] + self.positions[city1:city2][::-1] + self.positions[city2:]

    def solve(self):
        dont_look_bits = [0] * len(self.positions)
        for _ in range(self.iter_num):
            self.__perturbation()
            for i in range(len(self.positions)):
                if dont_look_bits[i]:
                    continue
                improved = False
                for j in range(len(self.positions)):
                    if dont_look_bits[j] or i == j:
                        continue
                    new_positions = self.positions.copy()
                    new_positions[i], new_positions[j] = new_positions[j], new_positions[i]
                    new_answer = self.get_answer(new_positions)
                    if new_answer < self.answer:
                        improved = True
                        self.positions = new_positions
                        self.answer = new_answer
                if not improved:
                    dont_look_bits[i] = 1

        return self.positions, self.answer


