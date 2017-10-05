#Tarvelling Saleman problem using Genetic Algoritm
#Author : Sanket Gujar (srgujar@wpi.edu)
#Github : 
#reference : AIMA-Python 

import time
import numpy as np
from utils import *

city = [(10,20),(3,5),(25,30),(15,35),(2,9), (30,20) , (5,5) , (20,15)]

'''
Problem class for TSP
goal_test : Test the state matches to the goal state
action : return avialbe swaps that can be performed
result : perform the swapping
value: checks the fitness of the individual. fitness = ( 1/ 1 + distance_travelled)
'''

class Problem():
    def __init__(self,num_cities):
        #initialize the class 
        self.num_cities = num_cities
        self.city = self.select_city(0)
        self.initial_state = self.order
        print 'The location of the cities are : ' + str(self.city) 
        print 'In order  [0,1,2,3,4,5,6,7]' 
        

    def create_neighbours(self):
        #swaps using random variable
        #swaps the order of the cities visited
        var1 = np.random.randint(0,self.num_cities)
        var2 = np.random.randint(0,self.num_cities)
        self.order[var1] , self.order[var2] = self.order[var2] , self.order[var1]
        #print self.order



    def select_city(self,city):
        #select city from example
        self.order = [0,1,2,3,4,5,6,7]
        if city == 0 :
            return ( [(10,20),(3,5),(25,30),(15,35),(2,9), (30,20) , (5,5) , (20,15)] )
    
    def actions(self,state):
        #return action of cities that can be swapped
        action = []
        for i in range(8):
            action.append([  np.random.randint(0,self.num_cities), np.random.randint(0,self.num_cities) ])
        return action
    

    def result(self,state,a):        
        #performs the swaping
        var1 , var2  = a
        self.order[var1] , self.order[var2] = self.order[var2] , self.order[var1]
        return self.order

    


    def value(self):
        #return the fitness of travelling cities in order and connecting to the first city 
        #fitness = ( 1 /  1 + distance_travelled)
        dist_sum = 0
        for i in range(len(self.order) - 1):
            city1 = self.city[self.order[i]] #return x,y
            city2 = self.city[self.order[i+1]]
            dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
        #connecting loop from last city to first
        city1 = self.city[self.order[i+1]] #return x,y
        city2 = self.city[self.order[0]]
        dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
        return  ( 1.0 / 1 + dist_sum )


def fitness_fn(state):
    '''
    return the fitness of travelling cities in order and connecting to the first city 
    fitness = ( 1 /  1 + distance_travelled)
    '''
    global city
    dist_sum = 0
    for i in range(len(state) - 1):
        city1 = city[state[i]] #return x,y
        city2 = city[state[i+1]]
        dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
    #connecting loop from last city to first
    city1 = city[state[i+1]] #return x,y
    city2 = city[state[0]]
    dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
    return   ( 1.0  / (dist_sum + 1 ) ) 


#Genetic search
def genetic_search(problem, fitness_fn, ngen=1000, pmut=0.1, n=8):
    s = problem.initial_state
    states = [problem.result(s, a) for a in problem.actions(s)]
    random.shuffle(states)
    #please change the ngen here.....
    ngen = 1000
    return genetic_algorithm(states[:n], fitness_fn, ngen, pmut)

#gentic Algorithm
def genetic_algorithm(population, fitness_fn, ngen=1000 , pmut=0.1 , gene_pool=[0, 1], f_thres=None  ):  # noqa
    '''
    please increase the generation number (ngen) to improve the result..
    please note that it will also increase the execution time
    '''
    for i in range(ngen):
        new_population = []
        random_selection = selection_chances(fitness_fn, population)
        for j in range(len(population)):
            x = random_selection()
            y = random_selection()
            child = reproduce(x, y)
            if random.uniform(0, 1) < pmut:
                child = mutate(child, gene_pool)
            new_population.append(child)

        population = new_population

        if f_thres:
            fittest_individual = argmax(population, key=fitness_fn)
            if fitness_fn(fittest_individual) >= f_thres:
                return fittest_individual

    return argmax(population, key=fitness_fn)


def init_population(pop_number, gene_pool, state_length):
    g = len(gene_pool)
    population = []
    for i in range(pop_number):
        new_individual = [gene_pool[random.randrange(0, g)] for j in range(state_length)]
        population.append(new_individual)

    return population

#performs the selections according to the fitness of the populations
#the individual with more fitness is expected to be choosen more frequently.
def selection_chances(fitness_fn, population):
    fitnesses = map(fitness_fn, population)
    return weighted_sampler(population, fitnesses)

#check if the city already exist in the list
def check_value_exist(x,y):
    for i in range(len(x)):
        if x[i] == y :
            return False
    return True

#reproduce perfroms crossover
#it makes sure no cities are repeated.
def reproduce(p1,p2):
    lenght = 8
    
    #print 'p1'  + str(p1)
    #print 'p2'  + str(p2)
     
    st = np.random.randint(0,lenght -2 )
    end = np.random.randint(st+1,lenght)
    
    #print 'start: ' + str(st) + ' end :' +  str(end)
    
    child = p1[st:end]
    #print 'child a' + str(child)
    left_places = lenght - len(child)
    #add the remaing left_places without repeating
    for i in range(len(p2)):
        if check_value_exist(child,p2[i]):
            #print p2[i]
            child += [p2[i]]
    #print 'child' + str(child)  
    #time.sleep(0.5)
    return child[:lenght]       
    

#mutate the genes
def mutate(x, gene_pool):
    var1 = np.random.randint(0,8)
    var2 = np.random.randint(0,8)
    x[var1] , x[var2] = x[var2] , x[var1]
    return x

#main_function:...
if __name__ == '__main__':
    prob =Problem(8)
    fittest_order =  ( genetic_search(prob,fitness_fn) )
    print 'The fittest order of the population is : ' + str(fittest_order) \
    + ' with cost of :' +str((1.0/fitness_fn(fittest_order)) - 1)