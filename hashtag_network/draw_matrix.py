import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from hashtag import * #the hashtags we want to retrive
hashtag_number=21
timeinterval_number=1

array_filename='co_occurrence_0.npy'#build the graph from adjacency matrix
matrix=np.load(array_filename)
G=nx.from_numpy_matrix(matrix)

for i in range(timeinterval_number):#add the node attributes: number,timeinterval,hashtag text and frequency
    for j in range(hashtag_number):
        G.node[i*hashtag_number+j]['no']=j
        G.node[i*hashtag_number+j]['timeinterval']=i
        G.node[i*hashtag_number+j]['text']=hashtag[j]
        G.node[i*hashtag_number+j]['frequency']=matrix[i*hashtag_number+j][i*hashtag_number+j]

remove=[node for node,value in G.node.items() if value['frequency']==0]#filter zero frequency nodes and self edges
G.remove_nodes_from(remove)
number_of_node=len(G.nodes())
for i in G.nodes():
    if i in G.neighbors(i):
        G.remove_edge(i,i)

edges=G.edges()#draw the graph
weights = np.array([G[u][v]['weight'] for u,v in edges])
node_labels=nx.get_node_attributes(G,'text')
node_size=np.array(nx.get_node_attributes(G,'frequency').values())
nx.draw(G,width=2,labels=node_labels,node_size=0.1*node_size,edge_color=weights,edge_cmap=plt.cm.Greens)

plt.show()
