import random
from algorithms.base import BaseGenetic

class TSP(BaseGenetic):
    def __init__(self, distances, population_size=200, generations=5000, mutation_rate=0.05):
        super().__init__()
        self.distances = distances
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

# Генерация начальной популяции
    def generate_population(self, num_cities):
        population = []
        for _ in range(self.population_size):
            chromosome = random.sample(range(num_cities), num_cities)
            population.append(chromosome)
        return population


    # Вычисление длины маршрута
    def fitness(self, route):
        total_length = 0
        for i in range(len(route) - 1):
            total_length += self.distances[route[i]][route[i + 1]]
        total_length += self.distances[route[-1]][route[0]]  # Замыкаем маршрут
        return total_length


    # Скрещивание (PMX)
    def crossover(self, parent1, parent2):
        size = len(parent1)
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)

        child = [-1] * size
        for i in range(start, end + 1):
            child[i] = parent1[i]

        for i in range(size):
            if parent2[i] not in child:
                j = i
                while child[j] != -1:
                    j = parent2.index(parent1[j])
                child[j] = parent2[i]

        return child


    # Мутация (Swap mutation)
    def mutate(self, chromosome):
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome


    # Генетический алгоритм для задачи коммивояжера
    def genetic_algorithm(self):
        num_cities = len(self.distances)
        population = self.generate_population(num_cities)
        # print("First Population:", population)

        for _ in range(self.generations):
            fitness_scores = [1 / self.fitness(chromosome) for chromosome in population]

            selected_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:10]
            selected_population = [population[i] for i in selected_indices]

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.choices(selected_population, k=2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child) if random.random() < self.mutation_rate else child
                new_population.append(child)

            population = new_population

        best_route = max(population, key=lambda chromosome: 1 / self.fitness(chromosome))
        best_length = self.fitness(best_route)
        return best_route, best_length

