from pulp import *
import copy
from pprint import pprint
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from collections import Counter
import random


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
                #reverse_path = copy.deepcopy(path)
                #reverse_path.reverse()
                #if reverse_path not in routes:
                routes.append(path)
                    
    #routes = []
    #for source in spf:
    #    for target, path in spf[source].items():
    #        if (source != target):
    #            reverse_path = copy.deepcopy(path)
    #            reverse_path.reverse()
    #            if reverse_path not in routes:
    #                routes.append(path)
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
def Nexts_Paths(pos, paths, subpaths, is_reversed=False):
    """
    Finds the next possible subpaths for composing the route

    ### Parameters:
        pos (int): current position on the route to start the scan
        route(list): route to analyze possible compositions of subpaths
        (list): possible subpaths of the route
        is_reversed (bool): flag indicating if the current segment is reversed

    ### Returns:
        list:list of next possible subpaths in the composition
    """    
    Nexts = []
    
    if paths[pos] != paths[len(paths)-1]:
        for subpath_index in range(len(subpaths)):
            current_subpath = subpaths[subpath_index]
            
            # Check if the subpath needs to be reversed
            if is_reversed:
                current_subpath = current_subpath[::-1]
            
            if paths[pos] == current_subpath[0]:
                Nexts.append(subpath_index)
                
    return Nexts


def Compose_Subpaths(Path, SubPaths, pos=0, path_segment=[], is_reversed=False):
    """
    Finds all possible subpath compositions of a path
    
    ### Parameters:
        path_segment (list): current segment of path
        rota (list): path to finds possible compositions
        subrotas (list): all possibles subpaths 
        pos (int): initial position to find, default 0
        is_reversed (bool): flag indicating if the current segment is reversed
        
    ### Returns:
        list: List of all possible subpath compositions of a path
    """    
    positions = Nexts_Paths(pos, Path, SubPaths, is_reversed)
    compose = []
    
    if positions == []:
        compose.append(path_segment)
        return compose
    else:
        compose_path = []
    
    for pos in positions:
        compose_path = copy.deepcopy(path_segment)
        current_subpath = SubPaths[pos]
        
        # Check if the subpath needs to be reversed
        if is_reversed:
            current_subpath = current_subpath[::-1]
        
        compose_path.append(current_subpath)
        
        # Recursively find the next subpaths
        index = Path.index(current_subpath[-1]) if not is_reversed else Path.index(current_subpath[0])
        saltos = Compose_Subpaths(Path, SubPaths, index, compose_path, is_reversed)
        compose.extend(saltos)
    
    return compose
def find_combinations(path, subpaths, current=[], start=0):
    # Caso base: se a sequência atual termina no último nó do caminho
    if current and current[-1][-1] == path[-1]:
        yield current
        return

    # Procurar subcaminhos que podem ser anexados à sequência atual
    for subpath in subpaths:
        # Verificar se o subcaminho pode ser anexado à sequência atual
        if start < len(path) and (subpath[0] == path[start] or subpath[-1] == path[start]):
            # Determine o próximo nó do caminho principal a ser alcançado
            next_node = subpath[-1] if subpath[0] == path[start] else subpath[0]
            # Encontre o índice desse nó no caminho principal
            if next_node in path:
                next_index = path.index(next_node)
                # Chamar a função recursivamente com o subcaminho adicionado à sequência atual
                new_subpath = subpath if subpath[0] == path[start] else subpath[::-1]
                yield from find_combinations(path, subpaths, current + [new_subpath], next_index + 1)


def generate_combinations(path, subpaths, current_sequence, last_node, used_indices, combinations):
    if last_node == path[-1]:  # Se o último nó do caminho foi atingido, adicione a sequência às combinações
        combinations.append(current_sequence)
        return
    
    for idx, subpath in enumerate(subpaths):
        if idx not in used_indices:
            if subpath[0] == last_node:  # Tente adicionar o subcaminho normal
                new_sequence = current_sequence + [subpath]
                new_last_node = subpath[-1]
                generate_combinations(path, subpaths, new_sequence, new_last_node, used_indices | {idx}, combinations)
            elif subpath[-1] == last_node:  # Tente adicionar o subcaminho invertido
                new_sequence = current_sequence + [subpath[::-1]]
                new_last_node = subpath[0]
                generate_combinations(path, subpaths, new_sequence, new_last_node, used_indices | {idx}, combinations)


