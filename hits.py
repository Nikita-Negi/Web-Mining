#importing libraries 
import networkx as nx 
import matplotlib.pyplot as plt 
#creating a random graph 
G=nx.gnp_random_graph(20,0.2,None,True) 
#finding hubs and authority value of each node 
h,a=nx.hits(G) 
#dispalying hub and authority values 
print("\nHub score of the nodes in the graph:") 
print("-----------------------------------------") 
print(h) 
print("\nAuthority score of the nodes in the graph:") 
print("-----------------------------------------") 
print(a) 
#plotting the graph 
nx.draw_circular(G,with_labels=1) 
plt.show()
