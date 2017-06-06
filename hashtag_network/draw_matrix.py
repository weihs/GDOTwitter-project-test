from pymongo import MongoClient


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from hashtag_toplist import *#the hashtags we want to retrive
hashtag_number=20
timeinterval_number=50
selfweight=10 #the weight for the edge between the same hashtag in different periods
hashtag=hashtag_toplist

array_filename='data/npy/combine_matrix.npy'#build the graph from adjacency matrix
matrix=np.load(array_filename)
G=nx.from_numpy_matrix(matrix)


for i in range(timeinterval_number):#add the node attributes: number,timeinterval,hashtag text and frequency
    for j in range(hashtag_number):
        G.node[i*hashtag_number+j]['no']=j
        G.node[i*hashtag_number+j]['timeinterval']=i
        G.node[i*hashtag_number+j]['text']=(hashtag[j])
        G.node[i*hashtag_number+j]['weight']=matrix[i*hashtag_number+j][i*hashtag_number+j]

remove=[node for node,value in G.node.items() if value['weight']==0]#filter zero frequency nodes and self edges
G.remove_nodes_from(remove)
number_of_node=len(G.nodes())
for i in G.nodes():
    if i in G.neighbors(i):
        G.remove_edge(i,i)


edges=G.edges()
nodes=G.nodes()
for u,v in edges:
    G[u][v]['weight']=int(G[u][v]['weight'])
    G[u][v]['type']=0#type 0 means edge in different hashtag, type 1 means edge in the same hashtag
for u in nodes:
    G.node[u]['weight']=int(G.node[u]['weight'])

for u in nodes:
    for v in nodes:
        if G.node[u]['no']==G.node[v]['no'] and abs(G.node[u]['timeinterval']-G.node[v]['timeinterval'])==1:
            G.add_edge(u,v)
            G[u][v]['weight']=selfweight
            G[u][v]['type']=1

#draw the graph
weights = np.array([G[u][v]['weight'] for u,v in edges])
node_labels=nx.get_node_attributes(G,'text')
node_size=np.array(list(nx.get_node_attributes(G,'weight').values()))
#nx.draw(G,width=2,labels=node_labels,node_size=0.005*node_size,edge_color=10*weights,edge_cmap=plt.cm.Blues)
nx.write_graphml(G,'data/graphml/GNIP_top20_50days.graphml')
#plt.show()
