import copy
from pprint import pprint
import networkx as nx
import numpy as np
from pulp import *
import time
import math


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
    return (routes)


def Count_Subsegment_Occurrences(routes):
    """
    Find and count how many times each subsegment occurs.

    ### Parameters:
    spf (dict) : routes with only one path between two host

    ### Returns
        dict : with the subsegments and how many times they occur in the path
    """

    # Clear routes, remove reverse path
    routes_aux = routes.copy()
    index = 0
    Path_Occurrences = []
    Path_Cost = []
    for route in routes:
        count = 0
        # print(f"Route: {route}")
        for route_aux in routes_aux:
            try:
                index = route_aux.index(route[0])
                if route == route_aux[index:index+len(route)]:
                    # pprint (route_aux)
                    count += 1
            except ValueError:
                pass
        Path_Occurrences.append((route, count, len(route)))
        Path_Cost.append(count)
    return (Path_Occurrences, Path_Cost)


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


def Compose_Subpaths(Path, SubPaths, pos=0, path_segment=[]):
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
        saltos = Compose_Subpaths(Path, SubPaths, Path.index(
            SubPaths[pos][(len(SubPaths[pos])-1)]), compose_path)
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
    inicio = time.process_time()
    pprint(f'Iniciando a função {NameFunction}')
    return (inicio)


def End(NameFunction):
    """
    Finishes calculating the time required for a given function

    ### Parameters:
        NameFunction (String): name of the function to be executed to calculate the time

    """
    pprint(
        f'Concluiu a função {NameFunction}, em {time.process_time() - inicio:.2f} segundos')
    pprint(f'#################################################################################')

inicio_total= time.process_time()

#rede = 'Geant2012.graphml'
#rede = 'Rnp.graphml'
rede = 'exemplo.graphml'
#rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)
spf = nx.shortest_path(G, weight='LinkSpeedRaw')

# Clear routes

inicio = time.process_time()

Start('ClearRoutes')
paths = ClearRoutes(spf)
End('ClearRoutes')

Start('Count_Subsegment_Occurrences')
# counts how many times a subsegment/subpath occurs in the spf
path_Occurrences, path_cost = Count_Subsegment_Occurrences(paths)
End('Count_Subsegment_Occurrences')

Measurements_List = []
Probes_List = []
Cost_List = []

Start('Find_Compose_Paths')
compose_paths = Find_Compose_Paths(path_Occurrences)
End('Find_Compose_Paths')

Start('Compose_Route_Cost')
Compose_Route_Cost(Probes_List)
End('Compose_Route_Cost')

# pprint(Probes_List)

max_len_probe = 0
max_probes_measurement = 0
for id_probe, probe in enumerate(Probes_List):
    if Measurements_List[id_probe] != probe:
        if len(probe) > max_len_probe:
            max_len_probe = len(probe)

# pprint(max_len_probe)

lista_medicao, num_sonda_medicao = np.unique(
    Measurements_List, return_counts=True)


routers = G.nodes


total_roteadores = len(routers)

# Router Source
RS = total_roteadores
# Router Destination
RD = total_roteadores
# Medições de um roteador para todos os outros
M = max(num_sonda_medicao)
# Possiveis composições das medições de um roteador para todos os outos
C = max_len_probe

SDMC_Cost = np.zeros((RS, RD, M, C))
SDMC_Id_Medicao = np.zeros((RS, RD, M, C))
SDMC_Id_Medicao[:][:][:][:] = -1
nodes_list = np.array(list(G.nodes()))

pprint(SDMC_Id_Medicao.shape)
Start('Matriz de Custos')


