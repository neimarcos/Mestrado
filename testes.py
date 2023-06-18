import networkx as nx
from pprint import pprint
import pandas as pd
import time


import copy

def Start(NameFunction):
    """
    Start calculating the time required for a given function    
    
    ### Parameters:
        NameFunction (String): name of the function to be executed to calculate the time  
        
    """
    global inicio 
    inicio= time.process_time()
    pprint(f'Iniciando a função {NameFunction}')
    return(inicio)

def End(NameFunction):
    """
    Finishes calculating the time required for a given function    
    
    ### Parameters:
        NameFunction (String): name of the function to be executed to calculate the time  
        
    """
    pprint(f'Concluiu a função {NameFunction}, em {time.process_time() - inicio:.2f} segundos')
    pprint(f'#################################################################################')



def Count_Subsegment_Occurrences(spf):
    """
    Find and count how many times each subsegment occurs.
    
    ### Parameters:
    spf (dict) : routes with only one path between two hosts

    ### Returns:
    dict : with the subsegments and how many times they occur in the path
    """
    routes = []
    for start_node in spf:
        for end_node in spf[start_node]:
            path = spf[start_node][end_node]
            routes.append(path)
    
    routes_aux = routes.copy()
    index = 0
    Path_Count_Occurrences = []
    for route in routes:
        if len(route)>1:
            count = 0
            for route_aux in routes_aux:
                if len(route_aux)>1:
                    try:
                        index = route_aux.index(route[0])
                        if route == route_aux[index:index+len(route)]:
                            count += 1
                    except ValueError:
                     pass
            Path_Count_Occurrences.append((route, count, len(route)))
    return Path_Count_Occurrences

import pandas as pd

def Count_Subsegment_Occurrences_DF(df):
    # Conjunto para armazenar as sequências únicas
    sequences_set = set()

    # Percorre todas as células do DataFrame
    for row in df.index:
        for col in df.columns:
            if len(df.loc[row, col])>1:
                cell_value = df.loc[row, col]
                # Percorre os elementos da célula
                sequences_set.add(tuple(cell_value))
    # Dicionário para armazenar as contagens das sequências
    sequence_counts = {}

    # Percorre as sequências únicas encontradas
    for sequence in sequences_set:
        count = 0
        # Percorre todas as células do DataFrame novamente para contar as ocorrências
        for row in df.index:
            for col in df.columns:
                # Verifica se a célula atual contém uma lista
                if len(df.loc[row, col])>1:
                    cell_value = df.loc[row, col]
                    # Verifica se a sequência está contida no valor da célula
                    if any(sequence == tuple(cell_value[i:i+len(sequence)]) for i in range(len(cell_value) - len(sequence) + 1)):
                        count += 1
        # Adiciona a contagem da sequência ao dicionário
        sequence_counts[sequence] = count
    return(sequence_counts)

## Criar um grafo não direcionado
G = nx.Graph()
#
## Adicionar nós ao grafo
G.add_nodes_from([1, 2, 3, 4])
#
## Adicionar arestas ao grafo (pares de nós)
G.add_edges_from([(1, 2), (2, 3), (2, 4)])
#
## Calcular o caminho mais curto para todos os pares de nós


#rede = 'exemplo.graphml'
rede = 'RNP.graphml'
    

G = nx.read_graphml(rede)
spf = nx.shortest_path(G, weight='LinkSpeedRaw')

spf = dict(nx.all_pairs_shortest_path(G))
#
df = pd.DataFrame.from_dict(spf, orient='index')

Start('Inicia o Pandas')
sequence_counts= Count_Subsegment_Occurrences_DF(df)
End('Final o Pandas')
#pprint(sequence_counts)

# Imprime o resultado
#for sequence, count in sequence_counts.items():
#    print(f"A sequência {sequence} ocorre {count} vezes no DataFrame.")



  
Start('Inicia o List')
path=Count_Subsegment_Occurrences(spf)
End('Final o List')          

#pprint(path)


#shortest_path_df = pd.DataFrame.from_dict(spf, orient='index')
#path_df = Count_Subsegment_Occurrences_DF(shortest_path_df)
#pprint(shortest_path_df)
#pprint(path_df)

#Measurements_List = []
#Probes_List = []
#Cost_List = []

#rede = 'exemplo.graphml'
#rede = 'exemplo_pequeno.graphml'
    

#G = nx.read_graphml(rede)
#spf = nx.shortest_path(G, weight='LinkSpeedRaw')

#path=(Count_Subsegment_Occurrences(spf))

#pprint(Find_Compose_Paths(path))
#pprint(Measurements_List)
#pprint(Probes_List)


    
#Compose_Route_Cost(Probes_List)


#pprint(Cost_List)