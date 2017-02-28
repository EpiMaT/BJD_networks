import BJD
import networkx as nx
import numpy as np
 
G = nx.read_gml('data/test5000.gml') 
ddtable = BJD.extract(G)
ddtable = np.array(ddtable)

print(np.transpose(ddtable))
print(BJD.validate(ddtable))

