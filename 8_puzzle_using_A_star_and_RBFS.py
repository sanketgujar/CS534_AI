#8 Puzzle  problem using A star and RBFS
#Author : Sanket Gujar (srgujar@wpi.edu)
#Github : 

from utils import *
import numpy as np
from copy import deepcopy
import time
Debug = 0

#nodes
a_star_nodes = 0
rbfs_nodes = 0


#return the manhattan_distance between two states. 
def manhattan_distance(state1,state2):
	man_distance = 0
	for i in range(0,3):
		for j in range(0,3):
			value  = state1[i,j]
			if value == 0 :
				continue
			goal_position = np.argwhere(state2 == value)
			distance = abs(goal_position[0,0] - i) + abs(goal_position[0,1] - j )
			man_distance += distance			
	return man_distance



'''
Problem class for 8 Puzzle
initial_state : any random state
goal_test : Test the state matches to the goal state
action : return possible directions where the blank can slide.
result: swipe the blank as defined in action.  
g : path_cost
h : manhattan_distance heuristic
f : g + h
'''
class Problem():
	def __init__(self, state,goal_state):
		self.initial = state
		self.goal_state = goal_state

	def action(self,state):
		actions = []
		#actions = 0 -> N , 1-> S , 2-> E , 3->W
		#will return an array of possible actions to do
		blank_space = np.argwhere(state == 0)[0]
		
		#for North
		if ( blank_space[0] - 1 >= 0 ):
			actions.append(0)
		
		#for South
		if ( blank_space[0] + 1 < 3 ):
			actions.append(1)
		
		#for East
		if ( blank_space[1] - 1 >= 0 ):
			actions.append(2)
		
		#for West
		if ( blank_space[1] + 1 < 3 ):
			actions.append(3)
		return actions

	def goal_test(self,state):
		if ((state) == self.goal_state).all():
			print 'Goal reached., the current state  is '
			print (state)
			return True
		else:
			return False    
	
	
	def result(self,current_puzzle,action):
		#return new  puzzle created for the actions
		blank_space = np.argwhere(current_puzzle == 0)[0]
		puzzle = deepcopy(current_puzzle)
		if (action == 0 ):
			#for North
			puzzle[blank_space[0],blank_space[1]], puzzle[blank_space[0] - 1, blank_space[1]] = \
			puzzle[blank_space[0] - 1, blank_space[1]] , puzzle[blank_space[0],blank_space[1]]
				
		elif (action == 1 ):
			#for South
			puzzle[blank_space[0],blank_space[1]], puzzle[blank_space[0] + 1, blank_space[1]] = \
			puzzle[blank_space[0] + 1, blank_space[1]] , puzzle[blank_space[0],blank_space[1]]
			
		elif (action == 2 ):
			#for East
			puzzle[blank_space[0],blank_space[1]], puzzle[blank_space[0], blank_space[1] - 1] = \
			puzzle[blank_space[0], blank_space[1] - 1] , puzzle[blank_space[0],blank_space[1]]
			

		elif (action == 3 ):
			#for West
			puzzle[blank_space[0],blank_space[1]], puzzle[blank_space[0], blank_space[1] + 1] = \
			puzzle[blank_space[0] , blank_space[1] + 1] , puzzle[blank_space[0],blank_space[1]]
 			
		return puzzle	


	def g(self,state):
		return manhattan_distance(state,self.initial) 
    
	def h(self,state):
		return manhattan_distance(state,self.goal_state)
	
	def f(self,state):
		return ( self.g(state)  + self.h(state) )



'''
Node class
expand: expand the current node by creating result node.
child_node : return the child node for the particular action.
'''
class Node():
    def __init__(self,state , puzzle, parent = None , action = None , path_cost = 0):
        self.state = state
        #print self.state
        self.parent = parent
        self.action = action
        #self.path_cost = parent.path_cost + 1
        self.f = (puzzle.h(self.state) + puzzle.g(self.state))
        if self.parent:
            self.path_cost = parent.path_cost + 1
        else:
            self.path_cost = 0 

        #print 'path_cost' + str(self.path_cost)
        #time.sleep(0.5)

    def expand(self , puzzle):
        # return all the nodes reachable for the node..
        return [self.child_node(puzzle,action) for action in puzzle.action(self.state)]


    def child_node(self,puzzle,action):
        #returns a child node for the given action
        next = puzzle.result(self.state , action)
        #print next
        #now create a new node.....
        return Node(next, puzzle ,self , action , puzzle.g(next)) 


