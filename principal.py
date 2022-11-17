import copy
from pprint import pprint
import networkx as nx
import pandas as pd
import numpy as np
from pulp import *

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
    return (Path_Count_Occurrences)

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
            for comp in retorno:
                Measurements_List.append(path)
                Probes_List.append(comp)
        #elif len(path) > 1:
        #    Measurements_List.append(path)
        #    Probes_List.append(path)
    return (ComposePaths)

def Compose_Route_Cost(df, rotascompostas):
    """
    Calculate cost based composition of subpaths
    
    ### Parameters:
        df (dataframe): dataframe with all paths
        rotascompostas (list): all possible possible compositon of subpaths for all paths
        
        
    """
    def encontrapeso(salto):
        df2 = df[df['path_str'].astype(str) == str(salto)]
        if df2.empty:
            reverso = list(reversed(salto))
            df2 = df[df['path_str'].astype(str) == str(reverso)]
        return (2 * (df2.iloc[0]['count']))
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


#rede = 'Geant2012.graphml'
rede = 'Rnp.graphml'
#rede = 'exemplo.graphml'
#rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)
spf = nx.shortest_path(G, weight='LinkSpeedRaw')

# Clear routes
paths = ClearRoutes (spf)

# counts how many times a subsegment/subpath occurs in the spf 
path_count = Count_Subsegment_Occurrences(paths)

df = pd.DataFrame(path_count)
df.columns = ['path', 'count', 'length']
df['path_str'] = df['path'].astype(str)

Measurements_List = []
Probes_List = []
Cost_List = []

compose_paths = Find_Compose_Paths(path_count)

Compose_Route_Cost(df, Probes_List)

MedidasSondas= {'Measurements': Measurements_List,
           'Probes': Probes_List,
           'Cost': Cost_List,
           }

dfMedidasSondas = pd.DataFrame(MedidasSondas)


lista_medicao, num_sonda_medicao = np.unique(Measurements_List, return_counts=True)

Medicoes_Pesos = []
dictMedicoes_Pesos = {}

#Medicao = [tuple(m) for m in Measurements_List]
str_medicao = []
for medicao in lista_medicao.tolist():
    str_medicao.append(extractlabel(medicao))

for idMedicao, Medicao in enumerate(Measurements_List):
    df_medicao = dfMedidasSondas[dfMedidasSondas['Measurements'].astype(str) == str(Medicao)]
    #pprint(Medicao)
    #pprint(df_medicao)
    Medicao_Peso = []
    for sonda in range (len(df_medicao)):
        Medicao_Peso.append(df_medicao.iloc[sonda]['Cost'])
    for x in range(sonda,(max(num_sonda_medicao))):
        Medicao_Peso.append(0)
    dictMedicoes_Pesos[extractlabel(Medicao)] = Medicao_Peso
    Medicoes_Pesos.append(Medicao_Peso)

Sondas = [*range(1, max(num_sonda_medicao)+1,1)]

SondasDict = LpVariable.dicts("combinacoes", (str_medicao, Sondas), 0, 1, LpInteger)

modelo_colocacao = LpProblem("Probes Placement Model", LpMaximize)
    
modelo_colocacao += (lpSum([SondasDict[m][s] * dictMedicoes_Pesos[m][s] for m in str_medicao for s in Sondas]),"Peso_total",)

for m in str_medicao:
        modelo_colocacao += (lpSum([SondasDict[m][s] for s in Sondas]) <= 1, "Max_Uma_Sonda_Por_MEdicao" + str(m))

routers = G.nodes

max_sondas = [3,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5]     

#pprint(dfMedidasSondas)
for router in routers:
    list_probes = []
    Measurement = ''
    for index, row in dfMedidasSondas.iterrows():
        if (Measurement != row['Measurements']):
            Measurement = row['Measurements']
            idprobe = 1
        else:
            idprobe += 1
        if router in Measurement:
            probes = row['Probes']
            #pprint(probes)
            for probe in probes:
                # se o probe tem inicio ou fim no router
                if (probe[0] == router) or (probe[len(probe)-1]== router):
                    list_probes.append([extractlabel(Measurement),idprobe])              
    modelo_colocacao += (lpSum([SondasDict[M][S] for M, S in list_probes]) <= max_sondas[int(router)], "Max_Probes_Router" + router)    


 
modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))
modelo_colocacao.solve()
print("Status:", LpStatus[modelo_colocacao.status])
for v in modelo_colocacao.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print("Custo = ", value(modelo_colocacao.objective))

