import BJD
import networkx as nx
import numpy as np
import graphs as g
import Fix
import Generate_Network 
import handle_funcs as HF
import Next_Net as NN

reload(HF)
reload(NN)
reload(Fix)
reload(BJD)
reload(Generate_Network)

B_old = nx.read_gml('data/small_test.gml') 

print('old', B_old.edges())

ddtable = BJD.extract(B_old)
ddtable = np.array(ddtable)

#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))


B_new=NN.make_graph(ddtable,'random_edge',B_old)
print('new', B_new.edges())
