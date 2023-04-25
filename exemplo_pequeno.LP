\* Probes_Placement_Model *\
Maximize
Total_Cost: 96 SDMC_0_1_0_0 + 288 SDMC_0_2_0_0 + 384 SDMC_0_3_0_0
 + 96 SDMC_0_4_0_0 + 672 SDMC_0_5_0_0 + 192 SDMC_0_6_0_0 + 96 SDMC_0_7_0_0
 + 576 SDMC_1_2_0_0 + 384 SDMC_1_3_0_0 + 96 SDMC_1_4_0_0 + 288 SDMC_1_5_0_0
 + 192 SDMC_1_6_0_0 + 96 SDMC_1_7_0_0 + 1056 SDMC_2_3_0_0 + 384 SDMC_2_4_0_0
 + 864 SDMC_2_5_0_0 + 576 SDMC_2_6_0_0 + 288 SDMC_2_7_0_0 + 192 SDMC_3_4_0_0
 + 1152 SDMC_3_5_0_0 + 768 SDMC_3_6_0_0 + 384 SDMC_3_7_0_0 + 288 SDMC_4_5_0_0
 + 192 SDMC_4_6_0_0 + 96 SDMC_4_7_0_0 + 1152 SDMC_5_6_0_0 + 576 SDMC_5_7_0_0
 + 672 SDMC_6_7_0_0
Subject To
Igual_Probes_'1',_'2',_'3',_'5'__0_1_4_1: SDMC_0_1_4_1 - SDMC_1_5_0_0 = 0
Igual_Probes_'1',_'2',_'3'__0_1_2_2: SDMC_0_1_2_2 - SDMC_1_3_0_0 = 0
Igual_Probes_'1',_'2',_'3'__0_1_6_1: SDMC_0_1_6_1 - SDMC_1_3_0_0 = 0
Igual_Probes_'1',_'2'__0_1_1_3: SDMC_0_1_1_3 - SDMC_1_2_0_0 = 0
Igual_Probes_'1',_'2'__0_1_3_2: SDMC_0_1_3_2 - SDMC_1_2_0_0 = 0
Igual_Probes_'1',_'2'__0_1_5_2: SDMC_0_1_5_2 - SDMC_1_2_0_0 = 0
Igual_Probes_'1',_'2'__0_1_7_1: SDMC_0_1_7_1 - SDMC_1_2_0_0 = 0
Igual_Probes_'2',_'3',_'5',_'6',_'7'__1_7_8_1: SDMC_1_7_8_1 - SDMC_2_7_0_0 = 0
Igual_Probes_'2',_'3',_'5',_'6',_'7'__4_7_8_1: - SDMC_2_7_0_0 + SDMC_4_7_8_1
 = 0
