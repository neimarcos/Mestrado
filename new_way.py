import copy
from pprint import pprint
import networkx as nx
import numpy as np
from pulp import *
import time
import concurrent.futures
import matplotlib.pyplot as plt
from collections import defaultdict
import math
from collections import Counter


node_dist_to_color = {
    1: "tab:red",
    2: "tab:orange",
    3: "tab:olive",
    4: "tab:green",
    5: "tab:blue",
    6: "tab:purple",
    7: "tab:gray",
}

def ClearRoutes(spf):
    """
    Clear routes, remove reverse path. We will only use it with bidirectional measurement

    ### Parameters    
    spf (dict) : dictionary of dictionaries with path[source][target]=[list of nodes in path], return from function shortest_path from networkx library

    ### Returns
        dict : routes with only one path between two host 
    """
    ###  
    routes = []
    for source in spf:
        for target, path in spf[source].items():
            if (source != target):
                reverse_path = copy.deepcopy(path)
                reverse_path.reverse()
                if reverse_path not in routes:
                    routes.append(path)
    return(routes)


def Count_Subsegment_Occurrences(routes):
    """
    Find and count how many times each subsegment occurs.
    
    ### Parameters:
    spf (dict) : routes with only one path between two host 

    ### Returns
        dict : with the subsegments and how many times they occur in the path
    """
    
    ### Clear routes, remove reverse path 
    routes_aux = routes.copy()
    index = 0
    Path_Count_Occurrences = []
    Path_Cost = []
    for route in routes:
        count = 0
        #print(f"Route: {route}")
        for route_aux in routes_aux:
            try:
                index = route_aux.index(route[0])
                if route == route_aux[index:index+len(route)]:
                    #pprint (route_aux)
                    count += 1
            except ValueError:
                pass
        Path_Count_Occurrences.append((route, count, len(route)))
        Path_Cost.append(count)
    return (Path_Count_Occurrences,Path_Cost)

#def Nexts_Paths(pos, paths, subpaths):
#    """
#    Finds the next possible subpaths for composing the route
#
#    ### Parameters:
#        pos (int): current position on the route to start the scan
#        route(list): route to analyze possible compositions of subpaths
#        (list): possible subpaths of the route
#
#    ### Returns:
#        list:list of next possible subpaths in the composition
#    """    
#    Nexts = []
#    if paths[pos] != paths[len(paths)-1]:
#        for subpath in range(len(subpaths)):
#            if len(subpaths[subpath]) >= len(paths):
#                continue
#            igual = True
#            for id, item in enumerate(subpaths[subpath]):
#                if id <= pos:
#                    continue
#                if paths[pos+id] == item:
#                   igual=False
#            if igual:   
#                Nexts.append(subpath)
#                pprint(f"são igual - {subpath} {subpaths[subpath]}")   
#    return (Nexts)                
def Nexts_Paths(pos, paths, subpaths):
    """
    Finds the next possible subpaths for composing the route

    ### Parameters:
        pos (int): current position on the route to start the scan
        route(list): route to analyze possible compositions of subpaths
        (list): possible subpaths of the route

    ### Returns:
        list:list of next possible subpaths in the composition
    """    
    Nexts = []
    if paths[pos] != paths[len(paths)-1]:
        for subpath in range(len(subpaths)):
            if paths[pos] == subpaths[subpath][0]:
                Nexts.append(subpath)
    return (Nexts)  

def Compose_Subpaths(Path, SubPaths, pos = 0 , path_segment = []):
    """
    Finds all possible subpath compositions of a path    
    
    ### Parameters:
        path_segment (list): current segment of path
        rota (list): path to finds possible compositions
        subrotas (list): all possibles subpaths 
        pos (int): initial position to find, default 0
        
    ### Returns:
        list: List of all possible subpath compositions of a path
    """    
    positions = Nexts_Paths(pos, Path, SubPaths)
    compose = []
    if positions == []:
        compose.append(path_segment)
        return (compose)
    else:
        compose_path = []
    for pos in positions:
        compose_path = copy.deepcopy(path_segment)
        compose_path.append(SubPaths[pos])
        saltos = Compose_Subpaths( Path, SubPaths, Path.index(SubPaths[pos][(len(SubPaths[pos])-1)]), compose_path)
        compose.extend(saltos)
    return (compose)

