import copy
import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from individual import Individual

class Population():

    best_fit_plt    = []
    mean_fit_plt    = []
    diversity       = []
    max_diversity   = None
    best_individual = None

    def __init__(self, encoding, psize, csize, min_bound, max_bound, ctax, mtax, generations, is_bin, el, tsize = None):
        self.individuals = [Individual(csize, encoding, min_bound, max_bound) for i in range (0, psize)]
        self.generations = generations
        self.psize = psize
        self.csize = csize
        self.ctax = ctax
        self.mtax = mtax
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.encoding = encoding
        self.is_bin = is_bin
        self.has_elitism = el
        self.tsize = tsize

    def _diversity(self):
        ''' tks @markx3 '''
        chromos = np.array([ind.chromosome for ind in self.individuals])
        ci = np.sum(chromos, axis=0) / self.psize
        div = np.sum((chromos - ci) ** 2)
        self.diversity.append(div)

    def evolve(self):
        print ('First population:\n{}'.format(self.__str__()))
        generation = 0
        while(generation < self.generations):
            self._diversity()
            parents = self._select()
            self._crossover(parents)
            self._mutate()
            generation += 1
        print ('Last population:\n{}'.format(self.__str__()))
        self._plot()
        self.get_best_result()

    def _select(self):
        ''' get the best individual in the generation '''
        max_fitness = 0.0
        for i in self.individuals:
            i.eval_fitness()
            if (i.fitness > max_fitness):
                max_fitness = i.fitness
                if (self.best_individual == None):
                    self.best_individual = i
                if (i.fitness > self.best_individual.fitness):
                    self.best_individual = i
        self.best_fit_plt += [max_fitness]
        sum_fitness = np.sum([i.fitness for i in self.individuals])
        self.mean_fit_plt += [float(sum_fitness) / self.psize]
        for i in self.individuals:
            i.fitness = i.fitness / sum_fitness
        if (self.tsize != None):
            return self._tournment()
        else:
            return self._roulette()

    def _crossover(self, parents):
        mates = 0
        if (self.has_elitism):
            self.individuals[mates] = copy.deepcopy(self.best_individual)
            self.best_individual
            mates += 1
        father, mother = None, None
        while (mates <= self.psize - 1):
            ctax = np.random.uniform(0, 1)
            individual = parents[np.random.randint(self.psize)]
            if (ctax > self.ctax):
                self.individuals[mates].chromosome = individual.chromosome
                mates += 1
            else:
                if (father == None):
                    father = individual
                else:
                    mother = individual
                    childs = father.mate(mother)
                    for c in childs:
                        if (mates < self.psize):
                            self.individuals[mates].chromosome = c
                            mates += 1
                    father, mother = None, None

    def _mutate(self):
        c = 0
        if (self.has_elitism):
            for i in range(1, self.psize):
                self.individuals[i].mutate(self.mtax)
        else:
            for i in range(self.psize):
                self.individuals[i].mutate(self.mtax)

    def _roulette(self):
        indexes = np.random.choice(self.psize, self.psize, p=[i.fitness for i in self.individuals])
        parents = [self.individuals[i] for i in indexes]
        return parents

    def _tournment(self):
        winners = []
        for i in range(self.psize):
            gladiators = random.sample(self.individuals, self.tsize)
            winners.append(sorted(gladiators, key=lambda ind: ind.fitness, reverse=True)[0])
        return winners

    def _plot(self):
        ''' Fig 1 - Fitness '''
        plt.figure(1)
        plt.plot(self.best_fit_plt)

        plt.plot(self.mean_fit_plt)
        plt.legend(['best', 'mean'])
        plt.ylabel('fitness')
        plt.xlabel('generation')

        ''' Fig 2 - Diversidade '''
        plt.figure(2)
        self.diversity = [(float(x) / max(self.diversity)) for x in self.diversity]
        plt.plot(self.diversity)
        plt.ylabel('diversity')
        plt.xlabel('generation')

        plt.show()

    def get_best_result(self):
        best = sorted(self.individuals, key=lambda i: i.fitness, reverse=True)[0]
        best.eval_fitness()
        if (hasattr(best, 'num_genes')):
            if (best.num_genes):
                print ('\nBest individual: {}'.format(best.get_result()))
        else:
            print ('\nBest individual: {}. Fitness: {}'.format(str(best), best.fitness))

    def __str__(self):
        strn = ''
        for i in self.individuals:
            strn += str(i) + '\n'
        return strn