medicao_anterior = ''
id_M = 0
for idMedicao, Medicao in enumerate(Measurements_List):
    # if (Probes_List[idMedicao] == Measurements_List [idMedicao]):
    if str(medicao_anterior) != str(Medicao):
        id_RS = np.where(nodes_list == Measurements_List[idMedicao][0])
        id_RD = np.where(nodes_list == Measurements_List[idMedicao][len(
            Measurements_List[idMedicao])-1])
        id_M = 0
        SDMC_Cost[id_RS, id_RD, id_M, 0] = Cost_List[idMedicao]
        SDMC_Id_Medicao[id_RS, id_RD, id_M, 0] = paths.index(
            Probes_List[idMedicao])
    else:
        id_C = 0
        id_M += 1
        for probe in Probes_List[idMedicao]:
            if probe in paths:
                id_cost = paths.index(probe)
            else:
                reverso = list(reversed(probe))
                id_cost = paths.index(reverso)
            SDMC_Cost[id_RS, id_RD, id_M, id_C] = path_cost[id_cost]
            SDMC_Id_Medicao[id_RS, id_RD, id_M, id_C] = id_cost
            id_C += 1
    medicao_anterior = Medicao
# pprint(SDMC_Cost)
End('Matriz de Custos')


Start('Inicia o modelo e cria a função de maximização')
RS_list = [*range(0, total_roteadores, 1)]
RD_list = [*range(0, total_roteadores, 1)]
M_list = [*range(0, max(num_sonda_medicao), 1)]
C_list = [*range(0, max_len_probe, 1)]


SDMC_Dict = LpVariable.dicts(
    "SDMC", (RS_list, RD_list, M_list, C_list), 0, 1, LpInteger)

# pprint(SDMC_Dict)

modelo_colocacao = LpProblem("Probes Placement Model", LpMaximize)


modelo_colocacao += (lpSum([SDMC_Dict[i_RS][i_RD][i_M][i_C] * SDMC_Cost[i_RS][i_RD][i_M][i_C]
                     for i_RS in RS_list for i_RD in RD_list for i_M in M_list for i_C in C_list if i_RS != i_RD]), "Total_Cost")

End('Inicia o modelo e cria a função de maximização')


Start('Limita sondas por roteador')

max_sondas = {n: (len(list(nx.all_neighbors(G, n))))for n in G.nodes}

# ATENÇÃO VER ORIGEM DESTINO ######## 1-> 2 = 2 -> 1
for id_router, router in enumerate(routers):
    # if id_router < (len(routers)-1):
    pprint(
        f'Limite de sondas no roteador: {router} - {max_sondas.get(router)}')
    # id_router = np.where(nodes_list == router)[0][0]
    modelo_colocacao += (lpSum([SDMC_Dict[id_router][i_RD][0][0] for i_RD in RD_list if id_router !=
                         i_RD]) <= max_sondas.get(router), "Max_Probes_Router" + str(id_router))

End('Limita sondas por roteador')


Start('Limita sondas por Link')


for u, v, atributos in G.edges(data=True):
    # print(f"Link: ({u}, {v}), Velocidade: {math.ceil(atributos['LinkSpeedRaw']/1000000000)}")
    if u != v:
        modelo_colocacao += (lpSum([SDMC_Dict[int(u)][int(v)][i_M][i_C] for i_M in M_list for i_C in C_list])
                             <= math.ceil(atributos['LinkSpeedRaw']/1000000000), "Max_Probes_Link" + str(u) + "_" + str(v))

End('Limita sondas por Link')


Start('Iguala as sondas')

for id_path, path in enumerate(paths):
    id_RS = int(np.where(nodes_list == path[0])[0])
    id_RD = int(np.where(nodes_list == path[len(path)-1])[0])
    for i_RS in RS_list:
        for i_RD in RD_list:
            for i_M in M_list:
                for i_C in C_list:
                    #if (SDMC_Id_Medicao[i_RS, i_RD, i_M, i_C]) > 0 and (i_M > 0) and (i_C > 0):
                    #    if id_path == int(SDMC_Id_Medicao[i_RS, i_RD, i_M, i_C]):
                    if id_path == int(SDMC_Id_Medicao[i_RS,i_RD,i_M,i_C]) and (i_M > 0) and (i_C > 0) :
                        modelo_colocacao += SDMC_Dict[i_RS][i_RD][i_M][i_C] == SDMC_Dict[id_RS][id_RD][0][0], "Igual_Probes" + str(path) + '_' + str(i_RS) + '_' + str(i_RD) + '_' + str(i_M) + '_' + str(i_C)
                            # pprint(id_path)
                            # pprint(int(SDMC_Id_Medicao[i_RS,i_RD,i_M,i_C]))
                            # pprint(SDMC_Dict[id_RS][id_RD][0][0])
                            # pprint(SDMC_Dict[i_RS][i_RD][i_M][i_C])
