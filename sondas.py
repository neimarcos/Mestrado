from pprint import pprint
import networkx as nx
import operator
import pandas as pd
import copy
from pulp import *




def EncontraRotasCompostas(caminhopeso):
    caminho_unidirecional = []
    caminhopeso_aux = caminhopeso.copy()
    for caminho in caminhopeso[:]:
        reverso =list(reversed(caminho[2]))
        #pprint(f"Caminho: {caminho[1]}")
        #pprint(f"Reverso: {reverso}")
        peso = caminho[0]
        for caminho_aux in caminhopeso_aux[:]:
            if caminho_aux[2] == reverso:
            #pprint(f"Tem reverso")
                caminhopeso.remove(caminho_aux)
                peso += caminho_aux[0]
        i = tuple ((peso, caminho[1], caminho[2]))
        irevese = tuple ((peso, caminho[1], reverso))
        if i not in caminho_unidirecional and irevese not in caminho_unidirecional:
            caminho_unidirecional.append(i) 
    #ordena as rotas pelo peso (número de ocorrência)
    rotas_pesos = sorted(caminho_unidirecional, key=operator.itemgetter(0))
    #Filtra rota com mais de 2 soltos, pois podem ser alcaçandas através da agregação
    #rota_compor = list(filter(lambda rota: rota[1] >= 3, rotas_pesos))
    return (rotas_pesos)

# Com base na posição do elemento(no) encontra posições que um elemente(no) ocorre em um lista (rotas)
# pos = posicao do elemento 
# rota =
# subrota = 
def encontraposicoes (pos,rota,subrotas):
    posicoes = []
    if rota[pos]!=rota[len(rota)-1]:
      for subrota in range(len(subrotas)):
            if rota[pos] == subrotas[subrota][0]:
                posicoes.append(subrota)
    return (posicoes)  
    

def compoe_subrotas(pos, par_rota_composta, rota, subrotas,pesos):
    posicoes = encontraposicoes(pos,rota,subrotas)
    saida = []
    if posicoes == []:
        #pprint(f'Composta: {par_rota_composta}')
        saida.append(par_rota_composta)
        return (saida)
    else:
        rota_composta = [] 
    for posicao in posicoes:
        rota_composta = copy.deepcopy(par_rota_composta)
        rota_composta.append(subrotas[posicao])
        saltos = compoe_subrotas(rota.index(subrotas[posicao][(len(subrotas[posicao])-1)]),rota_composta,rota,subrotas,pesos)
        saida.extend(saltos)
    return (saida)
 
 
def pesorotascompostas(df, rotascompostas):
    for rotascomp in rotascompostas: 
        #print(f'Essas rotas {rotascomp}')
        #print(f'Count {len(rotascomp)}')    
        for rota in rotascomp:
            #print(f'Essa rota {rota}')
            #print(f'Count {len(rota)}')
            if len(rota) >  1 :
                custo_rota = 0;
                composicao = []
                comp = ''
                for salto in rota:
                    #print(f'Count {len(salto)}')
                    df2=df[df['caminho_str'].astype(str)== str(salto)]
                    if df2.empty:
                       reverso =list(reversed(salto))               
                       df2=df[df['caminho_str'].astype(str)== str(reverso)]
                    val = 2 *(df2.iloc[0]['peso'])
                    custo_rota += val
                    comp = extractlabel(salto) 
                    #pprint(f'{salto} - {val}')
                    composicao.append (comp)
            caminho.append(composicao)
            peso.append(custo_rota)


def extractlabel(salto):
    caminho_string = ''
    for no in salto:
        caminho_string  += str(no) + '-'
    return caminho_string[:-1]


def EncontraRotasCompostas(caminhopeso):
    caminho_unidirecional = []
    caminhopeso_aux = caminhopeso.copy()
    for caminho in caminhopeso[:]:
        reverso =list(reversed(caminho[2]))
        #pprint(f"Caminho: {caminho[1]}")
        #pprint(f"Reverso: {reverso}")
        peso = caminho[0]
        for caminho_aux in caminhopeso_aux[:]:
            if caminho_aux[2] == reverso:
            #pprint(f"Tem reverso")
                caminhopeso.remove(caminho_aux)
                peso += caminho_aux[0]
        i = tuple ((peso, caminho[1], caminho[2]))
        irevese = tuple ((peso, caminho[1], reverso))
        if i not in caminho_unidirecional and irevese not in caminho_unidirecional:
            caminho_unidirecional.append(i) 
    #ordena as rotas pelo peso (número de ocorrência)
    rotas_pesos = sorted(caminho_unidirecional, key=operator.itemgetter(0))
    #Filtra rota com mais de 2 soltos, pois podem ser alcaçandas através da agregação
    #rota_compor = list(filter(lambda rota: rota[1] >= 3, rotas_pesos))
    return (rotas_pesos)


