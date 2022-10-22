import pulp
from pprint import pprint
import networkx as nx
import operator
import pandas as pd
import copy
import numpy as np

def EncontraRotasCompostas(caminhopeso):
    caminho_unidirecional = []
    caminhopeso_aux = caminhopeso.copy()
    for caminho in caminhopeso[:]:
        reverso = list(reversed(caminho[2]))
        #pprint(f"Caminho: {caminho[1]}")
        #pprint(f"Reverso: {reverso}")
        peso = caminho[0]
        for caminho_aux in caminhopeso_aux[:]:
            if caminho_aux[2] == reverso:
                #pprint(f"Tem reverso")
                caminhopeso.remove(caminho_aux)
                peso += caminho_aux[0]
        i = tuple((peso, caminho[1], caminho[2]))
        irevese = tuple((peso, caminho[1], reverso))
        if i not in caminho_unidirecional and irevese not in caminho_unidirecional:
            caminho_unidirecional.append(i)
    # ordena as rotas pelo peso (número de ocorrência)
    rotas_pesos = sorted(caminho_unidirecional, key=operator.itemgetter(0))
    # Filtra rota com mais de 2 soltos, pois podem ser alcaçandas através da agregação
    #rota_compor = list(filter(lambda rota: rota[1] >= 3, rotas_pesos))
    return (rotas_pesos)

# Com base na posição do elemento(no) encontra posições que um elemente(no) ocorre em um lista (rotas)
# pos = posicao do elemento
# rota =
# subrota =


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


def pesorotascompostas(df, rotascompostas):
    def encontrapeso(salto):
        df2 = df[df['caminho_str'].astype(str) == str(salto)]
        if df2.empty:
            reverso = list(reversed(salto))
            df2 = df[df['caminho_str'].astype(str) == str(reverso)]
        return (2 * (df2.iloc[0]['peso']))
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

def extractlabel(salto):
    caminho_string = ''
    for no in salto:
        caminho_string += str(no) + '-'
    return caminho_string[:-1]


def EncontraRotasCompostas(caminhopeso):
    caminho_unidirecional = []
    caminhopeso_aux = caminhopeso.copy()
    for caminho in caminhopeso[:]:
        reverso = list(reversed(caminho[2]))
        #pprint(f"Caminho: {caminho[1]}")
        #pprint(f"Reverso: {reverso}")
        peso = caminho[0]
        for caminho_aux in caminhopeso_aux[:]:
            if caminho_aux[2] == reverso:
                #pprint(f"Tem reverso")
                caminhopeso.remove(caminho_aux)
                peso += caminho_aux[0]
        i = tuple((peso, caminho[1], caminho[2]))
        irevese = tuple((peso, caminho[1], reverso))
        if i not in caminho_unidirecional and irevese not in caminho_unidirecional:
            caminho_unidirecional.append(i)
    # ordena as rotas pelo peso (número de ocorrência)
    rotas_pesos = sorted(caminho_unidirecional, key=operator.itemgetter(0))
    # Filtra rota com mais de 2 soltos, pois podem ser alcaçandas através da agregação
    #rota_compor = list(filter(lambda rota: rota[1] >= 3, rotas_pesos))
    return (rotas_pesos)


# Encontra o número de vezes que um combinação de rotas ocorre, idenpendete do tamnho
def ContaOcorrencias(chunks):
    chunks_aux = chunks.copy()
    index = 0
    count_sequencias = 0
    caminho = []
    peso = []
    caminhopeso = []
    for v in chunks:
        count = 0
        count_sequencias += 1
        #print(f" Sequencia: {v}")
        for v_aux in chunks_aux:
            try:
                index = v_aux.index(v[0])
                if v == v_aux[index:index+len(v)]:
                    #pprint (v_aux)
                    count += 1
            except ValueError:
                pass
        #pprint(f"V: {v} Total: {count}")
        caminho.append(v)
        peso.append(count)
        caminhopeso.append((count, len(v), v))
        #pprint(f" Total de Sequências diferentes: {count_sequencias}")
    return (caminho, peso, caminhopeso)


def EncontraComposicoesPosiveis(caminhopesobidirecional):
    df_caminhos = pd.DataFrame(caminhopesobidirecional)
    caminhos = tuple(df_caminhos[2])
    pesos = tuple(df_caminhos[0])
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


def encontrapeso(rota):
    if (len(rota) > 1):
        for i in range(len(caminho)):
            #pprint(f'Caminho{caminho[i]} - rota{list(rota)} - peso {peso[i]}')
            if caminho[i] == list(rota):
                return abs(peso[i])
    return (0)


#rede = 'Geant2012.graphml'
#rede = 'Rnp.graphml.graphml'
#rede = 'exemplo.graphml'
rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)


spf = nx.shortest_path(G, weight='LinkSpeedRaw')
routers = G.nodes

# pprint(spf)


