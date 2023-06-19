\* Probes_Placement_Model *\
Minimize
Total_Cost_and_Difference: Medicao_0 + Medicao_1 + Medicao_105 + Medicao_106
 + Medicao_108 + Medicao_110 + Medicao_114 + Medicao_122 + Medicao_13
 + Medicao_130 + Medicao_146 + Medicao_147 + Medicao_148 + Medicao_149
 + Medicao_151 + Medicao_153 + Medicao_157 + Medicao_187 + Medicao_188
 + Medicao_190 + Medicao_194 + Medicao_198 + Medicao_206 + Medicao_21
 + Medicao_222 + Medicao_29 + Medicao_3 + Medicao_30 + Medicao_32 + Medicao_34
 + Medicao_38 + Medicao_46 + Medicao_5 + Medicao_54 + Medicao_70 + Medicao_71
 + Medicao_72 + Medicao_73 + Medicao_75 + Medicao_79 + Medicao_83 + Medicao_9
 + diferenca_carga_roteador0 + diferenca_carga_roteador1
 + diferenca_carga_roteador2 + diferenca_carga_roteador4
 + diferenca_carga_roteador5 + diferenca_carga_roteador7
Subject To
Carga_Maior_Roteador0: Medicao_0 + Medicao_1 + Medicao_13 + Medicao_21
 + Medicao_3 + Medicao_5 + Medicao_9 + diferenca_carga_roteador0 >= 0
Carga_Maior_Roteador1: Medicao_29 + Medicao_30 + Medicao_32 + Medicao_34
 + Medicao_38 + Medicao_46 + Medicao_54 + diferenca_carga_roteador1 >= 0
Carga_Maior_Roteador2: Medicao_70 + Medicao_71 + Medicao_72 + Medicao_73
 + Medicao_75 + Medicao_79 + Medicao_83 + diferenca_carga_roteador2 >= 0
Carga_Maior_Roteador4: Medicao_105 + Medicao_106 + Medicao_108 + Medicao_110
 + Medicao_114 + Medicao_122 + Medicao_130 + diferenca_carga_roteador4 >= 0
Carga_Maior_Roteador5: Medicao_146 + Medicao_147 + Medicao_148 + Medicao_149
 + Medicao_151 + Medicao_153 + Medicao_157 + diferenca_carga_roteador5 >= 0
Carga_Maior_Roteador7: Medicao_187 + Medicao_188 + Medicao_190 + Medicao_194
 + Medicao_198 + Medicao_206 + Medicao_222 + diferenca_carga_roteador7 >= 0
Carga_Menor_Roteador0: Medicao_0 + Medicao_1 + Medicao_13 + Medicao_21
 + Medicao_3 + Medicao_5 + Medicao_9 - diferenca_carga_roteador0 <= 1
Carga_Menor_Roteador1: Medicao_29 + Medicao_30 + Medicao_32 + Medicao_34
 + Medicao_38 + Medicao_46 + Medicao_54 - diferenca_carga_roteador1 <= 1
Carga_Menor_Roteador2: Medicao_70 + Medicao_71 + Medicao_72 + Medicao_73
 + Medicao_75 + Medicao_79 + Medicao_83 - diferenca_carga_roteador2 <= 1
Carga_Menor_Roteador4: Medicao_105 + Medicao_106 + Medicao_108 + Medicao_110
 + Medicao_114 + Medicao_122 + Medicao_130 - diferenca_carga_roteador4 <= 1
Carga_Menor_Roteador5: Medicao_146 + Medicao_147 + Medicao_148 + Medicao_149
 + Medicao_151 + Medicao_153 + Medicao_157 - diferenca_carga_roteador5 <= 1
Carga_Menor_Roteador7: Medicao_187 + Medicao_188 + Medicao_190 + Medicao_194
 + Medicao_198 + Medicao_206 + Medicao_222 - diferenca_carga_roteador7 <= 1