# Encontra o número de vezes que um combinação de rotas ocorre, idenpendete do tamnho
def ContaOcorrencias(chunks):
    chunks_aux = chunks.copy()
    index = 0
    count_sequencias=0
    caminho = []
    peso = []
    caminhopeso = []
    for v in chunks:
        count = 0
        count_sequencias +=1 
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
        caminho.append (v)
        peso.append(count)
        caminhopeso.append((count,len(v), v))
        #pprint(f" Total de Sequências diferentes: {count_sequencias}")
    return(caminho, peso, caminhopeso) 

def EncontraComposicoesPosiveis(caminhopesobidirecional):
    global max_sum_caminhos 
    df_caminhos = pd.DataFrame(caminhopesobidirecional)
    caminhos = tuple(df_caminhos[2])
    pesos = tuple(df_caminhos[0])
    rotascompostas = []
    for i in spf:
        for k, v in spf[i].items(): 
            if len  (v) > 2:       
                #pprint(f"Origem: {i}, destino: {k}, rota spf: {v} ")
                test_str = v
                subcaminhos = []
                pesos_subcaminhos = []
                #rotascompostas.append(v)
                for i in range(len(test_str)):
                    for j in range(i + 1, len(test_str) + 1):
                        subcaminho = (test_str[i: j]) 
                        subcaminho_reverse= list(reversed(subcaminho))
                        if len(subcaminho) > 1 and len(subcaminho) < len (test_str):
                            #pprint(subcaminho)
                            #pprint(subcaminho_reverse)
                            try :
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
                #pprint(compoe_subrotas(0,caminhos_par))
                rotascompostas.append(compoe_subrotas(0,caminhos_par,v,subcaminhos,pesos_subcaminhos))
                if (len(subcaminhos) > max_sum_caminhos):
                    max_sum_caminhos = len(subcaminhos)
                    pprint(max_sum_caminhos)
    return(rotascompostas)
  

def encontrapeso(rota):
    if (len(rota)>1):
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


spf = nx.shortest_path(G,weight='LinkSpeedRaw')
routers = G.nodes

#pprint(spf)


rotas = []
for i in spf:
    for k, v in spf[i].items():
        if (len(v) >= 2):
            v_reverso = copy.deepcopy(v)
            v_reverso.reverse()
            if v_reverso not in rotas:
                rotas.append(v)

Medicao = [tuple(c) for c in rotas ]



caminho, peso, caminhopeso = (ContaOcorrencias(rotas))
#pprint(caminhopeso)
#pprint()
df= pd.DataFrame(caminhopeso)
df.columns = ['peso', 'tamanho', 'caminho']
df['caminho_str'] = df['caminho'].astype(str)


#pprint(caminho)


#pprint("Meio")
caminhopesobidirecional=EncontraRotasCompostas(caminhopeso)
#pprint(caminhopesobidirecional)
max_sum_caminhos = 0

rotascompostas = EncontraComposicoesPosiveis(caminhopesobidirecional)
#pprint(rotascompostas)

pesorotascompostas(df, rotascompostas) 

#pprint(caminho)

#possible_probes = [tuple(c) for c in caminho ]

#Ver se precisa do +1 da sonda sem composição
Composicao = range(1, max_sum_caminhos)

Sondas = LpVariable.dicts("Sonda", (Medicao, Composicao), cat="Binary")

pprint(Sondas)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Proble Problem", LpMaximize)


# The objective function is added to 'prob' first
prob += (
    lpSum([Sondas[i] * Sondas[i] * Peso[i] for i in Lista_Rota]),"Peso Total ",
)


# Cada medição pode ter uma unica composição
for m in Medicao:
    prob += lpSum([Sondas[m] [c] for c in Composicao]) <= 1





prob.writeLP(rede+'.pl')

'''
x = pulp.LpVariable.dicts(
    "probe", possible_probes, lowBound=0, upBound=1, cat=pulp.LpInteger
)



#pprint(x)




probes_model += pulp.lpSum([encontrapeso(probe) * x[probe] for probe in possible_probes])


#probes_model += (pulp.lpSum([x[probe] for probe in possible_probes]) <= 10,"Max_Probes",)


for router in routers:
    probes_model += ( pulp.lpSum([x[probe] for probe in possible_probes if router in probe]) <= 5, "Max_Probes_no_Router%s" % router,
    )

probes_model.writeLP(rede+'.pl')
probes_model.solve()
print("Os probes ativo são de um total de  %s:" % len(possible_probes))
#pprint(possible_probes)

for probe in possible_probes:
    if x[probe].value() == 1:
        pprint(probe)
'''