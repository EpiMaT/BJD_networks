import networkx as nx
import numpy as np
import random




_node = 0
_data = 1

_upper = 0
_lower = 1

# Graph output description:
#   bipartite attribute: 0 is upper, 1 is lower.
def count_vec(vec):
    """Creates row vector [1, .., n] of the same length as vec"""
    return np.matrix(np.arange(1,product(vec.shape)+1))

def product(tuple):
    """Calculates the product of a tuple"""
    prod = 1
    for x in tuple:
        prod = prod * x
    return prod



def deg_distr(degdeg_distr,bipartite):
    """Returns degree distribution"""
    if bipartite == 1: # lower
        margin = degdeg_distr.sum(axis=0)
    else:
        margin = degdeg_distr.sum(axis=1).transpose()

    count = count_vec(margin)
    divide = np.divide(margin, count)
    return divide

def upper_deg_distr(table):
    return deg_distr(table,0)

def lower_deg_distr(table):
    return deg_distr(table,1)

def add_nodes(B, degvec, letter, bipartite):
    """Add nodes with a letter prefix, and bipartite data to the graph B"""
    mcount = 0
    d = 1
    for deg in np.nditer(degvec):
        for i in xrange(1,deg+1):
            mcount = mcount + 1
            node = letter+'{}'.format(mcount)
            B.add_node(node, bipartite=bipartite, deg=d)
        d = d + 1

def add_upper_nodes(B, degvec):
    add_nodes(B, degvec, 'u', _upper)
def add_lower_nodes(B, degvec):
    add_nodes(B, degvec, 'l', _lower)

def is_upper(datanode):
    return datanode[_data]['bipartite'] == 0
def is_lower(datanode):
    return not is_upper(datanode)

B_initial = nx.read_gml('/Users/aazizibo/Desktop/feb_21_graph_gen/make nets/test.gml') 
def Fix_sub_net(G):
    Sub_G=G.copy()
    m_list= [n[0] for n in G.nodes(data=True) if is_lower(n)]#list of men
    for i in Sub_G.nodes():
        Sub_G.node[i]['primary_partner']=i     
    for i in m_list:
        deg_neigbor=[G.degree(j) for j in G.neighbors(i)]
        deg_min=min(deg_neigbor)
        Sub_G.node[i]['primary_partner']=random.sample([j for j  in G.neighbors(i) if G.degree(j)==deg_min],1)[0] 
    
    for edge in Sub_G.edges():
        e0=edge[0]
        e1=edge[1] 
        if e1 in m_list:
            if (e0 !=Sub_G.node[e1]['primary_partner']):
              Sub_G.remove_edge(*edge)
        elif e0 in m_list:      
            if (e1 !=Sub_G.node[e0]['primary_partner']):
              Sub_G.remove_edge(*edge)   
    
    for i in Sub_G.nodes():
        del Sub_G.node[i]['primary_partner']
    return Sub_G
#---------------------------------------
 