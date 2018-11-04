#importing essential libraries
import networkx as nx
import random
import matplotlib.pyplot as plt
import math
#creating a graph
G=nx.Graph()
nodeno=0
realnodes=0
#adding node if prob>0.02
while nodeno<50:
prob=random.randint(0,1)
if prob>0.02:
G.add_node(nodeno)
nodeno=nodeno+1
realnodes=realnodes+1
else:
nodeno=nodeno+1
#adding edges
no_of_edges=realnodes*(realnodes-1)/2
it=0
i=0
while i<50:
j=i+1
while j<50:
if it>no_of_edges:
i=100
j=100
else:
G.add_edge(i,j)
it=it+1
j=j+1
i=i+1
#drawing the graph
nx.draw_circular(G,with_labels=1)
plt.show()
print("Number of nodes:",realnodes)
print("Number of edges:",no_of_edges)
#finding average path length
i=0
x=0
apl=0
while i<49:
j=i+1
while j<50:
try:
try: #sum stores the sum of geodesics and num stores the number of nodes having geodesics
apl=apl+len(nx.shortest_path(G,i,j))
except networkx.exception.NetworkXNoPath:
apl=apl+0
except NameError:
apl=apl+0
j=j+1
i=i+1
#print(apl)
print("Average path lenth: ",float(apl/(math.factorial(realnodes)/(math.factorial(realnodes-2)*2))))
