import numpy as np
import math

class Individual_Bin:
    def __init__(self, size):
        self.size = size
        self.chromosome = self.__init_chromosome(size)

    def __init_chromosome(self, size):
        return np.random.randint(2, size=size)

    def fitness(self):
        fitness_value = 0
        for gene in range(self.size - 1):
            if self.chromosome[gene] != self.chromosome[gene + 1]:
                fitness_value += 1
        return fitness_value

    def __str__(self):
        return np.array2string(self.chromosome)

class Individual_Int:
    def __init__(self, size, min_bound, max_bound):
        self.size = size
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.chromosome = self.__init_chromosome(size, min_bound, max_bound)

    def __init_chromosome(self, size, min_bound, max_bound):
        return np.random.randint(min_bound, max_bound, size=size)

    def fitness(self):
        fitness_value = 0
        for gene in range(self.size - 1):
            if self.chromosome[gene] % 2 == 0:
                if self.chromosome[gene + 1] % 2 == 1:
                    fitness_value += 1
            else:
                if self.chromosome[gene + 1] % 2 == 0:
                    fitness_value += 1
        return fitness_value

    def __str__(self):
        return np.array2string(self.chromosome)

class Individual_Real:
    def __init__(self, size, min_bound, max_bound):
        self.size = size
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.chromosome = self.__init_chromosome(size, min_bound, max_bound)

    def __init_chromosome(self, size, min_bound, max_bound):
        return np.random.uniform(min_bound, max_bound, size=size)

    ''' Ackley's function '''
    def fitness(self):
    	first_sum = 0.0
    	second_sum = 0.0
    	for gene in self.chromosome:
    		first_sum += gene ** 2.0
    		second_sum += math.cos(2.0 * math.pi * gene)
    	n = float(self.size)
    	return -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e

    def __str__(self):
        return np.array2string(self.chromosome)

class Individual_Perm:
    def __init__(self, size):
        self.size = size
        self.chromosome = self.__init_chromosome(size)

    def __init_chromosome(self, size):
        return np.random.permutation(size)

    def fitness(self):
        return 'fitness int-perm'

    def __str__(self):
        return np.array2string(self.chromosome)

class Individual():

    ''' Return the object according to the encoding '''
    def __new__(cls, size, encoding, min_bound, max_bound):
        if encoding == 'BIN':
            return Individual_Bin(size)
        elif encoding == 'INT':
            return Individual_Int(size, min_bound, max_bound)
        elif encoding == 'REAL':
            return Individual_Real(size, min_bound, max_bound)
        elif encoding == 'INT-PERM':
            return Individual_Perm(size)
        else:
            raise Exception('Invalid encoding')