def Find_Compose_Paths(path_count):
    """ 
    Finds all possible compositions for all paths
    
    ### Parameters:
        path_count (list): all paths/subpaths and how many times it repeats
    ### Returns:
        list: all possible possible combinations of subpaths for all paths
    """
    paths = tuple([k[0] for k in path_count])
    ComposePaths = []
    global Measurements_List
    global Probes_List
    for path in paths:
        if len(path) > 2:
            # pprint(f"Origem: {i}, destino: {k}, rota spf: {v} ")
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
            ComposePaths.append(retorno)
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
    for idMedicao, _ in enumerate(Measurements_List):
        if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
            L_CompoeSonda = []
            for probe in Probes_List[idMedicao]:
                if probe[0] not in roteadores_sem_medicao:
                    L_CompoeSonda.append(Measurements_List.index(probe))                           
                else:
                    L_CompoeSonda = []
                    break
            if L_CompoeSonda:
                for i_Medicao_Compoe in L_CompoeSonda:
                    modelo_colocacao += SDMC_Dict[idMedicao] <= SDMC_Dict[i_Medicao_Compoe], "Composicao" + str(idMedicao) + "_" + str(i_Medicao_Compoe)       
    End('Fim Compoe sonda')

def Bidirecional(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio Bidirecional')   
    for i in range(len(Measurements_List)):
        if Measurements_List[i]==Probes_List[i]:
            for j in range(i+1, len(Measurements_List)):
                if Measurements_List[j]==Probes_List[j]:
                    if Measurements_List[i] == Measurements_List[j][::-1] and j not in roteadores_sem_medicao and i not in roteadores_sem_medicao:
                        modelo_colocacao += SDMC_Dict[i] == SDMC_Dict[j], "Bidirecional" + str(i) + "_" + str(j)
    End('Fim Bidirecional')


def Iguala_Sondas(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio do Iguala sonda')
    for idMedicao, Medicao in enumerate(Measurements_List):
        if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
            for idprobe, probe in enumerate (Probes_List[idMedicao]):
                if not probe in Measurements_List:
                    probe = probe[::-1]   
                modelo_colocacao += SDMC_Dict[idMedicao] == SDMC_Dict[Measurements_List.index(probe)]

    End('Final do Iguala')    

    
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
        pprint("Max_Probes_Link" + str(u) + "_" + str(v))
        for idMedicao, Medicao in enumerate(Measurements_List):
            if Medicao in lista_caminhos and Measurements_List[idMedicao]==Probes_List[idMedicao]: 
                lista_sondas_link.append(idMedicao)
                #pprint(f"ID: {idMedicao} - medicação {Medicao}")
        modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_link])<= math.ceil(float(atributos['LinkSpeed'])*2), "Max_Probes_Link" + str(u) + "_" + str(v))
    End('Limita sondas por link')

def Sondas_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao):
    Start('Limita sondas por roteador')

    max_sondas = {n: (len(list(nx.all_neighbors(G, n))))for n in G.nodes}

    for id_router, router in enumerate(routers):
        lista_sondas_roteador = []
        for idMedicao, Medicao in enumerate(Measurements_List):
            if Measurements_List[idMedicao]==Probes_List[idMedicao]:
                if id_router == int(Measurements_List[idMedicao][0]) or id_router == int(Measurements_List[idMedicao][len(Measurements_List[idMedicao])-1]):
                    lista_sondas_roteador.append(idMedicao)       
        Sondas_router = lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador])
        if router in roteadores_sem_medicao:
            modelo_colocacao += (Sondas_router  ==  0,  "Roteador_Sem_Medicao" + str(id_router))
        else:
            modelo_colocacao += (Sondas_router  <=  max_sondas.get(router) * 2,  "Maximo_Sondas_Roteador_" + str(id_router))
        

    End('Limita sondas por roteador')
    
    
    