Composicao107_105: - Medicao_105 + Medicao_107 <= 0
Composicao107_70: Medicao_107 - Medicao_70 <= 0
Composicao10_0: - Medicao_0 + Medicao_10 <= 0
Composicao10_147: Medicao_10 - Medicao_147 <= 0
Composicao10_187: Medicao_10 - Medicao_187 <= 0
Composicao111_105: - Medicao_105 + Medicao_111 <= 0
Composicao111_146: Medicao_111 - Medicao_146 <= 0
Composicao111_70: Medicao_111 - Medicao_70 <= 0
Composicao115_105: - Medicao_105 + Medicao_115 <= 0
Composicao115_146: Medicao_115 - Medicao_146 <= 0
Composicao115_147: Medicao_115 - Medicao_147 <= 0
Composicao115_70: Medicao_115 - Medicao_70 <= 0
Composicao131_105: - Medicao_105 + Medicao_131 <= 0
Composicao131_146: Medicao_131 - Medicao_146 <= 0
Composicao131_147: Medicao_131 - Medicao_147 <= 0
Composicao131_187: Medicao_131 - Medicao_187 <= 0
Composicao131_70: Medicao_131 - Medicao_70 <= 0
Composicao14_0: - Medicao_0 + Medicao_14 <= 0
Composicao14_146: Medicao_14 - Medicao_146 <= 0
Composicao14_70: Medicao_14 - Medicao_70 <= 0
Composicao14_71: Medicao_14 - Medicao_71 <= 0
Composicao152_147: - Medicao_147 + Medicao_152 <= 0
Composicao152_187: Medicao_152 - Medicao_187 <= 0
Composicao191_146: - Medicao_146 + Medicao_191 <= 0
Composicao191_147: - Medicao_147 + Medicao_191 <= 0
Composicao191_187: - Medicao_187 + Medicao_191 <= 0
Composicao22_0: - Medicao_0 + Medicao_22 <= 0
Composicao22_146: - Medicao_146 + Medicao_22 <= 0
Composicao22_70: Medicao_22 - Medicao_70 <= 0
Composicao22_72: Medicao_22 - Medicao_72 <= 0
Composicao2_0: - Medicao_0 + Medicao_2 <= 0
Composicao2_146: - Medicao_146 + Medicao_2 <= 0
Composicao31_29: - Medicao_29 + Medicao_31 <= 0
Composicao31_70: Medicao_31 - Medicao_70 <= 0
Composicao33_29: - Medicao_29 + Medicao_33 <= 0
Composicao33_71: Medicao_33 - Medicao_71 <= 0
Composicao35_146: - Medicao_146 + Medicao_35 <= 0
Composicao35_29: - Medicao_29 + Medicao_35 <= 0
Composicao35_70: Medicao_35 - Medicao_70 <= 0
Composicao39_146: - Medicao_146 + Medicao_39 <= 0
Composicao39_147: - Medicao_147 + Medicao_39 <= 0
Composicao39_29: - Medicao_29 + Medicao_39 <= 0
Composicao39_70: Medicao_39 - Medicao_70 <= 0
Composicao4_0: - Medicao_0 + Medicao_4 <= 0
Composicao4_147: - Medicao_147 + Medicao_4 <= 0
Composicao55_146: - Medicao_146 + Medicao_55 <= 0
Composicao55_147: - Medicao_147 + Medicao_55 <= 0
Composicao55_187: - Medicao_187 + Medicao_55 <= 0
Composicao55_29: - Medicao_29 + Medicao_55 <= 0
Composicao55_70: Medicao_55 - Medicao_70 <= 0
Composicao6_0: - Medicao_0 + Medicao_6 <= 0
Composicao6_146: - Medicao_146 + Medicao_6 <= 0
Composicao6_70: Medicao_6 - Medicao_70 <= 0
Composicao74_146: - Medicao_146 + Medicao_74 <= 0
Composicao74_70: - Medicao_70 + Medicao_74 <= 0
Composicao76_146: - Medicao_146 + Medicao_76 <= 0
Composicao76_147: - Medicao_147 + Medicao_76 <= 0
Composicao76_70: - Medicao_70 + Medicao_76 <= 0
Composicao84_146: - Medicao_146 + Medicao_84 <= 0
Composicao84_147: - Medicao_147 + Medicao_84 <= 0
Composicao84_187: - Medicao_187 + Medicao_84 <= 0
Composicao84_70: - Medicao_70 + Medicao_84 <= 0
Minimo_Sondas_Medicao_0ou148: Medicao_0 + Medicao_148 >= 1
Minimo_Sondas_Medicao_106ou94: Medicao_106 + Medicao_107 + Medicao_93
 + Medicao_94 >= 1
