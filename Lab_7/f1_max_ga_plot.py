import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from deap import base, creator, tools, algorithms

# Define the function f1(x1, x2)
def f1(individual):
    x1, x2 = individual
    z1 = math.sqrt(x1**2 + x2**2)
    z2 = math.sqrt((x1 - 1)**2 + (x2 + 1)**2)
    
    # To avoid division by zero
    if z1 == 0:
        term1 = 0
    else:
        term1 = math.sin(4 * z1) / z1
    
    if z2 == 0:
        term2 = 0
    else:
        term2 = math.sin(2.5 * z2) / z2
    
    return term1 + term2,

# Define the DEAP toolbox and the Genetic Algorithm
def main():
    # Define the creator
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Define the toolbox
    toolbox = base.Toolbox()
    
    # Attribute generator
    toolbox.register("attr_float", random.uniform, -5, 5)
    
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Operator registering
    toolbox.register("evaluate", f1)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Genetic Algorithm parameters
    population_size = 300
    generations = 50
    cxpb = 0.5  # Crossover probability
    mutpb = 0.2  # Mutation probability

    # Initialize population
    population = toolbox.population(n=population_size)

    # Hall of Fame to store the best individual
    hof = tools.HallOfFame(1)

    # Statistics to collect during the run
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda x: sum([ind[0] for ind in x])/len(x))
    stats.register("std", lambda x: (sum([(ind[0]-sum([i[0] for i in x])/len(x))**2 for ind in x])/len(x))**0.5)
    stats.register("min", min)
    stats.register("max", max)

    # Run the Genetic Algorithm
    algorithms.eaSimple(population, toolbox, cxpb, mutpb, generations, stats=stats, halloffame=hof, verbose=True)

    # Print the best individual
    best_ind = hof[0]
    print("Best individual is:", best_ind, best_ind.fitness.values)

    # 3D plot of f1
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = np.vectorize(lambda x, y: f1([x, y])[0])(x, y)

    angles = [(30, 30), (60, 30), (90, 30)]

    for i, (elev, azim) in enumerate(angles):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis')

        # Mark the best individual found by the genetic algorithm
        best_x1, best_x2 = best_ind
        best_z = f1(best_ind)[0]
        ax.scatter(best_x1, best_x2, best_z, color='r', s=100)  # Red color, size 100

        ax.set_xlabel('X1')
        ax.set_ylabel('X2')
        ax.set_zlabel('f1(X1, X2)')

        ax.view_init(elev=elev, azim=azim)
        plt.savefig(f'f1_3D_{elev}_{azim}.pdf')
        plt.close(fig)
        print(f"Plot saved as 'f1_#3D{elev}_{azim}.pdf'.")

if __name__ == "__main__":
    main()