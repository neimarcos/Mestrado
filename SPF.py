import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
from collections import defaultdict

node_dist_to_color = {
    1: "tab:red",
    2: "tab:orange",
    3: "tab:olive",
    4: "tab:green",
    5: "tab:blue",
    6: "tab:purple",
    7: "tab:gray",
}

# larger figure size
plt.figure(3,figsize=(12,12)) 
# some math labels
G = nx.read_graphml('Rnp.graphml.xml')

#Link = (G.edges(data='LinkLabel'))
#for i in range(G.number_of_edges(G)):
Links = nx.get_edge_attributes(G,'LinkLabel').values()
Speed = nx.get_edge_attributes(G,'LinkSpeed').values()



cores = []

for key in Links:
  if (key == '20Gbps'):
    cores.append(node_dist_to_color[1])
  elif(key=='10Gbps'):
    cores.append(node_dist_to_color[2])
  elif(key=='3.5Gbps'):
    cores.append(node_dist_to_color[3])
  elif (key == '3Gbps'):
    cores.append(node_dist_to_color[4])
  elif (key == '1.45Gbps'):
    cores.append(node_dist_to_color[5])
  elif(key=='200Mbps'):
    cores.append(node_dist_to_color[6])
  elif(key=='20Mbps'):
    cores.append(node_dist_to_color[7])

label_dic = dict(list(G.nodes(data="label")))
#pprint(label_dic)
Latitude = (list(G.nodes(data="Latitude")))
Longitude = (list(G.nodes(data="Longitude")))

#pprint(Latitude)

pos={}
poslabel={}
for i in range(G.number_of_nodes()):
  pos[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1])]
  poslabel[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1]+1)]

nx.draw_networkx_edges(G, pos,edge_color=cores, width=2)
#Now only add labels to the nodes you require (the hubs in my case)
nx.draw_networkx_labels(G, poslabel)
nx.draw_networkx_nodes(G, pos, node_size=60, node_color="#210070", alpha=0.9)


pprint([p for p in nx.all_shortest_paths(G, 0, 10, weight='LinkSpeed', method='dijkstra')])
#print ("")
#centralidade = nx.edge_load_centrality(G)
#betweenness = nx.edge_betweenness_centrality(Gnew,  weight='capacity')

#pprint(centralidade)
#print('**********************************')
#ordenados = sorted(centralidade.items(), key=lambda x: x[1])   

#alguns = list(filter(lambda x: x[1] > 90, ordenados))


#pprint(ordenados)


plt.show()

nx.write_graphml_xml(G,"saida.xml")
