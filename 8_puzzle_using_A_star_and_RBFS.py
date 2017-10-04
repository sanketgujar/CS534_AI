import numpy as np
from Queue import PriorityQueue
from copy import deepcopy
import time
Debug = 0


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



class sliding_puzzle():
	def __init__(self,initial_state,goal_state):
		self.initial_state = initial_state
		self.goal_state = goal_state

	
	def action(self , current_puzzle):
		self.actions = []
		#actions = 0 -> N , 1-> S , 2-> E , 3->W
		#will return an array of possible actions to do
		blank_space = np.argwhere(current_puzzle == 0)[0]
		puzzle = deepcopy(current_puzzle)
		
		#for North
		if ( blank_space[0] - 1 >= 0 ):
			self.actions.append(0)
		
		#for South
		puzzle = deepcopy(current_puzzle)
		if ( blank_space[0] + 1 < 3 ):
			self.actions.append(1)
		
		#for East
		puzzle = deepcopy(current_puzzle)
		if ( blank_space[1] - 1 >= 0 ):
			self.actions.append(2)
		
		#for West
		puzzle = deepcopy(current_puzzle)
		if ( blank_space[1] + 1 < 3 ):
			self.actions.append(3)
		
		return self.actions	

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

	def goal_test(self,state):
		if (state == self.goal_state).all():
			return True
		else:
			return False		

	def path_cost(self,state1):
		self.g = manhattan_distance(self.initial_state,state1)
		self.h = manhattan_distance(state1,goal_state)		
		#print 'self.g :' + str(self.g)
		#print 'self.h :' + str(self.h)
 		self.f = self.h + self.g
 		return self.f

 	def get_heuristics(self,state):
 		return 	manhattan_distance(state,self.goal_state)

 	def get_cost(self,state):	
 		return 	manhattan_distance(state,self.initial_state)


class Node():
	def __init__(self,state , parent = None , action = None , path_cost = 0):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
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
		return Node(next, self , action , puzzle.path_cost(next)) 




def check_visted(n1,n2):
	for i in range(len(n2)):
		if (n1 == n2[i]).all():
			return True
	return False


def A_star(puzzle):
	PQ = PriorityQueue()
	solution_found = 0
	node = Node(puzzle.initial_state)
	PQ.put((node.path_cost,node))
	explored = []
	while (PQ.qsize() and (not solution_found)):
		node = PQ.get()[1] 
		#print node.state
		explored.append(node.state)
		if (puzzle.goal_test(node.state)):
			print 'Solution found' + str(node.state)
			solution_found = 1
			return node
		for child in node.expand(puzzle):
			#print child.state	
			if (not(check_visted(child.state,explored))):
				#print 'child.path_cost ' +str(child.path_cost) + '  child.state' +str(child.state) + '   child ' + str(child)
				PQ.put((child.path_cost,child))
	print 'solution not found'			

visited = []

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
		'''
		print 'cost , g : ' +str(puzzle.get_cost(c.state))
		print 'cost , h  :' + str(puzzle.get_heuristics(c.state))
		print ' parent cost :' + str(node.f)
		'''
		if check_visted(c.state , visited):
			c.f = max( node.f + puzzle.get_cost(c.state) + puzzle.get_heuristics(c.state), node.f )  
		else:
			c.f = max( puzzle.get_cost(c.state) + puzzle.get_heuristics(c.state), node.f )
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
	node = Node(puzzle.initial_state)
	node.f = puzzle.get_heuristics(node.state)
	result,best_f = RBFS(puzzle , node , 9999)
	print 'Goal_state_reached  :' + str( result.state )

if __name__ == '__main__':
	#board = np.random.permutation(np.arange(9))
	board = np.array((7,2,4,5,0,6,8,3,1))
	board = board.reshape((3,3))
	goal_state = np.arange(9).reshape((3,3))
	puzzle = sliding_puzzle(board,goal_state)
	print puzzle.initial_state	
	

	'''
	action check
	action =  puzzle.action(puzzle.initial_state)
	for i in range(len(action)):
		print puzzle.result(puzzle.initial_state , action[i])
	#print ( puzzle.goal_test(puzzle.goal_state) )
	'''
	#parent_node =  Node(puzzle.initial_state)
	#parent_node.child_node(puzzle,3)
	'''
	ch = parent_node.expand(puzzle)
	for i in range( len(ch)):
		print ch[i].state
	'''
	start_time = time.clock()
	end_node = A_star(puzzle)
	print 'Goal reached for A_ star in : ' + str(time.clock() - start_time ) 
	start_time = time.clock()
	implement_RBFS(puzzle)
	print 'Goal reached for RBFS in    : '  + str(time.clock() - start_time ) 
	