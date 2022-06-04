\* Probes_Placement_Problem *\
Minimize
Sum_of_Transporting_Costs: Route_A_AC + Route_A_AE + Route_A_AG + Route_A_AH
 + Route_A_AJ + 5 Route_C_AC + 5 Route_C_CE + 5 Route_C_CG + 5 Route_C_CH
 + 5 Route_C_CJ + Route_E_AE + Route_E_CE + Route_E_EG + Route_E_EH
 + Route_E_EJ + Route_G_AG + Route_G_CG + Route_G_EG + Route_G_GH + Route_G_GJ
 + Route_H_AH + Route_H_CH + Route_H_EH + Route_H_GH + Route_H_HJ + Route_J_AJ
 + Route_J_CJ + Route_J_EJ + Route_J_GJ + Route_J_HJ
Subject To
Sum_of_Probes_In_LinkAC: Route_A_AC + Route_C_AC = 1
Sum_of_Probes_In_LinkAE: Route_A_AE + Route_E_AE = 1
Sum_of_Probes_In_LinkAG: Route_A_AG + Route_G_AG = 1
Sum_of_Probes_In_LinkAH: Route_A_AH + Route_H_AH = 1
Sum_of_Probes_In_LinkAJ: Route_A_AJ + Route_J_AJ = 1
Sum_of_Probes_In_LinkCE: Route_C_CE + Route_E_CE = 1
Sum_of_Probes_In_LinkCG: Route_C_CG + Route_G_CG = 1
Sum_of_Probes_In_LinkCH: Route_C_CH + Route_H_CH = 1
Sum_of_Probes_In_LinkCJ: Route_C_CJ + Route_J_CJ = 1
Sum_of_Probes_In_LinkEG: Route_E_EG + Route_G_EG = 1
Sum_of_Probes_In_LinkEH: Route_E_EH + Route_H_EH = 1
Sum_of_Probes_In_LinkEJ: Route_E_EJ + Route_J_EJ = 1
Sum_of_Probes_In_LinkGH: Route_G_GH + Route_H_GH = 1
Sum_of_Probes_In_LinkGJ: Route_G_GJ + Route_J_GJ = 1
Sum_of_Probes_In_LinkHJ: Route_H_HJ + Route_J_HJ = 1
Sum_of_Probes_In_route_A: Route_A_AC + Route_A_AE + Route_A_AG + Route_A_AH
 + Route_A_AJ <= 2
Sum_of_Probes_In_route_C: Route_C_AC + Route_C_CE + Route_C_CG + Route_C_CH
 + Route_C_CJ <= 10
Sum_of_Probes_In_route_E: Route_E_AE + Route_E_CE + Route_E_EG + Route_E_EH
 + Route_E_EJ <= 2
Sum_of_Probes_In_route_G: Route_G_AG + Route_G_CG + Route_G_EG + Route_G_GH
 + Route_G_GJ <= 2
Sum_of_Probes_In_route_H: Route_H_AH + Route_H_CH + Route_H_EH + Route_H_GH
 + Route_H_HJ <= 2
Sum_of_Probes_In_route_J: Route_J_AJ + Route_J_CJ + Route_J_EJ + Route_J_GJ
 + Route_J_HJ <= 2
Bounds
 0 <= Route_A_AC
 0 <= Route_A_AE
 0 <= Route_A_AG
 0 <= Route_A_AH
 0 <= Route_A_AJ
 0 <= Route_C_AC
 0 <= Route_C_CE
 0 <= Route_C_CG
 0 <= Route_C_CH
 0 <= Route_C_CJ
 0 <= Route_E_AE
 0 <= Route_E_CE
 0 <= Route_E_EG
 0 <= Route_E_EH
 0 <= Route_E_EJ
 0 <= Route_G_AG
 0 <= Route_G_CG
 0 <= Route_G_EG
 0 <= Route_G_GH
 0 <= Route_G_GJ
 0 <= Route_H_AH
 0 <= Route_H_CH
 0 <= Route_H_EH
 0 <= Route_H_GH
 0 <= Route_H_HJ
 0 <= Route_J_AJ
 0 <= Route_J_CJ
 0 <= Route_J_EJ
 0 <= Route_J_GJ
 0 <= Route_J_HJ
Generals
Route_A_AC
Route_A_AE
Route_A_AG
Route_A_AH
Route_A_AJ
Route_C_AC
Route_C_CE
Route_C_CG
Route_C_CH
Route_C_CJ
Route_E_AE
Route_E_CE
Route_E_EG
Route_E_EH
Route_E_EJ
Route_G_AG
Route_G_CG
Route_G_EG
Route_G_GH
Route_G_GJ
Route_H_AH
Route_H_CH
Route_H_EH
Route_H_GH
Route_H_HJ
Route_J_AJ
Route_J_CJ
Route_J_EJ
Route_J_GJ
Route_J_HJ
End
