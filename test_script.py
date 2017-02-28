import BJD
import networkx as nx
import numpy as np
import Fix
G = nx.read_gml('data/test5000.gml') 
#G = nx.read_gml('data/small_test.gml') 
ddtable = BJD.extract(G)
ddtable = np.array(ddtable)

#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))
M=Fix.subA(G)
print M.size()

