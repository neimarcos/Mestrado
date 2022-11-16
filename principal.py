import copy
from pprint import pprint
import networkx as nx
import pandas as pd


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

def encontraposicoes(pos, route, subrotas):
    """
    Finds  

    ### Parameters:
        pos (int): current position on the route to start checking
        route (list): _description_
        subrotas (list): _description_

    ### Returns:
        list: _description_
    """    
    posicoes = []
    if route[pos] != route[len(route)-1]:
        for subrota in range(len(subrotas)):
            if route[pos] == subrotas[subrota][0]:
                posicoes.append(subrota)
    return (posicoes)



def compoe_subrotas(par_rota_composta, rota, subrotas, pos = 0):
    """
    Finds all possible subpath compositions of a path    
    
    ### Parameters:
        par_rota_composta (list): _description_
        rota (list): path to finds possible compositions
        subrotas (list): all possibles subpaths 
        pos (int): initial position to find 
        
    ### Returns:
        list: List of all possible subpath compositions of a path
    """    
    posicoes = encontraposicoes(pos, rota, subrotas)
    saida = []
    if posicoes == []:
        #pprint(f'Rota {rota} - Composta: {par_rota_composta}  ')
        saida.append(par_rota_composta)
        return (saida)
    else:
        rota_composta = []
    for posicao in posicoes:
        rota_composta = copy.deepcopy(par_rota_composta)
        rota_composta.append(subrotas[posicao])
        saltos = compoe_subrotas( rota_composta, rota, subrotas, rota.index(subrotas[posicao][(len(subrotas[posicao])-1)]))
        saida.extend(saltos)
    return (saida)

def Find_Compose_Paths(path_count):
    """ 
    Finds all possible compositions for all paths
    
    ### Parameters:
        path_count (list): all paths/subpaths and how many times it repeats
    ### Returns:
        list: all possible possible combinations of subpaths for all paths
    """
    paths=tuple([k[0] for k in path_count])
    rotascompostas = []
    global Lista_Medicoes
    global Lista_Sonda_Medicao
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
            caminhos_par = []
            retorno = (compoe_subrotas(caminhos_par, path, subpaths))
            rotascompostas.append (retorno)
            for comp in retorno:
                Lista_Medicoes.append(path)
                Lista_Sonda_Medicao.append(comp)
        elif len(path) > 1:
            Lista_Medicoes.append(path)
            Lista_Sonda_Medicao.append(path)
    return (rotascompostas)

def Composite_Route_Cost(df, rotascompostas):
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
    global Lista_Sonda_Medicao_Peso
    
    for rotascomp in rotascompostas:
        val = 0
        for composicao in rotascomp:
            if type(composicao) is str:
                val = encontrapeso(rotascomp)
                break
            else:
                val += encontrapeso(composicao)
        Lista_Sonda_Medicao_Peso.append(val)


#rede = 'Geant2012.graphml'
#rede = 'Rnp.graphml.graphml'
#rede = 'exemplo.graphml'
rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)
spf = nx.shortest_path(G, weight='LinkSpeedRaw')


routes = ClearRoutes (spf)

path_count = Count_Subsegment_Occurrences(routes)

df = pd.DataFrame(path_count)
df.columns = ['path', 'count', 'length']
df['path_str'] = df['path'].astype(str)

List_Routes_Probes = routes.copy()
List_Routes_Compose_Probes = routes.copy()

Lista_Medicoes = []
Lista_Sonda_Medicao = []
Lista_Sonda_Medicao_Peso = []

compose_paths = Find_Compose_Paths(path_count)

Composite_Route_Cost(df, Lista_Sonda_Medicao)



pprint(Lista_Sonda_Medicao_Peso)
