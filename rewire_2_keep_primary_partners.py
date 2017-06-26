import networkx as nx
import copy
import random
import handle_funcs as HF

# import cProfile
_node = 0
_data = 1

_upper = 0
_lower = 1

   
def rewire(G,NB):
    #G: original first net
    #NB: the network is going to be rewired to have primary partners
    
    m_list= [n[0] for n in G.nodes(data=True) if HF.is_lower(n)]#list of men
    f_list= [n[0] for n in G.nodes(data=True) if HF.is_upper(n)]#list of women
    for i in m_list:
        j=G.node[i]['primarypartner']
        if j not  in NB.neighbors(i): 
            d1=NB.degree(i)
            d2=NB.degree(j)
            if len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])>0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j])>0:
                jp=random.sample([k for k  in NB.neighbors(i) if NB.degree(k)==d2],1)[0] 
                ip=random.sample([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j],1)[0] 
                NB.add_edge(i,j)#about age no worries
                NB.add_edge(ip,jp)#somehow need to apply their age
                NB.remove_edge(i,jp)
                NB.remove_edge(ip,j)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j])>0:     
                ip=random.sample([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j],1)[0] 
                jk=random.sample([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip)],1)[0] 
                NB.add_edge(i,j)#about age no worries
                NB.add_edge(ip,jk)#somehow need to apply their age
                NB.remove_edge(i,jk)
                NB.remove_edge(ip,j)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])>0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j])==0:
                ik=random.sample([k for k  in NB.neighbors(j) if G.node[k]['primarypartner']!=j],1)[0] 
                jp=random.sample([k for k  in NB.neighbors(i) if NB.degree(k)==d2],1)[0] 
                NB.add_edge(i,j)#about age no worries
                NB.add_edge(ik,jp)#somehow need to apply their age
                NB.remove_edge(ik,j)
                NB.remove_edge(i,jp)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 ])==0: 
           
                for l in [k for k  in m_list if k!=i and NB.degree(k)==d1]:
                    ip=l
                    if len([f for f  in f_list  if NB.degree(f)==d2 and f in NB.neighbors(ip) and f!=G.node[ip]['primarypartner']]) >0:
                        jp=random.sample([f for f  in f_list  if NB.degree(f)==d2 and f in NB.neighbors(ip) and f!=G.node[ip]['primarypartner']],1)[0]             
                        if len([f for f in NB.neighbors(i) if f not in NB.neighbors(ip)])>0:
                            S1=random.sample([f for f in NB.neighbors(i) if f not in NB.neighbors(ip)],1)[0]
                            if len([m for m in NB.neighbors(j) if m not in NB.neighbors(jp) and j!=G.node[m]['primarypartner']])>0:
                                S2=random.sample([m for m in NB.neighbors(j) if m not in NB.neighbors(jp)and j!=G.node[m]['primarypartner']],1)[0]
                                NB.add_edge(i,j)
                                NB.add_edge(ip,S1)#somehow need to apply their age
                                NB.add_edge(jp,S2)#somehow need to apply their age
                                NB.remove_edge(ip,jp)
                                NB.remove_edge(i,S1)
                                NB.remove_edge(j,S2)
                        break
    k=0
    for i in m_list:
        j=G.node[i]['primarypartner']
        if j not  in NB.neighbors(i): 
           k=k+1
    print('k=', k/float(len(m_list)))                 
    return NB 
     
     
