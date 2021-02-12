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

            
    def fitness(self,cost_matrix=False):
        pass

    
        
class Crossover():
    def __init___(self,):
        pass

    def SCRX(self):
        pass