Igual_Probes_'2',_'3',_'5',_'6'__1_6_4_1: SDMC_1_6_4_1 - SDMC_2_6_0_0 = 0
Igual_Probes_'2',_'3',_'5',_'6'__1_7_7_1: SDMC_1_7_7_1 - SDMC_2_6_0_0 = 0
Igual_Probes_'2',_'3',_'5',_'6'__4_6_4_1: - SDMC_2_6_0_0 + SDMC_4_6_4_1 = 0
Igual_Probes_'2',_'3',_'5',_'6'__4_7_7_1: - SDMC_2_6_0_0 + SDMC_4_7_7_1 = 0
Igual_Probes_'2',_'3',_'5'__0_1_3_1: SDMC_0_1_3_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__0_2_2_1: SDMC_0_2_2_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__0_4_3_1: SDMC_0_4_3_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__1_5_2_1: SDMC_1_5_2_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__1_6_3_1: SDMC_1_6_3_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__1_7_5_1: SDMC_1_7_5_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__1_7_6_1: SDMC_1_7_6_1 - SDMC_2_5_0_0 = 0
Igual_Probes_'2',_'3',_'5'__4_5_2_1: - SDMC_2_5_0_0 + SDMC_4_5_2_1 = 0
Igual_Probes_'2',_'3',_'5'__4_6_3_1: - SDMC_2_5_0_0 + SDMC_4_6_3_1 = 0
Igual_Probes_'2',_'3',_'5'__4_7_5_1: - SDMC_2_5_0_0 + SDMC_4_7_5_1 = 0
Igual_Probes_'2',_'3',_'5'__4_7_6_1: - SDMC_2_5_0_0 + SDMC_4_7_6_1 = 0
Igual_Probes_'2',_'3'__0_1_1_2: SDMC_0_1_1_2 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__0_1_5_1: SDMC_0_1_5_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__0_2_1_2: SDMC_0_2_1_2 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__0_2_3_1: SDMC_0_2_3_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__0_4_1_2: SDMC_0_4_1_2 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__0_4_5_1: SDMC_0_4_5_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_3_1_1: SDMC_1_3_1_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_5_1_1: SDMC_1_5_1_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_6_1_1: SDMC_1_6_1_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_6_2_1: SDMC_1_6_2_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_7_1_1: SDMC_1_7_1_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_7_2_1: SDMC_1_7_2_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_7_3_1: SDMC_1_7_3_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__1_7_4_1: SDMC_1_7_4_1 - SDMC_2_3_0_0 = 0
Igual_Probes_'2',_'3'__4_5_1_1: - SDMC_2_3_0_0 + SDMC_4_5_1_1 = 0
Igual_Probes_'2',_'3'__4_6_1_1: - SDMC_2_3_0_0 + SDMC_4_6_1_1 = 0
Igual_Probes_'2',_'3'__4_6_2_1: - SDMC_2_3_0_0 + SDMC_4_6_2_1 = 0
Igual_Probes_'2',_'3'__4_7_1_1: - SDMC_2_3_0_0 + SDMC_4_7_1_1 = 0
Igual_Probes_'2',_'3'__4_7_2_1: - SDMC_2_3_0_0 + SDMC_4_7_2_1 = 0
Igual_Probes_'2',_'3'__4_7_3_1: - SDMC_2_3_0_0 + SDMC_4_7_3_1 = 0
Igual_Probes_'2',_'3'__4_7_4_1: - SDMC_2_3_0_0 + SDMC_4_7_4_1 = 0
Igual_Probes_'2',_'4'__0_4_1_3: SDMC_0_4_1_3 - SDMC_2_4_0_0 = 0
Igual_Probes_'2',_'4'__0_4_3_2: SDMC_0_4_3_2 - SDMC_2_4_0_0 = 0
Igual_Probes_'2',_'4'__0_4_5_2: SDMC_0_4_5_2 - SDMC_2_4_0_0 = 0
Igual_Probes_'2',_'4'__0_4_7_1: SDMC_0_4_7_1 - SDMC_2_4_0_0 = 0
Igual_Probes_'2',_'4'__1_4_1_1: SDMC_1_4_1_1 - SDMC_2_4_0_0 = 0
Igual_Probes_'2',_'4'__3_4_1_1: - SDMC_2_4_0_0 + SDMC_3_4_1_1 = 0
Igual_Probes_'3',_'2',_'4'__0_4_2_2: SDMC_0_4_2_2 - SDMC_3_4_0_0 = 0
Igual_Probes_'3',_'2',_'4'__0_4_6_1: SDMC_0_4_6_1 - SDMC_3_4_0_0 = 0
Igual_Probes_'3',_'5',_'6',_'7'__1_7_12_1: SDMC_1_7_12_1 - SDMC_3_7_0_0 = 0
Igual_Probes_'3',_'5',_'6',_'7'__1_7_4_2: SDMC_1_7_4_2 - SDMC_3_7_0_0 = 0
Igual_Probes_'3',_'5',_'6',_'7'__2_7_4_1: SDMC_2_7_4_1 - SDMC_3_7_0_0 = 0
Igual_Probes_'3',_'5',_'6',_'7'__4_7_12_1: - SDMC_3_7_0_0 + SDMC_4_7_12_1 = 0
Igual_Probes_'3',_'5',_'6',_'7'__4_7_4_2: - SDMC_3_7_0_0 + SDMC_4_7_4_2 = 0
Igual_Probes_'3',_'5',_'6'__1_6_2_2: SDMC_1_6_2_2 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__1_6_6_1: SDMC_1_6_6_1 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__1_7_11_1: SDMC_1_7_11_1 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__1_7_3_2: SDMC_1_7_3_2 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__2_6_2_1: SDMC_2_6_2_1 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__2_7_3_1: SDMC_2_7_3_1 - SDMC_3_6_0_0 = 0
Igual_Probes_'3',_'5',_'6'__4_6_2_2: - SDMC_3_6_0_0 + SDMC_4_6_2_2 = 0
Igual_Probes_'3',_'5',_'6'__4_6_6_1: - SDMC_3_6_0_0 + SDMC_4_6_6_1 = 0
Igual_Probes_'3',_'5',_'6'__4_7_11_1: - SDMC_3_6_0_0 + SDMC_4_7_11_1 = 0
Igual_Probes_'3',_'5',_'6'__4_7_3_2: - SDMC_3_6_0_0 + SDMC_4_7_3_2 = 0
Igual_Probes_'3',_'5'__0_1_1_1: SDMC_0_1_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__0_1_2_1: SDMC_0_1_2_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__0_2_1_1: SDMC_0_2_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__0_3_1_1: SDMC_0_3_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__0_4_1_1: SDMC_0_4_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__0_4_2_1: SDMC_0_4_2_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_5_1_2: SDMC_1_5_1_2 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_5_3_1: SDMC_1_5_3_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_6_1_2: SDMC_1_6_1_2 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_6_5_1: SDMC_1_6_5_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_7_10_1: SDMC_1_7_10_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_7_1_2: SDMC_1_7_1_2 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_7_2_2: SDMC_1_7_2_2 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__1_7_9_1: SDMC_1_7_9_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__2_5_1_1: SDMC_2_5_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__2_6_1_1: SDMC_2_6_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__2_7_1_1: SDMC_2_7_1_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__2_7_2_1: SDMC_2_7_2_1 - SDMC_3_5_0_0 = 0
Igual_Probes_'3',_'5'__4_5_1_2: - SDMC_3_5_0_0 + SDMC_4_5_1_2 = 0
Igual_Probes_'3',_'5'__4_5_3_1: - SDMC_3_5_0_0 + SDMC_4_5_3_1 = 0
Igual_Probes_'3',_'5'__4_6_1_2: - SDMC_3_5_0_0 + SDMC_4_6_1_2 = 0
Igual_Probes_'3',_'5'__4_6_5_1: - SDMC_3_5_0_0 + SDMC_4_6_5_1 = 0
Igual_Probes_'3',_'5'__4_7_10_1: - SDMC_3_5_0_0 + SDMC_4_7_10_1 = 0
Igual_Probes_'3',_'5'__4_7_1_2: - SDMC_3_5_0_0 + SDMC_4_7_1_2 = 0
Igual_Probes_'3',_'5'__4_7_2_2: - SDMC_3_5_0_0 + SDMC_4_7_2_2 = 0
Igual_Probes_'3',_'5'__4_7_9_1: - SDMC_3_5_0_0 + SDMC_4_7_9_1 = 0
Igual_Probes_'4',_'2',_'3',_'5'__0_4_4_1: SDMC_0_4_4_1 - SDMC_4_5_0_0 = 0
Igual_Probes_'5',_'6',_'7'__0_7_2_1: SDMC_0_7_2_1 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__1_7_10_2: SDMC_1_7_10_2 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__1_7_14_1: SDMC_1_7_14_1 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__1_7_2_3: SDMC_1_7_2_3 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__1_7_6_2: SDMC_1_7_6_2 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__2_7_2_2: SDMC_2_7_2_2 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__2_7_6_1: SDMC_2_7_6_1 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__3_7_2_1: SDMC_3_7_2_1 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__4_7_10_2: SDMC_4_7_10_2 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__4_7_14_1: SDMC_4_7_14_1 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__4_7_2_3: SDMC_4_7_2_3 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6',_'7'__4_7_6_2: SDMC_4_7_6_2 - SDMC_5_7_0_0 = 0
Igual_Probes_'5',_'6'__0_6_1_1: SDMC_0_6_1_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__0_7_1_1: SDMC_0_7_1_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_6_1_3: SDMC_1_6_1_3 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_6_3_2: SDMC_1_6_3_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_6_5_2: SDMC_1_6_5_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_6_7_1: SDMC_1_6_7_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_7_13_1: SDMC_1_7_13_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_7_1_3: SDMC_1_7_1_3 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_7_5_2: SDMC_1_7_5_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__1_7_9_2: SDMC_1_7_9_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__2_6_1_2: SDMC_2_6_1_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__2_6_3_1: SDMC_2_6_3_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__2_7_1_2: SDMC_2_7_1_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__2_7_5_1: SDMC_2_7_5_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__3_6_1_1: SDMC_3_6_1_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__3_7_1_1: SDMC_3_7_1_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_6_1_3: SDMC_4_6_1_3 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_6_3_2: SDMC_4_6_3_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_6_5_2: SDMC_4_6_5_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_6_7_1: SDMC_4_6_7_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_7_13_1: SDMC_4_7_13_1 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_7_1_3: SDMC_4_7_1_3 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_7_5_2: SDMC_4_7_5_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'5',_'6'__4_7_9_2: SDMC_4_7_9_2 - SDMC_5_6_0_0 = 0
Igual_Probes_'6',_'7'__0_7_1_2: SDMC_0_7_1_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__0_7_3_1: SDMC_0_7_3_1 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_11_2: SDMC_1_7_11_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_13_2: SDMC_1_7_13_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_15_1: SDMC_1_7_15_1 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_1_4: SDMC_1_7_1_4 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_3_3: SDMC_1_7_3_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_5_3: SDMC_1_7_5_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_7_2: SDMC_1_7_7_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__1_7_9_3: SDMC_1_7_9_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__2_7_1_3: SDMC_2_7_1_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__2_7_3_2: SDMC_2_7_3_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__2_7_5_2: SDMC_2_7_5_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__2_7_7_1: SDMC_2_7_7_1 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__3_7_1_2: SDMC_3_7_1_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__3_7_3_1: SDMC_3_7_3_1 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_11_2: SDMC_4_7_11_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_13_2: SDMC_4_7_13_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_15_1: SDMC_4_7_15_1 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_1_4: SDMC_4_7_1_4 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_3_3: SDMC_4_7_3_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_5_3: SDMC_4_7_5_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_7_2: SDMC_4_7_7_2 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__4_7_9_3: SDMC_4_7_9_3 - SDMC_6_7_0_0 = 0
Igual_Probes_'6',_'7'__5_7_1_1: SDMC_5_7_1_1 - SDMC_6_7_0_0 = 0
Max_Probes_Link0_5: SDMC_0_5_0_0 <= 3
Max_Probes_Link1_2: SDMC_1_2_0_0 <= 10
Max_Probes_Link2_3: SDMC_2_3_0_0 <= 3
Max_Probes_Link2_4: SDMC_2_4_0_0 <= 10
Max_Probes_Link3_5: SDMC_3_5_0_0 <= 10
Max_Probes_Link5_6: SDMC_5_6_0_0 <= 10
Max_Probes_Link6_7: SDMC_6_7_0_0 <= 10
Max_Probes_Router0: SDMC_0_1_0_0 + SDMC_0_2_0_0 + SDMC_0_3_0_0 + SDMC_0_4_0_0
 + SDMC_0_5_0_0 + SDMC_0_6_0_0 + SDMC_0_7_0_0 <= 1