End('Iguala as sondas')

Start('Salva o Modelo')
modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))
End('Salva o Modelo')


Start('Pulp Solve')
modelo_colocacao.solve()
End('Pulp Solve')
lista_Sondas = []
print("Status:", LpStatus[modelo_colocacao.status])
if modelo_colocacao.status == 1:
    #pprint(modelo_colocacao)    
    for v in modelo_colocacao.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
            x = v.name.split("_")
            #if (int(x[3]) == 0 ):
            pprint(int(SDMC_Id_Medicao[int(x[1])][int(x[2])][int(x[3])][int(x[4])]))
            pprint(paths[int(SDMC_Id_Medicao[int(x[1])][int(x[2])][int(x[3])][int(x[4])])])
            lista_Sondas.append ( paths[int(SDMC_Id_Medicao[int(x[1])][int(x[2])][int(x[3])][int(x[4])])])
print("Custo = ", value(modelo_colocacao.objective))

# pprint(lista_Sondas)
# pprint("###########################")
# pprint(paths)
count_sondas = 0
count_sondas_reversas = 0
count_composicao = 0
count_sem_medicao = 0
for path in paths:
    pathreverse = path.reverse()
    if path in lista_Sondas:
        # pprint(f'Sonda - {path}')
        count_sondas += 1
    elif pathreverse in lista_Sondas:
        # pprint(f'{path} - Sonda - Reverse')
        count_sondas_reversas += 1
    else:
        # pprint(path)
        subpaths = []
        compostos = []
        if len(path) > 2:
            for i in range(len(path)):
                for j in range(i + 1, len(path) + 1):
                    subpath = (path[i: j])
                    if (len(subpath) > 1) and (len(subpath) < len(path)):
                        try:
                            subpaths.append(subpath)
                        except ValueError as e:
                            pprint("Subcaminho não existente")
            compostos = (Compose_Subpaths(path, subpaths))
        if compostos:
            # pprint(f'MEDICACAO Composta - {path}')
            # pprint(f'Composiçoes possiveis {compostos}')
            count_composicao += 1
        else:
            pprint(f'SEM MEDICACAO - {path}')
            count_sem_medicao += 1
pprint('Relátorio')
pprint(f'Total de Medições por Sondas: {count_sondas}')
pprint(f'Total de Medições por Sondas Reversas: {count_sondas_reversas}')
pprint(f'Total de Medições através de composiçôes: {count_composicao}')
pprint(f'Total rotas sem Mediçãos : {count_sem_medicao}')
pprint(
    f'Total de medições: {count_sondas+ count_sondas_reversas + count_composicao +count_sem_medicao} = {len(paths)} = {len(num_sonda_medicao)}')
pprint(f'#################################################################################')
pprint(
    f'Concluiu tudo em {time.process_time() - inicio_total:.2f} segundos')
pprint(f'#################################################################################')
pprint(f'Total de arestas {G.number_of_edges()}')
pprint(f'Total de nos {G.number_of_nodes()}')
pprint(f'Total de routas SPF {len(spf)}')
# pprint(type(paths))
# pprint(type(lista_Sondas))
#difference = list(set(paths[0]) - set(lista_Sondas[0]))
# pprint(difference)
#grafico(G)
#
#H = G.copy()
#
# edlist=[]
#H.remove_edges_from( G.edges())
# for v in modelo_colocacao.variables():
#    if v.varValue > 0:
#        x = v.name.split("_")
#        H.add_edge(str(x[1]),str(x[2]))
# grafico(H)
# pprint(SDMC_Id_Medicao)
# pprint(Probes_List)
# for (i, item) in enumerate(Probes_List, start=0):
# print(i, item)]
