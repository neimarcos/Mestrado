import copy
from pprint import pprint
import networkx as nx
import numpy as np
from pulp import *
import time


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
    caminho_string = ''
    for no in salto:
        caminho_string += str(no) + '-'
    return caminho_string[:-1]

def Start(funcao):
    global inicio 
    inicio= time.process_time()
    pprint(f'Iniciando a função {funcao}')
    return(inicio)

def End(funcao):
    pprint(f'Concluiu a função {funcao}, em {time.process_time() - inicio:.2f} segundos')
    pprint(f'#################################################################################')

#rede = 'Geant2012.graphml'
#rede = 'Rnp.graphml'
#rede = 'exemplo.graphml'
rede = 'exemplo_pequeno.graphml'

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

Start('Preparacao de dados1')


lista_medicao, num_sonda_medicao = np.unique(Measurements_List, return_counts=True)


dictMedicoes_Pesos = {}

#Medicao = [tuple(m) for m in Measurements_List]
str_medicao = []
for medicao in lista_medicao.tolist():
    str_medicao.append(extractlabel(medicao))

End('Preparacao de dados1')
Start('Preparacao de dados - dictMedicoes_Pesos')


medicao_anterior = ''
Medicao_Peso = []
Medicao_Sonda = []
Sonda = []
#dictRoteador_Medicao= {}

i_medicao = 0
i_sonda = 0
id_medicao_sonda = []


routers = G.nodes

import numpy as np

R = len(routers)
M = len(routers)
S = max(num_sonda_medicao)

RMS= np.zeros((R, M, S))

#print(RMS)

nodes_list = np.array(list(G.nodes()))



#for id_router_origem, router_origem in enumerate(nodes_list):
#    pprint(f'ID Origem: {id_router_origem} - nome {nodes_list[id_router_origem]}')
#    for id_router_destino, router_destino in enumerate(nodes_list):
#        if id_router_origem != id_router_destino:
#            pprint(f'ID Destino: {id_router_destino} - nome {nodes_list[id_router_destino]}')
#            for id in range (0,max(num_sonda_medicao)):
#                RMS[id_router_origem,id_router_destino,id]=id
    
pprint(RMS)

medicao_anterior = ''
for idMedicao, Medicao in enumerate(Measurements_List):
    #if (Probes_List[idMedicao] == Measurements_List [idMedicao]):
    if str(medicao_anterior)!=str(Medicao):
        i_sonda = 0
    pprint(f'Origem: {Measurements_List[idMedicao][0]}')
    pprint(f'Destino: {Measurements_List[idMedicao][len(Measurements_List[idMedicao])-1]}')
    pprint(Probes_List[idMedicao])
    id_origem = np.where(nodes_list == Measurements_List[idMedicao][0])
    id_destino = np.where(nodes_list == Measurements_List[idMedicao][len(Measurements_List[idMedicao])-1])
    RMS[id_origem,id_destino,i_sonda]=Cost_List[idMedicao]
    i_sonda += 1
    medicao_anterior = Medicao

pprint(RMS[0])



