import networkx as nx
import numpy as np



G= nx.read_gml('/Users/aazizibo/Desktop/feb_21_graph_gen/make nets/original5000.gml') 


 #E=G.number_of_edges()
    #P=G.number_of_nodes()
    #giant = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]

    #one_partner_list = [i for i in G.nodes() if G.degree(i)==1]
men=[n for n,d in G.nodes(data=True) if d['bipartite']==0]#list of men

women=[n for n,d in G.nodes(data=True) if d['bipartite']==1]#list of women

print len(men)+len(women)




km=max([G.degree(i) for i in men])

kw=max([G.degree(i) for i in women])
N=[[]]
dN=[[]]
dd_list=np.zeros(shape=(km,kw))
for i in range(0,km):
    degi=[]
    for j in men:
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
print BJD