Minimo_Sondas_Medicao_110ou156: Medicao_110 + Medicao_111 + Medicao_112
 + Medicao_113 + Medicao_153 + Medicao_154 + Medicao_155 + Medicao_156 >= 1
Minimo_Sondas_Medicao_114ou178: Medicao_114 + Medicao_115 + Medicao_116
 + Medicao_117 + Medicao_118 + Medicao_119 + Medicao_120 + Medicao_121
 + Medicao_171 + Medicao_172 + Medicao_173 + Medicao_174 + Medicao_175
 + Medicao_176 + Medicao_177 + Medicao_178 >= 1
Minimo_Sondas_Medicao_130ou221: Medicao_130 + Medicao_131 + Medicao_132
 + Medicao_133 + Medicao_134 + Medicao_135 + Medicao_136 + Medicao_137
 + Medicao_138 + Medicao_139 + Medicao_140 + Medicao_141 + Medicao_142
 + Medicao_143 + Medicao_144 + Medicao_145 + Medicao_206 + Medicao_207
 + Medicao_208 + Medicao_209 + Medicao_210 + Medicao_211 + Medicao_212
 + Medicao_213 + Medicao_214 + Medicao_215 + Medicao_216 + Medicao_217
 + Medicao_218 + Medicao_219 + Medicao_220 + Medicao_221 >= 1
Minimo_Sondas_Medicao_13ou129: Medicao_122 + Medicao_123 + Medicao_124
 + Medicao_125 + Medicao_126 + Medicao_127 + Medicao_128 + Medicao_129
 + Medicao_13 + Medicao_14 + Medicao_15 + Medicao_16 + Medicao_17 + Medicao_18
 + Medicao_19 + Medicao_20 >= 1
Minimo_Sondas_Medicao_146ou92: Medicao_146 + Medicao_92 >= 1
Minimo_Sondas_Medicao_147ou161: Medicao_147 + Medicao_161 >= 1
Minimo_Sondas_Medicao_151ou189: Medicao_151 + Medicao_152 + Medicao_188
 + Medicao_189 >= 1
Minimo_Sondas_Medicao_187ou162: Medicao_162 + Medicao_187 >= 1
Minimo_Sondas_Medicao_190ou104: Medicao_101 + Medicao_102 + Medicao_103
 + Medicao_104 + Medicao_190 + Medicao_191 + Medicao_192 + Medicao_193 >= 1
Minimo_Sondas_Medicao_1ou100: Medicao_1 + Medicao_100 + Medicao_2 + Medicao_99
 >= 1
Minimo_Sondas_Medicao_21ou53: Medicao_21 + Medicao_22 + Medicao_23
 + Medicao_24 + Medicao_25 + Medicao_26 + Medicao_27 + Medicao_28 + Medicao_46
 + Medicao_47 + Medicao_48 + Medicao_49 + Medicao_50 + Medicao_51 + Medicao_52
 + Medicao_53 >= 1
Minimo_Sondas_Medicao_29ou72: Medicao_29 + Medicao_72 >= 1
Minimo_Sondas_Medicao_30ou96: Medicao_30 + Medicao_31 + Medicao_95
 + Medicao_96 >= 1