Max_Probes_Router1: SDMC_1_0_0_0 + SDMC_1_2_0_0 + SDMC_1_3_0_0 + SDMC_1_4_0_0
 + SDMC_1_5_0_0 + SDMC_1_6_0_0 + SDMC_1_7_0_0 <= 1
Max_Probes_Router2: SDMC_2_0_0_0 + SDMC_2_1_0_0 + SDMC_2_3_0_0 + SDMC_2_4_0_0
 + SDMC_2_5_0_0 + SDMC_2_6_0_0 + SDMC_2_7_0_0 <= 3
Max_Probes_Router3: SDMC_3_0_0_0 + SDMC_3_1_0_0 + SDMC_3_2_0_0 + SDMC_3_4_0_0
 + SDMC_3_5_0_0 + SDMC_3_6_0_0 + SDMC_3_7_0_0 <= 2
Max_Probes_Router4: SDMC_4_0_0_0 + SDMC_4_1_0_0 + SDMC_4_2_0_0 + SDMC_4_3_0_0
 + SDMC_4_5_0_0 + SDMC_4_6_0_0 + SDMC_4_7_0_0 <= 1
Max_Probes_Router5: SDMC_5_0_0_0 + SDMC_5_1_0_0 + SDMC_5_2_0_0 + SDMC_5_3_0_0
 + SDMC_5_4_0_0 + SDMC_5_6_0_0 + SDMC_5_7_0_0 <= 3
