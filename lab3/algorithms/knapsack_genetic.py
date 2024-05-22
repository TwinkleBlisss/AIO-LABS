import random
import math
from algorithms.base import BaseGenetic

class Knapsack(BaseGenetic):
    def __init__(self, values, weights, max_weight, population_size=100, generations=100, mutation_rate=0.07):
        super().__init__()
        self.values = values
        self.weights = weights
        self.max_weight = max_weight
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate


# Генерация начальной популяции
    def generate_population(self, num_items):
        population = []
        for _ in range(self.population_size):
            chromosome = [random.randint(0, 1) for _ in range(num_items)]
            population.append(chromosome)
        return population


    # Оценка приспособленности особи
    def fitness(self, chromosome):
        total_value = 0
        total_weight = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                total_value += self.values[i]
                total_weight += self.weights[i]
        if total_weight > self.max_weight:
            return 0  # Штраф за превышение веса
        else:
            return total_value


    # Скрещивание (одноточечное)
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2


    # Мутация
    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome


    # Генетический алгоритм
    def genetic_algorithm(self):
        num_items = len(self.values)
        population = self.generate_population(num_items)

        for _ in range(self.generations):
            fitness_scores = [[self.fitness(population[i]), i]
                              for i in range(len(population))]

            # Выбор лучших особей для скрещивания

            indices_count = 10
            fitness_scores.sort(reverse=True)
            selected_indices = random.sample(range(0, len(population) // 4), round(indices_count * 0.5)) + \
                                random.sample(range(len(population) // 4, len(population) // 2), round(indices_count * 0.3)) + \
                                random.sample(range(len(population) // 2, 3 * len(population) // 4), round(indices_count * 0.15)) + \
                               random.sample(range(3 * len(population) // 4, len(population)), round(indices_count * 0.05))
            selected_population = [population[i] for i in selected_indices]

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.choices(selected_population, k=2)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])

            population = new_population

        best_chromosome = max(population, key=lambda chromosome: self.fitness(chromosome))
        best_value = self.fitness(best_chromosome)
        return best_chromosome, best_value