#urements_List):
#        if Router in Medicao:
#            pprint(Medicao)
#            RMC[idRouter][idMedicao].append(Cost_List[idMedicao])
#    
#pprint (RMC)
'''

    if (str(medicao_anterior)!=str(Medicao)) and (len(Medicao_Peso) > 0):
        for x in range(len(Medicao_Peso),(max(num_sonda_medicao))):
            Medicao_Peso.append(0)
            #Sonda.append(0)        
        dictMedicoes_Pesos[extractlabel(medicao_anterior)] = Medicao_Peso
        #dictRoteador_Medicao[extractlabel(medicao_anterior)] = Sonda
        i_sonda = 0
        Medicao_Peso = []
        Sonda = []
        i_medicao +=1
    Medicao_Peso.append(Cost_List[idMedicao])
    Sonda.append(idMedicao)
    medicao_anterior = Medicao  
    id_medicao_sonda.append([extractlabel(Medicao),i_sonda])
    i_sonda += 1 
    
for x in range(len(Medicao_Peso),(max(num_sonda_medicao))):
    Medicao_Peso.append(0) 
    #Sonda.append(0)     
dictMedicoes_Pesos[extractlabel(Medicao)] = Medicao_Peso
#dictRoteador_Medicao[extractlabel(medicao_anterior)] = Sonda

#for medicao, id_medicao in dictRoteador_Medicao.items():
#    for id in id_medicao:
#        pprint(f'medicao id {id} - {Probes_List[id]} ')
#pprint(dictRoteador_Medicao)
#pprint(dictMedicoes_Pesos)
End('Preparacao de dados - dictMedicoes_Pesos')

Start('Preparacao de dados - dictProbes_Compose')

dictProbes_Compose = {}
dif_probes=len(Probes_List)
default_compose = list(itertools.repeat(0, dif_probes ))
#Probes_Compose_Count = []
for idProbe, Probes in enumerate(Probes_List):
    Composose = copy.deepcopy(default_compose)
    if Probes == Measurements_List [idProbe]:
        Composose[idProbe] = 1
    else:
        for Probe in Probes:
            if list(Probe) in Probes_List:
                Composose[(list(Probes_List).index(Probe))]=1
            else:
                reverso = list(reversed(Probe))
                if reverso in Probes_List:
                    Composose[(list(Probes_List).index(reverso))]=1
    dictProbes_Compose[idProbe] = Composose 
   #pprint(idProbe)

#pprint(dictProbes_Compose)



            



     
End('Preparacao de dados - dictProbes_Compose')
Start('Preparacao de dados3')
Sondas = [*range(0, max(num_sonda_medicao),1)]
SondasCompostas = [*range(1, max(num_sonda_medicao),1)]


SondasDict = LpVariable.dicts("combinacoes", (str_medicao, Sondas), 0, 1, LpInteger)   
SondasAtivas = LpVariable.dicts("SondaAtiva", (str_medicao, Sondas), 0, 1, LpInteger)   





modelo_colocacao = LpProblem("Probes Placement Model", LpMaximize)
    
modelo_colocacao += (lpSum([SondasDict[m][s] * dictMedicoes_Pesos[m][s] for m in str_medicao for s in Sondas]),"Peso_total",)
End('Preparacao de dados3')
Start('Preparacao de dados4')

# Maximo de uma sonda para determinada medição
#for m in str_medicao:
#    modelo_colocacao += (lpSum([SondasDict[m][s]  for s in SondasCompostas]) <= 1, "Max_Uma_Sonda_Por_MEdicao" + str(m))


#End('Preparacao de dados4')
routers = G.nodes
max_sondas = {n: (len(list(nx.all_neighbors(G, n))))for n in G.nodes}
#Start('Preparacao de NEW')
#
#Probe_in_Compose = []
#for id_probe in range(0,dif_probes):
#    count = 0;
#    for id, valor in dictProbes_Compose.items():
#        if valor[id_probe] == 1:
#            count += 1
#    Probe_in_Compose.append(count)
#
##pprint(Probe_in_Compose)
#
#for id, valor in dictProbes_Compose.items():
#    if (Probes_List[id] != Measurements_List [id]):
#        #pprint(f'Sonda: {Probes_List[id]}') 
#        #pprint(SondasDict[id_medicao_sonda[id][0]][id_medicao_sonda[id][1]])
#        #for id_probe in range(0,dif_probes):
#            #if valor[id_probe] == 1: 
#                #pprint(f'Composição: {Probes_List[id_probe]}') 
#                #pprint(SondasDict[id_medicao_sonda[id_probe][0]][id_medicao_sonda[id_probe][1]])
#        
#        modelo_colocacao += (lpSum([SondasDict[id_medicao_sonda[id_probe][0]][id_medicao_sonda[id_probe][1]] for id_probe in range(0,dif_probes) if valor[id_probe] == 1]) == SondasDict[id_medicao_sonda[id][0]][id_medicao_sonda[id][1]], "Rep" + str(Probes_List[id]))                         
#    #for id_probe in range(0,dif_probes):
#     #   if valor[id_probe] == 1:
#      #      pprint(f'Composição: {Probes_List[id_probe]}')
#
#
#
##for id_probe in range(0,dif_probes):
##    if (Probes_List[id_probe] == Measurements_List [id_probe]):
#        #pprint(f'Probe {Probes_List[id_probe]}')
##        modelo_colocacao += (lpSum([SondasDict[id_medicao_sonda[id][0]][id_medicao_sonda[id][1]] for id, valor in dictProbes_Compose.items() if valor[id_probe] == 1]) <= Probe_in_Compose[id_probe], "Rep" + str(Probes_List[id_probe]))                         
#
#
#End('Preparacao de NEW')
#
##Start('Preparacao de dados5')
#
#
##pprint(max_sondas)
#for router in routers:
#    list_probes = []
#    Measurement = ''
#    for idMedicao, Medicao in enumerate(Measurements_List):
#        if (Measurement != Medicao):
#            Measurement = Medicao
#            idprobe = 0
#        else:
#            idprobe += 1
#        if router in Measurement:
#            probes = Probes_List[idMedicao]
#            #pprint(probes)
#            for probe in probes:
#                # se o probe tem inicio ou fim no router
#                if type(probe) is str and (probe == router):
#                    list_probes.append([extractlabel(Measurement),idprobe])
#                    break
#                elif (probe[0] == router) or (probe[len(probe)-1]== router):
#                    list_probes.append([extractlabel(Measurement),idprobe])         
#    #list_probes = list(dict.fromkeys(list_probes))
#    # Numero maximo de sondas por roteador
#    modelo_colocacao += (lpSum([SondasDict[M][S] for M, S in list_probes]) <= max_sondas.get(router), "Max_Probes_Router" + router)    
#
#End('Preparacao de dados5')
##for 


modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))

Start('Pulp Solve')
modelo_colocacao.solve()
End('Pulp Solve')


print("Status:", LpStatus[modelo_colocacao.status])
for v in modelo_colocacao.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print("Custo = ", value(modelo_colocacao.objective))

'''