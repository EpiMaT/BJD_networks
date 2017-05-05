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

for ms in [[i*g.southern_women for i in [1,2,4,8,16]],[i*g.southern_women.transpose() for i in [1,2,4,8,16]],[i*g.romance for i in [1,2,3]]]:
    for m in ms:
        t = time.time()
        out = Generate_Network.make_graph(nx.Graph(), m, 'max_stub_min_deg')
        elapsed = time.time() - t
        if type(out) is tuple:
            B = out[1]
            print("error",elapsed,B.number_of_nodes(),B.number_of_edges())
        else:
            B = out
            print(elapsed,B.number_of_nodes(),(len(HF.upper_nodes(B)),len(HF.lower_nodes(B))),B.number_of_edges())
            # print(out)
