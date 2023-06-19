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
    Path_List = []
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
        Path_List.append(route)
        Path_Cost.append(count)
    return (Path_List,Path_Cost)

              
def Nexts_Paths(pos, paths, subpaths):
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
    positions = Nexts_Paths(pos, Path, SubPaths)
    compose = []
    
    if positions == []:
        compose.append(path_segment)
        return compose
    else:
        compose_path = []
    
    for pos in positions:
        compose_path = copy.deepcopy(path_segment)
        current_subpath = SubPaths[pos]
        compose_path.append(current_subpath)
        # Recursively find the next subpaths
        index = Path.index(current_subpath[-1]) if not is_reversed else Path.index(current_subpath[0])
        saltos = Compose_Subpaths(Path, SubPaths, index, compose_path, is_reversed)
        compose.extend(saltos)
    
    return compose

def Find_Compose_Paths(paths):
    """ 
    Finds all possible compositions for all paths
    
    ### Parameters:
        path_count (list): all paths/subpaths and how many times it repeats
    ### Returns:
        list: all possible possible combinations of subpaths for all paths
    """
    
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


def MinimoMedicaoCaminho(Start, End, paths, Measurements_List, SDMC_Dict):
    Start('Inicio Minimo de uma medição por caminho')
    global modelo_colocacao
    medicao_processada = set() 
    for indice, sonda in enumerate(Measurements_List):
        if indice not in medicao_processada:
            Lista_Medicao_Path = [i for i, item in enumerate(Measurements_List) if item == sonda]
            Lista_Medicao_Path_Reverso =  [i for i, item in enumerate(Measurements_List) if item == Measurements_List[indice][::-1]]
            Lista_Medicoes_Iguais = Lista_Medicao_Path + Lista_Medicao_Path_Reverso
            if Lista_Medicoes_Iguais:
                modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in Lista_Medicoes_Iguais]) >= 1 , "Minimo_Sondas_Medicao_" + str(Lista_Medicoes_Iguais[0]) + 'ou'+ str(Lista_Medicoes_Iguais[-1]))
            for medicao in Lista_Medicoes_Iguais:
                medicao_processada.add(medicao)        
    End('Fim Minimo de uma medição por caminho')

def CompoeSonda(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao):
    Start('Inicio Compoe sonda')
    caminhos_processados = set()   
    paths_tuples = [tuple(sublist) for sublist in paths]
    for idMedicao, Medicao in enumerate(Measurements_List):
        if Measurements_List[idMedicao]!=Probes_List[idMedicao]:
            reverse_path = tuple(Medicao[::-1])
            if tuple(Medicao) in caminhos_processados or ((reverse_path in caminhos_processados) and (reverse_path in paths_tuples) ):
                continue
            caminhos_processados.add(tuple(Medicao))
            L_CompoeSonda = []
            for idprobe, probe in enumerate (Probes_List[idMedicao]):
                if probe[0] not in roteadores_sem_medicao:
                    L_CompoeSonda.append(Measurements_List.index(probe))                           
                elif probe[-1] not in roteadores_sem_medicao and probe[::-1] in paths:
                    L_CompoeSonda.append(Measurements_List.index(probe[::-1]))
                else:
                    L_CompoeSonda = []
                    break
            if L_CompoeSonda:
                for i_Medicao_Compoe in L_CompoeSonda:
                    modelo_colocacao += SDMC_Dict[idMedicao] <= SDMC_Dict[i_Medicao_Compoe], "Composicao" + str(idMedicao) + "_" + str(i_Medicao_Compoe)       
    End('Fim Minimo de uma medição por caminho')
               
                

