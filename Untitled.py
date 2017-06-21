import numpy as np
import random
import handle_funcs as HF
import copy



_node = 0
_data = 1

_upper = 0
_lower = 1



def primary_edge(B):
    m_list= [n[_node] for n in B.nodes(data=True) if HF.is_lower(n)]#list of men
    for man in m_list:
        B.node[man[_node]]['primary partner'] = man[_node] 
        deg_neigbor=[B.degree(j) for j in B.neighbors(man[_node])]
        deg_min=min(deg_neigbor)
        
        
        age_diff = [abs(man[_data]['age'] - n2[_data]['age'] ) for n2 in edge_ls]
        B.node[i]['primary_partner']=random.sample([j for j  in G.neighbors(i) if G.degree(j)==deg_min],1)[0]   
    for i in m_list:
        deg_neigbor=[G.degree(j) for j in G.neighbors(i)]
        deg_min=min(deg_neigbor)
        Sub_G.node[i]['primary_partner']=random.sample([j for j  in G.neighbors(i) if G.degree(j)==deg_min],1)[0] 
    
    for edge in Sub_G.edges():
        e0=edge[0]
        e1=edge[1] 
        if e1 in m_list:
            if (e0 !=Sub_G.node[e1]['primary_partner']):
              Sub_G.remove_edge(*edge)
        elif e0 in m_list:      
            if (e1 !=Sub_G.node[e0]['primary_partner']):
              Sub_G.remove_edge(*edge)   
    
    for i in Sub_G.nodes():
        del Sub_G.node[i]['primary_partner']
    return Sub_G

 