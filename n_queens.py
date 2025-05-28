import random
import matplotlib.pyplot as plt
import pandas as pd

N = 8
population_size = 1000
max_generations = 2000
mutation_rate = 0.05
visualize_every = 1
max_fitness = 28

pop_size_options = [10, 100, 500, 1000, 2000]
max_generations_options = [1000]
mutation_rate_options = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1]


def create_individual():
    genes = [random.randint(0, N-1) for _ in range(N)]
    fitness = evaluate_fitness(genes)
    return (genes, fitness)

def evaluate_fitness(genes):
    non_attacking = 0
    for i in range(len(genes)):
        for j in range(i+1, len(genes)):
            if genes[i] != genes[j] and abs(genes[i] - genes[j]) != abs(i-j):
                non_attacking += 1
    return non_attacking

def create_population(population_size):
    population = [create_individual() for i in range(population_size)]
    population.sort(key=lambda x: x[1], reverse=True)
    return population

def select_parent(population):
    new = random.sample(population, k=5)
    new.sort(key=lambda x: x[1], reverse=True)
    return new[0]

# crossover()
def crossover_n_pontos(parent1, parent2, n_pontos):
    ks = []

    assert n_pontos < len(parent1[0])
    # pegar n_pontos
    while len(ks) != n_pontos:
        k = random.randint(0, N-1)
        if k not in ks and (sum(ks) + k) < (len(parent1[0])-1):
            ks.append(k)

    # print(ks)
    # print(parent1[0])
    child = []
    
    for i, k in enumerate(ks):
        if i == 0:
            child.extend(parent1[0][:k])
        else:
            parent_atual = parent1 if i % 2 == 0 else parent2
            child.extend(parent_atual[0][ks[-1]:k])

    # print(child)
    # print(parent1[0], parent2[0])
    # print(child)
    # print(len(child))
    # child = parent1[0][:k] + parent2[0][k:]
    # print(parent1, parent2)
    return (child, evaluate_fitness(child))

def crossover(parent1, parent2):
    k = random.randint(0, N-1)

    child = parent1[0][:k] + parent2[0][k:] 
    # print(len(child))
    # print(parent1, parent2)
    return (child, evaluate_fitness(child))


def mutate(individual, mutation_rate):
    genes, _ = individual
    if random.random() < mutation_rate:
        i = random.randint(0, N-1)
        genes[i] = random.randint(0, N-1)
    return (genes, evaluate_fitness(genes))

def evolve_population(population, mutation_rate):
    new_generation = population[:10]
    while len(new_generation) < population_size:
        parent1 = select_parent(population)
        parent2 = select_parent(population)
        child = crossover_n_pontos(parent1, parent2, 3)
        child = mutate(child, mutation_rate)
        new_generation.append(child)
    new_generation.sort(key=lambda x: x[1], reverse=True)
    return new_generation

def plot_board(genes, generation, fitness, N):
    plt.figure(figsize=(6, 6))
    plt.title(f"Generation: {generation} - Fitness: {fitness}")

    # Definir os ticks nos eixos
    plt.xticks(range(N))
    plt.yticks(range(N))
    
    # Ativar a grade
    plt.grid(True)
    
    # Inverter o eixo y para o padrão de coordenadas (0, 0) no canto superior esquerdo
    plt.gca().invert_yaxis()

    # Desenhar as células do tabuleiro
    for x in range(N):
        for y in range(N):
            color = 'white' if (x + y) % 2 == 0 else 'gray'
            plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color=color))  # Corrigido para (x, y, width, height)
    
    # Plotar as "estrelas" nos locais dos genes
    for col, row in enumerate(genes):
        plt.text(col + 0.5, row + 0.5, 'X', fontsize=24, ha='center', va='center', color='red')

    # Definir os limites do gráfico
    plt.xlim(0, N)
    plt.ylim(0, N)

    # Definir a proporção do gráfico para que as células tenham o mesmo tamanho
    plt.gca().set_aspect('equal')

    # Exibir o gráfico
    plt.show()

def run_genetic_algorithm(max_generations, population_size, mutation_rate):
    population = create_population(population_size)
    
    for generation in range(1, max_generations+1):
        # print(population[0])
        best_indivudial = population[0]
        if best_indivudial[1] >= 28:
            print("Solução encontrada na geração:", generation)
            # plot_board(best_indivudial[0], generation=generation, fitness=best_indivudial[1], N=N)
            return "Solução encontrada na geração: " + str(generation)

        if generation % visualize_every == 0:
            print("Generation", generation, "Best fitness", best_indivudial[1])
            # plot_board(best_indivudial[0], generation, best_indivudial[1], N)

        population = evolve_population(population, mutation_rate=mutation_rate)
        # print(population)

    print("Não foi encontrada uma soluçãoo perfeita")
    # plot_board(population[0][0], max_generations, population[0][1], N)
    return "Solução não encontrada"

dados = []
for pop in pop_size_options:
    for mut_rate in mutation_rate_options:
        for max_gen in max_generations_options:
            r = run_genetic_algorithm(max_gen, pop, mut_rate)
            dados.append([pop, mut_rate, max_gen, r])

df = pd.DataFrame(dados, columns=["Population Size", "Mutation Rate", 'Max Generations', "Resultado"])

df.to_excel('resultados.xlsx', index=False)
