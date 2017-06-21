import numpy as np
import random
import handle_funcs as HF
import copy



_node = 0
_data = 1

_upper = 0
_lower = 1



def primary_edges(B):
    m_list= [n[0] for n in B.nodes(data=True) if HF.is_lower(n)]#list of men
   
    for man in m_list:
        age = B.node[man]['age']
        deg_neigbor=[B.degree(j) for j in B.neighbors(man)] 
        deg_min=min(deg_neigbor)
        sample1=[j for j in B.neighbors(man) if B.degree(j)==deg_min]
        sample2=[j for j in B.neighbors(man) if B.node[j]['age'] ==age]
        final_sample=list(set(sample1).intersection(sample2))
        if len(final_sample)>0:
           B.node[man]['primarypartner'] = random.sample(final_sample,1)[0]
        
        else:
            age_diff = [abs(age - B.node[j]['age']) for j in sample1]
            age_chosen=min(age_diff) 
            idx_list=[idx for idx, diff in enumerate(age_diff) if diff==int(age_chosen)]  
            B.node[man]['primarypartner']=sample1[np.random.choice(idx_list)]
        
    return B
    
   
 