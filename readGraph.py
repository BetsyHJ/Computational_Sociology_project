import re, sys, os
import time
import networkx as nx
from networkx.algorithms import topological_sort


def read_save_DAG(filename):
    ## read the combine file and put(save) the edges into the DAG
    ## return the DAG
    
    # define the DAG
    Graph = nx.DiGraph()
    # read file
    f = open(filename)
    for line in f.readlines():
        nodes = line.split(" ")
        Graph.add_edge(int(nodes[0]), int(nodes[1])) 
    f.close()
    return Graph

if __name__ == "__main__":
    start_time = time.time()
    Graph = read_save_DAG(sys.argv[1])
    print "loading data is finished in", (time.time() - start_time) / 1000, "s"
    print "the number of nodes is", Graph.number_of_nodes()
    print "the number of edge is", Graph.number_of_edges()
    
    start_time = time.time()
    print len(list(nx.simple_cycles(Graph)))
    print "finding circles is finished in", (time.time() - start_time) / 1000, "s"