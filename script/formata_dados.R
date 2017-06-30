library(readr)
library(dplyr)
options(scipen = 50)


cria_tabela_final_mensal = function(dados){
  # antes de usar essa funcao o data frame dados deve estar no formato gerado pela
  # funcao prepara_tabela_final

  tabela_final_mensal = dados %>%
    filter(vlrLiquido > 0) %>%
    select(txNomeParlamentar, idecadastro, sgUF,  ano, mes, vlrLiquido) %>%
    group_by(txNomeParlamentar, idecadastro, sgUF, ano, mes) %>%
    summarise(total = sum(vlrLiquido)) %>%
    na.omit() %>%
    inner_join(cotas) %>%
    mutate(coef = total/cota_mensal)

  return(tabela_final_mensal)

}

cria_tabela_final_categoria = function(dados){
  # antes de usar essa funcao o data frame dados deve estar no formato gerado pela
  # funcao prepara_tabela_final

  tabela_final_categoria = dados %>%
    filter(vlrLiquido > 0) %>%
    select(txNomeParlamentar, idecadastro, sgUF, ano, mes, nossas_categorias, vlrLiquido) %>%
    group_by(txNomeParlamentar, idecadastro, sgUF, ano, mes, nossas_categorias) %>%
    summarise(total = sum(vlrLiquido)) %>%
    na.omit() %>%
    inner_join(cotas) %>%
    mutate(coef = total/cota_mensal)

  return(tabela_final_categoria)
}

cria_tabela_final_votacoes = function(votacoes){

  votacoes = votacoes %>%
    group_by(id_dep) %>%
    mutate(nome = first(nome))

  sessoes = votacoes %>%
    filter(anov > 2014) %>%
    group_by(anov, mesv, diav) %>%
    distinct() %>%
    group_by(anov, mesv) %>%
    summarise(total_mes = n())

  tabela_final_votacoes = votacoes %>%
    filter(anov > 2014) %>%
    group_by(nome, id_dep, uf, anov, mesv, diav) %>%
    distinct() %>%
    group_by(nome, id_dep, uf, anov, mesv) %>%
    summarise(total_deputado = n()) %>%
    inner_join(sessoes) %>%
    mutate(coef = total_deputado/total_mes)

  return(tabela_final_votacoes)

}

cria_tabela_gastos_presenca = function(tabela_final_votacoes, tabela_final_mensal){

  names(tabela_final_mensal) = c("nome", "id", "uf", "ano", "mes", "total_gasto", "cota_mensal", "coef_gasto")
  names(tabela_final_votacoes) = c("nome", "id", "uf","ano", "mes", "total_presenca", "total_mes", "coef_presenca")

  sessoes = votacoes %>%
    filter(anov > 2014) %>%
    group_by(anov, mesv, diav) %>%
    distinct() %>%
    group_by(anov, mesv) %>%
    summarise(total_mes = n())

  tabela_gasto_presenca = tabela_final_mensal %>%
                          full_join(tabela_final_votacoes[,2:8])

  tabela_gasto_presenca$total_presenca[is.na(tabela_gasto_presenca$total_presenca)] = 0
  tabela_gasto_presenca$coef_presenca[is.na(tabela_gasto_presenca$coef_presenca)] = 0

  names(sessoes) = c("ano", "mes", "total_presenca_mes")

  tabela_gasto_presenca = tabela_gasto_presenca %>%
                          left_join(sessoes)
  tabela_gasto_presenca$total_presenca_mes[is.na(tabela_gasto_presenca$total_presenca_mes)] = 0
  tabela_gasto_presenca$total_mes = tabela_gasto_presenca$total_presenca_mes
  tabela_gasto_presenca = tabela_gasto_presenca %>%
                          ungroup() %>%
                          select(-total_presenca_mes)

  return(tabela_gasto_presenca)
}

cria_tabela_gasto_total_anos = function(tabela_final_mensal) {

  names(tabela_final_mensal) = c("nome", "id", "uf", "ano", "mes", "total_gasto", "cota_mensal", "coef_gasto")

  gasto_total_anos = tabela_final_mensal %>%
                    ungroup() %>%
                    group_by(ano) %>%
                    summarise(total_gasto = sum(total_gasto),
                              total_disponivel = sum(cota_mensal))

  return(gasto_total_anos)
}

cria_tabela_6_gastos = function(dados){

  tabela_6_gastos = dados %>%
                              select(idecadastro, txNomeParlamentar ) %>%
                              group_by(idecadastro, txNomeParlamentar) %>%
                              distinct()

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Alimentação") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise(Alimentação = sum(vlrLiquido)))

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Combustíveis") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise("Combustíveis" = sum(vlrLiquido)))

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Locação de veículos") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise("Locação de veículos" = sum(vlrLiquido)))

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Passagens aéreas") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise("Passagens aéreas" = sum(vlrLiquido)))

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Escritório") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise(Escritório = sum(vlrLiquido)))

  tabela_6_gastos = tabela_6_gastos %>%
                    left_join(dados %>% filter(nossas_categorias == "Divulgação de atividade parlamentar") %>%
                                group_by(idecadastro, txNomeParlamentar) %>%
                                summarise("Divulgação de atividade parlamentar" = sum(vlrLiquido)))

  tabela_6_gastos[is.na(tabela_6_gastos)] = 0

  tabela_6_gastos$total = rowSums(tabela_6_gastos[,3:8] )

  return(tabela_6_gastos)

}

cria_top_estourados_estado = function(estado, tabela_final_mensal) {

  estourados = tabela_final_mensal%>%
    ungroup() %>%
    filter (sgUF == estado) %>%
    arrange(-coef) %>%
    slice(1:10)

  return(estourados)

}

cria_top_estourados = function(tabela_final_mensal) {

  estourados = tabela_final_mensal%>%
    ungroup() %>%
    arrange(-coef) %>%
    slice(1:10)

  return(estourados)

}
