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
    inicio = time.process_time()
    pprint(f'Iniciando a função {funcao}')
    return(inicio)

def End(funcao):
    pprint(f'Concluiu a função {funcao}, em {time.process_time() - inicio:.2f} segundos')
    pprint(f'#################################################################################')

#rede = 'Geant2012.graphml'
rede = 'Rnp.graphml'
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

Start('Preparacao de dados1')


lista_medicao, num_sonda_medicao = np.unique(Measurements_List, return_counts=True)


dictMedicoes_Pesos = {}

#Medicao = [tuple(m) for m in Measurements_List]
str_medicao = []
for medicao in lista_medicao.tolist():
    str_medicao.append(extractlabel(medicao))

End('Preparacao de dados1')
Start('Preparacao de dados2')


medicao_anterior = ''
Medicao_Peso = []
Medicao_Sonda = []
Sonda = []
dictRoteador_Medicao= {}

i_medicao = 0
i_sonda = 0
id_medicao_sonda = []

for idMedicao, Medicao in enumerate(Measurements_List):
    if (str(medicao_anterior)!=str(Medicao)) and (len(Medicao_Peso) > 0):
        for x in range(len(Medicao_Peso),(max(num_sonda_medicao))):
            Medicao_Peso.append(0)
            #Sonda.append(0)        
        dictMedicoes_Pesos[extractlabel(medicao_anterior)] = Medicao_Peso
        dictRoteador_Medicao[extractlabel(medicao_anterior)] = Sonda
        id_medicao_sonda.append([extractlabel(Medicao),i_sonda])
        Medicao_Peso = []
        Sonda = []
        i_medicao +=1
        i_sonda = 0
    Medicao_Peso.append(Cost_List[idMedicao])
    Sonda.append(idMedicao)
    medicao_anterior = Medicao  
    id_medicao_sonda.append([extractlabel(Medicao),i_sonda])
    i_sonda += 1 
    
for x in range(len(Medicao_Peso),(max(num_sonda_medicao))):
    Medicao_Peso.append(0) 
    #Sonda.append(0)     
dictMedicoes_Pesos[extractlabel(Medicao)] = Medicao_Peso
dictRoteador_Medicao[extractlabel(medicao_anterior)] = Sonda


#for medicao, id_medicao in dictRoteador_Medicao.items():
#    for id in id_medicao:
#        pprint(f'medicao id {id} - {Probes_List[id]} ')

#pprint(dictRoteador_Medicao)
#pprint(dictMedicoes_Pesos)

dictProbes_Compose = {}
dif_probes=len(Probes_List)
dictProbes_Cost = {}
for idProbe, Probes in enumerate(Probes_List):
    Composose = []
    if Probes == Measurements_List [idProbe]:
        for x in range(0,idProbe):
            Composose.append(0)
        Composose.append(1)
        for x in range(idProbe,dif_probes):
            Composose.append(0)
    else:
        lista_ids = []
        for Probe in Probes:
            if list(Probe) in Probes_List:
                lista_ids.append (list(Probes_List).index(Probe))
            else:
                reverso = list(reversed(Probe))
                if reverso in Probes_List:
                    lista_ids.append (list(Probes_List).index(reverso))
        # -1 pq começa em 0
        for x in range(0,dif_probes):
            if x in lista_ids:
                Composose.append(1)
            else:
                Composose.append(0)
    dictProbes_Compose[idProbe] = Composose 
    Cost = []
    #print(f"Medicao: {Measurements_List[idProbe]} - COmposicao {Probes_List[idProbe]} ")  
    for comp_id, comp in enumerate(Composose):
        if comp != 0:
            Cost.append(Cost_List[comp_id])
            #pprint(f'Item da composicao {Measurements_List[comp_id]} custo {Cost_List[comp_id]}')
        else:
            Cost.append(0)
    dictProbes_Cost[idProbe] = Cost
    pprint(idProbe)
pprint(dictProbes_Compose)
pprint(dictProbes_Cost)

for key, valor in dictProbes_Compose.items():
    pprint(f'Composicao {Probes_List[key]} {valor}')
    for id_probe in range(0,dif_probes):
        if valor[id_probe] == 1:
            pprint(f'Probe ativo id: {id_probe}  -> {Probes_List[id_probe]}')



     
