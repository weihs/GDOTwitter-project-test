from pymongo import MongoClient
import gridfs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from hashtag import * #the hashtags we want to retrive
hashtag_number=21
timeinterval_number=10

array_filename='combine_matrix.npy'#build the graph from adjacency matrix
matrix=np.load(array_filename)
G=nx.from_numpy_matrix(matrix)


for i in range(timeinterval_number):#add the node attributes: number,timeinterval,hashtag text and frequency
    for j in range(hashtag_number):
        G.node[i*hashtag_number+j]['no']=j
        G.node[i*hashtag_number+j]['timeinterval']=i
        G.node[i*hashtag_number+j]['text']=(hashtag[j])
        G.node[i*hashtag_number+j]['frequency']=matrix[i*hashtag_number+j][i*hashtag_number+j]

remove=[node for node,value in G.node.items() if value['frequency']==0]#filter zero frequency nodes and self edges
G.remove_nodes_from(remove)
number_of_node=len(G.nodes())
for i in G.nodes():
    if i in G.neighbors(i):
        G.remove_edge(i,i)

db=MongoClient().test#save graph into database
fs=gridfs.GridFS(db)
edges=G.edges()
nodes=G.nodes()
for u,v in edges:
    G[u][v]['weight']=int(G[u][v]['weight'])
for u in nodes:
    G.node[u]['frequency']=int(G.node[u]['frequency'])
with fs.new_file(filename='second', content_type="text/xml") as f:
    nx.write_graphml(G,f)

#draw the graph
weights = np.array([G[u][v]['weight'] for u,v in edges])
node_labels=nx.get_node_attributes(G,'text')
node_size=np.array(list(nx.get_node_attributes(G,'frequency').values()))
nx.draw(G,width=2,labels=node_labels,node_size=0.05*node_size,edge_color=10*weights,edge_cmap=plt.cm.Blues)
plt.show()
