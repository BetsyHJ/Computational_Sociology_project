#-*-coding: utf8-*-
import re, sys, os
import time
import networkx as nx
from networkx.algorithms import topological_sort
from docutils.transforms import components
from networkx.generators.line import line_graph
from scipy.optimize.linesearch import LineSearchWarning
import copy

sys.setrecursionlimit(1500000)
N_degree = 10
egos = []

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
    #改这儿！！
    circle_graph = []
    g = G.subgraph(component)
    for scc in nx.strongly_connected_components(g):
        if len(scc) > 10:
            g2 = g.subgraph(scc)
            for start_node, end_node in g2.edges():
                circle_graph.append((start_node, end_node))
            group_code += 1
    return circle_graph, group_code

def find_cycle_star(G):
    # return the edges in the circle
    circles, stars = [], []
    group_code, component_code = 0, 0
    components = nx.weakly_connected_components(G)
    for component in components:
        num_c = len(component)
        # find circle graph, star graph
        circle_graph, group_code = findCircleGraph(G, component, group_code, num_c, component_code)
        star_graph, group_code = findStarGraph(G, component, group_code, num_c, component_code)
        #print circle_graph, star graph
        circles += circle_graph
    stars += star_graph
    return circles, star_graph

# save node wcc id and num
node_info = dict()

def findStarGraph(G, component, group_code, num_c, component_code):
    '''
    Parameters
    ----------
    component: set(nodes)
    group_code: int

    Return
    ----------
    star_graph: [(u, v, group_node, component_code, num_c),...]
    '''
    star_graph = []
    if len(component) <= 2:
        return star_graph, group_code
    g = G.subgraph(component)
    for u, outdegree in g.out_degree().iteritems():
        if outdegree < N_degree:
            continue
        for start_node, end_node in g.in_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        for start_node, end_node in g.out_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        group_code += 1
    for u, indegree in g.in_degree().iteritems():
        if indegree < N_degree:
            continue
        for start_node, end_node in g.in_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        for start_node, end_node in g.out_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        group_code += 1

    return star_graph, group_code
       
def dist_get(G):
    dist = {}
    fp = open("sav.txt",'w')

    for node in nx.topological_sort(G):
        pre = G.pred[node]
        if pre:
            dist[node]=[]
            for v in pre:
                temp = copy.copy(dist[v])
              #  print v ,dist[v]
                for t in temp:
                    tmp = copy.copy(t)
                    tmp.append(node) 
                   # print dist[v],v 
                    dist[node]= dist[node] + [tmp]
           # print dist[node] ,node
            
        else:
            a = []
            a.append(node)
            dist[node] = [a]
        fp.write(str(dist[node])+'\n')
        
    fp.close()   
          #  print dist[node] ,node
    return  dist


if __name__ == "__main__":
    start_time = time.time()
    Path = sys.argv[2]#'./twitter_combined.txt'
    G = read_save_DAG(Path)
    ## print the basis infomation
    print "loading data is finished in", (time.time() - start_time), "s"
    print "the number of nodes is", G.number_of_nodes()
    print "the number of edge is", G.number_of_edges()
    start_time = time.time()

    circles, stars = find_cycle_star(G)
    print "finding circles and stars is finished in", (time.time() - start_time), "s"

    #save the cycles
    fp = open("save_cycles.txt", 'w')
    for c in circles:
        fp.write(str(c)+"\n")
    fp.close()
    ##print "finding circles is finished in", (time.time() - start_time), "s"

    #save the stars
    start_time = time.time()
    fp = open("save_stars.txt", 'w')
    for s in stars:
        fp.write(str(s)+"\n")
    fp.close()
    ##print "finding stars is finished in", (time.time() - start_time), "s"

