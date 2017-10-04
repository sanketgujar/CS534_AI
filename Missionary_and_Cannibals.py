from copy import deepcopy
iterr = 0
visited_state = []
import sys

def check_visited(state):
	global visited_state
	for st in range(len(visited_state)):
		if (visited_state[st] == state):
			return True
	return False		

def valid(state):
	if (((state[0] == 0) or (state[0] >= state[1])) and ( (state[2] == 0) or (state[2] >= state[3] )) \
	and ( state[0] >= 0 and  state[1] >= 0 and state[2] >= 0 \
	and state[3] >= 0 )):
		return True
	else:
		return False


class create_state():
	#[ML,CL,MR,ML,BS]
	def __init__(self,state):
		self.state = state

	def valid(self):
		if ((self.state[0] >= self.state[1]) and (self.state[2] >= self.state[3] ) \
		and ( self.state[0] >= 0 and  self.state[1] >= 0 and self.state[2] >= 0 \
		and self.state[3] >= 0 )):
			return True
		else:
			return False


			
def create_next_state(state):
	global visited_state
	visited_state.append(state)
	if( state == [0,0,3,3,1]):
		print 'Goal State reached' + str(state)
		for sts in range(len(visited_state)):
			print visited_state[sts]
		sys.exit(0)
	next_state = []
	
	'''
	Possible Actions to take are:
	2M
	2C
	1M1C
	1M
	1C
	'''
	#print (state)
	if (state[4] == 0):  #LEFT SIDE	
		#new_state = create_state(state)
		#2M
		new_state = deepcopy(state)
		new_state[0] -= 2
		new_state[2] += 2
		if (valid(new_state)):
			new_state[4] = 1  
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#2C
		new_state[1] -= 2
		new_state[3] += 2
		if (valid(new_state)):
			new_state[4] = 1 
			next_state.append(new_state)

		new_state = deepcopy(state)
		#1M1C
		new_state[0] -= 1
		new_state[2] += 1
		new_state[1] -= 1
		new_state[3] += 1
		if (valid(new_state)):
			new_state[4] = 1 
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#1C
		new_state[1] -= 1
		new_state[3] += 1
		if (valid(new_state)):
			new_state[4] = 1 
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#1M
		new_state[0] -= 1
		new_state[2] += 1
		if (valid(new_state)):
			new_state[4] = 1 
			next_state.append(new_state)
			
		
	else:  #RIGHT SIDE	
		#new_state = create_state(state)
		#2M
		new_state = deepcopy(state)
		new_state[0] += 2
		new_state[2] -= 2
		if (valid(new_state)):
			new_state[4] = 0  
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#2C
		new_state[1] += 2
		new_state[3] -= 2
		if (valid(new_state)):
			new_state[4] = 0 
			next_state.append(new_state)

		new_state = deepcopy(state)
		#1M1C
		new_state[0] += 1
		new_state[2] -= 1
		new_state[1] += 1
		new_state[3] -= 1
		if (valid(new_state)):
			new_state[4] = 0 
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#1C
		new_state[1] += 1
		new_state[3] -= 1
		if (valid(new_state)):
			new_state[4] = 0 
			next_state.append(new_state)
		
		new_state = deepcopy(state)
		#1M
		new_state[0] += 1
		new_state[2] -= 1
		if (valid(new_state)):
			new_state[4] = 0 
			next_state.append(new_state)
	

	if ( len(new_state) > 0):
		for i in range(len(next_state)):
			if (check_visited(next_state[i])):
				pass
			else:	
				create_next_state(next_state[i])
							
#0 --> left
#1 --> RIGHT
if __name__ =='__main__':
	start_state = [3,3,0,0,0]
	create_next_state(start_state)




