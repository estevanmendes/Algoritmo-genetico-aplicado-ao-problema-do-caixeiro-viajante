import numpy as np
import heapq


class Genetic_algorithm():

    def __init__ (self,number_of_cities=20,population_size=100,mutation_prob=0.001,crossover_prob=0.5,cost_matrix=False,random_seed=42,generations=100,elitism_rate=0.3):

        #generations have to be larger than 1
        if generations<=1:
            print('='*100,'- ERROR -'*10,'='*10)

        self.number_of_cities=number_of_cities
        self.population_size=population_size
        self.mutation_prob=mutation_prob
        self.crossover_prob=crossover_prob
        self.generations=generations
        self.cost_matrix=cost_matrix
        self.seed=random_seed
        self.elitism_rate=elitism_rate

        # np.random.seed(random_seed)

        if not cost_matrix:
            self.cost_matrix=np.random.rand(number_of_cities,number_of_cities)*100
            self.cost_matrix[np.diag_indices(number_of_cities)]=999*np.ones(number_of_cities)

        initial_pop=np.tile(np.arange(number_of_cities),(population_size,1))

        for i in range(population_size):
            np.random.shuffle(initial_pop[i,:])

        self.population=initial_pop
        self.fitness_pop=np.zeros(population_size)
        self.population_history=np.ones((population_size,generations,number_of_cities))*100
        self.fitness_history=np.zeros((population_size,generations))
        self.best_paths=np.zeros(generations)
        


    def fitness(self,cost_matrix=False,maxmization=False):
        self.fitness_pop=np.zeros(self.population_size)
        for i in range(self.population_size):
            for j in range(self.number_of_cities-1):
                self.fitness_pop[i]+=self.cost_matrix[int(self.population[i,j]),int(self.population[i,j+1])]
        self.fitness_pop=1./self.fitness_pop
        best_child=np.argmax(self.fitness_pop)
        best_path=0.
        
        for k in range(self.number_of_cities-1):
                best_path+=self.cost_matrix[int(self.population[best_child,k]),int(self.population[best_child,k+1])]
        self.best_paths[int(np.where(self.best_paths==0)[0][0])]=best_path


    def Mutation(self):
        prob=self.mutation_prob
        mutation_random=np.random.uniform(size=self.population_size)
        threshold=np.ones(self.population_size)*prob
        pop_mutated=np.less_equal(mutation_random,threshold)
        temp=np.arange(self.population_size)
        pop_mutated=temp[pop_mutated]
        for  i in pop_mutated:
        
            changes=np.random.randint(0,self.number_of_cities,size=2)
            a=int(self.population[i,changes[0]])
            b=int(self.population[i,changes[1]])
            self.population[i,changes[0]]=b
            self.population[i,changes[1]]=a
        

    def roullete_wheel_selection(self):
        parents_selected=np.zeros(self.number_of_cities)
        tri_lower=np.tril(np.ones((self.population_size,self.population_size)))
        wheel=np.dot(tri_lower,self.fitness_pop)
        for j in range(self.number_of_cities):
            spin=np.random.uniform(low=10.**-8.,high=max(wheel))
            parents_selected[j]=(np.array(np.where(np.greater_equal(wheel,spin)==True)))[0,0]
        pair_parents=np.random.choice(parents_selected,(self.population_size,2))
       
        return pair_parents

    def crossover_selection(self,elite_size):
        chosen=np.random.uniform(size=self.population_size-elite_size)<=self.crossover_prob
        crossover_pop=np.arange(elite_size,self.population_size)
        non_crossover_pop=crossover_pop[~chosen]
        crossover_pop=crossover_pop[chosen]
        return crossover_pop, non_crossover_pop

    def elitism(self):
        elite=int(self.population_size*self.elitism_rate)
        index_elite=heapq.nlargest(elite, range(self.population_size), self.fitness_pop.take)
        
        return self.population[index_elite,:],elite


    def run(self,crossover_function,mutation=True,first_round=True):
        children=np.zeros((self.population_size,self.number_of_cities))
        if not first_round:
            self.population_history=np.hstack((np.ones((self.population_size,self.generations,self.number_of_cities)),np.flip(self.population_history,axis=1)))
            self.fitness_history=np.hstack((np.ones((self.population_size,self.generations)),np.flip(self.fitness_history,axis=1)))
            self.best_paths=np.hstack((self.best_paths,np.zeros(self.generations)))

        if mutation:
            for i in range(self.generations):
                self.fitness()
                parents_set=self.roullete_wheel_selection()   
                elite,size_elite=self.elitism()
                
                crossover_pop,non_crossover_pop=self.crossover_selection(size_elite)
                for j in crossover_pop:

                    children[j,:]=crossover_function(parents_set[j,:])

                children[non_crossover_pop,:]=self.population[non_crossover_pop,:]

                self.population=children
                self.Mutation()
                self.population[0:size_elite,:]=elite              
            
                self.population_history[:,i]=self.population
                self.fitness_history[:,i]=self.fitness_pop
                print('='*10,' '*3,str(i+1),' generations were done',' '*3,'='*10)

        else:
            for i in range(self.generations):
                self.fitness()
                parents_set=self.roullete_wheel_selection()                                
                crossover_pop,non_crossover_pop=self.crossover_selection()
                for j in crossover_pop:

                    children[j,:]=crossover_function(parents_set[j,:])
                    
                children[non_crossover_pop]=self.population[non_crossover_pop]   
                                    
                self.population=children
                self.population_history[:,i]=self.population
                self.fitness_history[:,i]=self.fitness_pop
                print('='*10,' '*3,str(i+1),' generations were done',' '*3,'='*10)
        if not first_round:
            self.fitness_history=np.flip(self.fitness_history,axis=1)
            self.population_history=np.flip(self.population_history,axis=1)
    
    def dataframe(self):
            import pandas as pd
            df_pop=pd.DataFrame(self.population_history.transpose)
            df_pop.index.name='Generation'
            df_pop.to_csv('population_history.csv')
            
        
    def graph(self,best_known_solution=False,save=False,name_img=None):

            import matplotlib.pyplot as plt
            fig,ax=plt.subplots(1,1,figsize=(9,9))
            maximum_fitness_history=np.amax(self.fitness_history,axis=0)
            shortest_paths=self.best_paths
            ax.plot(np.arange(len(maximum_fitness_history)),maximum_fitness_history,label='fitness',color='orange')
            ax.set(xlabel='generations',ylabel="best fitness")
            ax.legend(loc=2)
            ax = ax.twinx()
            ax.plot(np.arange(len(shortest_paths)),shortest_paths,label='distance')
            ax.set(xlabel='generations',ylabel="shortest path distance ")
            ax.set_title('Traveling Salesman Porblem')
            if best_known_solution:
                ax.plot(np.arange(len(shortest_paths)),np.ones(len(shortest_paths))*best_known_solution,label='Best - Solution',color='black',linestyle='dashed')
            ax.legend(loc=1)
            if save:
                plt.savefig(name_img,dpi=200)
            

    def TSPLIB(self,url):

        import pandas as pd
        import re
        df=pd.read_csv(url,header=None,skiprows=7)
        rows=df.iloc[:,0].values
        string=' '.join(rows) 
        regex='([0-9]+)'
        numbers=re.findall(regex,string)
        array=np.array(numbers)
        array=array.astype(float)
        array=array.reshape(int(len(array)**0.5),int(len(array)**0.5))
        
        self.cost_matrix=array
        
        return array
   
