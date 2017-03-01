import numpy as np
import handle_funcs as HF

try:
    xrange
except NameError:
    print("Running in Python 3")
    xrange = range
else:
    print("Running in Python 2")

_node = 0
_data = 1

_upper = 0
_lower = 1



def extract(G):
    """Returns BJD of the graph G, or an error if graph is not bipartite""" 
    m_list= [n[0] for n in G.nodes(data=True) if HF.is_lower(n)]#list of men

    f_list= [n[0] for n in G.nodes(data=True) if HF.is_upper(n)]#list of women


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

#-----------------------------------------------------------------------------------

