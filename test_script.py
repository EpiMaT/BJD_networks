import BJD
import networkx as nx
import numpy as np
import graphs as g
import Fix
import Generate_Network 
import handle_funcs as HF

reload(HF)

reload(Fix)
reload(BJD)
reload(Generate_Network)

G = nx.read_gml('data/small_test.gml') 
ddtable = BJD.extract(G)
ddtable = np.array(ddtable)

#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))


B=Generate_Network.make_graph(nx.Graph(),g.small,'random_edge')
print('original net', B.edges())
S=Fix.sub(B)
print('sub net', S.edges())

for i in B.nodes():
    for j in B.neighbors(i):
        print(len(nx.shortest_path(B,source=i,target=j))-1)
        print(len(nx.shortest_path(B,source=j,target=i))-1)