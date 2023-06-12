import docplex.cp.model as cp
from random import randint

# Definindo os processos e suas cargas
processos = list(range(1, 11))
cargas = {i: randint(20, 40) for i in processos}

# Definindo os processadores
processadores = list(range(1, 6))

# Criando o modelo de otimização
model = cp.CpoModel("Balanceamento_de_Carga")

# Definindo as variáveis de decisão
x_vars = {(i, j): model.binary_var(name="x_{0}_{1}".format(i, j)) for i in processos for j in processadores}
y_var = model(name="y", lb=0)

# Adicionando as restrições
for i in processos:
    model.add_constraint(model.sum(x_vars[(i, j)] for j in processadores) == 1, "rest_1_{0}".format(i))

for j in processadores:
    carga_processador = model.sum(x_vars[(i, j)] * cargas[i] for i in processos)
    model.add_constraint(carga_processador <= 100, "rest_2_{0}".format(j))
    model.add_constraint(carga_processador <= y_var, "rest_3_{0}".format(j))

# Definindo a função objetivo
model.add_minimize(y_var)

# Resolvendo o problema
solver = model.solve()

# Exibindo os resultados
print("Status:", solver.get_solve_status())
for v in x_vars.values():
    if v.solution_value > 0 and 'x' in v.get_name():
        print(v.get_name(), "=", v.solution_value)
print("Carga máxima =", y_var.solution_value)