if __name__ == '__main__':
    inicio_total= time.process_time()
    #rede = 'Geant2012.graphml'
    #rede = 'Rnp_2020.graphml'
    rede = 'Rnp.graphml'
    #rede = 'exemplo.graphml'
    #rede = 'exemplo_pequeno.graphml'
    G = nx.read_graphml(rede)
    spf = nx.shortest_path(G, weight='LinkSpeedRaw')
    
    # Converter o resultado para um dicionário serializável
    #spf_dict = dict(spf)

    # Salvar o dicionário em um arquivo JSON
    #with open(rede.replace(".graphml", "spf.json"), 'w') as file:
    #    json.dump(spf_dict, file, indent=4)
    
    #with open(rede.replace(".graphml", ".spf"), 'w') as f:
    #    f.write(str(spf)+'\n')
    
    ## Criar um grafo não direcionado
    #G = nx.Graph()
    #G.add_nodes_from(['1', '2', '3', '4'])
    #G.add_edges_from([('1', '2'), ('2', '3'), ('2', '4')])
    #spf = dict(nx.all_pairs_shortest_path(G))
    #rede = 'manual.graphml'

    Start('ClearRoutes')
    paths = ClearRoutes (spf)
    End('ClearRoutes')
    
    
    Start('Count_Subsegment_Occurrences')
    # counts how many times a subsegment/subpath occurs in the spf 
    paths_list, paths_cost = Count_Subsegment_Occurrences(paths)
    End('Count_Subsegment_Occurrences')

    Measurements_List = []
    Probes_List = []
    Cost_List = []

    Start('Find_Compose_Paths')
    compose_paths = Find_Compose_Paths(paths_list)
    End('Find_Compose_Paths')

    routers = G.nodes

    M = len(Measurements_List)
    M_list = [*range(0, M,1)]
    medicao_anterior = ''
    id_M = 0
    
    Router_list = list(G.nodes())
    roteadores_sem_medicao = random.sample(routers,int(len(routers) *0.1 ))
    #roteadores_sem_medicao = ['3','4']
    #roteadores_sem_medicao = []
    modelo_colocacao = LpProblem("Probes Placement Model", LpMinimize)
    SDMC_Dict = {s: LpVariable(f"Medicao_{s}", 0, 1, LpInteger) for s in M_list}
    diferenca_carga = {id_router: LpVariable(f"diferenca_carga_roteador{id_router}", 0, 1, LpInteger)for id_router in Router_list if id_router not in roteadores_sem_medicao}
    
    
    #modelo_colocacao += (lpSum([SDMC_Dict[i_M] for i_M in M_list if Probes_List[i_M]==Measurements_List[i_M]]),"Total_Cost")
    #modelo_colocacao += lpSum(diferenca_carga[id_router] for id_router in Router_list)
    modelo_colocacao += (lpSum([SDMC_Dict[i_M] for i_M in M_list if Probes_List[i_M]==Measurements_List[i_M] if Measurements_List[i_M][0] not in roteadores_sem_medicao])
                         + lpSum([diferenca_carga[id_router] for id_router in Router_list if id_router not in roteadores_sem_medicao]), "Total_Cost_and_Difference")
   
    MinimoMedicaoCaminho(Start, End, paths, Measurements_List, SDMC_Dict)
    CompoeSonda(Start, End, Measurements_List, Probes_List, SDMC_Dict, modelo_colocacao)


    carga_media_cima = (math.ceil(G.number_of_edges() / G.number_of_nodes() )) 
    carga_media_baixo = (math.floor(G.number_of_edges() / G.number_of_nodes() )) 

    for router in routers:
        lista_sondas_roteador = []
        for idMedicao, Medicao in enumerate(Measurements_List):
            if Measurements_List[idMedicao]==Probes_List[idMedicao]:
                if router == Measurements_List[idMedicao][0]: 
                    lista_sondas_roteador.append(idMedicao)       
        if router not in roteadores_sem_medicao: 
            modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador]) <= carga_media_cima + diferenca_carga[router] , "Carga_Menor_Roteador"+ router)
            modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador]) >= carga_media_baixo - diferenca_carga[router] , "Carga_Maior_Roteador"+ router)
        else: 
            modelo_colocacao += (lpSum([SDMC_Dict[id_lista] for id_lista in lista_sondas_roteador]) == 0 , "Roteador_Sem_Medicao"+ router)
    
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

    with open(rede.replace(".graphml", ".Measurements_List"), 'w') as f:
        for linha in Measurements_List:
            f.write(str(linha)+'\n')


    # Verifique o status da solução
    status = LpStatus[modelo_colocacao.status]
    print("Status da solução:", status)
    Sondas_ativas = []
    if modelo_colocacao.status == 1:
        
        #pprint(modelo_colocacao)    
        for v in modelo_colocacao.variables():
            x = v.name.split("_")
            if x[0] == "Medicao" and v.varValue > 0:
                #print(v.name, "=", v.varValue)
                #print(Probes_List[int(x[1])])
                Sondas_ativas.append (int(x[1]))
    print("Custo = ", value(modelo_colocacao.objective))
    pprint(f'Total de sondas: {len(Sondas_ativas)}')



    #pprint("###########################")
    count_sondas = 0 
    count_composicao = 0
    sondas_por_roteador = [0 for _ in range(len(routers))]
    medicao_processada = set()   
      
    for Sonda in Sondas_ativas:
        if Measurements_List[int(Sonda)] == Probes_List[int(Sonda)] :
            pprint(f'Sonda - {Measurements_List[int(Sonda)]}')
            #pprint(f'{Measurements_List[int(Sonda)]}')
            count_sondas += 1
            sondas_por_roteador[int(Probes_List[int(Sonda)][0])-1] +=1
            medicao_processada.add(tuple(Measurements_List[int(Sonda)]))
        elif tuple(Measurements_List[int(Sonda)]) not in medicao_processada: 
            pprint(f'Composição - {Measurements_List.index(Measurements_List[int(Sonda)])}|{Measurements_List[int(Sonda)]} = {Probes_List[int(Sonda)]}  ')
            #pprint(f'{Measurements_List[int(Sonda)]}')
            medicao_processada.add(tuple(Measurements_List[int(Sonda)]))
            if Measurements_List[int(Sonda)][::-1] in Measurements_List: 
                medicao_processada.add(tuple(Measurements_List[int(Sonda)][::-1]))
            count_composicao += 1
    
 

    #pprint(paths_tuples)
    #pprint(f'{paths_tuples-medicao_processada}')
    
    #diferenca = paths_tuples.difference(medicao_processada)
    #pprint(f'Diferença: {diferenca}')
         
    pprint('Relátorio')
    pprint(f'Total de Medições por Sondas: {count_sondas}')
    pprint(f'Total de Medições através de composiçôes: {count_composicao}')
    
    pprint(f'Total de medições: {count_sondas+ count_composicao }= {len(medicao_processada)} = {len(paths)} ')
    
    pprint(f'Total de Medições/Composições de Sondas possiveis: {len(Measurements_List)}')
    pprint(f'Total de Medições realizadas: {len(Sondas_ativas)}')
    
    pprint('Medições não realizadas')
    todas = True
    for sublist in paths:
        if (tuple(sublist) not in medicao_processada) and (tuple(sublist[::-1]) not in medicao_processada):
            pprint(sublist)
            todas = False
    if todas:
        pprint('Todas as medições foram realizadas')
        
    pprint(f'#################################################################################')
    pprint(f'Concluiu tudo em {time.process_time() - inicio_total:.2f} segundos')
    pprint(f'#################################################################################')
    
    #pprint(paths_list)
    
    total_paths = sum(len(v) for k, v in spf.items() if k != '')

    pprint(f'Total de arestas {G.number_of_edges()}')
    pprint(f'Total de nos {G.number_of_nodes()}')
    pprint(f'Total de routas SPF {len(paths)}')

    #pprint(f'Total de : {i}')
    
    pprint(f'Sondas por roteadores: {sondas_por_roteador}')
    pprint(f'Routers sem medicão: {roteadores_sem_medicao}')