def Reversa(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio do Iguala sonda')
    
    for i in range(len(Measurements_List)):
        sublist = Measurements_List[i]

        for j in range(i, len(Measurements_List)):
            current_sublist = Measurements_List[j]

            if sublist == current_sublist[::-1]:
                #print("Sublist:", sublist)
                #print("Current Sublist:", current_sublist)
                modelo_colocacao += SDMC_Dict[i] == SDMC_Dict[j]

    End('Final do Iguala') 
    
    
#def Carga_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao, Carga_Media):
#    Start('Limita sondas por roteador')
#
#    for id_router, router in enumerate(routers):
#        if router not in roteadores_sem_medicao:
#            lista_sondas_roteador = []
#            for idMedicao, Medicao in enumerate(Measurements_List):
#                if Measurements_List[idMedicao]==Probes_List[idMedicao]:
#                    if id_router == int(Measurements_List[idMedicao][0]) and id_router not in roteadores_sem_medicao :
#                        lista_sondas_roteador.append(idMedicao)       
#            carga = lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador])
#
#            modelo_colocacao += (carga  <=  Carga_Media , "CargaMedia_" + str(id_router))
#            #modelo_colocacao += (carga  >=  Carga_Media , "CargaMedia2_" + str(id_router))
#
#    End('Limita sondas por roteador')



#def Carga_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao, Carga_Media):
#
#    Start('Limita sondas por roteador')
#
#    # Variáveis contínuas para representar a carga total de cada roteador
#    carga_total_roteadores = {
#        r: LpVariable(f'carga_total_roteador{r}', lowBound=0)
#        for r in routers
#    }
#
#    # Atualize a estrutura de dados Probes_List
#    Probes_List = [[str(router) for router in sublist] if isinstance(sublist, list) else str(sublist) for sublist in Probes_List]
#
#    # Restrições
#    for r in routers:
#        # Filtra as medições cujo primeiro elemento da lista Probes_List é igual ao roteador atual
#        filtered_measurements = [s for s, probes in enumerate(Probes_List) if str(probes[0]) == str(r)]
#        # Calcula a soma das cargas correspondentes às medições filtradas
#        carga = lpSum(SDMC_Dict[s] for s in filtered_measurements)
#        # Adiciona a restrição de carga total para o roteador atual
#        modelo_colocacao += carga_total_roteadores[r] == carga
#
#        # Adiciona a restrição de carga média para o roteador atual
#        modelo_colocacao += carga_total_roteadores[r] <= Carga_Media
#        modelo_colocacao += carga_total_roteadores[r] >= Carga_Media
#
#
#    # Função objetivo
#    modelo_colocacao += Carga_Media
#    
#    End('Limita sondas por roteador')
#

def Carga_Roteador_funcional(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao, Carga_Media):
    Start('Limita sondas por roteador')
    
    # Variáveis binárias para indicar se um processo é alocado em um processador
    alocado = {
        (m, r): LpVariable(f'medicao{m}_roteador{r}', cat=LpBinary)
        for m, _ in enumerate(Measurements_List) for r, _ in enumerate(routers)
    }
    
    
    # Variáveis contínuas para representar a diferença entre a carga de cada roteador e a carga média total
    diferenca_carga = {
        r: LpVariable(f'diferenca_carga_roteador{r}', lowBound=0)
        for r, _ in enumerate(routers)
    }
    
    # Variáveis contínuas para representar a carga total de cada roteador
    carga_total_roteadores = {
        r: LpVariable(f'carga_total_roteador{r}', lowBound=0)
        for r in routers
    }
    carga_media_total = lpSum(carga_total_roteadores.values()) / len(routers)


    for id_router, router in enumerate(routers):
        if router not in roteadores_sem_medicao:
            lista_sondas_roteador = []
            for idMedicao, _ in enumerate(Measurements_List):
                if Measurements_List[idMedicao]==Probes_List[idMedicao]:
                    if id_router == int(Measurements_List[idMedicao][0]) and id_router not in roteadores_sem_medicao :
                        lista_sondas_roteador.append(idMedicao)
                        
            # Variáveis auxiliares
            produto_variaveis = {
                (id_lista, id_router): LpVariable(f'produto_{id_lista}_{id_router}', lowBound=0)
                for id_lista in lista_sondas_roteador
            }

            # Restrições para relacionar as variáveis auxiliares às variáveis existentes
            for id_lista, id_router in produto_variaveis:
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] <= SDMC_Dict[id_lista]
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] <= alocado[(id_lista, id_router)]
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] >= SDMC_Dict[id_lista] + alocado[(id_lista, id_router)] - 1

            # Criação da expressão de carga
            carga = lpSum(produto_variaveis.values())   
            
            modelo_colocacao += carga  <=  carga_media_total + diferenca_carga[id_router] , "CargaMedia_" + str(id_router)
            modelo_colocacao += carga  >=  carga_media_total - diferenca_carga[id_router] , "CargaMediaM_" + str(id_router)
    End('Limita sondas por roteador')