#perform Astar search algorithm....
#uses Priority Queue giving priority to f
#reference : AIMA Python 
def astar_search(problem, f=None):
    f = memoize(f, 'f')
    node = Node(problem.initial,problem)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        global a_star_nodes
        a_star_nodes += 1
        if problem.goal_test(node.state):
            return node
        #print node.state
        explored.add(tuple([tuple(row) for row in node.state]))
        for child in node.expand(problem):
            if tuple([tuple(row) for row in child.state]) not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


visited = []

#check if the state is visited or not.
def check_visted(n1,n2):
	for i in range(len(n2)):
		if (n1 == n2[i]).all():
			return True
	return False


#performs RBFS:
#reference AIMA Python
def RBFS(puzzle , node , f_limit):
	#print node.state
	global visited
	visited.append(node.state)
	if puzzle.goal_test(node.state):
		return node,0

	child = node.expand(puzzle)
	if len(child) == 0:
		return None, 9999
	for c in child:
		#print c.state
		#print 'cost , g : ' +str(puzzle.get_cost(c.state))
		#print 'cost , h  :' + str(puzzle.get_heuristics(c.state))
		#print ' parent cost :' + str(node.f)
		global rbfs_nodes
		rbfs_nodes += 1
		if check_visted(c.state , visited):
			c.f = max( node.f + puzzle.h(c.state) , node.f )  
		else:
			c.f = max( puzzle.g(c.state) + puzzle.h(c.state), node.f )
		#c.f = (puzzle.get_heuristics(c.state))
		#print c.f
	#time.sleep(1)
	while True:
		child.sort(key = lambda x:x.f)
		best_child = child[0]
		if best_child.f > f_limit:
			return None, best_child.f
		if len(child) > 1:
			alternate = child[1].f
		else:
			alternate = 9999
		result , best_child.f =  RBFS(puzzle,best_child,min(f_limit,alternate))
		if result is not None:
			return result, best_child.f


def implement_RBFS(puzzle,h = None):
	node = Node(puzzle.initial,puzzle)
	node.f = puzzle.h(node.state)
	result,best_f = RBFS(puzzle , node , 9999)
	#print 'Goal_state_reached  :' + str( result.state )


#the main function
if __name__ == '__main__':
	random_board = [np.array((1,0,6,5,2,8,7,3,4)),
	np.array((1,6,4,3,5,0,7,8,2)),
	np.array((2,6,4,3,1,8,5,7,0))]
	for i in range(0,len(random_board)):
		board = random_board[i]
		board = board.reshape((3,3))
		goal_state = np.arange(9).reshape((3,3))
		problem = Problem(board,goal_state)
		print  '\n\n\n*************************************************'
		print  ' The Random puzzle problem is : '
		print problem.initial
		
		global a_star_nodes
		print 'Started A star search'
		start_time = time.clock()
		end_node = astar_search(problem, problem.f)
		print 'Goal reached for A_ star in : ' + str(time.clock() - start_time ) 
		print 'the nodes visited by A* '  + str(a_star_nodes)

		print 'started RBFS search '
		start_time = time.clock()
		implement_RBFS(problem,problem.f)
		print 'Goal reached for RBFS in    : '  + str(time.clock() - start_time ) 
		global rbfs_nodes
		print 'the nodes visited by '+ str(rbfs_nodes)
		'''
		#if Debug == 1:
			#FOR DEBUGGING PURPOSE ONLY
			#action check
			#action =  problem.action(problem.initial)
			#print action
			#for i in range(len(action)):
			#	print problem.result(problem.initial , action[i])
			#print ( puzzle.goal_test(puzzle.goal_state) )
			#parent_node =  Node(puzzle.initial_state)
			#parent_node.child_node(puzzle,3)
			#ch = parent_node.expand(puzzle)
			#for i in range( len(ch)):
			#	print ch[i].state
		'''	