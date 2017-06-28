
import BJD
import networkx as nx
import numpy as np
#!/usr/bin/python
import matplotlib.pyplot as plt
from random import *
from networkx.algorithms import bipartite
from pylab import show
import numpy as np

#import statistics
import Generate_Aged_Network as GAN
import find_primary_partners as FPP

import graphs as g

#import Generate_Network as GN
import handle_funcs as HF
import Next_Aged_Net as NAN
import time
import Rewire_2_keep_Primary as RKP



reload(HF)
reload(NAN)
reload(BJD)
reload(g)
reload(FPP)
reload(GAN)
reload(RKP)

#==========first net=============#
t1=time.time()
B=GAN.make_graph(nx.Graph(),g.romance,'random_edge')#generate the first network
B0=FPP.primary_edges(B)#define its primary partners
nx.write_gml(B0,'/Users/aazizibo/Desktop/BJD_networks/data/B0_romance.gml')
B0=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/B0_romance.gml')
t2=time.time()
print("------%s seconds to generate  net---" % (t2-t1))
# #==============6 months later===============
B=NAN.make_graph(g.romance,'random_edge',B0)#generate the new  network 1 year later
t3=time.time()
print("------%s seconds to generate next net---" % (t3-t2))
B1=RKP.rewire(B0,B)
nx.write_gml(B1,'/Users/aazizibo/Desktop/BJD_networks/data/B1_romance.gml')
B1=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/B1_romance.gml')
t4=time.time()
print("------%s seconds to rewire net---" % (t4-t3))
G=B0.copy()
men= [n[0] for n in G.nodes(data=True) if G.node[n[0]]['bipartite']==1]#list of men
A= [ [  ] for x in range( 11) ]
for age in range(15,26):
   for i in  men:
      if G.node[i]['age']==age:
        for j in G.neighbors(i):
           # print(B.node[i]['age'],B.node[j]['age'])
              A[age-15].append(G.node[j]['age'])
                 
fig = plt.figure()
ax = fig.add_subplot(111)    
bp = ax.boxplot(A, showmeans=True)
ax.set_xticklabels([ '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'])
plt.title('before rewiring')
plt.xlabel('age of men')
plt.ylabel('age of their partners')
plt.show()

G=B1.copy()
men= [n[0] for n in G.nodes(data=True) if G.node[n[0]]['bipartite']==1]#list of men
A= [ [  ] for x in range( 11) ]
for age in range(15,26):
   for i in  men:
      if G.node[i]['age']==age:
        for j in G.neighbors(i):
           # print(B.node[i]['age'],B.node[j]['age'])
              A[age-15].append(G.node[j]['age'])
                 
fig = plt.figure()
ax = fig.add_subplot(111)    
bp = ax.boxplot(A, showmeans=True)
ax.set_xticklabels([ '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'])
plt.title('after rewiring')
plt.xlabel('age of men')
plt.ylabel('age of their partners')
plt.show()
'''
 
NB0=NAN.make_graph(g.romance,'random_edge',OB)#generate the new  network 1 year later
NB=RKPP.rewire(OB,NB0)
nx.write_gml(NB,'/Users/aazizibo/Desktop/BJD_networks/data/NB_romance.gml')
NB=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/NB_romance.gml')

#G=GAN.make_graph(nx.Graph(),g.test_5000,'random_edge')#generate the first network
#nx.write_gml(G,'/Users/asma11/Desktop/BJD_networks/data/NOLA5000.gml')

G=nx.read_gml('/Users/asma11/Desktop/BJD_networks/data/NOLA5000.gml')
men= [n[0] for n in G.nodes(data=True) if G.node[n[0]]['bipartite']==1]#list of men
A= [ [  ] for x in range( 11) ]
for age in range(15,26):
   for i in  men:
      if G.node[i]['age']==age:
        for j in G.neighbors(i):
           # print(B.node[i]['age'],B.node[j]['age'])
              A[age-15].append(G.node[j]['age'])
                 
fig = plt.figure(1, figsize=(9, 11))
ax = fig.add_subplot(111)    
bp = ax.boxplot(A, showmeans=True)
ax.set_xticklabels([ '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'])
plt.title('with age restriction')
plt.xlabel('age of men')
plt.ylabel('age of their partners')
plt.show()


#B=GAN.make_graph(nx.Graph(),g.romance,'random_edge')
#B_old=FPP.primary_edges(B)
#nx.write_gml(B_old,'/Users/aazizibo/Desktop/BJD_networks/data/R1.gml')
B_old=nx.read_gml('/Users/asma11/Desktop/BJD_networks/data/nola5000.gml') 
t1=time.time()
B_new=NAN.make_graph(g.test_5000,'random_edge',B_old)
nx.write_gml(B_new,'/Users/asma11/Desktop/BJD_networks/data/nola2.gml')
t2=time.time()
print("------%s seconds to generate next net---" % (t2-t1))
B_new=nx.read_gml('/Users/asma11/Desktop/BJD_networks/data/nola2.gml')

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
print 'diff redindency coefficient', Rc_old-Rc_new
print 'redindency coefficient', Rc_old

print("------%s seconds to analyze---" % (time.time()-t2))


#===============box plot================
G=nx.read_gml('/Users/asma11/Desktop/BJD_networks/data/nola2.gml')
men=[n[0] for n in G.nodes(data=True) if G.node[n[0]['bipartite']==1]]
A=[[] for x in range(11)]
for age in range(15,26):
    for i in men:
        if G.node[i]['age']==age:
            for j in G.neighbors(i):
                A[age-15].append(G.node[j]['age'])

fig=plt.figure(1,figsize=(9,11))
ax=fig.add_subplot(111)
bx=ax.boxplot(A,showmeans=True)
ax.set_xticklabels(['15','16','17','18','19','20','21','22','23','24','25'])
plt.title('with age reastriction')
plt.xlabel('men age')
plt.ylabel('partners age')
plt.show()
#print(np.transpose(ddtable))
#print(BJD.validate(ddtable))

##B=GAN.make_graph(nx.Graph(),g.test_5000,'random_edge')

#B1=FPP.primary_edges(B)


#nx.write_gml(B1,'/Users/asma11/Desktop/BJD_networks/data/nola5000.gml')

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