rotas = []
for i in spf:
    for k, v in spf[i].items():
        if (len(v) >= 2):
            v_reverso = copy.deepcopy(v)
            v_reverso.reverse()
            if v_reverso not in rotas:
                rotas.append(v)

Medicao = [tuple(c) for c in rotas]


caminho, peso, caminhopeso = (ContaOcorrencias(rotas))
# pprint(caminhopeso)
# pprint()
df = pd.DataFrame(caminhopeso)
df.columns = ['peso', 'tamanho', 'caminho']
df['caminho_str'] = df['caminho'].astype(str)

Lista_Rota_Sonda = rotas.copy()
Lista_Composicao_Sonda = rotas.copy()

Lista_Medicoes = []
Lista_Sonda_Medicao = []
Lista_Sonda_Medicao_Peso = []


caminhopesobidirecional = EncontraRotasCompostas(caminhopeso)
# pprint(caminhopesobidirecional)

rotascompostas = EncontraComposicoesPosiveis(caminhopesobidirecional)
# pprint(rotascompostas)

pesorotascompostas(df, Lista_Sonda_Medicao)


MedidasSondas= {'Medida': Lista_Medicoes,
           'Sondas': Lista_Sonda_Medicao,
           'Pesos': Lista_Sonda_Medicao_Peso,
           }

dfMedidasSondas = pd.DataFrame(MedidasSondas)

pprint(dfMedidasSondas)

sonda_medico, num_sonda_medicao = np.unique(Lista_Medicoes, return_counts=True)
#PesoSonda = [ [0 for i in range(max(num_sonda_medicao))] for j in range(len(sonda_medico)) ]


Medicoes_Pesos = []
dictMedicoes_Pesos = {}

for idMedicao, Medicao in enumerate(Lista_Medicoes):
    df_medicao = dfMedidasSondas[dfMedidasSondas['Medida'].astype(str) == str(Medicao)]
    #pprint(Medicao)
    #pprint(df_medicao)
    Medicao_Peso = []
    for sonda in range (len(df_medicao)):
        Medicao_Peso.append(df_medicao.iloc[sonda]['Pesos'])
        
    for x in range(sonda,(max(num_sonda_medicao)-1)):
        Medicao_Peso.append(0)
    dictMedicoes_Pesos[str(Medicao)] = Medicao_Peso
    Medicoes_Pesos.append(Medicao_Peso)

pprint(dictMedicoes_Pesos)
#pprint(dfMedidasSondas)

Sondas = range(1, max(num_sonda_medicao))
Medicao = [tuple(m) for m in Lista_Medicoes]

SondasDict = pulp.LpVariable.dicts("combinacoes", (Medicao, Sondas), 0, None, pulp.LpInteger)
pprint(SondasDict)

prob = pulp.LpProblem("Proble Problem", pulp.LpMaximize)

prob += (pulp.lpSum([SondasDict[m][s] * dictMedicoes_Pesos[m][s] for (m, s) in zip(sonda_medico,range(0,max(num_sonda_medicao)))]),"Peso_total",)


# #commit
# # The objective function is added to 'prob' first
# 


# # The objective function is added to 'prob' first
# #prob += (
# #    lpSum(caminho[C] * rotascompostas[S] * peso[P] for P, S, C in caminhopeso),"Peso Total ",
# #)

# #testey = LpVariable.dicts('y',  peso, cat='Integer')


# '''

# MedicaoDict = LpVariable.dicts('M',  Medicao, cat='Integer')
# pprint(MedicaoDict)

# pesoDict = LpVariable.dicts('P',  peso, cat='Integer')
# pprint(pesoDict)

# ComposicaoDict = LpVariable.dicts('C', sondas, cat='Integer')
# pprint(ComposicaoDict)

# Sondas = LpVariable.dicts("Sonda", (Medicao, Composicao), cat="Binary")

# pprint(Sondas)







# # Cada medição pode ter uma unica composição
# for m in Medicao:
#     prob += lpSum([Sondas[m] [c] for c in Composicao]) <= 1





# prob.writeLP(rede+'.pl')


# x = pulp.LpVariable.dicts(
#     "probe", possible_probes, lowBound=0, upBound=1, cat=pulp.LpInteger
# )


# probes_model = pulp.LpProblem("Probes Placement Model", pulp.LpMaximize)


# probes_model += pulp.lpSum([encontrapeso(probe) * x[probe] for probe in possible_probes])


# probes_model += (pulp.lpSum([x[probe] for probe in possible_probes]) <= 10,"Max_Probes",)


# for router in routers:
#     probes_model += ( pulp.lpSum([x[probe] for probe in possible_probes if router in probe]) <= 5, "Max_Probes_no_Router%s" % router,
#     )

# probes_model.writeLP(rede+'.pl')
# probes_model.solve()
# print("Os probes ativo são de um total de  %s:" % len(possible_probes))
# #pprint(possible_probes)

# for probe in possible_probes:
#     if x[probe].value() == 1:
#         pprint(probe)
# '''