End('Preparacao de dados2')
Start('Preparacao de dados3')
Sondas = [*range(0, max(num_sonda_medicao),1)]

SondasDict = LpVariable.dicts("combinacoes", (str_medicao, Sondas), 0, 1, LpInteger)

modelo_colocacao = LpProblem("Probes Placement Model", LpMaximize)
    
modelo_colocacao += (lpSum([SondasDict[m][s] * dictMedicoes_Pesos[m][s] for m in str_medicao for s in Sondas]),"Peso_total",)
End('Preparacao de dados3')
Start('Preparacao de dados4')
for m in str_medicao:
    modelo_colocacao += (lpSum([SondasDict[m][s] for s in Sondas]) <= 1, "Max_Uma_Sonda_Por_MEdicao" + str(m))

for m in str_medicao:
    for s in Sondas:
        if dictMedicoes_Pesos [m][s] !=0:
            #pprint(f' ID: {dictRoteador_Medicao[m][s]} - Sonda {Probes_List[dictRoteador_Medicao[m][s]]}')
            if Probes_List[dictRoteador_Medicao[m][s]] == Measurements_List [dictRoteador_Medicao[m][s]]:
                #pprint(f'não é composicao, sonda {dictRoteador_Medicao[m][s]}')
                lista_ids = []
                for m_aux in str_medicao:
                    for s_aux in Sondas: 
                        if (dictMedicoes_Pesos [m_aux][s_aux] !=0) and (Probes_List[dictRoteador_Medicao[m_aux][s_aux]] != Measurements_List[dictRoteador_Medicao[m_aux][s_aux]]):
                            for composicao in Probes_List[dictRoteador_Medicao[m_aux][s_aux]]:    
                                if list(composicao) in Probes_List and not list(Probes_List).index(composicao) in lista_ids:
                                    lista_ids.append (list(Probes_List).index(composicao))
                                else:
                                    
                                    reverso = list(reversed(composicao))
                                    if reverso in Probes_List and not list(Probes_List).index(reverso) in lista_ids:
                                        lista_ids.append (list(Probes_List).index(reverso))
                #pprint(lista_ids)
                Medicao_Lista = []
                Sondas_Lista = []
                for id in lista_ids:
                    Medicao_Lista.append((id_medicao_sonda[id])[0])
                    Sondas_Lista.append((id_medicao_sonda[id])[1])
                #pprint(Medicao_Lista)
                #pprint(Sondas_Lista)
                #pprint(composicao)
                #pprint(str(m))
                modelo_colocacao += (lpSum([SondasDict[m_for][s_for] for m_for in Medicao_Lista for s_for in Sondas_Lista]) == len(Sondas_Lista), "Rep" + str(m))                         


routers = G.nodes

#para não ter um parametros aleatorio tenho a parte inteira da metade das arestas/links em cada no/host
max_sondas = {n: (len(list(nx.all_neighbors(G, n)))//2)for n in G.nodes}
End('Preparacao de dados4')


         


Start('Preparacao de dados5')
#pprint(max_sondas.keys()[max_sondas.values().index(18)])





#pprint(max_sondas)
for router in routers:
    list_probes = []
    Measurement = ''
    for idMedicao, Medicao in enumerate(Measurements_List):
        if (Measurement != Medicao):
            Measurement = Medicao
            idprobe = 0
        else:
            idprobe += 1
        if router in Measurement:
            probes = Probes_List[idMedicao]
            #pprint(probes)
            for probe in probes:
                # se o probe tem inicio ou fim no router
                if type(probe) is str and (probe == router):
                    list_probes.append([extractlabel(Measurement),idprobe])
                    break
                elif (probe[0] == router) or (probe[len(probe)-1]== router):
                    list_probes.append([extractlabel(Measurement),idprobe])              
    modelo_colocacao += (lpSum([SondasDict[M][S] for M, S in list_probes]) <= max_sondas.get(router), "Max_Probes_Router" + router)    

End('Preparacao de dados5')
#for 


modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))

Start('Pulp Solve')
modelo_colocacao.solve()
End('Pulp Solve')


print("Status:", LpStatus[modelo_colocacao.status])
for v in modelo_colocacao.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print("Custo = ", value(modelo_colocacao.objective))
