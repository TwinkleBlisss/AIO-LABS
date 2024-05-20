# TODO: Переделать в класс

import random


# Генерация начальной популяции
def generate_population(size, num_cities):
    population = []
    for _ in range(size):
        chromosome = random.sample(range(num_cities), num_cities)
        population.append(chromosome)
    return population


# Вычисление длины маршрута
def calculate_route_length(route, distances):
    total_length = 0
    for i in range(len(route) - 1):
        total_length += distances[route[i]][route[i + 1]]
    total_length += distances[route[-1]][route[0]]  # Замыкаем маршрут
    return total_length


# Скрещивание (PMX)
def crossover(parent1, parent2):
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
def mutate(chromosome):
    idx1, idx2 = random.sample(range(len(chromosome)), 2)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome


# Генетический алгоритм для задачи коммивояжера
def genetic_algorithm(distances, population_size=5, generations=3, mutation_rate=0.01):
    num_cities = len(distances)
    population = generate_population(population_size, num_cities)
    print("First Population:", population)

    for _ in range(generations):
        fitness_scores = [1 / calculate_route_length(chromosome, distances) for chromosome in population]

        print(f"\n\nPopulation in generation №{_}:", population)
        print(f"\nFitness scores in generation №{_}:", fitness_scores)

        selected_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:10]
        selected_population = [population[i] for i in selected_indices]



        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(selected_population, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child) if random.random() < mutation_rate else child
            new_population.append(child)

        population = new_population

    best_route = max(population, key=lambda chromosome: 1 / calculate_route_length(chromosome, distances))
    best_length = calculate_route_length(best_route, distances)
    return best_route, best_length


# Пример использования генетического алгоритма для задачи коммивояжера
distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
best_route, best_length = genetic_algorithm(distances)
print("Лучший маршрут:", best_route)
print("Длина лучшего маршрута:", best_length)

print(calculate_route_length([0, 1, 2, 3], distances))