Minimo_Sondas_Medicao_32ou109: Medicao_108 + Medicao_109 + Medicao_32
 + Medicao_33 >= 1
Minimo_Sondas_Medicao_34ou160: Medicao_157 + Medicao_158 + Medicao_159
 + Medicao_160 + Medicao_34 + Medicao_35 + Medicao_36 + Medicao_37 >= 1
Minimo_Sondas_Medicao_38ou186: Medicao_179 + Medicao_180 + Medicao_181
 + Medicao_182 + Medicao_183 + Medicao_184 + Medicao_185 + Medicao_186
 + Medicao_38 + Medicao_39 + Medicao_40 + Medicao_41 + Medicao_42 + Medicao_43
 + Medicao_44 + Medicao_45 >= 1
Minimo_Sondas_Medicao_3ou166: Medicao_165 + Medicao_166 + Medicao_3
 + Medicao_4 >= 1
Minimo_Sondas_Medicao_54ou237: Medicao_222 + Medicao_223 + Medicao_224
 + Medicao_225 + Medicao_226 + Medicao_227 + Medicao_228 + Medicao_229
 + Medicao_230 + Medicao_231 + Medicao_232 + Medicao_233 + Medicao_234
 + Medicao_235 + Medicao_236 + Medicao_237 + Medicao_54 + Medicao_55
 + Medicao_56 + Medicao_57 + Medicao_58 + Medicao_59 + Medicao_60 + Medicao_61
 + Medicao_62 + Medicao_63 + Medicao_64 + Medicao_65 + Medicao_66 + Medicao_67
 + Medicao_68 + Medicao_69 >= 1
Minimo_Sondas_Medicao_5ou82: Medicao_5 + Medicao_6 + Medicao_7 + Medicao_79
 + Medicao_8 + Medicao_80 + Medicao_81 + Medicao_82 >= 1
Minimo_Sondas_Medicao_70ou91: Medicao_70 + Medicao_91 >= 1
Minimo_Sondas_Medicao_71ou105: Medicao_105 + Medicao_71 >= 1
Minimo_Sondas_Medicao_73ou150: Medicao_149 + Medicao_150 + Medicao_73
 + Medicao_74 >= 1
Minimo_Sondas_Medicao_75ou170: Medicao_167 + Medicao_168 + Medicao_169
 + Medicao_170 + Medicao_75 + Medicao_76 + Medicao_77 + Medicao_78 >= 1
Minimo_Sondas_Medicao_83ou205: Medicao_198 + Medicao_199 + Medicao_200
 + Medicao_201 + Medicao_202 + Medicao_203 + Medicao_204 + Medicao_205
 + Medicao_83 + Medicao_84 + Medicao_85 + Medicao_86 + Medicao_87 + Medicao_88
 + Medicao_89 + Medicao_90 >= 1
Minimo_Sondas_Medicao_9ou197: Medicao_10 + Medicao_11 + Medicao_12
 + Medicao_194 + Medicao_195 + Medicao_196 + Medicao_197 + Medicao_9 >= 1
Roteador_Sem_Medicao3: Medicao_101 + Medicao_91 + Medicao_92 + Medicao_93
 + Medicao_95 + Medicao_97 + Medicao_99 = 0
Roteador_Sem_Medicao6: Medicao_161 + Medicao_162 + Medicao_163 + Medicao_165
 + Medicao_167 + Medicao_171 + Medicao_179 = 0
