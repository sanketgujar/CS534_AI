#Travelling salesman problem using Astar and RBFS
#Author: Sanket Gujar (srgujar@wpi.edu)
#Github : 
from utils import *


'''
Problem class for TSP
goal_test : Test the state matches to the goal state
action : return available cities remaining to visit.
result: add the city to list of city visited.  
g : path_cost, distance of city visited in order
h : MST heuristic, distance of city not visited in order.
f : g + h
'''
class Problem():
    def __init__(self, num_cities,city_selection):
        #initialize the class 
        self.num_cities = num_cities
        self.city = self.select_city(city_selection)
        self.initial_state = []
        self.initial_city = self.order[0]
        self.city_visited = []
        print 'The coordinate of location of the cities are : ' + str(self.city) 
        print 'In order  [0,1,2,3,4,5,6,7]' 
        

    def goal_test(self,state):
        if len(state) == self.num_cities:
            print 'Goal reached., the path is ' + str(state) +  ' and the cost is : ' + str(self.g(state))
            return True
        else:
            return False    

    def select_city(self,city):
        #select city from example
        self.order = [0,1,2,3,4,5,6,7]
        if city == 0 :
            return ( [(3,10),(5,30),(10,35),(2,9), (55,25),(30,20) , (30,25) , (20,35)] )
        
        if city == 4:    
            return ( [(55,25),(3,10),(5,30),(10,35),(2,9), (30,20) , (30,25) , (20,35)] )
            
        if city == 1:    
            return ( [(1,10),(5,30), (2,9),(10,35), (30,20),(55,25), (20,35), (30,25)  ] )
                
        if city == 2:
            return ( [(80,40),(5,15),(10,45),(15,55),(4,14), (45,30) , (45,40) , (30,52)] )
        
        if city == 3:
            return ( [(2,7),(4,22),(8,26), (1,7), (22,15),(41,18), (15,24), (22,18)  ] )
                
 
    def action(self,state):
        action = []
        for i in range(len(self.order)):
            if ( check_visited(state,self.order[i])):
                action.append(self.order[i])
        return action

    def g(self,state):
        #return the path cost
        dist_sum = 0
        for i in range(len(state) - 1):
            city1 = self.city[state[i]] #return x,y
            city2 = self.city[state[i+1]]
            dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
        return  (dist_sum)
    
    def h(self,state):    
        #return the MST heuristics
        city_not_visited = []
        for i in range(len(self.order)):
            if ( check_visited(state,self.order[i])):
                city_not_visited.append(self.order[i])
        
        #print city_not_visited        
        dist_sum = 0
        for i in range(len(city_not_visited) - 1):
            city1 = self.city[city_not_visited[i]] #return x,y
            city2 = self.city[city_not_visited[i+1]]
            dist_sum += (city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 
        return  (dist_sum)

    def f(self,state):
        return ( self.g(state)  + self.h(state) )


    def result(self,order,a):        
        return ( order + [a] )




class Node():
    def __init__(self,state , puzzle, parent = None , action = None , path_cost = 0):
        self.state = state
        #print self.state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.f = (puzzle.h(self.state) + puzzle.g(self.state))
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
        return Node(next, puzzle ,self , action , puzzle.g(next)) 


#checks if the city is visited or not in list a
def check_visited(a,b):
    for i in range(len(a)):
        if a[i] == b :
            return False
    return True


#AIMA-Python Modified version...
#Performs A star
#will return optimal path if heuristic is admissible
def astar_search(problem, f=None):
    f = memoize(f, 'f')
    node = Node(problem.initial_state,problem)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(tuple(node.state))
        for child in node.expand(problem):
            if tuple(child.state) not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None



#AIMA-Pyhton modeified version.....
#Performs the RBFS search 
def recursive_best_first_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0   
        #print ' node: ' + str(node.state)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, 99999
        for s in successors:
            s.f = max( s.path_cost + problem.h(s.state), node.f)
            #print ' state : ' + str(s.state) + '  s.f' + str(s.f)
            #print 's.g  +'  + str(problem.g(s.state))
            #print 's.h  +'  + str(problem.h(s.state))
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = 99999
            #print '  best ' + str(best.state)
            #k = input('enter key')    
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial_state,problem)
    node.f = problem.g(node.state)
    result, bestf = RBFS(problem, node, 99999)
    return result




if __name__ == '__main__':
    for i in range(4):
        print '\n\n**************Defining problem on new cities*************************'
        problem = Problem(8,i)
        print ' Starting A star search .....'
        astar_search(problem,problem.f)
        print ' Starting RBFS search .......'
        recursive_best_first_search(problem,problem.h)
    