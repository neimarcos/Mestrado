\* Probes_Placement_Model *\
Minimize
Total_Cost_and_Difference: Medicao_0 + Medicao_1 + Medicao_11 + Medicao_13
 + Medicao_14 + Medicao_16 + Medicao_3 + Medicao_8 + Medicao_9
 + diferenca_carga_roteador1 + diferenca_carga_roteador3
 + diferenca_carga_roteador4
Subject To
Carga_Maior_Roteador1: Medicao_0 + Medicao_1 + Medicao_3
 + diferenca_carga_roteador1 >= 0
Carga_Maior_Roteador3: Medicao_11 + Medicao_8 + Medicao_9
 + diferenca_carga_roteador3 >= 0
Carga_Maior_Roteador4: Medicao_13 + Medicao_14 + Medicao_16
 + diferenca_carga_roteador4 >= 0
Carga_Menor_Roteador1: Medicao_0 + Medicao_1 + Medicao_3
 - diferenca_carga_roteador1 <= 1
Carga_Menor_Roteador3: Medicao_11 + Medicao_8 + Medicao_9
 - diferenca_carga_roteador3 <= 1
Carga_Menor_Roteador4: Medicao_13 + Medicao_14 + Medicao_16
 - diferenca_carga_roteador4 <= 1
Composicao12_13: Medicao_12 - Medicao_13 <= 0
Composicao12_8: Medicao_12 - Medicao_8 <= 0
Composicao2_0: - Medicao_0 + Medicao_2 <= 0
Composicao2_8: Medicao_2 - Medicao_8 <= 0
Composicao4_0: - Medicao_0 + Medicao_4 <= 0
Composicao4_13: - Medicao_13 + Medicao_4 <= 0
Minimo_Sondas_Medicao_0ou5: Medicao_0 + Medicao_5 >= 1
Minimo_Sondas_Medicao_11ou17: Medicao_11 + Medicao_12 + Medicao_16
 + Medicao_17 >= 1
Minimo_Sondas_Medicao_13ou7: Medicao_13 + Medicao_7 >= 1
Minimo_Sondas_Medicao_1ou10: Medicao_1 + Medicao_10 + Medicao_2 + Medicao_9
 >= 1
Minimo_Sondas_Medicao_3ou15: Medicao_14 + Medicao_15 + Medicao_3 + Medicao_4
 >= 1
Minimo_Sondas_Medicao_8ou6: Medicao_6 + Medicao_8 >= 1
Roteador_Sem_Medicao2: Medicao_5 + Medicao_6 + Medicao_7 = 0
Binaries
Medicao_0
Medicao_1
Medicao_10
Medicao_11
Medicao_12
Medicao_13
Medicao_14
Medicao_15
Medicao_16
Medicao_17
Medicao_2
Medicao_3
Medicao_4
Medicao_5
Medicao_6
Medicao_7
Medicao_8
Medicao_9
diferenca_carga_roteador1
diferenca_carga_roteador3
diferenca_carga_roteador4
End
