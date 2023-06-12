from pulp import *
from random import randint

# Processos com cargas variando de 20 a 80
processos = list(range(1, 11))
cargas = {i: randint(20, 40) for i in processos}

# Processadores
processadores = list(range(1, 6))

# Definindo o problema
prob = LpProblem("Balanceamento_de_Carga", LpMinimize)

# Variáveis de decisão
x_vars = LpVariable.dicts("x", [(i, j) for i in processos for j in processadores], 0, 1, LpBinary)
y_vars = LpVariable("y", 0, None, LpContinuous)

# Cada processo deve ser atribuído a exatamente um processador
for i in processos:
    prob += lpSum([x_vars[(i, j)] for j in processadores]) == 1

# A carga total de cada processador não deve ultrapassar 100 e y
for j in processadores:
    carga_processador = lpSum([x_vars[(i, j)] * cargas[i] for i in processos])
    prob += carga_processador <= 100
    prob += carga_processador <= y_vars

# Função objetivo
prob += y_vars

# Resolvendo o problema
prob.solve()

# Mostrando os resultados
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    if v.varValue > 0 and 'x' in v.name:
        print(v.name, "=", v.varValue)
print("Carga máxima =", value(prob.objective))
