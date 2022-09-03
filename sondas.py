import pulp
from pprint import pprint
import networkx as nx



# Encontra o número de vezes que um combinação de rotas ocorre, idenpendete do tamnho
def ContaOcorrencias(chunks):
    chunks_aux = chunks.copy()
    index = 0
    count_sequencias=0
    caminho = []
    peso = []
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
        caminho.append (v)
        peso.append(count)
        #pprint(f" Total de Sequências diferentes: {count_sequencias}")
    return(caminho, peso)   

def encontrapeso(rota):
    if (len(rota)>1):
        for i in range(len(caminho)):
            #pprint(f'Caminho{caminho[i]} - rota{list(rota)} - peso {peso[i]}')
            if caminho[i] == list(rota):
                return abs(peso[i])
    return (0)

max_probes = 5
max_probe_size = 4

G = nx.read_graphml('exemplo.xml')
spf = nx.shortest_path(G,weight='LinkSpeedRaw')
routers = G.nodes

pprint(spf)


rotas = []
for i in spf:
    for k, v in spf[i].items():
        rotas.append(v)

caminho, peso = (ContaOcorrencias(rotas))

possible_probes = [tuple(c) for c in rotas ]

x = pulp.LpVariable.dicts(
    "probe", possible_probes, lowBound=0, upBound=1, cat=pulp.LpInteger
)

probes_model = pulp.LpProblem("Probes Placement Model", pulp.LpMinimize)

probes_model += pulp.lpSum([encontrapeso(probe) * x[probe] for probe in possible_probes])

probes_model += (pulp.lpSum([x[probe] for probe in possible_probes]) == 10,"Max_Route_Com_Probes",
)

for router in routers:
    probes_model += ( pulp.lpSum([x[probe] for probe in possible_probes if router in probe]) <= 2, "Max_Probes_no_Router%s" % router,
    )

probes_model.solve()
probes_model.writeLP("Probes-Sondas")
print("The choosen tables are out of a total of %s:" % len(possible_probes))
pprint(possible_probes)

for table in possible_probes:
    if x[table].value() == 1.0:
        print(table)
        
