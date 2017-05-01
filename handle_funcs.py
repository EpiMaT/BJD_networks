import numpy as np
import networkx as nx

_node = 0
_data = 1

_upper = 0
_lower = 1
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


def count_vec(vec):
    """Creates row vector [1, .., n] of the same length as vec"""
    return np.matrix(np.arange(1,product(vec.shape)+1))

def product(tuple):
    """Calculates the product of a tuple"""
    prod = 1
    for x in tuple:
        prod = prod * x
    return prod


def validate(ddtable):
    """Checks if a degree-degree table is valid"""
    margin_upp = ddtable.sum(axis=1).transpose()
    count_upp = count_vec(margin_upp)
    remainder_upp = np.remainder(margin_upp, count_upp)

    margin_low = ddtable.sum(axis=0)
    count_low = count_vec(margin_low)
    remainder_low = np.remainder(margin_low, count_low)

    if not ((remainder_low == 0).all() and (remainder_upp == 0).all()):
        return False

    # e_ij <= d^u_i * d^l_j
    div_upp = np.divide(margin_upp, count_upp)
    div_low = np.divide(margin_low, count_low)
    for i in xrange(0,div_upp.size):
        for j in xrange(0,div_low.size):
            if ddtable[i,j] > div_upp.A1[i] * div_low.A1[j]: # is this the right way to access this?
                print (i, j, ddtable[i,j], div_upp.A1[i] * div_low.A1[j])
                return False
    return True



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
 
def choose(ls):
    i = np.random.randint(0,len(ls))
    return ls[i]

def choose_and_remove(ls):
    i = np.random.randint(0,len(ls))
    return ls.pop(i)

def choose_and_remove_with_rank(ls,ranker):
    idx = 0
    sval = ranker (ls[idx])
    for j in xrange(1,len(ls)):
        if sval == ranker (ls[j]):
            idx = idx + 1
        else:
            break
    i = np.random.randint(0,idx+1)
    return ls.pop(i)


def weighted_choice(li, which):
    total = reduce(lambda x,y: x+y, map(lambda x: x[which], li))
    pick = np.random.randint(0,int(total))
    lbound = 0
    for entry in li:
        if pick <= lbound:
            return entry
        else:
           lbound = lbound + entry[1]
    return li[-1]

def compare_graph_to_table(G, table, dual_check):
    test_mat = table.copy()

    for edge in G.edges():
        (node1, node2) = edge
        if dual_check and G.number_of_edges(node1, node2) > 1:
            # print G.edges()
            return -1, test_mat

        n1degi = G.degree(node1)-1
        n2degi = G.degree(node2)-1

        if G.node[node1]['bipartite'] == 0:
            test_mat[(n1degi,n2degi)] = test_mat[n1degi,n2degi] - 1
        else:
            test_mat[n2degi,n1degi] = test_mat[n2degi,n1degi] - 1
    # print test_mat
    nz = np.count_nonzero(test_mat)
    return nz, test_mat

def list_edge_degs(degdeg_distr):
    (row,col) = degdeg_distr.shape
    edges = []
    for i in xrange(0,row):
        for j in xrange(0,col):
            for k in xrange(0,degdeg_distr[i,j]):
                edges.append((i+1,j+1))
    return edges
    
def max_shortest_path(G):
    a=[]
    for i in G.nodes():
        p=len(nx.shortest_path(G,source=i))-1
        a.append(p) 
    return max(a)   