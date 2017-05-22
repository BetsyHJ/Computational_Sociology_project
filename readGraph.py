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

def findCircleGraph(G, component, group_code, num_c, component_code):
    circle_graph = []
    g = G.subgraph(component)
    for scc in nx.strongly_connected_components(g):
        if len(scc) > 1:
            g2 = g.subgraph(scc)
            for start_node, end_node in g2.edges():
                circle_graph.append((start_node, end_node))
            group_code += 1
    return circle_graph, group_code

def find_cycle(G):
    # return the edges in the circle
    circles = []
    group_code, component_code = 0, 0
    components = nx.weakly_connected_components(G)
    for component in components:
	num_c = len(component)
        # find circle graph
        circle_graph, group_code = findCircleGraph(G, component, group_code, num_c, component_code)
	#print circle_graph
        circles += circle_graph
    return circles	

if __name__ == "__main__":
    start_time = time.time()
    G = read_save_DAG(sys.argv[1])
    ## print the basis infomation
    print "loading data is finished in", (time.time() - start_time), "s"
    print "the number of nodes is", G.number_of_nodes()
    print "the number of edge is", G.number_of_edges()
    start_time = time.time()

    circles = find_cycle(G)
    #save the cycles
    fp = open("save_cycles.txt", 'w')
    for c in circles:
        fp.write(str(c)+"\n")
    fp.close()
    print "finding circles is finished in", (time.time() - start_time), "s"