def Carga_Roteador(Start, End, G, Measurements_List, Probes_List, routers, SDMC_Dict, modelo_colocacao, Carga_Media):
    Start('Limita sondas por roteador')
    
    # Variáveis binárias para indicar se uma medição é alocada em um roteador
    alocado = {
        (m, r): LpVariable(f'medicao{m}_roteador{r}', cat=LpBinary)
        for m, _ in enumerate(Measurements_List) for r in routers
    }
    
    # Variáveis contínuas para representar a diferença entre a carga de cada roteador e a carga média total
    diferenca_carga = {
        r: LpVariable(f'diferenca_carga_roteador{r}', lowBound=0)
        for r in routers
    }
    
    # Variáveis contínuas para representar a carga total de cada roteador
    carga_total_roteadores = {
        r: LpVariable(f'carga_total_roteador{r}', lowBound=0)
        for r in routers
    }
    
    carga_media_total = lpSum(carga_total_roteadores.values()) / len(routers)

    # Restrições
    for id_router, router in enumerate(routers):
        if router not in roteadores_sem_medicao:
            lista_sondas_roteador = [idMedicao for idMedicao, _ in enumerate(Measurements_List) if
                                     Measurements_List[idMedicao] == Probes_List[idMedicao] and
                                     id_router == int(Measurements_List[idMedicao][0]) and
                                     id_router not in roteadores_sem_medicao]

            # Variáveis auxiliares
            produto_variaveis = {
                (id_lista, id_router): LpVariable(f'produto_{id_lista}_{id_router}', lowBound=0)
                for id_lista in lista_sondas_roteador
            }

            # Restrições para relacionar as variáveis auxiliares às variáveis existentes
            for id_lista, id_router in produto_variaveis:
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] <= SDMC_Dict[id_lista]
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] <= alocado[(id_lista, id_router)]
                modelo_colocacao += produto_variaveis[(id_lista, id_router)] >= SDMC_Dict[id_lista] + alocado[(id_lista, id_router)] - 1

            # Criação da expressão de carga
            carga = lpSum(produto_variaveis.values())

            # Restrição de carga máxima por roteador
            modelo_colocacao += carga <= Carga_Media

            # Função objetivo para minimizar a quantidade total de sondas alocadas
            modelo_colocacao += lpSum(alocado.values())

            # Restrição de carga média
            modelo_colocacao += carga_total_roteadores[id_router] == carga
            modelo_colocacao += carga_total_roteadores[id_router] <= Carga_Media + diferenca_carga[id_router]
            modelo_colocacao += carga_total_roteadores[id_router] >= Carga_Media - diferenca_carga[id_router]

    End('Limita sondas por roteador')




def MinimoMedicaoCaminho(Start, End, paths, Measurements_List, SDMC_Dict):
    Start('Inicio Minimo de uma medição por caminho')
    global modelo_colocacao
    medicao_processada = set() 
    for indice, sonda in enumerate(Measurements_List):
        if indice not in medicao_processada:
            Lista_Medicao_Path = [i for i, item in enumerate(Measurements_List) if item == sonda]
            Lista_Medicao_Path_Reverso =  [i for i, item in enumerate(Measurements_List) if item == Measurements_List[indice][::-1]]
            Lista_Medicoes_Iguais = Lista_Medicao_Path + Lista_Medicao_Path_Reverso
            modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in Lista_Medicoes_Iguais]) >= 1 , "Minimo_Sondas_Medicao_" + str(Lista_Medicoes_Iguais[0]) + 'ou'+ str(Lista_Medicoes_Iguais[-1]))
            for medicao in Lista_Medicoes_Iguais:
                medicao_processada.add(medicao)
                
    End('Fim Minimo de uma medição por caminho')
