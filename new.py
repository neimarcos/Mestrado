def encontrar_rotas(lista_de_rotas, rota):
    resultado = []
    if rota:
        for i, lst in enumerate(lista_de_rotas):
            if lst[0] == rota[0]:
                sub_resultado = encontrar_rotas(lista_de_rotas[:i]+lista_de_rotas[i+1:], rota[1:])
                if sub_resultado:
                    for sub in sub_resultado:
                        resultado.append([lst]+sub)
                else:
                    if not rota[1:]:
                        resultado.append([lst])
    return resultado

lista_de_rotas = [['5', '0'], ['3', '5'], ['2', '3'], ['2', '3', '5'], ['2', '3', '5', '6'], ['1', '2'], ['3', '5', '6'], ['4', '2', '3', '5'], ['5', '6'], ['5', '6', '7'], ['6', '7']]
rota = ['1', '2', '3', '5']
print(encontrar_rotas(lista_de_rotas, rota))