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
    #cycles = list(nx.algorithms.find_cycle(Graph))
    fp = open("save_cycles.txt", 'w')
    '''
    fp = open("save_cycles.txt", 'w')
    for i in range(len(cycles)):
	fp.write(str(cycles[i])+"\n")
    '''

    s_components = nx.strongly_connected_components(Graph)
    #cycles = []
    #print "first", list(s_components)
    #print "over", list(s_components)
    for s_component in list(s_components):
        #print "len is", len(s_component)
	cycles = []
	if len(s_component) == 1:
	    #print s_component, 'hhh'
	    continue
	else:
	    #print s_component , "ppp"
	    sub_graph = Graph.subgraph(list(s_component))
	    for cycle in nx.algorithms.simple_cycles(sub_graph):
		cycles.append(cycle)
	    for i in range(len(cycles)):
		fp.write(str(cycles[i])+"\n")
    #print "over2"
    #fp = open("save_cycles.txt", 'w')
    #for i in range(len(cycles)):
    #    fp.write(str(cycles[i])+"\n")
    fp.close()
    print "finding circles is finished in", (time.time() - start_time) / 1000, "s"
