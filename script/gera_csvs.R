source("formata_dados.R")
source("prepara_gastos.R")
options(scipen = 50)

library(readr)

dados_gastos = cria_data_frame_2015_2017() %>% filter(nuLegislatura > 2014, !is.na(numMes), !is.na(numAno))
cotas = read_csv("../data/final/cota_por_estado.csv")
#votacoes = read_csv("../data/final/votacoes2.csv")
votacoes = read_csv("https://raw.githubusercontent.com/nazareno/dados-da-camara-federal/master/dados/votacoes.csv") %>%
  formata_data_votacoes()
#emendas = le_csv_zip("http://portal.convenios.gov.br/images/docs/CGSIS/csv/siconv_emenda.csv.zip", "siconv_emenda.csv")
twitter_profiles = read_csv("../data/final/twitter_profiles.csv")
info_deputados = read_csv("../data/final/infodeputados.csv")

# esse csv não gera nenhuma tabela no bd
 tabela_final_gastos = cria_tabela_final_gastos(dados_gastos)
# write.csv(tabela_final_gastos, "tabela_final_gastos.csv", row.names = F)

# tabela_final_categoria = cria_tabela_final_categoria(dados_gastos)
# write.csv(tabela_final_categoria, "tabela_final_categoria.csv", row.names = F)

# tabela_gastos_presenca = cria_tabela_gastos_presenca(tabela_final_votacoes, tabela_final_gastos)
# write.csv(tabela_gastos_presenca, "tabela_gastos_presenca.csv", row.names = F)

# esse csv não gera nenhuma tabela no bd
# tabela_gasto_total_anos = cria_tabela_gasto_total_anos(tabela_final_gastos)
# write.csv(tabela_gasto_total_anos, "tabela_gasto_total_anos.csv", row.names = F)

# tabela_6_gastos = cria_tabela_6_gastos(dados_gastos)
# write.csv(tabela_6_gastos, "tabela_6_gastos.csv", row.names = F)

# esse csv não gera nenhuma tabela no bd
 tabela_6_gastos_mensal = cria_tabela_6_gastos_mensal(dados_gastos, tabela_final_gastos)
# write.csv(tabela_6_gastos_mensal, "tabela_6_gastos_mensal.csv", row.names = F)

# top_estourados = cria_top_estourados(tabela_final_gastos)
# write.csv(top_estourados, "top_estourados.csv", row.names = F)

# for(i in 1:NROW(cotas)){
#   temp = cria_top_estourados_estado(cotas$sgUF[i], tabela_final_gastos)
#   
#   uf = cotas$sgUF[i]
#   write.csv(temp, paste("top_10_estourados_", uf, ".csv", sep=""), row.names = F)
# }

tabela_final_votacoes = cria_tabela_final_votacoes(votacoes)
write.csv(tabela_final_votacoes, "tabela_final_votacoes.csv", row.names = F)

sessoes_mensal = cria_sessoes_mensal(votacoes)
write.csv(sessoes_mensal, "sessoes_mensal.csv", row.names = F)

empresas = cria_empresas(dados_gastos)
write.csv(empresas, "empresas.csv", row.names = F)

tabela_gastos_empresas = cria_tabela_gastos_empresas(dados_gastos, empresas)
write.csv(tabela_gastos_empresas, "tabela_gastos_empresas.csv", row.names = F)

tabela_info_deputados = cria_tabela_info_deputados(info_deputados, twitter_profiles, dados_gastos)
write.csv(tabela_info_deputados, "tabela_info_deputados.csv", row.names = F)

ganhadores_selos = cria_ganhadores_selos(tabela_6_gastos_mensal, tabela_final_gastos)
write.csv(ganhadores_selos, "ganhadores_selos.csv", row.names = F)

rm(tabela_info_deputados, tabela_gastos_empresas, empresas, sessoes_mensal,tabela_final_votacoes)
#rm(tabela_6_gastos_mensal, tabela_final_gastos, tabela_gasto_total_anos, tabela_info_pessoais,twitter_profiles, dados_gastos, info_deputados, votacoes)
