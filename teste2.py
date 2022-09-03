import copy

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
    if posicoes == []:
        print('rotacomposta')
        print (f' {par_subcaminhos}')
    else:    
        subcaminhos = [] 
    for posicao in posicoes:
        subcaminhos = copy.deepcopy(par_subcaminhos)
        subcaminhos.append(subrotas[posicao])
        compoe_subrotas(rota.index(subrotas[posicao][(len(subrotas[posicao])-1)]),subcaminhos)



sub = []
compoe_subrotas(0, sub)

