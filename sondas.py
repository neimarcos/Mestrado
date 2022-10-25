
from pprint import pprint
import networkx as nx
import operator
import pandas as pd
import copy
import numpy as np
from pulp import *

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

lista_medicao, num_sonda_medicao = np.unique(Lista_Medicoes, return_counts=True)

Medicoes_Pesos = []
dictMedicoes_Pesos = {}

#Medicao = [tuple(m) for m in Lista_Medicoes]
str_medicao = []
for medicao in lista_medicao.tolist():
    str_medicao.append(extractlabel(medicao))

for idMedicao, Medicao in enumerate(Lista_Medicoes):
    df_medicao = dfMedidasSondas[dfMedidasSondas['Medida'].astype(str) == str(Medicao)]
    #pprint(Medicao)
    #pprint(df_medicao)
    Medicao_Peso = []
    for sonda in range (len(df_medicao)):
        Medicao_Peso.append(df_medicao.iloc[sonda]['Pesos'])
    for x in range(sonda,(max(num_sonda_medicao)-1)):
        Medicao_Peso.append(0)
    dictMedicoes_Pesos[extractlabel(Medicao)] = Medicao_Peso
    Medicoes_Pesos.append(Medicao_Peso)

Sondas = [*range(1, max(num_sonda_medicao),1)]

SondasDict = LpVariable.dicts("combinacoes", (str_medicao, Sondas), 0, 1, LpInteger)

modelo_colocacao = LpProblem("Probes Placement Model", LpMaximize)
    
modelo_colocacao += (lpSum([SondasDict[m][s] * dictMedicoes_Pesos[m][s] for m in str_medicao for s in Sondas]),"Peso_total",)

for m in str_medicao:
        modelo_colocacao += (lpSum([dictMedicoes_Pesos[m][s] for s in Sondas]) <= 1, "Max_Uma_Sonda_Por_MEdicao" + str(m))

 
modelo_colocacao.writeLP(rede.replace(".graphml", ".LP"))
modelo_colocacao.solve()
print("Status:", LpStatus[modelo_colocacao.status])
for v in modelo_colocacao.variables():
    #if v.varValue > 0:
        print(v.name, "=", v.varValue)
print("Custo = ", value(modelo_colocacao.objective))

#exibegrafico(G)