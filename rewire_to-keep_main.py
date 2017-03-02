import networkx as nx
import copy
import random
import handle_funcs as HF

# import cProfile
_node = 0
_data = 1

_upper = 0
_lower = 1

   
def rewire(G,SG,NB):
    #G: original net which does not change
    #SG: sub net of G ith main partnership
    #NB: the network is going to be rewired to have SG
    B=SG.copy()
    m_list= [n[0] for n in B.nodes(data=True) if HF.is_lower(n)]#list of men
    f_list= [n[0] for n in B.nodes(data=True) if HF.is_upper(n)]#list of women
    for i in m_list:
        B.node[i]['primary']=SG.neighbors(i)[0]
    for i in m_list:
        j=B.node[i]['primary'] 
        if j not  in NB.neighbors(i): 
            
            d1=NB.degree(i)
            d2=NB.degree(j)
            if len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])>0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if B.node[k]['primary']!=j])>0:
                jp=random.sample([k for k  in NB.neighbors(i) if NB.degree(k)==d2],1)[0] 
                ip=random.sample([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if B.node[k]['primary']!=j],1)[0] 
                NB.add_edge(i,j)
                NB.add_edge(ip,jp)
                NB.remove_edge(i,jp)
                NB.remove_edge(ip,j)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if B.node[k]['primary']!=j])>0:     
                ip=random.sample([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if B.node[k]['primary']!=j],1)[0] 
                jk=random.sample([k for k  in NB.neighbors(i) if k not in NB.neighbors(ip)],1)[0] 
                NB.add_edge(i,j)
                NB.add_edge(ip,jk)
                NB.remove_edge(i,jk)
                NB.remove_edge(ip,j)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])>0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 if B.node[k]['primary']!=j])==0:
                ik=random.sample([k for k  in NB.neighbors(j) if B.node[k]['primary']!=j],1)[0] 
                jp=random.sample([k for k  in NB.neighbors(i) if NB.degree(k)==d2],1)[0] 
                NB.add_edge(i,j)
                NB.add_edge(ik,jp)
                NB.remove_edge(ik,j)
                NB.remove_edge(i,jp)
            elif len([k for k  in NB.neighbors(i) if NB.degree(k)==d2])==0 and len([k for k  in NB.neighbors(j) if NB.degree(k)==d1 ])==0: 
           
                for l in [k for k  in m_list if k!=i and NB.degree(k)==d1]:
                    ip=l
                    if len([k for k  in f_list  if NB.degree(k)==d2 and k in NB.neighbors(ip) and k!=B.node[ip]['primary']]) >0:
                        jp=random.sample([k for k  in f_list  if NB.degree(k)==d2 and k in NB.neighbors(ip) and k!=B.node[ip]['primary']],1)[0]             
                        if len([x for x in NB.neighbors(i) if x not in NB.neighbors(ip)])>0:
                            S1=random.sample([x for x in NB.neighbors(i) if x not in NB.neighbors(ip)],1)[0]
                            if len([x for x in NB.neighbors(j) if x not in NB.neighbors(jp)])>0:
                                S2=random.sample([x for x in NB.neighbors(j) if x not in NB.neighbors(jp)],1)[0]
                                NB.add_edge(i,j)
                                NB.add_edge(ip,S1)
                                NB.add_edge(jp,S2)
                                NB.remove_edge(ip,jp)
                                NB.remove_edge(i,S1)
                                NB.remove_edge(j,S2)
                        break
    k=0
    for i in m_list:
        j=B.node[i]['primary'] 
        if j not  in NB.neighbors(i): 
           k=k+1          
    return (k,NB) 
     
     
