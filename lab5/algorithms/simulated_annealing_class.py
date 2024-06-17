import math
import numpy as np
from copy import deepcopy
from algorithms.cell_formation_problem import CFP

class SimulatedAnnealing:
    def __init__(self, matrix, T0=500, Tf=200,
                 alpha=0.8, max_iterations=200, D=50,
                 max_stagnant=25, trapped_percentage=0.25):
        self.matrix = matrix
        self.T0 = T0
        self.Tf = Tf
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.D = D # period of exchange move
        self.max_stagnant = max_stagnant
        self.counter = self.counter_mc = self.counter_trapped \
            = self.counter_stagnant = 0
        self.current_solution = None
        self.best_local_solution = None
        self.best_solution = None
        self.trapped_percentage = trapped_percentage
        self.current_cells = 0
        self.cfp = None
        self.optimal_cells = self.current_cells

    def __move_helper(self, split_parts):

        suitable_cells = [index for index, cell in enumerate(split_parts) if len(cell) >= 2]
        cell_index = suitable_cells[np.random.randint(0, len(suitable_cells))]
        cell = split_parts[cell_index]
        part = cell[np.random.randint(0, len(cell))]
        cell.remove(part)
        return cell, cell_index, part

    def __single_move(self, solution):
        split_parts, _ = deepcopy(solution)
        cell, cell_index, part = self.__move_helper(split_parts)
        max_target = -99999
        best = None
        for i in range(len(split_parts)):
            if i != cell_index:
                split_parts[i].append(part)
                new_split_machines = self.cfp.split_by_machines(split_parts)
                new_target = self.cfp.target_function(split_parts, new_split_machines)
                if new_target > max_target:
                    max_target = new_target
                    best = deepcopy(split_parts), new_split_machines
                split_parts[i].pop()
        return best

    def __exchange_move(self, solution):
        split_parts, _ = deepcopy(solution)
        cell, cell_index, part = self.__move_helper(split_parts)
        max_target = -99999
        best = None
        for i in range(len(split_parts)):
            if i != cell_index:
                exchange_part = split_parts[i][np.random.randint(0, len(split_parts[i]))]
                split_parts[i].remove(exchange_part)
                cell.append(exchange_part)
                split_parts[i].append(part)
                new_split_machines = self.cfp.split_by_machines(split_parts)
                new_target = self.cfp.target_function(split_parts, new_split_machines)
                if new_target > max_target:
                    max_target = new_target
                    best = deepcopy(split_parts), new_split_machines
                split_parts[i].pop()
                split_parts[i].append(exchange_part)
                cell.remove(exchange_part)
        return best

    def __iteration(self):
        while self.counter_mc < self.max_iterations and self.counter_trapped < self.max_iterations * self.trapped_percentage:
            # if self.counter_mc % 50 == 0:
            #     print(f"iter {self.counter_mc}/{self.max_iterations}")

            new_solution = self.__single_move(self.current_solution)
            if self.counter % self.D == 0:
                new_solution = self.__exchange_move(new_solution)
            new_solution_target = self.cfp.target_function(new_solution[0], new_solution[1])
            best_local_solution_target = self.cfp.target_function(self.best_local_solution[0],
                                                                  self.best_local_solution[1])
            if new_solution_target > best_local_solution_target:
                self.current_solution = self.best_local_solution = new_solution
                self.counter_stagnant = 0
            elif new_solution_target == best_local_solution_target:
                self.current_solution = new_solution
                self.counter_stagnant += 1
            else:
                delta_target = new_solution_target - self.cfp.target_function(self.current_solution[0],
                                                                              self.current_solution[1])
                if math.exp(delta_target / self.T) > np.random.uniform():
                    self.current_solution = new_solution
                    self.counter_trapped = 0
                else:
                    self.counter_trapped += 1
            self.counter_mc += 1

    def __search(self):
        self.counter = self.counter_mc = self.counter_stagnant = self.counter_trapped = 0
        self.T = self.T0
        self.__iteration()
        while self.T > self.Tf and self.counter_stagnant <= self.max_stagnant:
            # if self.counter % 50 == 0:
            #     print(f"iter {self.counter}/{self.max_iterations}")

            self.T *= self.alpha
            self.counter_mc = 0
            self.counter += 1
            self.__iteration()

    def solve(self):
        self.current_cells = 2
        self.cfp = CFP(self.matrix, self.current_cells)
        self.best_local_solution = self.best_solution = self.current_solution = self.cfp.initial_solution()
        self.optimal_cells = self.current_cells
        self.__search()
        while (self.cfp.target_function(self.best_local_solution[0], self.best_local_solution[1]) >
               self.cfp.target_function(self.best_solution[0], self.best_solution[1])):
            self.best_solution = self.best_local_solution
            self.optimal_cells = self.current_cells
            self.current_cells += 1
            self.cfp = CFP(self.matrix, self.current_cells)
            self.current_solution = self.cfp.initial_solution()
            self.best_local_solution = self.current_solution
            self.__search()

        return self.best_solution, self.cfp.target_function(*self.best_local_solution)
