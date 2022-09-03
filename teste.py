import copy
from pprint import pprint
rota = ['7', '1', '0', '3']
subrotas = [['7', '1'], ['7', '1', '0'], ['1', '0'], ['1', '0', '3'], ['0', '3']]

def encontraposicoes (pos):
    posicoes = []
    if rota[pos]!=rota[len(rota)-1]:
      for subrota in range(len(subrotas)):
        if rota[pos] == subrotas[subrota][0]:
          posicoes.append(subrota)
    return (posicoes)  
    
      
def compoe_subrotas(pos, par_subcaminhos):
    posicoes = encontraposicoes(pos)
    saida = []
    if posicoes == []:
        #print('rotacomposta')
        return (par_subcaminhos)
    else:    
        subcaminhos = [] 
    for posicao in posicoes:
        subcaminhos = copy.deepcopy(par_subcaminhos)
        subcaminhos.append(subrotas[posicao])
        composto = compoe_subrotas(rota.index(subrotas[posicao][(len(subrotas[posicao])-1)]),subcaminhos)
        pprint(composto)
    pprint('antes do return')
    pprint (saida)
    #if pos == 0:
    return (saida) 
sub = []
rotascompostas=compoe_subrotas(0,sub)
pprint(rotascompostas)