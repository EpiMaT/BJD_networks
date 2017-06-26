

* **handle_funcs**

    is a function that all helping functions are defined in it.

* **BJD**

    get a bipartite network as input and find its BJD matrix

* **Generate_networks**

    get the BJD matrix and generate a bipartite network using one of the methods: max_stub_min_degree, random_edge and ...

* **Generate_Aged_networks**
   generate aged network using random edge algorithm.


***Next_Net****

    takes the old network and try to re-partner people from the people with the minimum distance.
    
 ***Next_Aged_Net****

    takes the old aged network and try to re-partner people from the people with the minimum distance.
    
    ***Rewire_2_keep_primary_partners****
    takes the new next_aged_network and make its primary edges if it is not there.   
    
* **graphs**

    defines several BJD matrix as inputs

* **rewire_to_keep_main**

    get a network and rewire it to make main partnership

***find_primary_ppartner***

     after generating aged network select primary partner for only men