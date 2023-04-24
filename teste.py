import networkx as nx
import math

from pprint import pprint

# Carrega o grafo a partir de um arquivo GraphML
G = nx.read_graphml('exemplo.graphml')

# Calcula as distâncias usando o algoritmo de caminho mais curto com pesos
distancias = nx.shortest_path(G, weight='LinkSpeedRaw')

pprint(distancias)

# Encontra os vizinhos do nó 1
vizinhos = []
for no, caminhos in distancias.items():
    vizinhos = []
    pprint(f"NO : {no}")
    for vizinho, seq in caminhos.items():
        if len(seq)==2:
            vizinhos.append(vizinho)
    pprint(f"Vizinhos : {vizinhos}")
# Exibe os vizinhos


def imprime_links_e_velocidades(G):
    for u, v, atributos in G.edges(data=True):
        print(f"Link: ({u}, {v}), Velocidade: {math.ceil(atributos['LinkSpeedRaw']/1000000000)}")

# Carrega o grafo a partir de um arquivo GraphML
G = nx.read_graphml('exemplo.graphml')

# Exibe todos os links e suas velocidades
imprime_links_e_velocidades(G)