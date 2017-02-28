import BJD
import networkx as nx
 
G = nx.read_gml('./test5000.gml') 

ddtable = BJD.extract(G)

print(ddtable)
print(BJD.validate(ddtable))

