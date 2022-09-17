
import networkx as nx
from pprint import pprint
import operator
import matplotlib.pyplot as plt
import pandas as pd
from pulp import *
import copy
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

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
 

def carregaRNP(G):
    G = nx.read_graphml('Rnp.graphml.xml')
    return(nx.shortest_path(G,weight='LinkSpeedRaw'))

def carregaExemplo(G):
    G = nx.read_graphml('exemplo.xml')
    return(nx.shortest_path(G))


# Baseado no retorno do SPF do NetworkX descobre todos os caminhos únicos
def limparotas(spf):
    MIN_LEN = 2
    chunks = list()
    for i in spf:
        for k, v in spf[i].items():  
            if (len(v) >= MIN_LEN) :
                chunks.append(v)
    return (chunks)

# Encontra o número de vezes que um combinação de rotas ocorre, idenpendete do tamnho
def ContaOcorrencias(chunks):
    chunks_aux = chunks.copy()
    index = 0
    count_sequencias=0
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
        #pprint(f" Total: {count}")
        caminhopeso.append((count,len(v), v))
        #pprint(f" Total de Sequências diferentes: {count_sequencias}")
    return(caminhopeso)        
        

# Organiza  e Filtra as rotas, deixando somente um sentido, pois nossas medidas são bidirecionais e também
# Filtra rota com mais de 2 soltos, pois podem ser alcaçandas através da agregação
# uma unica direção, remover os inversos , 1-> 2 = 2 -> 1

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

def pesorotascompostas(df, rotascompostas):
    for rotascomp in rotascompostas: 
        #print(f'Essas rotas {rotascomp}')
        #print(f'Count {len(rotascomp)}')    
        for rota in rotascomp:
            #print(f'Essa rota {rota}')
            #print(f'Count {len(rota)}')
            if len(rota) >  1 :
                custo_rota = 0;
                composicao = ''
                for salto in rota:
                    #print(f'Count {len(salto)}')
                    df2=df[df['caminho_str'].astype(str)== str(salto)]
                    val = 2 *(df2.iloc[0]['peso'])
                    composicao += extractlabel(salto) + '+'
                    #pprint(f'{label} - {val}')
                    custo_rota += val
                composicao = composicao[:-1]
                Lista_Rota.append(str(composicao))
                Lista_Custo.append(str(custo_rota))
            else:
                df2=df[df['caminho_str'].astype(str)== str(salto)]
                val = 2 *(df2.iloc[0]['peso'])
                Lista_Rota.append(str(rota))
                Lista_Custo.append(str(val))

def extractlabel(salto):
    caminho_string = ''
    for no in salto:
        caminho_string  += str(no) + '-'
    return caminho_string[:-1]



def EncontraComposicoesPosiveis(caminhopesobidirecional):
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
                #pprint(rotascompostas)
    return(rotascompostas)

def exibegrafico(G):
  node_dist_to_color = {
      1: "tab:red",
      2: "tab:orange",
      3: "tab:olive",
      4: "tab:green",
      5: "tab:blue",
      6: "tab:purple",
      7: "tab:gray",
  }

  plt.figure(rede,figsize=(12,12)) 

  Links = nx.get_edge_attributes(G,'LinkLabel').values()

  cores = []
  for key in Links:
    if (key == '20Gbps'):
      cores.append(node_dist_to_color[1])
    elif(key=='10Gbps'):
      cores.append(node_dist_to_color[2])
    elif(key=='3.5Gbps'):
      cores.append(node_dist_to_color[3])
    elif (key == '3Gbps'):
      cores.append(node_dist_to_color[4])
    elif (key == '1.45Gbps'):
      cores.append(node_dist_to_color[5])
    elif(key=='200Mbps'):
      cores.append(node_dist_to_color[6])
    elif(key=='20Mbps'):
      cores.append(node_dist_to_color[7])
  # setup Lambert Conformal basemap.
  # set resolution=None to skip processing of boundary datasets.
  m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution=None,lat_1=45.,lat_2=55,lat_0=-15.9350619,lon_0=-51.8217625)

  label_dic = dict(list(G.nodes(data="label")))
  Latitude = (list(G.nodes(data="Latitude")))
  Longitude = (list(G.nodes(data="Longitude")))


  pos={}
  poslabel={}
  for i in range(G.number_of_nodes()):
    pos[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1])]
    poslabel[str(i)]= [float(Longitude[i][1]), float(Latitude[i][1]+1)]

  nx.draw_networkx_edges(G, pos,edge_color=cores, width=2)
  nx.draw_networkx_labels(G, poslabel,label_dic,font_size=8)
  nx.draw_networkx_nodes(G, pos, node_size=40, node_color="#210070", alpha=0.9)

  m.drawcountries()
  m.drawstates()
  m.bluemarble()
  plt.title(rede)


  plt.show()