class Crossover(Genetic_algorithm):

                    
    def SCRX(self,parents_number):
        
        child=np.ones(int(self.number_of_cities))*-1.
        parent1=self.population[int(parents_number[0]),:]
        parent2=self.population[int(parents_number[1]),:]
        cities_left=np.zeros(self.number_of_cities)
        node=[0,0]

        for k in range(self.number_of_cities-1):

            if node[0]>=self.number_of_cities-1 and node[1]>=self.number_of_cities-1:
                child[k]=cities_left[0]

            elif (node[0]>=self.number_of_cities-1 and parent2[node[1]] in child):
               child[k]=cities_left[0]
            
            elif (node[1]>=self.number_of_cities-1 and parent1[node[0]] in child):
               child[k]=cities_left[0]

            elif (node[0]>=self.number_of_cities-1 and parent2[node[1]] not in child) or (parent1[node[0]] in child and parent2[node[1]] not in child):
               child[k]=parent2[node[1]]

            elif (node[1]>=self.number_of_cities-1 and parent1[node[0]] not in child) or (parent2[node[1]] in child and parent1[node[0]] not in child) :
                child[k]=parent1[node[0]]


               
            elif parent2[node[1]] in child and parent1[node[0]] in child:
                child[k]=cities_left[0]

            elif parent1[node[0]]==parent2[node[1]]:
                child[k]=parent1[node[0]]

            else:
                loc1=[parent1[node[0]],parent1[node[0]+1]]
                fit_1=self.cost_matrix[int(loc1[0]),int(loc1[1])]

                loc2=[parent2[node[1]],parent2[node[1]+1]]
                fit_2=self.cost_matrix[int(loc2[0]),int(loc2[1])]
                if fit_1<=fit_2:
                    child[k]=parent1[node[0]]
                else:
                    child[k]=parent2[node[1]]

            node=[int(np.where(parent1==child[k])[0]+1),int(np.where(parent2==child[k])[0])+1]
            cities_left=np.setdiff1d(np.arange(self.number_of_cities),child)

        child[-1]=cities_left

        return child

    def OX(self,parents_number):

        child=np.ones(int(self.number_of_cities))*-1.
        parent1=self.population[int(parents_number[0]),:]
        parent2=self.population[int(parents_number[1]),:]

        edges=np.sort(np.random.randint(self.number_of_cities+1,size=2))
        child[edges[0]:edges[1]]=parent1[edges[0]:edges[1]]
        left=parent2[~np.in1d(parent2,child)]
        child[edges[1]:]=left[0:self.number_of_cities-edges[1]]
        left=parent2[~np.in1d(parent2,child)]
        child[0:edge[0]]=left

        return child

