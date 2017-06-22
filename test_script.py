import BJD
import networkx as nx
import numpy as np
#!/usr/bin/python
from networkx import *
from random import *
from networkx.algorithms import bipartite
from pylab import show
import numpy as np
import networkx as nx
#import statistics
import Generate_Aged_Network as GAN
import find_primary_partners as FPP

import graphs as g

#import Generate_Network as GN
import handle_funcs as HF
import Next_Aged_Net as NAN
import Next_Net as NN


reload(HF)
reload(NAN)
reload(NN)
reload(BJD)
reload(g)
reload(FPP)
reload(GAN)


B=GAN.make_graph(nx.Graph(),g.romance,'random_edge')
B_old=FPP.primary_edges(B)
nx.write_gml(B_old,'/Users/aazizibo/Desktop/BJD_networks/data/R1.gml')
B_old=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/R1.gml') 
B_new=NAN.make_graph(g.romance,'random_edge',B_old)
nx.write_gml(B_new,'/Users/aazizibo/Desktop/BJD_networks/data/R2.gml')
B_new=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/R2.gml')
#==============ANALYSING TWO NETWORKS

a=[]
for i in B_new.nodes():
    for j in B_new.neighbors(i):
        if nx.has_path(B_old, i, j):
            a.append(nx.shortest_path_length(B_old, source=i, target=j))
        else: 
            a.append(-1)
print 'far=', a.count(-1)/float(len(a))          
print 'close=', a.count(3)/float(len(a))           
print 'same=', a.count(1)/float(len(a)) 


Bcc_old=sorted(nx.connected_component_subgraphs(B_old), key = len, reverse=True)
B0_old=Bcc_old[0]
nc_old=nx.number_connected_components(B_old)
sg_old=B0_old.order()
cl_old=bipartite.average_clustering(B_old)
nodeb2_old=[i for i in B_old.nodes() if B_old.degree(i)>1]
rc_old=bipartite.node_redundancy(B_old,nodes=nodeb2_old)
Rc_old=(sum(rc_old.values())/len(rc_old.values()))
    
Bcc_new=sorted(nx.connected_component_subgraphs(B_new), key = len, reverse=True)
B0_new=Bcc_new[0]
nc_new=nx.number_connected_components(B_new)
sg_new=B0_new.order()
cl_new=bipartite.average_clustering(B_new)
nodeb2_new=[i for i in B_new.nodes() if B_new.degree(i)>1]
rc_new=bipartite.node_redundancy(B_new,nodes=nodeb2_new)
Rc_new=(sum(rc_new.values())/len(rc_new.values()))
        
print 'diff number of connected components',nc_old-nc_new
print 'diff size of giant component',sg_old-sg_new
print 'diff clustering coefficinet',cl_old-cl_new
print 'diffredindency coefficient', Rc_old-Rc_new

#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))

##B=GAN.make_graph(nx.Graph(),g.test_5000,'random_edge')

#B1=FPP.primary_edges(B)


#nx.write_gml(B1,'/Users/asma11/Desktop/BJD_networks/data/nola5000.gml')
'''
for i in  B.nodes():
    print(i,B.node[i]['primarypartner'],B.node[i]['age'])
    for j in B.neighbors(i):
        print(j,B.node[j]['age'],B.node[j]['deg'] )
      
    print('================')
print(len(B.nodes())) 

   
A= [ [  ] for x in range( 11) ]
for age in range(15,25):
   for i in  B.nodes():
      if B.node[i]['age']==age:
        for j in B.neighbors(i):
           # print(B.node[i]['age'],B.node[j]['age'])
              A[age-15].append(B.node[j]['age'])
                 
fig = plt.figure(1, figsize=(9, 11))
ax = fig.add_subplot(111)    
bp = ax.boxplot(A, showmeans=True)
ax.set_xticklabels([ '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'])
plt.title('with age restriction')

plt.show()
    
#print(A)

B=GAN.make_graph(nx.Graph(),g.test_5000,'random_edge')
if isinstance(B, tuple):
    print(B[0])
else:
    nx.write_gml(B,'data/test_5000.gml')
   
    
 
B_old = nx.read_gml('data/test_5000.gml') 

for i in range(1):

    B_new=NN.make_graph(nx.Graph(),g.test_5000,'random_edge',B_old)
    if isinstance(B_new, tuple):
        print(B_new[0])
    else:
        print('')

#==============ANALYSING TWO NETWORKS
    a=[]
    for i in B_new.nodes():
        for j in B_new.neighbors(i):
            if nx.has_path(B_old, i, j):
                a.append(nx.shortest_path_length(B_old, source=i, target=j))
            else: 
                a.append(-1)
    print 'far=', a.count(-1)/float(len(a))          
    print 'close=', a.count(3)/float(len(a))           
    print 'same=', a.count(1)/float(len(a)) 


Bcc_old=sorted(nx.connected_component_subgraphs(B_old), key = len, reverse=True)
B0_old=Bcc_old[0]
nc_old=nx.number_connected_components(B_old)
sg_old=B0_old.order()
cl_old=bipartite.average_clustering(B_old)
nodeb2_old=[i for i in B_old.nodes() if B_old.degree(i)>1]
rc_old=bipartite.node_redundancy(B_old,nodes=nodeb2_old)
Rc_old=(sum(rc_old.values())/len(rc_old.values()))
    
Bcc_new=sorted(nx.connected_component_subgraphs(B_new), key = len, reverse=True)
B0_new=Bcc_new[0]
nc_new=nx.number_connected_components(B_new)
sg_new=B0_new.order()
cl_new=bipartite.average_clustering(B_new)
nodeb2_new=[i for i in B_new.nodes() if B_new.degree(i)>1]
rc_new=bipartite.node_redundancy(B_new,nodes=nodeb2_new)
Rc_new=(sum(rc_new.values())/len(rc_new.values()))
        
print 'diff number of connected components',nc_old-nc_new
print 'diff size of giant component',sg_old-sg_new
print 'diff clustering coefficinet',cl_old-cl_new
print 'diffredindency coefficient', Rc_old-Rc_new
'''