""" 
        
        if sonda_anterior==sonda:
            Lista_Medicao_Path.append(indice)
            medicao_processada.add(indice)
            indice_reverso = Measurements_List.index()
            Lista_Medicao_Path.append(indice_reverso)
            medicao_processada.add(indice_reverso)
        elif Lista_Medicao_Path:
            
            Lista_Medicao_Path = []
            if tuple(sonda) not in medicao_processada:
                Lista_Medicao_Path.append(indice)
                medicao_processada.add(indice)
                indice_reverso = Measurements_List.index(Measurements_List[indice][::-1])
                Lista_Medicao_Path.append(indice_reverso)
                medicao_processada.add(indice_reverso)
        sonda_anterior=sonda
 """    
    


                
                

if __name__ == '__main__':
    inicio_total= time.process_time()
    #rede = 'Geant2012.graphml'
    #rede = 'Rnp_2020.graphml'
    #rede = 'Rnp.graphml'
    #rede = 'exemplo.graphml'
    #rede = 'exemplo_pequeno.graphml'
    #G = nx.read_graphml(rede)
    #spf = nx.shortest_path(G, weight='LinkSpeedRaw')
    
    ## Criar um grafo não direcionado
    G = nx.Graph()
    G.add_nodes_from(['1', '2', '3', '4'])
    G.add_edges_from([('1', '2'), ('2', '3'), ('2', '4')])
    spf = dict(nx.all_pairs_shortest_path(G))
    rede = 'manual.graphml'

    Start('ClearRoutes')
    paths = ClearRoutes (spf)
    #paths = copy.deepcopy(spf)
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

    #pprint(Probes_List)

    M = len(Measurements_List)
    M_list = [*range(0, M,1)]
    medicao_anterior = ''
    id_M = 0
    
    Router_list = list(G.nodes())
 
 
    max_cost = max(Cost_List)
    #pprint(f'{Cost_List}')
    # Converta a lista em um array NumPy
    Cost_Array = np.array(Cost_List)

    # Calcule o valor mínimo e o valor máximo do array
    min_value = np.min(Cost_Array)
    max_value = np.max(Cost_Array)
    avg_cost = np.average(Cost_Array)

    # Normalize o array subtraindo o valor mínimo e dividindo pelo range
    Normalized_Cost_Array = (Cost_Array - min_value) / (max_value - min_value)

    # Converta o array NumPy de volta em uma lista, se necessário
    Cost_List = Normalized_Cost_Array.tolist()
    #pprint(f'{Cost_List}')
    roteadores_sem_medicao = random.sample(routers,int(len(routers) *0 ))

    modelo_colocacao = LpProblem("Probes Placement Model", LpMinimize)

    Start('Inicia o modelo e cria a função LpMinimize')

    SDMC_Dict = {s: LpVariable(f"Medicao_{s}", 0, 1, LpContinuous) for s in M_list}
    # Variáveis
    total_routers = len(routers) 
    total_medicoes = len(Measurements_List)  

    # Variáveis binárias para indicar se um medicao é alocado em um roteador
    alocado = {}
    medicao_atual = 0 
        
    for id_router in Router_list:
        for id_medicao in range(medicao_atual, len(Measurements_List)):
            SDMC_Dict[id_medicao] = random.randint(0, 1)
            if Measurements_List[id_medicao][0] == id_router:
                if Measurements_List[int(id_medicao)] ==  Probes_List[id_medicao]:
                    alocado[(int(id_router),id_medicao)] = LpVariable(f'Roteador{int(id_router)}_medicao{id_medicao}', cat=LpBinary)
                    alocado[(int(id_router),id_medicao)] = random.randint(0, 1)
            else:
                medicao_atual=id_medicao
                break

    # Variáveis contínuas para representar a diferença entre a carga de cada roteador e a carga média total
    diferenca_carga = {
        id_router: LpVariable(f'diferenca_carga_roteador{id_router}', lowBound=0)
        for id_router in Router_list
    }

    # Função objetivo
    carga_total_processadores = {
        key: lpSum(SDMC_Dict[key[1]] * alocado[(key[0], key[1])])
        for key in alocado
    }
        
    carga_media_total = lpSum(carga_total_processadores.values()) / len(routers) 

    modelo_colocacao += lpSum(diferenca_carga[id_router] for id_router in Router_list)

    # Restrições
    for key in alocado:
        modelo_colocacao += lpSum(SDMC_Dict[key[1]] * alocado[(key[0], key[1])] ) <= carga_media_total + diferenca_carga[str(key[0])]
        modelo_colocacao += lpSum(SDMC_Dict[key[1]] * alocado[(key[0], key[1])] ) >= carga_media_total - diferenca_carga[str(key[0])]
    
    #modelo_colocacao += (lpSum([SDMC_Dict[i_M] for i_M in M_list if Probes_List[i_M]==Measurements_List[i_M]]),"Total_Cost")   
   
    MinimoMedicaoCaminho(Start, End, paths, Measurements_List, SDMC_Dict)
    #Reversa(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
   # CompoeSonda(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
    #Bidirecional(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
    #Iguala_Sondas(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)
    
    # Resolva o problema
    #solver = GUROBI_CMD()
    
    solver = CPLEX_CMD()
    modelo_colocacao.solve(solver)
    #modelo_colocacao.solve()
    Start('Salva o Modelo')
    modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))
    End('Salva o Modelo')
    with open(rede.replace(".graphml", ".result_CBC"), 'w') as f:
        for v in modelo_colocacao.variables():
            f.write(v.name + ' = ' + str(v.varValue) + '\n')

    pprint(alocado)

    pprint(SDMC_Dict)
    for numsonda, sonda in SDMC_Dict.items():
        if sonda == 1:
            pprint(f'{numsonda} - {Measurements_List[numsonda]}')
    # Verifique o status da solução
    status = LpStatus[modelo_colocacao.status]
