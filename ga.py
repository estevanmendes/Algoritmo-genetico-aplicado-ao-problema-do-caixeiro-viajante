import numpy as np

class Genetic_algoruthm():

    def __init__ (self,number_of_city=20,population_size=100,mutation_prob=0.001,crossover_prob=0.6,cost_matrix=False,random_seed=42,generations=100):

        self.number_of_city=number_of_city
        self.population_size=population_size
        self.mutation_prob=mutation_prob
        self.crossover_prob=crossover_prob
        self.generations=generations
        self.cost_matrix=cost_matrix
        self.seed=random_seed
        
        np.random.seed(random_seed)

        if not cost_matrix:
            self.cost_matrix=np.random.rand(number_of_city,number_of_city)*100
            self.cost_matrix[np.diag_indices(number_of_city)]=999*np.ones(number_of_city)

        fitness_matrix=1./self.cost_matrix
        self.fitness_matrix=fitness_matrix

        initial_pop=np.tile(np.arange(number_of_city),(population_size,1))

        for i in range(population_size):
            np.random.shuffle(initial_pop[i,1:-1])

        self.population=initial_pop
        self.fitness_pop=np.zeros(population_size)


    def fitness(self,cost_matrix=False,maxmization=False):

        for i in range(self.population_size):
            for j in range(self.number_of_city-1):
                self.fitness_pop[i]+=self.fitness_matrix[int(self.population[i,j]),int(self.population[i,j+1])]


    def Mutation(self):
        prob=self.mutation_prob
        mutation_random=np.random.uniform(size=self.population_size)
        threshold=np.ones(self.population_size)*prob
        pop_mutated=np.less_equal(mutation_random,threshold)
        temp=np.arange(self.population_size)
        pop_mutated=temp[pop_mutated]
        for  i in pop_mutated:
            changes=np.random.randint(1,self.number_of_city-1,size=2)
            a=int(self.population[i,changes[0]])
            b=int(self.population[i,changes[1]])
            self.population[i,changes[0]]=b
            self.population[i,changes[1]]=a
        

    def roullete_wheel_selection(self):
        parents_selected=np.zeros(2)
        tri_lower=np.tril(np.ones((self.population_size,self.population_size)))
        wheel=np.dot(tri_lower,self.fitness_pop)
        for j in range(2):
            spin=np.random.uniform(max(wheel))
            parents_selected[j]=(np.array(np.where(np.greater_equal(wheel,spin)==True)))[0,0]
        return parents_selected

    def run(self,crossover_function=None,mutation=True):
        children=np.zeros((self.population_size,self.number_of_city))
        if mutation:
            for i in range(self.generations):
                self.fitness()
                for j in range(self.population_size):              
                    parents_number=self.roullete_wheel_selection() 
                    children[j,:]=self.SCRX(parents_number)
                self.population=children
                self.Mutation()
        else:
            for i in range(self.generations):
                self.fitness()
                for j in range(self.population_size):              
                    parents_number=self.roullete_wheel_selection()
                    children[j,:]=self.crossover_function(parents_number)
                self.population=children

   
class Crossover(Genetic_algoruthm):

    def SCRX(self,parents_number):
        
        child=np.zeros(int(self.number_of_city))
        parent1=self.population[int(parents_number[0]),:]
        parent2=self.population[int(parents_number[1]),:]
        equal=np.equal(parent1,parent2)
        child[equal]=parent1[equal]
        differ=np.arange(self.number_of_city)[~equal]
        for i in differ:
            loc1_1=parent1[i-1]
            loc1_2=parent1[i]
            
            loc2_1=parent2[i-1]
            loc2_2=parent2[i]

            fit1=self.fitness_matrix[int(loc1_1),int(loc1_2)]
            fit2=self.fitness_matrix[int(loc2_1),int(loc2_2)]

            if fit1>fit2:
                child[i]=parent1[i]
            else:
                child[i]=parent2[i]

        return child
                    



