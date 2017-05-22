import sys, re, os
from networkx.algorithms import topological_sort
from readGraph import *

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
        if outdegree < 5:
            continue
        for start_node, end_node in g.in_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        for start_node, end_node in g.out_edges(u):
            star_graph.append(
                (start_node, end_node, str(group_code), component_code, num_c))
        group_code += 1

    return star_graph, group_code


if __name__ == '__main__':
    start_time = time.time()
    G = read_save_DAG(sys.argv[1])
    print "loading data is finished in", (time.time() - start_time) / 1000, "s"
    print "the number of nodes is", G.number_of_nodes()
    print "the number of edge is", G.number_of_edges()

    start_time = time.time()
    group_code, component_code = 0, 0
    components = nx.weakly_connected_components(G)
    for component in components:
        num_c = len(component)
        component_code += 1
        for node in component:
            node_info[node] = (component_code, num_c)
        star_graph, group_code = findStarGraph(G,
                                               component, group_code, num_c, component_code)
    print "finding star graph is finished in", (time.time() - start_time) / 1000, "s"

    with open sys.argv[2] as fp:
        for item in star_graph:
            fp.write(str(item) + "\n")
    print "result saved"
