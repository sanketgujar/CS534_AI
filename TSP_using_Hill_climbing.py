#Tarvelling Saleman problem using Hill Climbing Alogrithm
#Author : Sanket Gujar (srgujar@wpi.edu)
#Github : 
#reference : AIMA-Python 

import numpy as np
import sys
import time
number_cities = 10

class Problem():
	def __init__(self,num_cities):
		#initialize the class 
		self.num_cities = num_cities
		self.city = self.select_city(0)
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
		if city == 1 :
			return ( [(55,25),(3,10),(5,30),(10,35),(2,9), (30,20) , (30,25) , (20,35)] )
		if city == 2:
			return ( [(80,40),(5,15),(10,45),(15,55),(4,14), (45,30) , (45,40) , (30,52)] )
		if city == 3:
			return ( [(2,7),(4,22),(8,26), (1,7), (22,15),(41,18), (15,24), (22,18)  ] )
        

	def get_cost(self):
		#return the cost of travelling cities in order and connecting to the first city 
		dist_sum = 0
		for i in range(len(self.order) - 1):
			city1 = self.city[self.order[i]] #return x,y
			city2 = self.city[self.order[i+1]]
			dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
		#connecting loop from last city to first
		city1 = self.city[self.order[i+1]] #return x,y
		city2 = self.city[self.order[0]]
		dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
		return dist_sum	



def hill_climbing(Problem):
	'''
	Hill climbing algorithm
	here the value is the path cost so we need to find the minimum cost between the neighbous.
	iteration_count : count the iteration performed
	continous_count : count the CONTINOUS neighbours where the cost was greater then the current cost.
	 				  it avoids the plateau conditions, increase the count for more accuarte result.
	 				  but also note it will increase the execution time.
	current_cost    : the cost of present order

	previous_cost    : the cost of previous lowest cost order_new
	create_neighbours : return the neighbours of the current order. 				  	 	
	'''
	iteration_count = 0  #counts the iteration
	continous_count = 0  #count for how long neighbour has not produced minimum, avoid getting stuck.
	lowest_cost = 999999 #infinity
	prev_cost = 999999   #infinity 
	while(1):
		if continous_count > 12:
			#if it doesnt find 12 neighbours with lower cost
			print 'No neighbours with lower cost found , stopping local search.........'
			break
		current_cost = Problem.get_cost()
		if current_cost < lowest_cost:
			lowest_cost = Problem.get_cost()
			print 'lowest_cost found at iteration: ' +str(iteration_count) +  ' order of cities is ' + str(Problem.order) +\
			'  having cost  : ' + str(lowest_cost) 
		if (prev_cost - current_cost > 0 ):   #check if the cost is decreasing or not.
 			continous_count = 0
		else:
			continous_count += 1 	 
		prev_cost = current_cost
		#create neighbours of the current node by swapping	 
		Problem.create_neighbours()
		iteration_count += 1
		
'''	
	#lexiographical swapping algorithm
	def lexical_swap(self):
		#print self.order
		largest_index = - 1
		for i in range(len(self.order) -1 ):
			if ( self.order[i] < self.order[i+ 1]):
				largest_index = i 
		if largest_index == - 1:
			print'Tested every lexiographical search '
			print 'Program finished'
			sys.exit(0)	
		largest_j =  -1	
		for j in range(len(self.order)):
			if( self.order[j] > self.order[largest_index]):
				largest_j = j 

		self.order[largest_index], self.order[largest_j] = self.order[largest_j],self.order[largest_index]	
		order_new =  self.order[largest_index:]
		self.order = np.concatenate( (self.order[0:largest_index] ,  order_new) ,axis =0 ) 
		print self.order
'''

if __name__ == '__main__':
	prob = Problem(8)
	hill_climbing(prob)
