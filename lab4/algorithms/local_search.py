from algorithms.base import Base
class LocalSearch(Base):
    def __init__(self, flows, distances, iter_num=10):
        super().__init__(flows, distances, iter_num)

    def solve(self):
        dont_look_bits = [0] * len(self.positions)
        for _ in range(self.iter_num):
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


