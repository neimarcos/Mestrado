import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
from mpl_toolkits.basemap import Basemap as Basemap
import numpy as np

m = Basemap(
        projection='merc',
        llcrnrlon=-75.,
        llcrnrlat=-35.,
        urcrnrlon=-27.,
        urcrnrlat=15.,
        lat_ts=0,
        resolution='l',
        suppress_ticks=True)


rede = 'Rnp.graphml'
#rede = 'exemplo.graphml'
#rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)
node_dist_to_color = {
      1: "tab:red",
      2: "tab:orange",
      3: "tab:olive",
      4: "tab:green",
      5: "tab:blue",
      6: "tab:purple",
      7: "tab:gray",
  }

  #plt.figure(rede,figsize=(12,12)) 

Links = nx.get_edge_attributes(G,'LinkLabel').values()

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
  pos[str(i)]= m(Longitude[i][1],Latitude[i][1])
  poslabel[str(i)]= m(Longitude[i][1],Latitude[i][1]+1)

#for i in range(G.number_of_nodes()):
 #   pprint(f'Item {i} posicao {m(Longitude[i][1],Latitude[i][1])}')




nx.draw_networkx_edges(G,pos,edge_color=cores, width=2, alpha = 0.3)
nx.draw_networkx_labels(G,poslabel,label_dic,font_size=8)
nx.draw_networkx_nodes(G, pos, node_size=5, node_color="#210070", alpha=0.5)



m.drawcountries(linewidth = 0.5)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=0.2)
plt.tight_layout()
plt.savefig("./map_1.png", format = "png", dpi = 300)
plt.show()
