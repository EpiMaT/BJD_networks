import numpy as np

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


def extract(G):
    """Returns BJD of the graph G, or an error if graph is not bipartite""" 
    m_list= [n[0] for n in G.nodes(data=True) if is_lower(n)]#list of men

    f_list= [n[0] for n in G.nodes(data=True) if is_upper(n)]#list of women


    km=max([G.degree(i) for i in m_list])
    kw=max([G.degree(i) for i in f_list])

    N=[[]]
    dN=[[]]
    dd_list=np.zeros(shape=(km,kw))
    for i in range(0,km):
        degi=[]
        for j in m_list:
            if G.degree(j)==i+1:
                degi.append(j)
        Nj=[]
        dNj=[]
        for j in degi:
            Nj.extend(G.neighbors(j))

        for n in Nj:
            dNj.append(G.degree(n))

        N.append(Nj) 
        dN.append(dNj)

        for jj in range(0,kw):
            dd_list[i][jj]=(dN[i+1]).count(jj+1)

    Bjd=dd_list.astype(int)   
    BJD=Bjd.transpose()

    return BJD



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
            if table[i,j] > div_upp.A1[i] * div_low.A1[j]: # is this the right way to access this?
                print (i, j, table[i,j], div_upp.A1[i] * div_low.A1[j])
                return False
    return True
