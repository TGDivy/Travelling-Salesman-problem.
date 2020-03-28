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

def minimum_spanning_tree2(graph, n,start): # A function to create a minimum spanning tree from a graph.
    reached = set([start]) # Set of nodes already used.
    rows, cols = set(range(n)), set(range(n)) # Number of rows or columns in a graph.
    mst = {} # Minimum Spanning tree initialized.
    b = 0
    for i in range(n-1): # Loops until all the noes are added. (time looped = V) 
        toUse, toReach = 0,0 # Node used in order to reach node.
        mini = math.inf
        for row in reached:
            for col in (cols-reached): # time looped = Rows*Cols 
                b+=1
                if(graph[row][col]<mini):
                    mini = graph[row][col]
                    toUse = row
                    toReach = col
                    
        mst[toUse] = mst[toUse]+[toReach] if toUse in mst else [toReach]
        reached.add(toReach)
    print("b:",b,"n:",n)
    return(mst)

class Graph:
    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
        (self.dist, 
        self.perm, 
        self.n) = Euclidean(filename) if n==-1 else General(n, filename)
    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        return sum([self.dist[i,j] for i,j in 
                    zip(self.perm, self.perm[1:]+self.perm[0:1])])
    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        new_perm = self.perm.copy()
        i_1 = 0 if (i+1)>= self.n else i+1
        
        new_perm[i_1] = self.perm[i]
        new_perm[i]   = self.perm[i_1]

        initial_cost= cost(self.perm,self.dist)
        new_cost    = cost(new_perm,self.dist)
        flag = new_cost < initial_cost

        self.perm = new_perm if flag else self.perm
        return flag
    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self,i,j):
        new_perm = self.perm.copy()        
        new_perm[i:j+1] = new_perm[i:j+1][::-1]

        initial_cost, new_cost = cost(self.perm,self.dist), cost(new_perm,self.dist)
        flag = new_cost < initial_cost- 0.0000000001

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
    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        self.perm[0] = 0
        unused = set(range(1,self.n))
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

    def Custom(self):
        end = []
        def l_(d, k):
            #print(end)
            end.append(k)
            d[k].sort()
            for i in d[k]:
                if(i in d):
                    l_(d, i)
                else:
                    end.append(i)
            return end
        mini = math.inf
        for i in range(1):#self.n):
            temp = []
            try:
                end = []
                mst = minimum_spanning_tree2(self.dist,self.n,i)
                temp = l_(mst,i)
            except:
                continue
            c = cost(temp,self.dist)
            if(c<mini):
                self.perm = temp 
                mini = cost(temp,self.dist)
                print(i)

if __name__ == '__main__':
    graph = Graph(6,"sixnodes")
    #graph = Graph(-1,"cities50")

    print("Raw:",graph.tourValue())
    graph.swapHeuristic()
    print("Swapped:",graph.tourValue())
    graph.TwoOptHeuristic()
    print("TwoOpt",graph.tourValue())
    #graph = Graph(6,"sixnodes")
    graph.Greedy()
    print("Greedy,",graph.tourValue())
    graph.Custom()
    print("Custom",graph.tourValue())