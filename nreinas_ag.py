#!/usr/bin/python
#-*- coding:UTF-8 -*-

# Deap es un framework de computación evolutiva
# lo que nos permite trabajar con algoritmos genéticos
# Para instalar --> sudo pip install deap
# https://deap.readthedocs.io/en/master/tutorials/advanced/gp.html

# https://deap.readthedocs.io/en/master/api/algo.html#module-deap.algorithms
from deap import algorithms

# https://deap.readthedocs.io/en/master/api/base.html#module-deap.base
from deap import base

# https://deap.readthedocs.io/en/master/api/creator.html#deap.creator.create
from deap import creator

# https://deap.readthedocs.io/en/master/api/tools.html#module-deap.tools
from deap import tools

# Librerias
import random
import sys

# Cantidad de Reinas
reinas = int(sys.argv[1])

# Evaluar cada reina (calcular fitness)
def evaluar(individual):
    # tamaño del tablero
    size = len(individual)

    # Cuenta el número de choques con otras reinas.
    # Los choques solo pueden ser diagonales, se cuentasn en cada diagonal
    di = [0] * (2*size-1)
    dr = [0] * (2*size-1)
    
    # Sumar el número de reinas en cada diagonal
    for i in range(size):
        di[i+individual[i]] += 1
        dr[size-1-i+individual[i]] += 1
    
    # Contar el número de choques en cada diagonal
    choques = 0
    for i in range(2*size-1):
        if di[i] > 1:
            choques += di[i] - 1
        if dr[i] > 1:
            choques += dr[i] - 1
    return choques,

# Definimos el problema (Encontrar mejor fitness, reinas como individuos)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Usamos las herramientas del framework
# https://deap.readthedocs.io/en/master/api/tools.html#module-deap.tools
toolbox = base.Toolbox()

# Como hay una sola reina por linea
# los individuos se representan como una permutacion
toolbox.register("permutation", random.sample, range(reinas), reinas)

# Un individuo representa la posicion de cada reina
# Almacenamos solo la linea, la columna es el indice del numero en la lista
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)

# Generamosla poblacion que es una lista de individuos
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Fucniones genéticas
toolbox.register("evaluate", evaluar)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/reinas)
toolbox.register("select", tools.selTournament, tournsize=3)

# Obtenemos una poblacion de 100 individuos
poblacion = toolbox.population(n=100)

# Obtenemos el mejor de todos (mejor fitness)
mejor = tools.HallOfFame(1)

# Iniciamos el algoritmo
algorithms.eaSimple(poblacion, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, halloffame=mejor, verbose=False)

# Mostramos la población
print(poblacion)
print("")

# Mostramos el mejor
print(mejor)
