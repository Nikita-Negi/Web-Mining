#importing necessary libraries for network and plotting functions
import networkx as nx
import matplotlib.pyplot as plt
import jgraph as jg
import numpy as np

#defining a directional graph
G=nx.DiGraph()

#adding nodes
G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8)
G.add_node(9)
G.add_node(10)
G.add_node(11)
G.add_node(12)
G.add_node(13)
G.add_node(14)

#adding directional edges from starting to destination node
G.add_edge(1,0)
G.add_edge(2,1)
G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(1,5)
G.add_edge(0,5)
G.add_edge(1,6)
G.add_edge(6,0)
G.add_edge(5,6)
G.add_edge(0,7)
G.add_edge(8,0)
G.add_edge(9,6)
G.add_edge(9,10)
G.add_edge(11,9)
G.add_edge(10,11)
G.add_edge(10,12)
G.add_edge(13,12)
G.add_edge(11,14)
G.add_edge(14,0)
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#SECTION FOR ANSWER 1

#finding a dictionary with betweeness, degree and closeness centrality
deg_cen=nx.degree_centrality(G)
bet_cen=nx.betweenness_centrality(G)
clo_cen=nx.closeness_centrality(G)

#displaying centrality measures
print("Social Network measure for each node are:\n\n")
print ("Degree Centrality\n")
print("--------------------")
i=0
while i<15:
     print ("Node ",i,":\t",deg_cen[i],"\n")
     i=i+1
print ("Betweeness Centrality\n")
print("------------------------")
i=0
while i<15:
     print ("Node ",i,":\t",bet_cen[i],"\n")
     i=i+1
print ("Closeness Centrality\n")
print("-----------------------")
i=0
while i<15:
     print ("Node ",i,":\t",clo_cen[i],"\n")
     i=i+1

#forming adjacency matrix for prestige measures
C=nx.to_numpy_matrix(G)
C=np.array(C)
i=0

#calculating degree prestige
print ("Degree Prestige\n")
print("-----------------------")
while i<15:
     j=0
     sum=0
     while j<15:
         sum=sum+C[j][i]
         j=j+1
     print("Node ", i, ":\t", sum/14, "\n")
     i=i+1

#calculating rank prestige
print ("Rank Prestige\n")
print("-----------------------")
rankcopy=nx.pagerank(G)
i=0
while i<15:
     sum=0
     j=0
     while j<15:
          if C[j][i]==1:
               sum=sum+rankcopy[j]
          j=j+1
     print("Node ", i, ":\t", sum, "\n")
     i=i+1

#calculating proximity prestige
print ("Proximity Prestige\n")
print("-----------------------")
i=0
while i<15:
     sum=0
     num=0
     j=0
     while j<15:
          path=[]
          if j==i:
              j=j+1
          try:
               try:
                    #sum stores the sum of geodesics and num stores the number of nodes having geodesics
                    sum=sum+len(nx.bidirectional_shortest_path(G,j,i))
                    num=num+1
               except networkx.exception.NetworkXNoPath:
                    sum+0
          except NameError:
               sum=sum+0
          j=j+1
     if num==0:
          print("Node ", i, ":\t", sum, "\n")
     else:
          print("Node ", i, ":\t", sum/num, "\n")
     i=i+1

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#SECTION FOR ANSWER 2

#takes the nodes to check as input
print("\nEnter two nodes to check for co-citation and bibliographic coupling.")
node1=int(input("Enter first node:"))
node2=int(input("Enter second node:"))
print("Calculating results...............\n")
scorer=0
scorec=0
scorer1=0
scorec1=0
i=0

#finding row and column length for each node
while i<15:
     if C[node1][i]==1:
          scorer=scorer+1
     if C[i][node1]==1:
          scorec=scorec+1
     i=i+1

#if row length is zero then it cannot form a co-citation couple
if scorer==0:
     print("\n These two nodes DO NOT form a bibliographic couple.")
else:
     i=0
     pair=[]
     while i<15:
          if C[node1][i]==1 and C[node2][i]==1:
               scorer1=scorer1+1
               pair.append(i)
          i=i+1
     #if row length is equal to dot product of the two rows then they form a co-citation couple
     if scorer1==scorer:
          print("\n-->These two nodes DO form bibliographic couple.")
          print("\nThey are referred by",scorer," nodes.")
          print("\nList of nodes:",pair)
     else:
          print("\n-->These two nodes DO NOT form a bibliographic couple.")

#if column length is zero then it cannot form a bibliographic couple
if scorec==0:
     print("\nThese two nodes DO NOT form a co-citation couple.")
else:
     i=0
     pair=[]
     while i<15:
          if C[i][node1]==1 and C[i][node2]==1:
               scorec1=scorec1+1
               pair.append(i)
          i=i+1
     # if column length is equal to dot product of the two columns then they form a bibliographic couple
     if scorec1==scorec:
          print("\n-->These two nodes DO form a co-citation couple.")
          print("\nThey co-cited",scorec," nodes.")
          print("\nList of nodes:", pair)
     else:
          print("\n-->These two nodes DO NOT form a co-citation couple.")
print("\n")
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#SECTION FOR ANSWER 3

#finding page rank of the nodes in the graph
rank=nx.pagerank(G)

#printing page rank in descending order
print("\nPage Rank of the nodes in the graph in descending order:\n")
print("------------------------------------------------------------")
pagerank=rank.values()
pagerank=sorted(pagerank)
i=14
while i>-1:
     for key in rank:
          if(pagerank[i]==rank[key]):
               print(key,"\t:\t",pagerank[i])
               i=i-1

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
print(C)
#plotting the directed graph
nx.draw_circular(G,with_labels=1)
plt.show()

