import handle_funcs as HF
import BJD

_node = 0
_data = 1

_upper = 0
_lower = 1

   
def RBJD(G,Sub_G):    
    m_list= [n[0] for n in G.nodes(data=True) if HF.is_lower(n)]#list of men                
    remain_degdeg=BJD.extract(G) 
    for edge in Sub_G.edges():
        e0=edge[0]  
        d0=G.degree(e0)
        e1=edge[1]
        d1=G.degree(e1)
        if e1 in m_list:
            remain_degdeg[d0-1,d1-1]= remain_degdeg[d0-1,d1-1]-1 
        elif e0 in m_list:   
            remain_degdeg[d1-1,d0-1]= remain_degdeg[d1-1,d0-1]-1 
    return remain_degdeg      