import numpy as np

class Genetic_algoruthm():

    def __init__ (self,number_of_city=20,population_size=100,mutation_prob=0.001,crossover_prob=0.6,cost_matrix=False,random_seed=42):
        self.number_of_city=number_of_city
        self.population_size=population_size
        self.mutation_prob=mutation_prob
        self.crossover_prob=crossover_prob
        self.cost_matrix=cost_matrix
        self.seed=random_seed
        
        np.random.seed(random_seed)

        if not cost_matrix:
            self.cost_matrix=np.random.rand(number_of_city,number_of_city)


        initial_pop=np.tile(np.arange(number_of_city),(population_size,1))

        for i in range(population_size):
            np.random.shuffle(initial_pop[i,1:-1])

        self.population=initial_pop
        self.fitness_pop=np.zeros(population_size)


    def fitness(self,cost_matrix=False,maxmization=False):
        fitness_matrix=1./self.cost_matrix
        self.fitness_matrix=fitness_matrix

        for i in range(self.population_size):
            for j in range(self.number_of_city-1):
                self.fitness_pop[i]+=fitness_matrix[self.population[i,j],self.population[i,j+1]]


    def Mutation(self):
        pass


    def roullete_wheel_selection(self,n_parents):
        parents_selected=np.zeros((n_parents,2))
        tri_lower=np.tril(np.ones((self.population_size,self.population_size)))
        wheel=np.dot(tri_lower,self.fitness_pop)
        for i in range(n_parents)
            for j in range(2):
                spin=np.random.uniform(max(wheel))
                parents_selected[i,j]=(np.array(np.where(np.greater_equal(wheel,spin)==True)))[0,0]
        return parents_selected

    def choice():
        np.linspace(n1,n2)
        np.
        



class Crossover(Genetic_algoruthm):

    def SCRX(self):
        pass


    def run(self):
        pass