import BJD
import networkx as nx
import numpy as np
import graphs as g
import Fix
import Generate_Network as GN
import handle_funcs as HF
import Next_Net as NN


reload(HF)
reload(NN)
reload(Fix)
reload(BJD)
#reload(Generate_Network)

#B_old = nx.read_gml('data/small_test.gml') 

#print(nx.is_connected(B_old))




#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))



B=GN.make_graph(nx.Graph(),g.romance,'random_edge')
if isinstance(B, tuple):
    print(B[0])
else:
    nx.write_gml(B,'data/romance.gml')
    
B_old = nx.read_gml('data/romance.gml') 
#print B_old.edges()
#ddtable = BJD.extract(B_old)
#dddtable = np.array(ddtable)

B_new=NN.make_graph(nx.Graph(),g.romance,'random_edge',B_old)
if isinstance(B_new, tuple):
    print(B_new[0])
else:
    print('')

#print B_new.edges()
a=[]
for i in B_new.nodes():
    for j in B_new.neighbors(i):
       if nx.has_path(B_old, i, j):
          a.append(nx.shortest_path_length(B_old, source=i, target=j))
       else: 
          a.append(0)
print 'far=', a.count(0)/float(len(a))          
print 'close=', a.count(3)/float(len(a))           
