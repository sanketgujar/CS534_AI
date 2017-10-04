#TSP A* Problem .....
from utils import *

class Problem():
    def __init__(self, num_cities):
        #initialize the class 
        self.num_cities = num_cities
        self.city = self.select_city(0)
        self.initial_state = []
        self.initial_city = self.order[0]
        self.city_visited = []
        print 'The location of the cities are : ' + str(self.city) 
        print 'In order  [0,1,2,3,4,5,6,7]' 
        

    def create_neighbours(self):
        #swaps using random variable
        #swaps the order of the cities visited
        var1 = np.random.randint(0,self.num_cities)
        var2 = np.random.randint(0,self.num_cities)
        self.order[var1] , self.order[var2] = self.order[var2] , self.order[var1]
        #print self.order

    def goal_test(self,state):
        if len(state) == self.num_cities:
            print 'Goal reached., the path is ' + str(state)
            return True
        else:
            return False    

    def select_city(self,city):
        #select city from example
        self.order = [0,1,2,3,4,5,6,7]
        if city == 0 :
            return ( [(10,20),(3,5),(25,30),(15,35),(2,9), (30,20) , (5,5) , (20,15)] )
    
 
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
        #return the MST
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



def check_visited(a,b):
    for i in range(len(a)):
        if a[i] == b :
            return False
    return True

def astar_search(problem, f=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    #f = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, f)

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
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

def recursive_best_first_search(problem, h=None):
    """[Figure 3.26]"""
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0   # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, 99999
        for s in successors:
            s.f = max( s.path_cost + problem.h(s.state), node.f)
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
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial_state,problem)
    #node.f = h(node.state)
    result, bestf = RBFS(problem, node, 99999)
    return result




if __name__ == '__main__':
    problem = Problem(8)
    #print problem.actions(4,[1,2,3,5] )
    #print problem.result([1,3,4],5)
    #print problem.goal_test()
    astar_search(problem,problem.f)
    recursive_best_first_search(problem,problem.h)