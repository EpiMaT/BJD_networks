#this function treat partner of screened people
import math
import random
import networkx as nx
import pylab as pl
import numpy as np
import config as cfg
import multiprocessing


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


####################
def avgf(k1,k2):
    k_avg=(k1*k2)*2.0/(k1+k2)
    return k_avg
#----------------------------------Network and its properties


#---------end of for transmission rate----------
def one_sim(l):
    random.seed(l)
    pl.seed(l)
    np.random.seed(l)
    betam2f=6*[0]
    betaf2m=6*[0]
    for i in range(0,6):
        betam2f[i]=(1-cfg.beta_m2f)**edge_weight(i+1)
        betaf2m[i]=(1-cfg.beta_f2m)**edge_weight(i+1)
    
    #G=nx.read_gml('/Users/aazizibo/Desktop/Network_Model_codes/Data_Input/test.gml')
    G=nx.read_gml('../Data_Input/test.gml')
    people_list = [i for i in G.nodes()]
    m_list=[n for n,d in G.nodes(data=True) if d['bipartite']==0]#list of men
    f_list=[n for n,d in G.nodes(data=True) if d['bipartite']==1]#list of women
    
    number_of_people = len(people_list)
    print "total population is ", number_of_people 
    
    
    
    
    number_of_men = len(m_list)
    number_of_female = len(f_list)

    t=number_of_people*[0]
    #begin simulation
        
    ifct= [1127, 2004, 4896, 224, 3710, 285, 348, 56, 4351, 3329, 120, 2868, 3725, 213, 3567, 4446, 3934, 2820, 2665, 4342, 4998, 61, 2748, 1406, 1779, 4794, 834, 2914, 4149, 2228, 3180, 4992, 3390, 4940, 551, 3866, 1818, 4735, 2431, 461, 729, 4698, 2842, 2429, 24, 7, 3938, 3959, 4749, 4620, 2603, 155, 3758, 3320, 4659, 4454, 715, 2544, 4762, 4989, 1034, 4049, 3089, 3730, 4688, 4113, 3568, 3782, 4741, 28, 3352, 4333, 3893, 1894, 352, 4930, 4122, 3096, 4745, 4902, 4836, 4650, 268, 4267, 471, 492, 4947, 4452, 275, 365, 169, 2216, 2850, 2610, 242, 4565, 4965, 1991, 4718, 3421, 1739, 1785, 4682, 174, 1512, 4043, 3478, 4109, 4633, 708, 4323, 2568, 3667, 4979, 4866, 2509, 4634, 4553, 2988, 2001, 2981, 2529, 1961, 3584, 3000, 4665, 985, 3119, 4872, 2643, 2606, 2366, 3698, 1584, 4501, 83, 3973, 276, 4182, 4833, 386, 35, 845, 2388, 4851, 4851, 3371, 2556, 4480, 2443, 4933, 3247, 303, 3314, 45, 2863, 4672, 3563, 3138, 3424, 2398, 3211, 4971, 3377, 163, 21, 4141, 2068, 280, 4567, 271, 4727, 2439, 3892, 4602, 1891, 44, 3912, 3980, 3178, 4308, 4488, 4703, 1351, 4962, 2785, 4372, 4987, 2006, 2615, 2947, 2792, 932, 4484, 4974, 3896, 2828, 4535, 3408, 3802, 4402, 3488, 4956, 3281, 3292, 3825, 2003, 1293, 523, 3030, 2560, 82, 473, 60, 29, 2453, 78, 3502, 4389, 2178, 3521, 2379, 3562, 3112, 4399, 3852, 1274, 1423, 3847, 3549, 4422, 935, 4582, 1, 4056, 3919, 248, 2498, 202, 3799, 3972, 4922, 516, 4464, 4335, 2446, 1556, 1401, 2483, 2, 1838, 4468, 4024, 151, 0, 3793, 2240, 4983, 281, 1892, 2724, 4685, 143, 2655, 3984, 4643, 3182, 3662, 4440, 3354, 657, 4170, 1918, 2771, 731, 4783, 49, 4760, 2657, 4835, 4986, 4548, 2110, 2381, 4671, 3269, 3260, 51, 4453, 2599, 65, 3684, 4867, 4491, 4363, 2385, 4787, 2450, 4278, 3058, 16, 3217, 1114, 2369, 4924, 2884, 2422, 72, 3794, 4963, 4038, 3891, 2257, 1799, 4374, 2231, 815, 4915, 1141, 4576, 4343, 37, 93, 2373, 4223, 274, 4080, 4905, 4654, 47, 4984, 4763, 2473, 4619, 2727, 2798, 2624, 4875, 2895, 2676, 3150, 1324, 4574, 3489, 3317, 865, 3918, 3465, 4472, 2952, 4996, 1634, 1986, 4547, 4852, 4677, 3953, 2700, 720, 3050, 3579, 4999, 3703, 2311, 2365, 3340, 30, 15, 2592, 4889, 2793, 3841, 4816, 4178, 70, 176, 4932, 4469, 2740, 427, 2508, 3091, 1794, 250, 4615, 3209, 300, 1901, 4818, 3145, 2866, 142, 4954, 2096, 3876, 3976, 6, 266, 2666, 4382, 1377, 2751]




    
 #initial infected list
    Treat_partner_of_male_matrix=[[]]
    Treat_partner_of_female_matrix=[[]]
    Test_treat_matrix=[[]]
    Rescreening_matrix = [[]]
    Again_infected_matrix=[[]]
    time_between_treat_and_infection=[[0,0]]
    for i in ifct:
        t[i]=-1
    T = []
    
    
    number_of_infected = []
    number_of_infected_male = []
    number_of_infected_female= []
    new_ifct_case=[]
    
    
    number_of_ifct=cfg.t_simulation*[0]
    number_of_male_ifct=cfg.t_simulation*[0]
    number_of_new_male=cfg.t_simulation*[0]
    number_of_female_ifct=cfg.t_simulation*[0]
    number_of_new_female=cfg.t_simulation*[0]
    number_of_screening=cfg.t_simulation*[0]
     
    for i in G.nodes():
        G.node[i]['infection time']=0
        G.node[i]['screening time']=0
        
    #------------------------------------- 
    for k in range(0,cfg.t_simulation):
        # walk through infecteds list and try to infect neighbors
        to_remove=[]
        to_add=[]
        for i in ifct: #do recovery
            if t[i]==-1:
                t[i]=max(1,round(-math.log(1-pl.rand())/cfg.gamma))
                G.node[i]['infection time']=t[i]
                if G.node[i]['screening time']>0:
                   time_between_treat_and_infection=np.vstack([time_between_treat_and_infection, [k-G.node[i]['screening time'],k]])
            elif t[i]>0:
                t[i]=t[i]-1
            elif t[i]==0:
                to_remove.append(i)
                
            #------------track neighbors-------------do transmission
            for j in G.neighbors(i):
                if j not in ifct and G.node[j]['bipartite']==1:
                    if pl.rand()<edge_weight(G.degree(j)):
                        if pl.rand()< cfg.beta_m2f:
                    #if  (1-betam2f[G.degree(j)-1])> pl.rand():
                          to_add.append(j)
                          t[j]=-1
                elif j not in ifct and G.node[j]['bipartite']==0:
                    if pl.rand()<edge_weight(G.degree(i)):
                        if pl.rand()< cfg.beta_f2m: 
                   # if (1-betaf2m[G.degree(i)-1])> pl.rand():
                            to_add.append(j)
                            t[j]=-1
        # infected list by gender
        male_infected_list=[j for j in ifct if G.node[j]['bipartite']==0]
        female_infected_list=[j for j in ifct if G.node[j]['bipartite']==1]
        # become infected today
        new_male_list=[j for j in to_add if G.node[j]['bipartite']==0]
        new_female_list=[j for j in to_add if G.node[j]['bipartite']==1]
        number_of_new_male[k]=len(new_male_list)
        number_of_new_female[k]=len(new_female_list)
        #=========================START INTERVENTION======================#
        partner_of_ifct_male_list=[]
        social_friend_of_ifct_male_list=[]####
        partner_of_ifct_female_list=[]
        social_friend_of_ifct_female_list=[]####
        Partner_of_male_notified_list=[]
        Partner_of_female_notified_list=[]
        Treat_partner_of_male_list=[]
        Treat_partner_of_female_list=[]
        Test_treat_partner_of_male_list=[]
        Test_treat_partner_of_female_list=[]
        Test_treat_partner_list=[]
        Rescreening_list = []
        Again_infected_list=[]
        screened_list_today=[]
        screened_ifct_male_list=[]
        partner_of_ifct_male_list=[]
        screened_ifct_female_list=[]
        partner_of_ifct_female_list=[]
        #**************************MALE**********************************
        candidate_male=[i for i in male_infected_list] 
        n1=len(candidate_male)
        m1=int(math.floor(cfg.screening_rate_men*n1))
        p1=(cfg.screening_rate_men*n1)-m1
        if pl.rand()<p1:
            screened_ifct_male_list=random.sample(candidate_male,m1+1)
        else:
            screened_ifct_male_list=random.sample(candidate_male,m1) 
            
        #===================social friend of found ifct men====================== 
        for   man in screened_ifct_male_list:
              social_for_him=[]
              p1=G.node[man]['avgcontact']
              for woman in G.neighbors(man):
                  for social_friend in  G.neighbors(woman):
                      p2=G.node[social_friend]['avgcontact']
                      k=len(nx.common_neighbors(G, man, social_friend))
                      if pl.rand()< 1-(1-p1*p2)**k:
                         social_for_him.append(social_friend)
                         
                         social_friend_of_ifct_male_list.append(social_friend)
                          
                      
        #===========================add contact tracing===========================    
        if k>=cfg.time_lag_test_treat:
           for i in Test_treat_matrix[k-cfg.time_lag_test_treat]:
                if i in male_infected_list:
                    if i not in screened_ifct_male_list:
                       screened_ifct_male_list.append(i)    
        #till now we found scereened men, some randomly and some through contact tracing
        screened_list_today=[i for i in screened_ifct_male_list]
        for i in screened_ifct_male_list:
            partner_of_ifct_male_list.extend(G.neighbors(i))
        number_of_partners=len(partner_of_ifct_male_list)
        
        #============================PARTNERS NOTIFIED=====================
        n=int(math.floor(cfg.partner_notification*number_of_partners))#size of partner notified and seek treating
        pts=(cfg.partner_notification*number_of_partners)-n
        if pl.rand()<pts: #partner to choose for treating
            Partner_of_male_notified_list=random.sample(partner_of_ifct_male_list,n+1)
        else:
            Partner_of_male_notified_list=random.sample(partner_of_ifct_male_list,n) 
        number_of_partners_notified=len(Partner_of_male_notified_list)    
        #===========================Treating Partners===========================
        m=int(math.floor(cfg.partner_treat*number_of_partners_notified))#size of partner to choose for treating
        pts=(cfg.partner_treat*number_of_partners_notified)-m
        if pl.rand()<pts: #partner to choose for treating
            Treat_partner_of_male_list=random.sample(Partner_of_male_notified_list,m+1)
        else:
            Treat_partner_of_male_list=random.sample(Partner_of_male_notified_list,m)  
        Treat_partner_of_male_matrix.append(Treat_partner_of_male_list) 
        #===========================Test and treat Partners===========================
        Test_treat_partner_of_male_list=[i for i in Partner_of_male_notified_list if i not in Treat_partner_of_male_list]
                
        #====================Do Screening=========================
        for i in screened_ifct_male_list:
            Scr_rec=max(1,round(float(np.random.lognormal(cfg.gamma_s, .25, 1)[0])))
            if t[i]> Scr_rec:
               t[i]= Scr_rec
                 
        #=================screen partners from time_lag days later before ===========================         
        if k>=cfg.time_lag_partner_treatment: 
            for i in Treat_partner_of_male_matrix[k-cfg.time_lag_partner_treatment]:
                if i in female_infected_list:
                   Scr_rec=max(1,round(float(np.random.lognormal(cfg.gamma_s, .25, 1)[0])))
                   if t[i]> Scr_rec:
                      t[i]= Scr_rec 
        #**************************FEMALE********************************** 
        candidate_female=[i for i in female_infected_list] #men candidate for screening
        n1=len(candidate_female)
        m1=int(math.floor(cfg.screening_rate_women*n1))#number of men to be screened
        p1=(cfg.screening_rate_women*n1)-m1
        if pl.rand()<p1:
            screened_ifct_female_list=random.sample(candidate_female,m1+1)
        else:
            screened_ifct_female_list=random.sample(candidate_female,m1) 
        #===========================add contact tracing===========================    
        if k>=cfg.time_lag_test_treat:
           for i in Test_treat_matrix[k-cfg.time_lag_test_treat]:
                if i in female_infected_list:
                    if i not in screened_ifct_female_list:
                        screened_ifct_female_list.append(i)    
        #till now we found scereened women, some randomly and some through contact tracing
        for i in screened_ifct_female_list:
            partner_of_ifct_female_list.extend(G.neighbors(i))
        number_of_partners=len(partner_of_ifct_female_list)
        #============================PARTNERS NOTIFIED=====================
        n=int(math.floor(cfg.partner_notification*number_of_partners))#size of partner notified and seek treating
        pts=(cfg.partner_notification*number_of_partners)-n
        if pl.rand()<pts: #partner to choose for treating
            Partner_of_female_notified_list=random.sample(partner_of_ifct_female_list,n+1)
        else:
            Partner_of_female_notified_list=random.sample(partner_of_ifct_female_list,n) 
        number_of_partners_notified=len(Partner_of_female_notified_list)    
        #===========================Treating Partners===========================
        m=int(math.floor(cfg.partner_treat*number_of_partners_notified))#size of partner to choose for treating
        pts=(cfg.partner_treat*number_of_partners_notified)-m
        if pl.rand()<pts: #partner to choose for treating
            Treat_partner_of_female_list=random.sample(Partner_of_female_notified_list,m+1)
        else:
            Treat_partner_of_female_list=random.sample(Partner_of_female_notified_list,m)  
        Treat_partner_of_female_matrix.append(Treat_partner_of_female_list) 
        #===========================Test and treat Partners===========================
        Test_treat_partner_of_female_list=[i for i in Partner_of_female_notified_list if i not in Treat_partner_of_female_list]
                  
        #====================Do Screening=========================
        for i in screened_ifct_female_list:
             if i not in screened_list_today:
                screened_list_today.append(i)
                Scr_rec=max(1,round(float(np.random.lognormal(cfg.gamma_s, .25, 1)[0])))
                if t[i]> Scr_rec:
                   t[i]= Scr_rec  
        #=================screen partners from time_lag days later before ===========================        
        if k>=cfg.time_lag_partner_treatment: 
            for i in Treat_partner_of_female_matrix[k-cfg.time_lag_partner_treatment]:
                if i in male_infected_list:
                    if i not in screened_list_today:
                       Scr_rec=max(1,round(float(np.random.lognormal(cfg.gamma_s, .25, 1)[0])))
                       if t[i]> Scr_rec:
                          t[i]= Scr_rec 
        #*****************************************************************************
        #=====================update test and treat partners====================
        Test_treat_partner_list=Test_treat_partner_of_male_list+Test_treat_partner_of_female_list
        Test_treat_matrix.append(Test_treat_partner_list)
        for i in screened_list_today:
            G.node[i]['screening time']=k
        #======================Re-screening list and do Rescreening======================  
        #how to add rescreen people to the screen today?
        n=int(math.floor(cfg.rescreening_rate*len(screened_list_today)))  
        pts=cfg.rescreening_rate*len(screened_list_today)-n
        if pl.rand()<pts:
            Rescreening_list=random.sample(screened_list_today,n+1)
        else:
            Rescreening_list=random.sample(screened_list_today,n)  
        Rescreening_matrix.append(Rescreening_list)  
        if k>= cfg.time_lag_rescreening:#rescreening people
            for i in  Rescreening_matrix[k-cfg.time_lag_rescreening]:
                if i in ifct:
                    if i not in screened_list_today:#test them if they are infected but not screened earlier today
                       G.node[i]['screening time']=k
                       Scr_rec=max(1,round(float(np.random.lognormal(cfg.gamma_s, .25, 1)[0])))
                       if t[i]> Scr_rec:
                          t[i]= Scr_rec 
        #===================== UPDATA DATA AT THE END OF DAY====================== 
        for i in to_remove:
            ifct.remove(i)
        for j in to_add:
           ifct.append(j)
        male_infected_list=[j for j in ifct if G.node[j]['bipartite']==0]#at the end of the day update infected list
        female_infected_list=[j for j in ifct if G.node[j]['bipartite']==1]
        number_of_ifct[k]=len(ifct)
        number_of_male_ifct[k]=len(male_infected_list)
        number_of_female_ifct[k]=len(female_infected_list)
        T.extend([float(k)])
        number_of_infected.extend([number_of_ifct[k]])
        number_of_infected_male.extend([number_of_male_ifct[k]])
        number_of_infected_female.extend([number_of_female_ifct[k]])
        new_ifct_case.extend([number_of_new_male[k]+number_of_new_female[k]])
         
        #TODAY DONE!
   
    
#number_of_reinfected_list=[len(x) for x in Again_infected_matrix]
    DataOut = np.column_stack((T,number_of_infected,number_of_infected_male,number_of_infected_female,new_ifct_case))
    np.savetxt('../Data_Output/simulation'+str(l+1)+'.dat',DataOut,fmt=('%i', '%4.3f', '%4.3f', '%4.3f', '%4.3f'))
   # np.savetxt('../Data_Output/node_information'+str(l+1)+'.dat',DataNode,fmt=('%4.3f', '%4.3f'))
    np.savetxt('../Data_Output/infection_information'+str(l+1)+'.dat',time_between_treat_and_infection,fmt=('%4.3f'))
    

processes =[multiprocessing.Process(target=one_sim, args=(num,)) for num in range(0,cfg.n_simulation)]
for p in processes:
    p.start()

for p in processes:
    p.join()
