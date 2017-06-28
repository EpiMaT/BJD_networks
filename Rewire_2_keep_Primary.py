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
    age_ok=0
    age_bad=0
    for i in m_list:
        j=G.node[i]['primarypartner']
        ai=G.node[i]['age']
        aj=G.node[j]['age']
        if j not  in NB.neighbors(i): 
            d1=NB.degree(i)
            d2=NB.degree(j)
            #=====================with age restriction========================#
            if len([k for k  in NB.neighbors(i) if NB.degree(k)==d2 if abs(ai-G.node[k]['age'])>2])>0: #and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j if abs(aj-G.node[k]['age'])>2])>0:
                for l in [k for k  in NB.neighbors(i) if NB.degree(k)==d2 if abs(ai-G.node[k]['age'])>2]:
                    jp=l
                    if len([k for k  in NB.neighbors(j) if k not in NB.neighbors(jp)  if G.node[k]['primarypartner']!=j if abs(aj-G.node[k]['age'])>2])>0:
                        ip=random.sample([k for k  in NB.neighbors(j) if k not in NB.neighbors(jp)  if G.node[k]['primarypartner']!=j if abs(aj-G.node[k]['age'])>2],1)[0]
                        NB.add_edge(i,j)
                        NB.add_edge(ip,jp)
                        NB.remove_edge(i,jp)
                        NB.remove_edge(ip,j)
                        age_ok=age_ok+1
                        break
            elif  len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j if abs(aj-G.node[k]['age'])>2])>0:
                  for l in [k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j if abs(aj-G.node[k]['age'])>2]:
                      ip=l
                      if len([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip) if abs(ai-G.node[k]['age'])>2])>0:
                        jp=random.sample([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip) if abs(ai-G.node[k]['age'])>2],1)[0] 
                        NB.add_edge(i,j)
                        NB.add_edge(ip,jp)
                        NB.remove_edge(i,jp)
                        NB.remove_edge(ip,j)
                        age_ok=age_ok+1 
                        break      
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2 if abs(ai-G.node[k]['age'])>2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if abs(aj-G.node[k]['age'])>2 ])==0: 
                 for l in [k for k  in m_list if k!=i and NB.degree(k)==d1]:
                    ip=l
                    aip=G.node[ip]['age']
                    if len([f for f  in f_list  if NB.degree(f)==d2 and f in NB.neighbors(ip) and f!=G.node[ip]['primarypartner'] if abs(aip-G.node[f]['age'])>2]) >0:
                        jp=random.sample([f for f  in f_list  if NB.degree(f)==d2 and f in NB.neighbors(ip) and f!=G.node[ip]['primarypartner'] if abs(aip-G.node[f]['age'])>2],1)[0]             
                        if len([f for f in NB.neighbors(i) if f not in NB.neighbors(ip)if abs(ai-G.node[f]['age'])>2 ])>0:
                            S1=random.sample([f for f in NB.neighbors(i) if f not in NB.neighbors(ip) if abs(ai-G.node[f]['age'])>2],1)[0]
                            if len([m for m in NB.neighbors(j) if m not in NB.neighbors(jp) and j!=G.node[m]['primarypartner'] if abs(aj-G.node[m]['age'])>2])>0:
                                S2=random.sample([m for m in NB.neighbors(j) if m not in NB.neighbors(jp)and j!=G.node[m]['primarypartner'] if abs(aj-G.node[m]['age'])>2],1)[0]
                                NB.add_edge(i,j)
                                NB.add_edge(ip,S1)
                                NB.add_edge(jp,S2)
                                NB.remove_edge(ip,jp)
                                NB.remove_edge(i,S1)
                                NB.remove_edge(j,S2)
                                age_ok=age_ok+1
                        break
            #=====================without age restriction========================#
            if len([k for k  in NB.neighbors(i) if NB.degree(k)==d2 ])>0: 
                for l in [k for k  in NB.neighbors(i) if NB.degree(k)==d2]:
                    jp=l
                    if len([k for k  in NB.neighbors(j) if k not in NB.neighbors(jp)  if G.node[k]['primarypartner']!=j ])>0:
                        ip=random.sample([k for k  in NB.neighbors(j) if k not in NB.neighbors(jp)  if G.node[k]['primarypartner']!=j],1)[0]
                        NB.add_edge(i,j)
                        NB.add_edge(ip,jp)
                        NB.remove_edge(i,jp)
                        NB.remove_edge(ip,j)
                        age_bad=age_bad+1
                        break
            elif  len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j])>0:
                  for l in [k for k  in NB.neighbors(j) if NB.degree(k)==d1 if G.node[k]['primarypartner']!=j]:
                      ip=l
                      if len([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip)])>0:
                        jp=random.sample([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip)],1)[0] 
                        NB.add_edge(i,j)
                        NB.add_edge(ip,jp)
                        NB.remove_edge(i,jp)
                        NB.remove_edge(ip,j)
                        age_bad=age_bad+1 
                        break      
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1])==0: 
                 for l in [k for k  in m_list if k!=i and NB.degree(k)==d1]:
                    ip=l
                    if len([f for f  in f_list  if NB.degree(f)==d2 if f in NB.neighbors(ip) if f!=G.node[ip]['primarypartner']]) >0:
                        jp=random.sample([f for f  in f_list  if NB.degree(f)==d2 if f in NB.neighbors(ip) if f!=G.node[ip]['primarypartner']],1)[0]             
                        if len([f for f in NB.neighbors(i) if f not in NB.neighbors(ip)])>0:
                            S1=random.sample([f for f in NB.neighbors(i) if f not in NB.neighbors(ip)],1)[0]
                            if len([m for m in NB.neighbors(j) if m not in NB.neighbors(jp) and j!=G.node[m]['primarypartner']])>0:
                                S2=random.sample([m for m in NB.neighbors(j) if m not in NB.neighbors(jp)and j!=G.node[m]['primarypartner']],1)[0]
                                NB.add_edge(i,j)
                                NB.add_edge(ip,S1)
                                NB.add_edge(jp,S2)
                                NB.remove_edge(ip,jp)
                                NB.remove_edge(i,S1)
                                NB.remove_edge(j,S2)
                                age_bad=age_bad+1
                        break             
    k=0
    for i in m_list:
        j=G.node[i]['primarypartner']
        if j not  in NB.neighbors(i): 
           k=k+1
    print('k=', k/float(len(m_list))) 
    print('age_ok ' ,age_ok)       
    print('age_bad ' ,age_bad)         
    return NB 
     
     
