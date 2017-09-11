import numpy as np
import time
import os
import sys
class Reflex_Agent():
	def __init__(self,board):
		#initialzing the agent in the environment
		self.x = board.shape[0]  / 2
		self.y = board.shape[1]  / 2
 		self.agent_board = np.zeros((board.shape[0],board.shape[1]),dtype = 'int')

	def random_action(self,board):
		#The function of random_action taken by the agent
		act = np.random.randint(0,4)
		#action is selected at random		
		if ((act == 0) and (self.x < board.shape[0] - 1)):
			self.x += 1  #going right
		elif ((act == 1) and (self.x > 0 )):
			self.x -= 1  #going left
		elif ((act == 2) and (self.y < board.shape[0] - 1)):
			self.y += 1  #going down
		elif ((act == 3) and (self.y > 0)):
			self.y -= 1  #going up
		

	def Action(self,board):
		#actions are in random....
		if (board[self.x , self.y] == 1):
			board[self.x , self. y ] = 0
			print '*******  cleaning dirt at' + str([self.x , self.y]) + '  ***************************'
			#time.sleep(0.5)
		agent.Display(board)
		agent.reward(board)
		time.sleep(0.5)
		#os.system('clear')
		agent.random_action(board)
		agent.Action(board)
		print '**next_iteration**'
	
	def reward(self,board):
		#Utility function to check the current clean squares
		shape_board = (board.shape[0]*board.shape[1])
		reward = shape_board - np.count_nonzero(board)
		print 'Utility at this stage is ' + str(reward)
		if ( reward == shape_board):
			print '*************Square is cleaned***************'
			sys.exit(0)
			#closes the program...

	def Display(self,board):
		#Displays user the current environment and the agent
		print '******The emvironment is shown below *********'
		print board
		self.agent_board[self.x , self. y ] = 1
		print '********Agent position is shown below ************'
		print (self.agent_board)
		self.agent_board[self.x , self. y ] = 0
		
			

class board():
	def __init__(self,size):
		self.board = np.zeros((size),dtype= 'int')
		print self.board

	def initailize_the_environment_randomly(self):
		#choosing the number of dirt randomly
		dirt_blocks = np.random.randint(0 ,self.board.shape[0]*self.board.shape[1])
		
		#choosing the blocks randomly
		for i in range(dirt_blocks):
			# choosing the coordinates randomly
			x_cor = np.random.randint(0,self.board.shape[0])
			y_cor = np.random.randint(0,self.board.shape[1])
			# Making the block choosed as dirt block
			self.board[x_cor,y_cor] = 1  # 1 indicates the dirt block
				
	def initailize_problem(self):
		self.board = np.ones((1,2),dtype  = 'int')

if __name__ == '__main__':
	# User enter the size of environment
	size = (input('enter the size of the environment'))
	#env. is created	
	env = board(size)
	#Intialize dirt block randomly
	#1 : Dirt , 0: Clean
	opt = input('Enter 0 if u want to intialize randomly, 1 to fill it according to the example ')
	if ( opt == 0 ):
		env.initailize_the_environment_randomly()
	else:
		env.initailize_problem()	
	print env.board
	#Creating  a reflex agent for the environnmwnt.
	agent = Reflex_Agent(env.board)	
	agent.Action(env.board)
