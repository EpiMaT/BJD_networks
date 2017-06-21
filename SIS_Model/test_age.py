#this function treat partner of screened people
import math
import random
import networkx as nx
import pylab as pl
import numpy as np
import config as cfg
import matplotlib.pyplot as plt


#---------for transmission rate----------
def edge_weight(d):
    if d==1:
        return 0.1104
    elif d==2:
        return 0.0563
    elif d==3:
        return 0.0442
    elif d==4:
        return 0.0241
    elif d==5:
        return 0.0503
    else:
        return 0.0222



def age_list(N):
    elements=[15,16,17,18,19,20,21,22,23,24,25]
    probs=[1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0,1/11.0]
    age=np.random.choice(elements, N, p=probs)
    return age



#---------end of for transmission rate----------

betam2f=6*[0]
betaf2m=6*[0]
for i in range(0,6):
        betam2f[i]=(1-cfg.beta_m2f)**edge_weight(i+1)
        betaf2m[i]=(1-cfg.beta_f2m)**edge_weight(i+1)
    
    #G=nx.read_gml('/Users/aazizibo/Desktop/Network_Model_codes/Data_Input/test.gml')
G=nx.read_gml('/Users/aazizibo/Desktop/BJD_networks/data/romance.gml')
people_list = [i for i in G.nodes()]

m_list=[n for n,d in G.nodes(data=True) if d['bipartite']==0]#list of men
f_list=[n for n,d in G.nodes(data=True) if d['bipartite']==1]#list of women

number_of_people = len(people_list)

age=age_list(number_of_people)
plt.figure()
plt.hist(age, bins=11)  # plt.hist passes it's arguments to np.histogram
plt.show()

number_of_men = len(m_list)
number_of_female = len(f_list)

t=number_of_people*[0]
#begin simulation


ifct= [u'l284', u'u16',u'l57', u'l58']

for i in ifct:
    G.node[i]['infection time']=-1
    
Age_distribution=[] 
j=0     
for i in G.nodes():
    G.node[i]['age']=age[j]
    
    j=j+1
            
#------------------------------------- 
for k in range(0,cfg.t_simulation):
    # walk through infecteds list and try to infect neighbors
    to_remove=[]
    to_add=[]
    for i in ifct: #do recovery
        if G.node[i]['infection time']==-1:
            G.node[i]['t']=max(1,round(-math.log(1-pl.rand())/cfg.gamma))
            G.node[i]['infection time']=G.node[i]['infection time']
        elif G.node[i]['infection time']>0:
            G.node[i]['infection time']=G.node[i]['infection time']-1
        elif G.node[i]['infection time']==0:
            to_remove.append(i)
                
        #------------track neighbors-------------do transmission
        for j in G.neighbors(i):
            if j not in ifct and G.node[j]['bipartite']==1:
                if pl.rand()<edge_weight(G.degree(j)):
                    if pl.rand()< cfg.beta_m2f:
                      to_add.append(j)
                      G.node[j]['infection time']=-1
            elif j not in ifct and G.node[j]['bipartite']==0:
                if pl.rand()<edge_weight(G.degree(i)):
                    if pl.rand()< cfg.beta_f2m: 
               
                        to_add.append(j)
                        G.node[j]['infection time']=-1
    # infected list by gender
    male_infected_list=[j for j in ifct if G.node[j]['bipartite']==0]
    female_infected_list=[j for j in ifct if G.node[j]['bipartite']==1]
    # become infected today
    new_male_list=[j for j in to_add if G.node[j]['bipartite']==0]
    new_female_list=[j for j in to_add if G.node[j]['bipartite']==1]
    
    #===================== UPDATA DATA AT THE END OF DAY====================== 
    for i in to_remove:
        ifct.remove(i)
    for j in to_add:
       ifct.append(j)
    male_infected_list=[j for j in ifct if G.node[j]['bipartite']==0]#at the end of the day update infected list
    female_infected_list=[j for j in ifct if G.node[j]['bipartite']==1]
    #==========at the end of year age people

    if k % 365==0:
        for i in G.nodes():
            G.node[i]['age']=G.node[i]['age']+1
            if G.node[i]['age']>25:
               G.node[i]['age']=15
               if i in ifct:
                   ifct.remove(i)
            
     
for i in G.nodes():
    Age_distribution.append(G.node[i]['age'])    
plt.figure()    
plt.hist(Age_distribution, bins=11)  # plt.hist passes it's arguments to np.histogram
plt.title('all')
plt.show()


Age_men=[]
for i in m_list:
    Age_men.append(G.node[i]['age'])    
plt.figure()    
plt.hist(Age_men, bins=11)  # plt.hist passes it's arguments to np.histogram
plt.title('men')
plt.show()

Age_women=[]
for i in f_list:
    Age_women.append(G.node[i]['age'])    
plt.figure()    
plt.hist(Age_women, bins=11)  # plt.hist passes it's arguments to np.histogram
plt.title('women')
plt.show()
