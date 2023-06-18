\* Probes_Placement_Model *\
Minimize
OBJ: diferenca_carga_roteador1 + diferenca_carga_roteador2
 + diferenca_carga_roteador3 + diferenca_carga_roteador4
Subject To
Minimo_Sondas_Medicao_0ou5: __dummy >= 1
Minimo_Sondas_Medicao_11ou17: __dummy >= 0
Minimo_Sondas_Medicao_1ou10: __dummy >= -1
Minimo_Sondas_Medicao_3ou15: __dummy >= -1
Minimo_Sondas_Medicao_6ou8: __dummy >= 0
Minimo_Sondas_Medicao_7ou13: __dummy >= 0
_C1: - diferenca_carga_roteador1 <= 0.75
_C10: diferenca_carga_roteador2 >= 0.75
_C11: - diferenca_carga_roteador2 <= 0.75
_C12: diferenca_carga_roteador2 >= 0.75
_C13: - diferenca_carga_roteador3 <= -0.25
_C14: diferenca_carga_roteador3 >= -0.25
_C15: - diferenca_carga_roteador3 <= 0.75
_C16: diferenca_carga_roteador3 >= 0.75
_C17: - diferenca_carga_roteador3 <= 0.75
_C18: diferenca_carga_roteador3 >= 0.75
_C19: - diferenca_carga_roteador4 <= -0.25
_C2: diferenca_carga_roteador1 >= 0.75
_C20: diferenca_carga_roteador4 >= -0.25
_C21: - diferenca_carga_roteador4 <= -0.25
_C22: diferenca_carga_roteador4 >= -0.25
_C23: - diferenca_carga_roteador4 <= 0.75
_C24: diferenca_carga_roteador4 >= 0.75
_C3: - diferenca_carga_roteador1 <= 0.75
_C4: diferenca_carga_roteador1 >= 0.75
_C5: - diferenca_carga_roteador1 <= 0.75
_C6: diferenca_carga_roteador1 >= 0.75
_C7: - diferenca_carga_roteador2 <= 0.75
_C8: diferenca_carga_roteador2 >= 0.75
_C9: - diferenca_carga_roteador2 <= 0.75
Bounds
 __dummy = 0
End
