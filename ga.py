import numpy as np



class Genetic_algorithm():

    def __init__ (self,number_of_city=20,population_size=100,mutation_prob=0.001,crossover_prob=0.6,cost_matrix=False,random_seed=42,generations=100):

        #generations have to be larger than 1

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
        self.population_history=np.ones((population_size,generations,number_of_city))*100
        self.fitness_history=np.zeros((population_size,generations))
        
        


    def fitness(self,cost_matrix=False,maxmization=False):
        self.fitness_pop=np.zeros(self.population_size)
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
        parents_selected=np.zeros(self.number_of_city)
        tri_lower=np.tril(np.ones((self.population_size,self.population_size)))
        wheel=np.dot(tri_lower,self.fitness_pop)
        for j in range(self.number_of_city):
            spin=np.random.uniform(low=10.**-8.,high=max(wheel))
            parents_selected[j]=(np.array(np.where(np.greater_equal(wheel,spin)==True)))[0,0]
        pair_parents=np.random.choice(parents_selected,(self.population_size,2))
        same_parent=np.where(pair_parents[:,0]==pair_parents[:,1])
        if len(same_parent)!=0:
            parents_selected=np.delete(parents_selected,np.where(pair_parents[same_parent,0]==parents_selected),None)
            for i in same_parent:                
                pair_parents[i,0]=np.random.choice(parents_selected)
       
        return pair_parents

    def run(self,crossover_function,mutation=True,first_round=True):
        children=np.zeros((self.population_size,self.number_of_city))
        if not first_round:
            self.population_history=np.hstack((np.ones((self.population_size,self.generations,self.number_of_city)),np.flip(self.population_history,axis=1)))
            self.fitness_history=np.hstack((np.ones((self.population_size,self.generations)),np.flip(self.fitness_history,axis=1)))

        if mutation:
            for i in range(self.generations):
                self.fitness()
                parents_set=self.roullete_wheel_selection()                                
                for j in range(self.population_size):
                    children[j,:]=crossover_function(parents_set[j,:])
                                    
                self.population=children
                self.Mutation()
                self.population_history[:,i]=self.population
                self.fitness_history[:,i]=self.fitness_pop

        else:
            for i in range(self.generations):
                self.fitness()
                parents_set=self.roullete_wheel_selection()                                
                for j in range(self.population_size):
                    children[j,:]=crossover_function(parents_set[j,:])
                                    
                self.population=children
                self.population_history[:,i]=self.population
                self.fitness_history[:,i]=self.fitness_pop
    
    def dataframe(self):
            pass
        
    def graph(self,save=False,name_img=None):

            import matplotlib.pyplot as plt
            fig,ax=plt.subplots(1,1,figsize=(9,9))
            maximum_fitness_history=np.amax(self.fitness_history,axis=0)
            ax.plot(np.arange(len(maximum_fitness_history)),1./maximum_fitness_history)
            ax.set(xlabel='generations',ylabel="shortest path distance ")
            ax.set_title('Traveling Salesman Porblem')
   
class Crossover(Genetic_algorithm):

                    
    def SCRX(self,parents_number):
        
        child=np.ones(int(self.number_of_city))*-1.
        parent1=self.population[int(parents_number[0]),:]
        parent2=self.population[int(parents_number[1]),:]
        cities_left=np.zeros(self.number_of_city)
        node=[0,0]

        for k in range(self.number_of_city-1):

            if node[0]>=self.number_of_city-1 and node[1]>=self.number_of_city-1:
                child[k]=cities_left[0]

            elif (node[0]>=self.number_of_city-1 and parent2[node[1]] in child):
               child[k]=cities_left[0]
            
            elif (node[1]>=self.number_of_city-1 and parent1[node[0]] in child):
               child[k]=cities_left[0]

            elif (node[0]>=self.number_of_city-1 and parent2[node[1]] not in child) or (parent1[node[0]] in child and parent2[node[1]] not in child):
               child[k]=parent2[node[1]]

            elif (node[1]>=self.number_of_city-1 and parent1[node[0]] not in child) or (parent2[node[1]] in child and parent1[node[0]] not in child) :
                child[k]=parent1[node[0]]


               
            elif parent2[node[1]] in child and parent1[node[0]] in child:
                child[k]=cities_left[0]

            elif parent1[node[0]]==parent2[node[1]]:
                child[k]=parent1[node[0]]

            else:
                
                loc1=[parent1[node[0]],parent1[node[0]+1]]
                fit_1=self.fitness_matrix[int(loc1[0]),int(loc1[1])]

                loc2=[parent2[node[1]],parent2[node[1]+1]]
                fit_2=self.fitness_matrix[int(loc2[0]),int(loc2[1])]
                if fit_1>=fit_2:
                    child[k]=parent1[node[0]]
                else:
                    child[k]=parent2[node[1]]

            node=[int(np.where(parent1==child[k])[0]+1),int(np.where(parent2==child[k])[0])+1]
            cities_left=np.setdiff1d(np.arange(self.number_of_city),child)

        child[-1]=cities_left

        return child