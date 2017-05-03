import networkx as nx
import numpy as np
import copy
import handle_funcs as HF
# import cProfile


_node = 0
_data = 1

_upper = 0
_lower = 1


def make_graph(B,degdeg_distr, method_ext,B_old):
    """Take an empty Graph, B, a BJD matrix and a desired method of generation"""
    number_of_nodes = len(B_old)
   

    def max_deg(nodedata):
        return nodedata[_data]['deg']

    def curr_deg(nodedata):
        return B.degree(nodedata[_node])

    def is_neighbor(n1, n2):
        return n1[_node] in B.neighbors(n2[_node])

    

    n_edges = degdeg_distr.sum()
    degdeg_remaining = degdeg_distr.copy()

    # Fill graph with nodes
    HF.add_upper_nodes(B, HF.upper_deg_distr(degdeg_remaining))
    HF.add_lower_nodes(B, HF.lower_deg_distr(degdeg_remaining))

    upper_nodes = [n for n in B.nodes(data=True) if HF.is_upper(n)]
    lower_nodes = [n for n in B.nodes(data=True) if HF.is_lower(n)]

    double_edges = []
    # Fill graph with edges
    if method_ext[-5:] == "_NORW":
        method = method_ext[0:-5]
    else:
        method = method_ext

    # top_node = ''
    edge_degs_list = HF.list_edge_degs(degdeg_remaining)
    if method == 'random_edge':
        pass
    else:
        return ("Not a valid method -- {}".format(method), B)

    for edge_i in xrange(n_edges):
        edge_found = False
        # Pick an edge
        impossibles = []
        if method == 'random_edge1':
            return ("Not a valid method method")
        else:
            if method == 'random_edge':
                edge = HF.choose_and_remove(edge_degs_list)

            upper_options = [n for n in upper_nodes if max_deg(n) == edge[0] and curr_deg(n) < max_deg(n)]
            lower_options = [n for n in lower_nodes if max_deg(n) == edge[1] and curr_deg(n) < max_deg(n)]
            #==================REVISED RANDOM EDGE=============== 
            
            possibles_unsorted = []

            for upp in upper_options:
                for low in lower_options:
                    possible_edge = (upp, low)
                    if is_neighbor(upp, low):
                        impossibles.append(possible_edge)
                    else:
                       if nx.has_path(B_old, upp[_node], low[_node]):
                           path_len = nx.shortest_path_length(B_old, source=upp[_node], target=low[_node])
                           if path_len == 1:
                              path_len=number_of_nodes+1
                       else:
                           path_len = number_of_nodes+1

                       possibles_unsorted.append((possible_edge, path_len))
                        
            
            if len(possibles_unsorted) > 0:
                possibles = sorted(possibles_unsorted, key=lambda tup: tup[1])

                first = possibles[0]
                new_possibles = []
                for entry in possibles:
                   if entry[1] == first[1]:
                        new_possibles.append(entry[0])
                   else:
                       break
                (upper,lower) = HF.choose(new_possibles)
                edge_found = True
            
           
        #==================ORIGINAL RANDOM EDGE=============== 
        '''
            possibles = []
            for upp in upper_options:
                for low in lower_options:
                    possible_edge = (upp,low)
                    if is_neighbor(upp, low):
                        impossibles.append(possible_edge)
                    else:
                        possibles.append(possible_edge)

            if len(possibles) > 0:
                (upper,lower) = HF.choose(possibles)
                edge_found = True
            #print upper    
         '''     
        #=================================        
        if not edge_found:
            if len(impossibles) <= 0:
                return ("Major error -- {}".format(edge_i), B)
            (upper,lower) = HF.choose(impossibles)
            edge = (max_deg(upper),max_deg(lower))
            double_edges.append((upper,lower))

        # Remove_edge
        B.add_edge(upper[_node],lower[_node])
        degdeg_remaining[edge[0]-1,edge[1]-1] = degdeg_remaining[edge[0]-1,edge[1]-1] - 1

    nz, tm = HF.compare_graph_to_table(B, degdeg_distr, False)
    if nz != 0:
        return ("Failed to make valid graph (allowing multiple edges).", B)

    if method_ext[-5:] == "_NORW":
        if len(double_edges) > 0:
            return ("Needed to rewire", B)
        else:
            return ((0,0), B)

    rewire2 = 0
    rewire3 = 0
    for dedge in double_edges:
        (upper,lower) = dedge
        if B.number_of_edges(upper[_node],lower[_node]) <= 1:
            continue

        up_deg = max_deg(upper)
        low_deg = max_deg(lower)

        alternateUV = []
        for u_prime in upper_nodes:
            if max_deg(u_prime) != up_deg:
                continue
            for l_prime in lower_nodes:
                if max_deg(l_prime) != low_deg:
                    continue
                if u_prime == upper and l_prime == lower:
                    continue
                if is_neighbor(u_prime, l_prime):
                    continue

                if u_prime == upper or l_prime == lower: # 2-rewire
                    do_prime = l_prime
                    do_partner = upper
                    do_base = lower
                    if l_prime == lower:
                        do_prime = u_prime
                        do_partner = lower
                        do_base = upper
                    do_others = []
                    for other in B.neighbors(do_prime[_node]):
                        if other != do_partner[_node] and not B.has_edge(other, do_base[_node]):
                            do_others.append(other)
                    alternateUV.append((do_prime,do_partner,do_base,do_others))
                else: # 3-rewire
                    l_others = []
                    for low in B.neighbors(u_prime[_node]):
                        if low != lower[_node] and not B.has_edge(low,upper[_node]):
                            l_others.append(low)
                    u_others = []
                    for upp in B.neighbors(l_prime[_node]):
                        if upp != upper[_node] and not B.has_edge(upp,lower[_node]):
                            u_others.append(upp)

                    if len(l_others) > 0 and len(u_others) > 0:
                        alternateUV.append((u_prime,l_prime,l_others,u_others))

        if len(alternateUV) <= 0:
            print B.edges()
            print upper, lower, B.edges()
            return ("Cannot rewire.", B)

        tup = HF.choose(alternateUV)
        if type(tup[2]) is list:
            (u_prime, l_prime, l_others, u_others) = tup
            l_other = HF.choose(l_others)
            u_other = HF.choose(u_others)

            B.remove_edge(upper[_node],lower[_node])
            B.remove_edge(u_prime[_node],l_other)
            B.remove_edge(l_prime[_node],u_other)

            B.add_edge(upper[_node],l_other)
            B.add_edge(lower[_node],u_other)
            B.add_edge(u_prime[_node],l_prime[_node])
            rewire3 = rewire3 + 1
        else:
            (do_prime, do_partner, do_base, do_others) = tup
            do_other = HF.choose(do_others)

            B.remove_edge(do_base[_node],do_partner[_node])
            B.remove_edge(do_prime[_node],do_other)

            B.add_edge(do_base[_node],do_other)
            B.add_edge(do_prime[_node],do_partner[_node])
            rewire2 = rewire2 + 1

    nz, tm = HF.compare_graph_to_table(B, degdeg_distr, True)
    if nz != 0:
        return ("Table not comparable to graph, {}: ndouble {}".format(nz,len(double_edges)), B)

    return B






