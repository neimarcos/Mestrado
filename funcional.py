import pulp
import random


# Criar o problema de minimização
problema = pulp.LpProblem("Problema de Alocação de Processos", pulp.LpMinimize)

# Variáveis
processadores = range(1, 10)  # Processadores numerados de 1 a 5
processos = range(1, 50)  # Processos numerados de 1 a 10

# Variáveis binárias para indicar se um processo é alocado em um processador
alocado = {
    (p, pr): pulp.LpVariable(f'processo{p}_processador{pr}', cat=pulp.LpBinary)
    for p in processos for pr in processadores
}

# Variáveis contínuas para representar a diferença entre a carga de cada processador e a carga média total
diferenca_carga = {
    pr: pulp.LpVariable(f'diferenca_carga_processador{pr}', lowBound=0)
    for pr in processadores
}

# Dados
carga_processos = {i: (i % 11) + 1 for i in range(1, 201)}

SDMC_Dict = {s: pulp.LpVariable(f"Medicao_{s}", 0, 1, pulp.LpContinuous) for s in carga_processos}

for s in carga_processos:
    SDMC_Dict[s] = carga_processos[s] * random.randint(1,3)

# Função objetivo
carga_total_processadores = {
    pr: pulp.lpSum(SDMC_Dict[p] * alocado[(p, pr)] for p in processos)
    for pr in processadores
}
carga_media_total = pulp.lpSum(carga_total_processadores.values()) / len(processadores)

problema += pulp.lpSum(diferenca_carga[pr] for pr in processadores)

# Restrições
for pr in processadores:
    problema += pulp.lpSum(SDMC_Dict[p] * alocado[(p, pr)] for p in processos) <= carga_media_total + diferenca_carga[pr]
    problema += pulp.lpSum(SDMC_Dict[p] * alocado[(p, pr)] for p in processos) >= carga_media_total - diferenca_carga[pr]
    
for p in processos:
    problema += pulp.lpSum(alocado[(p, pr)] for pr in processadores) == 1
# Resolva o problema
#solver = pulp.GUROBI_CMD()
#
solver = pulp.CPLEX_CMD()
problema.solve(solver)
#problema.solve()

# Verifique o status da solução
status = pulp.LpStatus[problema.status]
print("Status da solução:", status)

# Obtenha os valores das variáveis e imprima a carga de cada processo e a carga total por processador
carga_por_processador = {pr: [] for pr in processadores}
for p in processos:
    for pr in processadores:
        if alocado[(p, pr)].value() > 0:
            carga_por_processador[pr].append((p, carga_processos[p]))

# Calcule e imprima a carga média por processador
carga_total_por_processador = {
    pr: sum(carga_processos[p] for p, _ in processos_alocados)
    for pr, processos_alocados in carga_por_processador.items()
}

for pr, processos_alocados in carga_por_processador.items():
    print(f"Processos alocados no processador {pr}:")
    for p, carga_p in processos_alocados:
        print(f"   - Processo {p}: Carga {carga_p}")
    print(f"Carga total no processador {pr}: {carga_total_por_processador[pr]}")
