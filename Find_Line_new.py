import re, sys, os
import time
import networkx as nx
from networkx.algorithms import topological_sort
from docutils.transforms import components
from networkx.generators.line import line_graph
from scipy.optimize.linesearch import LineSearchWarning
import copy
from readGraph import *

sys.setrecursionlimit(1500000)


'''
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
'''

def find_Line(G):
    D = nx.DiGraph()
    circles = find_cycle(G)
    D.add_edges_from(circles)
    for start_node , end_node in D.edges():
        G.remove_edge(start_node, end_node)         
    #line = []
    group_code , component_code =  0 , 0
    components = nx.weakly_connected_components(G)
    for component in  components:
        num_c  = len(component)
        #line_graph, _ = findLineGrah(G , component ,group_code,num_c,component_code)
        findLineGrah(G , component ,group_code,num_c,component_code)
    return 

        
    
def findLineGrah(G , component ,group_code,num_c,component_code):
    fp = open("save_lines.txt",'w')
    line_gragh = []
    if len(component) <=2 :
        return line_gragh ,group_code
    g = G.subgraph(component)
    d= dist_get(g)
    for node in nx.topological_sort(g):
         if g.succ[node]:
             continue
         else :
             for l in d[node]:
                 fp.write(str(l)+"\n")   
    
             
    fp.close()
    return        
        
'''
        for  lp in l:
            line = []
            if len(lp) >=3 :
                pre_node = None
                for end_node in lp:
                    if pre_node:
                        line.append((pre_node,end_node ,str(group_code),"2",component_code,num_c))
                    pre_node =end_node
                group_code += 1
            line_graph += line
 
    except nx.NetworkXUnfeasible:
        pass
    return line_gragh , group_code
'''
def line_path(G):
   # dist = {}
    nodes = []# list of out-degress
    for node in G.nodes():
        if G.succ[node]:
            continue
        else :
            nodes.append(node)
    l = []
    for lastnode in nodes:
        
        line = []
        global all_line
        all_line =[]
        line_get(lastnode, line ,all_line ,G )
        l += all_line

    
    return l

def line_get(node , line ,all_line, G):
    line.append(node)
    pre_node = G.pred[node]
    if pre_node:
        for v in G.pred[node]:
            
            line_get(v , line ,all_line ,G)
           
            line.remove(v)
                
    else: 
        
        if len(line) >1:
            all_line.append( list(reversed(line)))
        return
    
def dist_get(G):
    dist = {}

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
          #  print dist[node] ,node
        
    
    return  dist


if __name__ == "__main__":
    start_time = time.time()
    Path = './twitter_combined.txt'
    G = read_save_DAG(Path)
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
    
    start_time = time.time()
    find_Line(G)
    #save the lines
    print "finding lines is finished in", (time.time() - start_time), "s"
    
        
        
        
    
    