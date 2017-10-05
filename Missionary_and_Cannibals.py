#MC problem using BFS
#Author: Sanket Gujar (srgujar@wpi.edu)
#Github :
#reference : AIMA Python


from utils import *
from copy import deepcopy
visited_state = []
import sys


'''
Problem class for MC problem
state  = [left_side_M, left_side_C, right_side_M, right_side_C, boat_side]
initial state = all people and the boat are on left side 
goal state : all people and boat are on the right side 
action : return the valid option people can travel in boat
result : return the state of the particular action
'''
class Problem():
	def __init__(self,state):
		self.initial = state


	def goal_test(self,state):
		if ( state == [0,0,3,3,1]):
			print  'Goal reached ' + str(state)
			return True
		else:
			return False

	#2M,1M,1M1C,1C,2C	
	def action(self,state):	
		actions = []
		if (state[4] == 0):  #LEFT SIDE	
		#new_state = create_state(state)
		#2M
			new_state = deepcopy(state)
			new_state[0] -= 2
			new_state[2] += 2
			if (valid(new_state)):
				actions.append(0)
			new_state = deepcopy(state)
			#2C
			new_state[1] -= 2
			new_state[3] += 2
			if (valid(new_state)):
				actions.append(4)
			
			new_state = deepcopy(state)
			#1M1C
			new_state[0] -= 1
			new_state[2] += 1
			new_state[1] -= 1
			new_state[3] += 1
			if (valid(new_state)):
				actions.append(2)
			
			new_state = deepcopy(state)
			#1C
			new_state[1] -= 1
			new_state[3] += 1
			if (valid(new_state)):
				actions.append(3)

			new_state = deepcopy(state)
			#1M
			new_state[0] -= 1
			new_state[2] += 1
			if (valid(new_state)):
				actions.append(1)	
	
		else: #right_side	
			new_state = deepcopy(state)
			new_state[0] += 2
			new_state[2] -= 2
			if (valid(new_state)):
				actions.append(0)

			new_state = deepcopy(state)
			#2C
			new_state[1] += 2
			new_state[3] -= 2
			if (valid(new_state)):
				actions.append(4)
			
			new_state = deepcopy(state)
			#1M1C
			new_state[0] += 1
			new_state[2] -= 1
			new_state[1] += 1
			new_state[3] -= 1
			if (valid(new_state)):
				actions.append(2)
			
			new_state = deepcopy(state)
			#1C
			new_state[1] += 1
			new_state[3] -= 1
			if (valid(new_state)):
				actions.append(3)

			new_state = deepcopy(state)
			#1M
			new_state[0] += 1
			new_state[2] -= 1
			if (valid(new_state)):
				actions.append(1)	
		return actions

	def result(self,state,a):
		if (state[4] == 0):  #LEFT SIDE	
			#new_state = create_state(state)
			#2M
			if ( a == 0 ):
				new_state = deepcopy(state)
				new_state[0] -= 2
				new_state[2] += 2
				new_state[4] = 1  
				return (new_state)
			
			if(a==4):
				new_state = deepcopy(state)
				#2C
				new_state[1] -= 2
				new_state[3] += 2
				new_state[4] = 1 
				return (new_state)

			if(a == 2):	
				new_state = deepcopy(state)
				#1M1C
				new_state[0] -= 1
				new_state[2] += 1
				new_state[1] -= 1
				new_state[3] += 1
				new_state[4] = 1 
				return (new_state)
				
			if (a==3):
				new_state = deepcopy(state)
				#1C
				new_state[1] -= 1
				new_state[3] += 1
				new_state[4] = 1 
				return (new_state)
			
			if (a==1):	
				new_state = deepcopy(state)
				#1M
				new_state[0] -= 1
				new_state[2] += 1
				new_state[4] = 1 
				return (new_state)
					
		
		else:		
			#new_state = create_state(state)
			#2M
			if ( a == 0 ):
				new_state = deepcopy(state)
				new_state[0] += 2
				new_state[2] -= 2
				new_state[4] = 0  
				return (new_state)
			
			if(a==4):
				new_state = deepcopy(state)
				#2C
				new_state[1] += 2
				new_state[3] -= 2
				new_state[4] = 0 
				return (new_state)

			if(a == 2):	
				new_state = deepcopy(state)
				#1M1C
				new_state[0] += 1
				new_state[2] -= 1
				new_state[1] += 1
				new_state[3] -= 1
				new_state[4] = 0 
				return (new_state)
				
			if (a==3):
				new_state = deepcopy(state)
				#1C
				new_state[1] += 1
				new_state[3] -= 1
				new_state[4] = 0 
				return (new_state)
			
			if (a==1):	
				new_state = deepcopy(state)
				#1M
				new_state[0] += 1
				new_state[2] -= 1
				new_state[4] = 0 
				return (new_state)
					


'''
Node class
creates node for state
expand : expand the current node using child nodes
child_node : create a child node for a valid action
'''
class Node():
	def __init__(self,state , parent = None , action = None):
		self.state = state
		print self.state
		self.parent = parent
		self.action = action
		if self.parent:
			self.depth = parent.depth + 1
		else:
			self.depth = 0 


	def expand(self , puzzle):
		# return all the nodes reachable for the node..
		return [self.child_node(puzzle,action) for action in puzzle.action(self.state)]


	def child_node(self,puzzle,action):
		#returns a child node for the given action
		next = puzzle.result(self.state , action)
		#print next
		#now create a new node.....
		return Node(next, self , action ) 

					
#check visited node
def check_visited(state):
	global visited_state
	for st in range(len(visited_state)):
		if (visited_state[st] == state):
			return True
	return False		

#check if the state is valid or not
def valid(state):
	if (((state[0] == 0) or (state[0] >= state[1])) and ( (state[2] == 0) or (state[2] >= state[3] )) \
	and ( state[0] >= 0 and  state[1] >= 0 and state[2] >= 0 \
	and state[3] >= 0 )):
		return True
	else:
		return False


explored = [] #stores the explored states to avoid recurssion.


#check the node is explored or not
def check_explored(node):
	global explored
	for i in range(len(explored)):
		if node.state == explored[i]:
			return True
	return False


#reference : AIMA Python
#BFS: returns the solution at minimum depth
def breadth_first_tree_search(problem,frontier):
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if check_explored(node):
            pass
        else:
        	if problem.goal_test(node.state):
    			return node
    		global explored
    		explored.append(node.state)    
    		frontier.extend(node.expand(problem))
    return None



if __name__ =='__main__':
	problem = Problem([3,3,0,0,0]) 
	breadth_first_tree_search(problem,FIFOQueue())
	#depth_first_tree_search(problem,Stack())


