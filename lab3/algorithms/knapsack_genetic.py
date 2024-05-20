# TODO: Переделать в класс

import random


# Генерация начальной популяции
def generate_population(size, num_items):
    population = []
    for _ in range(size):
        chromosome = [random.randint(0, 1) for _ in range(num_items)]
        population.append(chromosome)
    return population


# Оценка приспособленности особи
def fitness(chromosome, values, weights, max_weight):
    total_value = 0
    total_weight = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += values[i]
            total_weight += weights[i]
    if total_weight > max_weight:
        return 0  # Штраф за превышение веса
    else:
        return total_value


# Скрещивание (одноточечное)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Мутация
def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome


# Генетический алгоритм
def genetic_algorithm(values, weights, max_weight, population_size=100, generations=100, mutation_rate=0.01):
    num_items = len(values)
    population = generate_population(population_size, num_items)

    for _ in range(generations):
        fitness_scores = [fitness(chromosome, values, weights, max_weight) for chromosome in population]

        # Выбор лучших особей для скрещивания
        selected_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:10]
        selected_population = [population[i] for i in selected_indices]

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(selected_population, k=2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    best_chromosome = max(population, key=lambda chromosome: fitness(chromosome, values, weights, max_weight))
    best_value = fitness(best_chromosome, values, weights, max_weight)
    return best_chromosome, best_value


# Пример использования генетического алгоритма для задачи о рюкзаке
values = [3, 2, 5, 8]
weights = [4, 3, 6, 9]
max_weight = 10
best_solution, best_value = genetic_algorithm(values, weights, max_weight)
print("Лучшее решение:", best_solution)
print("Лучшее значение:", best_value)
