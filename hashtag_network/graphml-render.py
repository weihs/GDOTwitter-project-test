import networkx as nx
import numpy as np

origin_file_name='data/graphml/GDOtest1.graphml'
result_file_name='data/graphml/GNIP_top20_50days_rendered.graphml'

with open(origin_file_name,mode='r') as f:
    G=nx.read_graphml(f,int)

for u,v in G.edges():
    if G.edge[u][v]['type']==1:
        G.edge[u][v]['r']=G.node[u]['r']
        G.edge[u][v]['g']=G.node[u]['g']
        G.edge[u][v]['b']=G.node[u]['b']


nx.write_graphml(G,result_file_name)
