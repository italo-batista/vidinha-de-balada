library(readr)
library(dplyr)

# dados = read_csv("dados-gerais-2015-2017.csv")
# cotas = read_delim("valor-cota-por-estado.csv", delim = ";")
# votacoes = read_csv("votacoes2.csv")

formata_cota_mensal = function(cotas){

  cota_mensal = c(44632.46,
                  40944.10,
                  43570.12, 
                  43374.78,
                  39010.85, 
                  42451.77, 
                  30788.66, 
                  37423.91, 
                  35507.06, 
                  42151.69,
                  36092.71,
                  40542.84,
                  39428.03,
                  42227.45,
                  42032.56,
                  41676.80,
                  40971.77,
                  38871.86,
                  35759.97,
                  42731.99,
                  43672.49,
                  45612.53,
                  40875.90,
                  39877.78,
                  40139.26,
                  37043.53,
                  39503.61)
  
  cotas$cota_mensal = cota_mensal
  names(cotas) = c("sgUF", "cota_mensal")
  return(cotas)

}

prepara_tabela_final = function(dados){

  dados$ano = as.numeric(format(as.Date(dados$datEmissao), "%Y"))
  dados$mes = as.numeric(format(as.Date(dados$datEmissao), "%m"))
  dados$vlrLiquido = gsub(",", ".", dados$vlrLiquido) %>% 
    as.numeric()
  
  return(dados)
}

cria_tabela_final_mensal = function(dados){
 # antes de usar essa funcao o data frame dados deve estar no formato gerado pela
  # funcao prepara_tabela_final
  
  tabela_final_mensal = dados %>%
    filter(vlrLiquido > 0) %>%
    select(txNomeParlamentar, idecadastro, sgUF, ano, mes, vlrLiquido) %>%
    group_by(txNomeParlamentar, idecadastro, sgUF, ano, mes) %>%
    summarise(total = sum(vlrLiquido)) %>%
    na.omit() %>%
    inner_join(cotas) %>%
    mutate(coef = total/cota_mensal)
  
  return(tabela_final_mensal)
  
}

cira_tabela_final_categoria = function(dados){
  # antes de usar essa funcao o data frame dados deve estar no formato gerado pela
  # funcao prepara_tabela_final
  
  tabela_final_categoria = dados %>%
    filter(vlrLiquido > 0) %>%
    select(txNomeParlamentar, idecadastro, sgUF, ano, mes, nossas_categorias, codNossas_categorias, vlrLiquido) %>%
    group_by(txNomeParlamentar, idecadastro, sgUF, ano, mes, nossas_categorias, codNossas_categorias) %>%
    summarise(total = sum(vlrLiquido)) %>%
    na.omit() %>%
    inner_join(cotas) %>%
    mutate(coef = total/cota_mensal)
  
  return(tabela_final_categoria)
}

cria_tabela_final_votacoes = function(votacoes){
  
  sessoes = votacoes %>%
    filter(anov > 2014) %>%
    group_by(anov, mesv, diav) %>%
    distinct()
  
  sessoes = sessoes %>%
    group_by(anov, mesv) %>%
    summarise(total_mes = n())
  
  tabela_final_votacoes = votacoes %>%
    filter(anov > 2014) %>%
    group_by(nome, id_dep, anov, mesv, diav) %>%
    distinct() %>%
    group_by(nome, id_dep, anov, mesv) %>%
    summarise(total_deputado = n()) %>%
    inner_join(sessoes) %>%
    mutate(coef = total_deputado/total_mes)
  
  return(tabela_final_votacoes)
  
}



















