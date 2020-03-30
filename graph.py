import math
import numpy as np
import collections

def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)

def Euclidean(filename): #A funtion to initialise in case of euclidean metric.
    file = open(filename, "r")
    content = [ [int(chr) for chr in line.strip("\n").split(" ") if chr != ""] 
                for line in file.readlines()]
    n = len(content)
    dist = np.zeros((n,n)) #Initialize the dist
    #Populate the dist
    for i in range(n):
        for j in range(n):
            if(i==j):
                dist[i,j] = np.inf #Because we never want to get to the same place again (from any place)
            else:
                dist[i,j] = euclid(content[i],content[j]) #Calculating the euclidean distance between all nodes from all nodes.
    #intializing the perm as the simplest traverse order 0..n perm
    perm = list(range(0,n))
    return(dist,perm,n)

def General(n,filename): #A function to initialise in case of a genereal metric.
    file = open(filename, "r")
    content = [ [int(chr) for chr in line.strip("\n").split(" ") if chr != ""] 
                for line in file.readlines()]
    dist = np.zeros((n,n))+np.inf #Initialize the dist with infinity values.
    #Populate the dist
    for p,q,distance in content: 
        if(dist[p,q]==np.inf): #In case the metric is not symetric.
            dist[p,q] = distance #As mentioned in the input file.
            dist[q,p] = distance
        else:
            dist[p,q] = distance
    # Iniializing the perm from 0-n.
    perm = list(range(0,n))
    print(dist)
    return(dist,perm,n)

def cost(arr, dist): #Cost of the current tour value give the travel array and the distance matrix.
    return sum([dist[i,j] for i,j in 
                zip(arr, arr[1:]+arr[0:1])]) #Sum all costs from 0 - n+1 (where n+1 = 0)

def minimum_spanning_tree(graph, n):      # A function to create a minimum spanning tree from a graph.
    reached     = set([0])                  # Set of nodes already used.
    all_nodes   = set(range(n))                 # All nodes.
    mst         = {}                            # Minimum Spanning tree initialized.
    graph[:,0] = np.inf
    b = 0
    for i in range(n-1): # Loops until all the nodes are added. (time looped = V) 
        toUse, toReach = 0,0 # Node used in order to reach node.
        mini = math.inf
        for row in reached:
            cm = np.min(graph[row])
            if(cm<mini):
                mini    = cm
                toUse   = row
                toReach = np.argmin(graph[row])
                    
        mst[toUse] = mst[toUse]+[toReach] if toUse in mst else [toReach]
        reached.add(toReach)
        graph[:,toReach] = np.inf
    return(mst)

class Graph:
    def __init__(self,n,filename):
        (self.dist, 
        self.perm, 
        self.n) = Euclidean(filename) if n==-1 else General(n, filename) #Euclidean format n==-1 otherwise general.

    def tourValue(self): #Cost of the tourvalue as described by specifications.
        return sum([self.dist[i,j] for i,j in 
                    zip(self.perm, self.perm[1:]+self.perm[0:1])])
    
    def trySwap(self,i):
        new_perm = self.perm.copy() # making a copy of the current best tour.
        i_1 = 0 if (i+1)>= self.n else i+1 # In order to loop around the list. index value.
        
        #Swapping values 
        new_perm[i_1] = self.perm[i]
        new_perm[i]   = self.perm[i_1]
        #Comparing the two tour's costs
        initial_cost= cost(self.perm,self.dist)
        new_cost    = cost(new_perm,self.dist)
        flag = new_cost < initial_cost
        #Making the decsion to select the tour.
        self.perm = new_perm if flag else self.perm
        return flag

    def tryReverse(self,i,j):
        new_perm = self.perm.copy() #making a copy of the current best tour.
        new_perm[i:j+1] = new_perm[i:j+1][::-1] #reversing a part of the tour.
        #Calculating the costs of the tours.
        initial_cost, new_cost = cost(self.perm,self.dist), cost(new_perm,self.dist)
        flag = new_cost < initial_cost- 0.0000000001 # neccessary due to the python rounding issues.
        #Making decision to select the better tour.
        self.perm = new_perm if flag else self.perm
        return flag
    
    def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True
    
    def TwoOptHeuristic(self):
        better = True
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True                
    
    def Greedy(self):
        self.perm[0] = 0 # intializing the tour at 0, (can select anything.)
        unused = set(range(1,self.n)) # Set of nodes current unused.
        for i in range(0, self.n-1):
            mini = math.inf
            next_node = 0
            for node in unused:
                dist = self.dist[self.perm[i],node]
                if(dist<mini):
                    mini = dist
                    next_node = node
            self.perm[i+1] = next_node
            unused.remove(next_node)

    def twoApproximation(self):
        end = []
        def l(d, k):
            end.append(k)
            d[k].sort()
            for i in d[k]:
                if(i in d):
                    l(d, i)
                else:
                    end.append(i)
            return end
        mst = minimum_spanning_tree(self.dist.copy(),self.n)
        #print(mst)
        self.perm = l(mst,0)
        self.perm = res = [i for n, i in enumerate(self.perm) if i not in self.perm[:n]]
        #print("perm",self.perm)
