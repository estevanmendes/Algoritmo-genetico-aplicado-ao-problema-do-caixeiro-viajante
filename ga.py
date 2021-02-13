import numpy as np

class Genetic_algoruthm():

    def __init__ (self,number_of_city=20,population_size=5,mutation_prob=0.001,crossover_prob=0.6,cost_matrix=False,random_seed=42):
        self.number_of_city=number_of_city
        self.population_size=population_size
        self.mutation_prob=mutation_prob
        self.crossover_prob=crossover_prob
        self.cost_matrix=cost_matrix
        self.seed=random_seed
        
        np.random.seed(random_seed)

        if not cost_matrix:
            self.cost_matrix=np.random.rand(number_of_city,number_of_city)


        initial_pop=np.tile(np.arange(1,number_of_city+1),(population_size,1))

        for i in range(population_size):
            np.random.shuffle(initial_pop[i,1:-1])

        self.popolation=initial_pop
        self.fitness=np.zeros(population_size)


    def fitness(self,cost_matrix=False,maxmization=False):
        fitness_matrix=1./self.cost_matrix
        self.fitness_matrix=fitness_matrix

        for i in range(self.popolation):
            for j in range(self.number_of_city):
                self.fitness[i]+=fitness_matrix[self.popolation[j:j+1]]

        pass

    def run(self,generations=10):
        pass

    def Mutation(self):
        pass

class Crossover(Genetic_algoruthm):

    def SCRX(self):
        pass
