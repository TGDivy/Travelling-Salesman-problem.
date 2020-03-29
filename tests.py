import math
import graph
import matplotlib.pyplot as pyplot
import seaborn as sns

if __name__ == '__main__':
    g = graph.Graph(6,"sixnodes")
    #g = graph.Graph(-1,"cities75")

    print("Raw: %0.3f"%(g.tourValue()))
    g.swapHeuristic()
    print("Swapped: %0.3f"%g.tourValue())
    g.TwoOptHeuristic()
    print("TwoOpt %0.3f"%g.tourValue())
    #graph = Graph(6,"sixnodes")
    g.Greedy()
    print("Greedy %0.3f"%g.tourValue())
    g.Custom()
    print("Custom %0.3f"%g.tourValue())