#spf= carregaExemplo(G)
#spf= carregaRNP()
#pprint(spf)
    

#rede = 'Geant2012.graphml'
rede = 'Rnp.graphml'
#rede = 'exemplo.graphml'
#rede = 'exemplo_pequeno.graphml'

G = nx.read_graphml(rede)

spf = nx.shortest_path(G,weight='LinkSpeedRaw')
#pprint(spf)             
exibegrafico(G)
rotas=limparotas(spf)
#pprint(rotas)

caminhopeso = ContaOcorrencias(rotas)
#pprint()
df= pd.DataFrame(caminhopeso)
df.columns = ['peso', 'tamanho', 'caminho']
df['caminho_str'] = df['caminho'].astype(str)

Lista_Rota = []
Lista_Custo = []
for k, v, x in caminhopeso: 
    Lista_Rota.extend({extractlabel (x)})
    Lista_Custo.append(str(k))
    #pprint(f'{extractlabel (x)} =  {k}')

Lista_RotaSimple =  copy.deepcopy(Lista_Rota)
    
caminhopesobidirecional=EncontraRotasCompostas(caminhopeso)
#pprint(caminhopesobidirecional)

rotascompostas = EncontraComposicoesPosiveis(caminhopesobidirecional)
#pprint(rotascompostas)
          
pesorotascompostas(df, rotascompostas)    



#pprint(Lista_Rota) 
#pprint(Lista_Custo) 

Dic_Custo = dict(zip(Lista_Rota,[int(x) for x in Lista_Custo]))

#pprint(Dic_Custo)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Proble Problem", LpMaximize)

# A dictionary called 'Custo_var' is created to contain the referenced Variables
rota_var = LpVariable.dicts("R", Lista_Rota, 0, 1, LpInteger)

# The objective function is added to 'prob' first
prob += (
    lpSum([Dic_Custo[i] * rota_var[i] for i in Lista_Rota]),"Total Cost ",
)


routers = G.nodes

max_sondas = [3,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5,5,4,5,6,8,2,3,6,7,3,6,3,5,1,0,1,3,2,2,3,4,1,3,1,3,2,4,2,5,3,1,2,3,5]     

    
# Maximo de sondas em um roteador
for router in routers:
    Lista_Inicio_Fim = []
    #pprint(f'Router: {router}')
    for rota in Lista_Rota:
        #pprint(rota[0:rota.find('-')])
        #pprint(rota[rota.rfind('-')+1:])
        #pprint(rota.find(router+'+'+router))
        if router == rota[0:rota.find('-')] or router == rota[rota.rfind('-')+1:] or rota.find(router+'+'+router)>0:
            #pprint (f'Rota: {rota} - Inicio: {rota[0:len(router)]} - Fim {rota[len(rota)-len(str(router)):]}')
            #pprint (f' Len Rota {len(rota)} Len do route {len(router)}')
            Lista_Inicio_Fim.append(rota)
    if Lista_Inicio_Fim:
        #pprint(Lista_Inicio_Fim)
        prob += (lpSum([rota_var[i] for i in Lista_Inicio_Fim]) <= max_sondas[int(router)], "Origem_Destino" + str(router))    

# Evita medição duplicada - Rota reversa
for rota in Lista_RotaSimple:
    Inverso = []
    #if rota[0:rota.find('-')]  == rota[len(rota) - rota.find('-'):]:
    origem = rota[0:rota.find('-')]
    destino = rota[rota.rfind('-')+1:]
    #pprint (f'Rota: {rota} Origem - {origem} Destino - {destino}')
    #pprint(origem)
    for rota_aux in Lista_RotaSimple:
        origem_aux=rota_aux[0:rota_aux.find('-')]
        destino_aux=rota_aux[rota_aux.rfind('-')+1:]
        #pprint (f'Rota_aux: {rota_aux} Origem - {origem_aux} Destino - {destino_aux}')
        if origem == destino_aux and destino == origem_aux:
            #pprint (f'Rota inversa: {rota_aux}')
            #pprint (f'Rota_aux: {rota_aux} Origem - {origem_aux} Destino - {destino_aux}')
            Inverso.append(rota)
            Inverso.append(rota_aux)
    if Inverso:
        #pprint(Inverso)
        prob += (lpSum([rota_var[i] for i in Inverso]) <= 1, "RotaInversa" + str(rota))



prob.writeLP(rede.replace(".graphml", ".LP"))
prob.solve()
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print("Custo = ", value(prob.objective))

exibegrafico(G)