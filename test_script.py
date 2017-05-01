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
reload(GN)

B_old = nx.read_gml('data/small_test.gml') 
print('old', B_old.edges())

B_new=NN.make_graph(nx.Graph(),g.small,'random_edge',B_old)
print('new', B_new.edges())


