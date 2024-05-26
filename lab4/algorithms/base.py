import itertools
import random


class Base:
    def __init__(self, flows, distances, iter_num=20):
        self.flows = flows
        self.distances = distances
        self.positions = list(range(len(flows)))
        random.shuffle(self.positions)
        self.answer = self.get_answer()
        self.iter_num = iter_num


    def get_answer(self, positions=None):
        if positions is None:
            positions = self.positions
        answer = 0
        for i in range(len(self.flows)):
            for j in range(len(self.distances)):
                answer += self.distances[self.positions[i]][self.positions[j]] * self.flows[i][j]
        return answer

    def solve():
        pass

