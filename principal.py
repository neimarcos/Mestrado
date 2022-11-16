import copy
from pprint import pprint
import networkx as nx
import pandas as pd



def ClearRoutes(spf):
    """
    Clear routes, remove reverse path.
    ### Parameters
    1. spf : dict
        - [dictionary of dictionaries with path[source][target]=[list of nodes in path], return from function shortest_path from networkx library]

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
    ### Parameters
    1. spf : dict
        - [routes]

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

def encontraposicoes(pos, rota, subrotas):
    posicoes = []
    if rota[pos] != rota[len(rota)-1]:
        for subrota in range(len(subrotas)):
            if rota[pos] == subrotas[subrota][0]:
                posicoes.append(subrota)
    return (posicoes)



def compoe_subrotas(pos, par_rota_composta, rota, subrotas, pesos):
    posicoes = encontraposicoes(pos, rota, subrotas)
    saida = []
    if posicoes == []:
        #pprint(f'Rota {rota} - Composta: {par_rota_composta}  ')
        saida.append(par_rota_composta)
        return (saida)
    else:
        rota_composta = []
    peso_total = 0
    for posicao in posicoes:
        rota_composta = copy.deepcopy(par_rota_composta)
        rota_composta.append(subrotas[posicao])
        saltos = compoe_subrotas(rota.index(subrotas[posicao][(
            len(subrotas[posicao])-1)]), rota_composta, rota, subrotas, pesos)
        saida.extend(saltos)
    return (saida)

def Find_Compose_Paths(path_count):
    pesos=tuple([k[1] for k in path_count])
    caminhos=tuple([k[0] for k in path_count])
    rotascompostas = []
    global Lista_Medicoes
    global Lista_Sonda_Medicao
    for i in spf:
        for k, v in spf[i].items():          
            if len(v) > 2:
                #pprint(f"Origem: {i}, destino: {k}, rota spf: {v} ")
                test_str = v
                subcaminhos = []
                pesos_subcaminhos = []
                # rotascompostas.append(v)
                for i in range(len(test_str)):
                    for j in range(i + 1, len(test_str) + 1):
                        subcaminho = (test_str[i: j])
                        subcaminho_reverse = list(reversed(subcaminho))
                        if len(subcaminho) > 1 and len(subcaminho) < len(test_str):
                        # pprint(subcaminho)
                        # pprint(subcaminho_reverse)
                            try:
                                if subcaminho in caminhos:
                                    pos = caminhos.index(subcaminho)
                                    #pprint(f"Subcaminho {subcaminho} na posição {pos} com peso {pesos[pos]}  " )
                                    subcaminhos.append(subcaminho)
                                    pesos_subcaminhos.append(pesos[pos])
                                else:
                                    pos = caminhos.index(subcaminho_reverse)
                                    #pprint(f"Subcaminho_reverse {subcaminho_reverse} na posição {pos} com peso {pesos[pos]}  " )
                                    subcaminhos.append(subcaminho)
                                    pesos_subcaminhos.append(pesos[pos])
                            except ValueError as e:
                                pprint("Subcaminho não existente")
                caminhos_par = []
                #print(f'SubRotas: {subcaminhos}')
                # pprint(compoe_subrotas(0,caminhos_par))
                retorno = (compoe_subrotas(0, caminhos_par, v, subcaminhos, pesos_subcaminhos))
                rotascompostas.append (retorno)
                for comp in retorno:
                    Lista_Medicoes.append(v)
                    Lista_Sonda_Medicao.append(comp)
            elif len(v) > 1:
                Lista_Medicoes.append(v)
                Lista_Sonda_Medicao.append(v)
    # for i, nome in enumerate(neimar):
    #     pprint(f'IDX {i} - rota {nome}')
    #     for compos in rotascompostas[i]:
    #         if type(compos) is str:
    #             pprint(rotascompostas[i])
    #             break
    #         else:
    #             pprint (compos)
    return (rotascompostas)



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

pprint(compose_paths)
