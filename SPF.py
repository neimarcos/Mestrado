import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

def exibegrafico(G):
  node_dist_to_color = {
      1: "tab:red",
      2: "tab:orange",
      3: "tab:olive",
      4: "tab:green",
      5: "tab:blue",
      6: "tab:purple",
      7: "tab:gray",
  }

  plt.figure(3,figsize=(12,12)) 

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
  Latitude = (list(G.nodes(data="Latitude")))
  Longitude = (list(G.nodes(data="Longitude")))


  pos={}
  poslabel={}
  for i in range(G.number_of_nodes()):
    pos[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1])]
    poslabel[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1]+1)]

  nx.draw_networkx_edges(G, pos,edge_color=cores, width=2)
  nx.draw_networkx_labels(G, poslabel,label_dic,font_size=8)
  nx.draw_networkx_nodes(G, pos, node_size=40, node_color="#210070", alpha=0.9)
  plt.show()


G = nx.read_graphml('Rnp.graphml.xml')

exibegrafico(G)
