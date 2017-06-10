library(readr)
library(dplyr)


le_cria_dados_completos = function(path){
  votos = read_csv(paste(path, "votacoes.csv"))
  
  ano_2010 = read_delim(paste(path, "Ano-2010.csv", delim=";"))
  ano_2011 = read_delim(paste(path, "Ano-2011.csv", delim=";"))
  ano_2012 = read_delim(paste(path, "Ano-2012.csv", delim=";"))
  ano_2013 = read_delim(paste(path, "Ano-2013.csv", delim=";"))
  ano_2014 = read_delim(paste(path, "Ano-2014.csv", delim=";"))
  ano_2015 = read_delim(paste(path, "Ano-2015.csv", delim=";"))
  ano_2016 = read_delim(paste(path, "Ano-2016.csv", delim=";"))
  ano_2017 = read_delim(paste(path, "Ano-2017.csv", delim=";"))
  
  dados_completos = ano_2010 %>%
                    rbind(ano_2011,
                          ano_2012,
                          ano_2013,
                          ano_2014,
                          ano_2015,
                          ano_2016,
                          ano_2017)
  
  return(dados_completos)
}

cria_novas_categorias = function(dados_completos){
  dados_completos$nossas_categorias = NA
  
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR"] = "Escritório"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "SERVIÇOS POSTAIS"] = "Serviços Postais"
  dados_completos$nossas_categorias[dados_completos$txtDescricao %in% c("LOCAÇÃO OU FRETAMENTO DE VEÍCULOS AUTOMOTORES", "LOCAÇÃO OU FRETAMENTO DE AERONAVES", "LOCAÇÃO OU FRETAMENTO DE EMBARCAÇÕES", "LOCAÇÃO DE VEÍCULOS AUTOMOTORES OU FRETAMENTO DE EMBARCAÇÕES")] = "Locação de veículos"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "COMBUSTÍVEIS E LUBRIFICANTES."] = "Combustíveis"
  dados_completos$nossas_categorias[dados_completos$txtDescricao %in% c("PASSAGENS AÉREAS", "Emissão Bilhete Aéreo")] = "Passagens aéreas"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "TELEFONIA"] = "Telefonia"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR."] = "Divulgação de atividade parlamentar"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR"] = "Alimentação"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL."] = "Hospedagem"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "SERVIÇO DE TÁXI, PEDÁGIO E ESTACIONAMENTO"] = "Locomoção"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "CONSULTORIAS, PESQUISAS E TRABALHOS TÉCNICOS."] = "Consultoria"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "ASSINATURA DE PUBLICAÇÕES"] = "Revistas/Jornais"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "TELEFONIA"] = "Telefonia"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "SERVIÇO DE SEGURANÇA PRESTADO POR EMPRESA ESPECIALIZADA."] = "Segurança particular"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "PASSAGENS TERRESTRES, MARÍTIMAS OU FLUVIAIS"] = "Passagens (exceto aéreas)"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "PARTICIPAÇÃO EM CURSO, PALESTRA OU EVENTO SIMILAR"] = "Cursos e palestras"
  
  return(dados_completos)
}