Binaries
Medicao_0
Medicao_1
Medicao_10
Medicao_100
Medicao_101
Medicao_102
Medicao_103
Medicao_104
Medicao_105
Medicao_106
Medicao_107
Medicao_108
Medicao_109
Medicao_11
Medicao_110
Medicao_111
Medicao_112
Medicao_113
Medicao_114
Medicao_115
Medicao_116
Medicao_117
Medicao_118
Medicao_119
Medicao_12
Medicao_120
Medicao_121
Medicao_122
Medicao_123
Medicao_124
Medicao_125
Medicao_126
Medicao_127
Medicao_128
Medicao_129
Medicao_13
Medicao_130
Medicao_131
Medicao_132
Medicao_133
Medicao_134
Medicao_135
Medicao_136
Medicao_137
Medicao_138
Medicao_139
Medicao_14
Medicao_140
Medicao_141
Medicao_142
Medicao_143
Medicao_144
Medicao_145
Medicao_146
Medicao_147
Medicao_148
Medicao_149
Medicao_15
Medicao_150
Medicao_151
Medicao_152
Medicao_153
Medicao_154
Medicao_155
Medicao_156
Medicao_157
Medicao_158
Medicao_159
Medicao_16
Medicao_160
Medicao_161
Medicao_162
Medicao_163
Medicao_165
Medicao_166
Medicao_167
Medicao_168
Medicao_169
Medicao_17
Medicao_170
Medicao_171
Medicao_172
Medicao_173
Medicao_174
Medicao_175
Medicao_176
Medicao_177
Medicao_178
Medicao_179
Medicao_18
Medicao_180
Medicao_181
Medicao_182
Medicao_183
Medicao_184
Medicao_185
Medicao_186
Medicao_187
Medicao_188
Medicao_189
Medicao_19
Medicao_190
Medicao_191
Medicao_192
Medicao_193
Medicao_194
Medicao_195
Medicao_196
Medicao_197
Medicao_198
Medicao_199
Medicao_2
Medicao_20
Medicao_200
Medicao_201
Medicao_202
Medicao_203
Medicao_204
Medicao_205
Medicao_206
Medicao_207
Medicao_208
Medicao_209
Medicao_21
Medicao_210
Medicao_211
Medicao_212
Medicao_213
Medicao_214
Medicao_215
Medicao_216
Medicao_217
Medicao_218
Medicao_219
Medicao_22
Medicao_220
Medicao_221
Medicao_222
Medicao_223
Medicao_224
Medicao_225
Medicao_226
Medicao_227
Medicao_228
Medicao_229
Medicao_23
Medicao_230
Medicao_231
Medicao_232
Medicao_233
Medicao_234
Medicao_235
Medicao_236
Medicao_237
Medicao_24
Medicao_25
Medicao_26
Medicao_27
Medicao_28
Medicao_29
Medicao_3
Medicao_30
Medicao_31
Medicao_32
Medicao_33
Medicao_34
Medicao_35
Medicao_36
Medicao_37
Medicao_38
Medicao_39
Medicao_4
Medicao_40
Medicao_41
Medicao_42
Medicao_43
Medicao_44
Medicao_45
Medicao_46
Medicao_47
Medicao_48
Medicao_49
Medicao_5
Medicao_50
Medicao_51
Medicao_52
Medicao_53
Medicao_54
Medicao_55
Medicao_56
Medicao_57
Medicao_58
Medicao_59
Medicao_6
Medicao_60
Medicao_61
Medicao_62
Medicao_63
Medicao_64
Medicao_65
Medicao_66
Medicao_67
Medicao_68
Medicao_69
Medicao_7
Medicao_70
Medicao_71
Medicao_72
Medicao_73
Medicao_74
Medicao_75
Medicao_76
Medicao_77
Medicao_78
Medicao_79
Medicao_8
Medicao_80
Medicao_81
Medicao_82
Medicao_83
Medicao_84
Medicao_85
Medicao_86
Medicao_87
Medicao_88
Medicao_89
Medicao_9
Medicao_90
Medicao_91
Medicao_92
Medicao_93
Medicao_94
Medicao_95
Medicao_96
Medicao_97
Medicao_99
diferenca_carga_roteador0
diferenca_carga_roteador1
diferenca_carga_roteador2
diferenca_carga_roteador4
diferenca_carga_roteador5
diferenca_carga_roteador7
End