Max_Probes_Router6: SDMC_6_0_0_0 + SDMC_6_1_0_0 + SDMC_6_2_0_0 + SDMC_6_3_0_0
 + SDMC_6_4_0_0 + SDMC_6_5_0_0 + SDMC_6_7_0_0 <= 2
Max_Probes_Router7: SDMC_7_0_0_0 + SDMC_7_1_0_0 + SDMC_7_2_0_0 + SDMC_7_3_0_0
 + SDMC_7_4_0_0 + SDMC_7_5_0_0 + SDMC_7_6_0_0 <= 1
Binaries
SDMC_0_1_0_0
SDMC_0_1_1_1
SDMC_0_1_1_2
SDMC_0_1_1_3
SDMC_0_1_2_1
SDMC_0_1_2_2
SDMC_0_1_3_1
SDMC_0_1_3_2
SDMC_0_1_4_1
SDMC_0_1_5_1
SDMC_0_1_5_2
SDMC_0_1_6_1
SDMC_0_1_7_1
SDMC_0_2_0_0
SDMC_0_2_1_1
SDMC_0_2_1_2
SDMC_0_2_2_1
SDMC_0_2_3_1
SDMC_0_3_0_0
SDMC_0_3_1_1
SDMC_0_4_0_0
SDMC_0_4_1_1
SDMC_0_4_1_2
SDMC_0_4_1_3
SDMC_0_4_2_1
SDMC_0_4_2_2
SDMC_0_4_3_1
SDMC_0_4_3_2
SDMC_0_4_4_1
SDMC_0_4_5_1
SDMC_0_4_5_2
SDMC_0_4_6_1
SDMC_0_4_7_1
SDMC_0_5_0_0
SDMC_0_6_0_0
SDMC_0_6_1_1
SDMC_0_7_0_0
SDMC_0_7_1_1
SDMC_0_7_1_2
SDMC_0_7_2_1
SDMC_0_7_3_1
SDMC_1_0_0_0
SDMC_1_2_0_0
SDMC_1_3_0_0
SDMC_1_3_1_1
SDMC_1_4_0_0
SDMC_1_4_1_1
SDMC_1_5_0_0
SDMC_1_5_1_1
SDMC_1_5_1_2
SDMC_1_5_2_1
SDMC_1_5_3_1
SDMC_1_6_0_0
SDMC_1_6_1_1
SDMC_1_6_1_2
SDMC_1_6_1_3
SDMC_1_6_2_1
SDMC_1_6_2_2
SDMC_1_6_3_1
SDMC_1_6_3_2
SDMC_1_6_4_1
SDMC_1_6_5_1
SDMC_1_6_5_2
SDMC_1_6_6_1
SDMC_1_6_7_1
SDMC_1_7_0_0
SDMC_1_7_10_1
SDMC_1_7_10_2
SDMC_1_7_11_1
SDMC_1_7_11_2
SDMC_1_7_12_1
SDMC_1_7_13_1
SDMC_1_7_13_2
SDMC_1_7_14_1
SDMC_1_7_15_1
SDMC_1_7_1_1
SDMC_1_7_1_2
SDMC_1_7_1_3
SDMC_1_7_1_4
SDMC_1_7_2_1
SDMC_1_7_2_2
SDMC_1_7_2_3
SDMC_1_7_3_1
SDMC_1_7_3_2
SDMC_1_7_3_3
SDMC_1_7_4_1
SDMC_1_7_4_2
SDMC_1_7_5_1
SDMC_1_7_5_2
SDMC_1_7_5_3
SDMC_1_7_6_1
SDMC_1_7_6_2
SDMC_1_7_7_1
SDMC_1_7_7_2
SDMC_1_7_8_1
SDMC_1_7_9_1
SDMC_1_7_9_2
SDMC_1_7_9_3
SDMC_2_0_0_0
SDMC_2_1_0_0
SDMC_2_3_0_0
SDMC_2_4_0_0
SDMC_2_5_0_0
SDMC_2_5_1_1
SDMC_2_6_0_0
SDMC_2_6_1_1
SDMC_2_6_1_2
SDMC_2_6_2_1
SDMC_2_6_3_1
SDMC_2_7_0_0
SDMC_2_7_1_1
SDMC_2_7_1_2
SDMC_2_7_1_3
SDMC_2_7_2_1
SDMC_2_7_2_2
SDMC_2_7_3_1
SDMC_2_7_3_2
SDMC_2_7_4_1
SDMC_2_7_5_1
SDMC_2_7_5_2
SDMC_2_7_6_1
SDMC_2_7_7_1
SDMC_3_0_0_0
SDMC_3_1_0_0
SDMC_3_2_0_0
SDMC_3_4_0_0
SDMC_3_4_1_1
SDMC_3_5_0_0
SDMC_3_6_0_0
SDMC_3_6_1_1
SDMC_3_7_0_0
SDMC_3_7_1_1
SDMC_3_7_1_2
SDMC_3_7_2_1
SDMC_3_7_3_1
SDMC_4_0_0_0
SDMC_4_1_0_0
SDMC_4_2_0_0
SDMC_4_3_0_0
SDMC_4_5_0_0
SDMC_4_5_1_1
SDMC_4_5_1_2
SDMC_4_5_2_1
SDMC_4_5_3_1
SDMC_4_6_0_0
SDMC_4_6_1_1
SDMC_4_6_1_2
SDMC_4_6_1_3
SDMC_4_6_2_1
SDMC_4_6_2_2
SDMC_4_6_3_1
SDMC_4_6_3_2
SDMC_4_6_4_1
SDMC_4_6_5_1
SDMC_4_6_5_2
SDMC_4_6_6_1
SDMC_4_6_7_1
SDMC_4_7_0_0
SDMC_4_7_10_1
SDMC_4_7_10_2
SDMC_4_7_11_1
SDMC_4_7_11_2
SDMC_4_7_12_1
SDMC_4_7_13_1
SDMC_4_7_13_2
SDMC_4_7_14_1
SDMC_4_7_15_1
SDMC_4_7_1_1
SDMC_4_7_1_2
SDMC_4_7_1_3
SDMC_4_7_1_4
SDMC_4_7_2_1
SDMC_4_7_2_2
SDMC_4_7_2_3
SDMC_4_7_3_1
SDMC_4_7_3_2
SDMC_4_7_3_3
SDMC_4_7_4_1
SDMC_4_7_4_2
SDMC_4_7_5_1
SDMC_4_7_5_2
SDMC_4_7_5_3
SDMC_4_7_6_1
SDMC_4_7_6_2
SDMC_4_7_7_1
SDMC_4_7_7_2
SDMC_4_7_8_1
SDMC_4_7_9_1
SDMC_4_7_9_2
SDMC_4_7_9_3
SDMC_5_0_0_0
SDMC_5_1_0_0
SDMC_5_2_0_0
SDMC_5_3_0_0
SDMC_5_4_0_0
SDMC_5_6_0_0
SDMC_5_7_0_0
SDMC_5_7_1_1
SDMC_6_0_0_0
SDMC_6_1_0_0
SDMC_6_2_0_0
SDMC_6_3_0_0
SDMC_6_4_0_0
SDMC_6_5_0_0
SDMC_6_7_0_0
SDMC_7_0_0_0
SDMC_7_1_0_0
SDMC_7_2_0_0
SDMC_7_3_0_0
SDMC_7_4_0_0
SDMC_7_5_0_0
SDMC_7_6_0_0
End
