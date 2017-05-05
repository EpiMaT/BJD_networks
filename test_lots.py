import networkx as nx
import numpy as np
import time

import example_graphs as g

import BJD
import handle_funcs as HF
import Generate_Network
try:
    reload(BJD)
    reload(HF)
    reload(Generate_Network)
except NameError:
    print("Not running in Canopy")
else:
    print("Running in Canopy")

b = [1,10]
for name in ['small','many3','large','basic_fail','asymmetric','asymmetric2']:
    dd = getattr(g,name)
    print(name)
    for i in b:
        print(i)
        out = Generate_Network.make_graph(nx.Graph(), i*dd, 'max_stub_min_deg')
        if type(out) is tuple:
            B = out[1]
            print(out)