def Find_Compose_Paths(path_count):
    """ 
    Finds all possible compositions for all paths
    
    ### Parameters:
        path_count (list): all paths/subpaths and how many times it repeats
    ### Returns:
        list: all possible possible combinations of subpaths for all paths
    """
    paths=tuple([k[0] for k in path_count])
    ComposePaths = []
    global Measurements_List
    global Probes_List
    for path in paths:
        if len(path) > 2:
            #pprint(f"Origem: {i}, destino: {k}, rota spf: {v} ")
            subpaths = []
            for i in range(len(path)):
                for j in range(i + 1, len(path) + 1):
                    subpath = (path[i: j])
                    if (len(subpath) > 1) and (len(subpath) < len(path)):
                        try:
                            subpaths.append(subpath)
                        except ValueError as e:
                            pprint("Subcaminho não existente")
            retorno = (Compose_Subpaths(path, subpaths))
            ComposePaths.append (retorno)
            # Medicao da propia sonda
            Measurements_List.append(path)
            Probes_List.append(path)
            for comp in retorno:
                Measurements_List.append(path)
                Probes_List.append(comp)
        elif len(path) > 1:
            Measurements_List.append(path)
            Probes_List.append(path)
    return (ComposePaths)

def Compose_Route_Cost(rotascompostas):
    """
    Calculate cost based composition of subpaths
    
    ### Parameters:
        rotascompostas (list): all possible possible compositon of subpaths for all paths
        
    """
    
    def encontrapeso(salto):
        if salto in paths:
            index = paths.index(salto)
        else:
            index = paths.index(list(reversed(salto)))
        return (path_cost[index])
    global Cost_List
    
    for rotascomp in rotascompostas:
        val = 0
        for composicao in rotascomp:
            if type(composicao) is str:
                val = encontrapeso(rotascomp)
                break
            else:
                val += encontrapeso(composicao)
        Cost_List.append(val)

def extractlabel(salto):
    """
    Return um string with all nodes of a path divide per one hyphen    
    
    ### Parameters:
        salto (list): string of jumps of one paths  
        
    """
    caminho_string = ''
    for no in salto:
        caminho_string += str(no) + '-'
    return caminho_string[:-1]

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


def grafico(G):
    """
    Draws a graph representing a "Graph" object (G) passed as a parameter.
    Uses the NetworkX and Matplotlib libraries to draw the graph.

    Parameters:
        G (nx.Graph): "Graph" object to be drawn.

    Returns:
        None
    """
    plt.figure("Todos os Links",figsize=(12,12)) 
    # some math labels

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
      pos[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1])]
      poslabel[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1]+1)]
    
    nx.draw_networkx_edges(G, pos,edge_color=cores, width=2)
    #nx.draw_networkx_labels(G, poslabel,label_dic,font_size=8)
    nx.draw_networkx_labels(G, poslabel)
    nx.draw_networkx_nodes(G, pos, node_size=40, node_color="#210070", alpha=0.9)
    plt.show()


def CompoeSonda(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio Compoe sonda')
       
    for idMedicao, Medicao in enumerate(Measurements_List):
        if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
            for idprobe, probe in enumerate (Probes_List[idMedicao]):
                if probe in Measurements_List:
                    id_M = Measurements_List.index(probe)
                else:
                    id_M = Measurements_List.index(probe[::-1])
                modelo_colocacao += SDMC_Dict[idMedicao] <= SDMC_Dict[id_M], "Composicao" + str(idMedicao) + "_" + str(id_M)

    End('Fim Compoe sonda')

    
    
    
    
def Sondas_Link(Start, End, G, paths, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Limita sondas por link')

    for u, v, atributos in G.edges(data=True):
        lista_caminhos = []
        for id_path, path in enumerate(paths):
            if u in path and v in path:
                lista_caminhos.append(path)
                #pprint(f"id {id_path}")
                #pprint(f"caminho  {path}")        
        lista_sondas_link = []
        for idMedicao, Medicao in enumerate(Measurements_List):
            if Measurements_List[idMedicao]==Probes_List[idMedicao] and Medicao in lista_caminhos: 
                lista_sondas_link.append(idMedicao)
        modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_link])<= math.ceil(atributos['LinkSpeedRaw']/100000000)*3, "Max_Probes_Link" + str(u) + "_" + str(v))
    End('Limita sondas por link')

def Sondas_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao):
    Start('Limita sondas por roteador')

    max_sondas = {n: (len(list(nx.all_neighbors(G, n))))for n in G.nodes}

    for id_router, router in enumerate(routers):
        lista_sondas_roteador = []
        for idMedicao, Medicao in enumerate(Measurements_List):
            if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
                if id_router == int(Measurements_List[idMedicao][0]) or id_router == int(Measurements_List[idMedicao][len(Measurements_List[idMedicao])-1]):
                    lista_sondas_roteador.append(idMedicao)       
        modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador]) <=  max_sondas.get(router)*3, "Max_Probes_Router" + str(id_router))

    End('Limita sondas por roteador')