#    print("Status da solução:", status)
#    Sondas_ativas = []
#    if modelo_colocacao.status == 1:
#        
#        #pprint(modelo_colocacao)    
#        for v in modelo_colocacao.variables():
#            x = v.name.split("_")
#            if x[0] == "Medicao" and v.varValue > 0:
#                print(v.name, "=", v.varValue)
#                print(Probes_List[int(x[1])])
#                Sondas_ativas.append (int(x[1]))
#    print("Custo = ", value(modelo_colocacao.objective))
#    pprint(f'Total de sondas: {len(Sondas_ativas)}')
#
#
#
#    #pprint("###########################")
#    #pprint(paths)
#    #pprint(len(paths))
#    count_sondas = 0 
#    count_composicao = 0
#    sondas_por_roteador = [0 for _ in range(len(routers))]
#    medicao_processada = set()   
#      
#    for Sonda in Sondas_ativas:
#        if Measurements_List[int(Sonda)] == Probes_List[int(Sonda)] :
#            pprint(f'Sonda - {Measurements_List[int(Sonda)]}')
#            count_sondas += 1
#            sondas_por_roteador[int(Probes_List[int(Sonda)][0])-1] +=1
#            medicao_processada.add(tuple(Measurements_List[int(Sonda)]))
#        elif tuple(Measurements_List[int(Sonda)]) and tuple(Measurements_List[int(Sonda)][::-1]) not in medicao_processada:
#            pprint(f'Composição - {Measurements_List.index(Measurements_List[int(Sonda)][::-1])} - {Measurements_List[int(Sonda)]}')
#            medicao_processada.add(tuple(Measurements_List[int(Sonda)]))
#            medicao_processada.add(tuple(Measurements_List[int(Sonda)][::-1]))
#            count_composicao += 1
#   
#         
#    pprint('Relátorio')
#    pprint(f'Total de Medições por Sondas: {count_sondas}')
#    pprint(f'Total de Medições através de composiçôes: {count_composicao}')
#    
#    pprint(f'Total de medições: {count_sondas+ count_composicao } = {len(paths)} ')
#    
#    pprint(f'Total de Medições/Composições de Sondas possiveis: {len(Measurements_List)}')
#    
#    
#    
#    pprint(f'#################################################################################')
#    pprint(f'Concluiu tudo em {time.process_time() - inicio_total:.2f} segundos')
#    pprint(f'#################################################################################')
#    
#    
#    total_paths = sum(len(v) for k, v in spf.items() if k != '')
#
#    pprint(f'Total de arestas {G.number_of_edges()}')
#    pprint(f'Total de nos {G.number_of_nodes()}')
#    pprint(f'Total de routas SPF {len(paths)}')
#
#    #pprint(f'Total de : {i}')
#    
#    pprint(f'Sondas por roteadores: {sondas_por_roteador}')
#    pprint(f'Routers sem medicão: {roteadores_sem_medicao}')
#   
#  
    #pprint(medicao_processada)
    #pprint(tuple(paths))
    
    
    