def Iguala_Sondas(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio do Iguala sonda')
    for idMedicao, Medicao in enumerate(Measurements_List):
        if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
            for idprobe, probe in enumerate (Probes_List[idMedicao]):
                if not probe in Measurements_List:
                    probe = probe[::-1]   
                modelo_colocacao += SDMC_Dict[idMedicao] == SDMC_Dict[Measurements_List.index(probe)]

    End('Final do Iguala')

if __name__ == '__main__':
    inicio_total= time.process_time()
    rede = 'Geant2012.graphml'
    #rede = 'Rnp_2020.graphml'
    #rede = 'Rnp.graphml'
    #rede = 'exemplo.graphml'
    #rede = 'exemplo_pequeno.graphml'
    
    

    G = nx.read_graphml(rede)
    spf = nx.shortest_path(G, weight='LinkSpeedRaw')
    # Clear routes

    inicio=time.process_time()

    Start('ClearRoutes')
    paths = ClearRoutes (spf)
    End('ClearRoutes')

    Start('Count_Subsegment_Occurrences')
    # counts how many times a subsegment/subpath occurs in the spf 
    path_count, path_cost = Count_Subsegment_Occurrences(paths)
    End('Count_Subsegment_Occurrences')

    Measurements_List = []
    Probes_List = []
    Cost_List = []

    Start('Find_Compose_Paths')
    compose_paths = Find_Compose_Paths(path_count)
    End('Find_Compose_Paths')

    Start('Compose_Route_Cost')
    Compose_Route_Cost(Probes_List)
    End('Compose_Route_Cost')

    routers = G.nodes
    total_roteadores = len(routers)

    M = len(Measurements_List)
    M_list = [*range(0, M,1)]
    medicao_anterior = ''
    id_M = 0
    
    nodes_list = np.array(list(G.nodes()))
 
    Start('Inicia o modelo e cria a função de maximização')

    SDMC_Dict = LpVariable.dicts("Medicao", (M_list), 0, 1, LpInteger)   
    
    modelo_colocacao = LpProblem("Probes Placement Model", LpMinimize)

    modelo_colocacao += (lpSum([SDMC_Dict[i_M] for i_M in M_list]),"Total_Cost")
    End('Fim modelo e cria a função de maximização')
    

    Sondas_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao)

    #Sondas_Link(Start, End, G, paths, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)

    Start('Inicio Minimo uma medição por caminho')
    posicao = ''
    for id_path, path in enumerate(paths):
        Lista_Sondas = [indice for indice, sonda in enumerate(Measurements_List) if path == sonda]
        modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in Lista_Sondas]) >= 1 , "Minimo_Sondas_Medicao" + str(id_path))
            
    End('Fim Compoe sonda')


    CompoeSonda(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
    
    #Iguala_Sondas(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
    
    
    Start('Salva o Modelo')
    modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))
    End('Salva o Modelo')

    Start('Pulp Solve')
    modelo_colocacao.solve()
    End('Pulp Solve')

    with open(rede.replace(".graphml", ".result"), 'w') as f:
        for v in modelo_colocacao.variables():
            f.write(v.name + ' = ' + str(v.varValue) + '\n')
    
    print("Status:", LpStatus[modelo_colocacao.status])
    Sondas_ativas = []
    if modelo_colocacao.status == 1:
        
        pprint(modelo_colocacao)    
        for v in modelo_colocacao.variables():
            if v.varValue > 0:
                #print(v.name, "=", v.varValue)
                x = v.name.split("_")
                pprint(Probes_List[int(x[1])])
                Sondas_ativas.append (int(x[1]))
    print("Custo = ", value(modelo_colocacao.objective))
    pprint(f'Total de sondas: {len(Sondas_ativas)}')



    #pprint("###########################")
    #pprint(paths)
    count_sondas = 0 
    count_composicao = 0
      
    for Sonda in Sondas_ativas:
        if Measurements_List[int(Sonda)] == Probes_List[int(Sonda)] :
            pprint(f'Sonda - {Probes_List[int(Sonda)]}')
            count_sondas += 1
        else:
            pprint(f'Sonda - {Probes_List[int(Sonda)]}')
            count_composicao += 1
         
    pprint('Relátorio')
    pprint(f'Total de Medições por Sondas: {count_sondas}')
    pprint(f'Total de Medições através de composiçôes: {count_composicao}')

    pprint(f'Total de medições: {count_sondas+ count_composicao } = {len(paths)} ')
    
    
    pprint(f'#################################################################################')
    pprint(f'Concluiu tudo em {time.process_time() - inicio_total:.2f} segundos')
    pprint(f'#################################################################################')
    
    
    total_paths = sum(len(v) for k, v in spf.items() if k != '')

    pprint(f'Total de arestas {G.number_of_edges()}')
    pprint(f'Total de nos {G.number_of_nodes()}')
    pprint(f'Total de routas SPF {len(paths)}')
