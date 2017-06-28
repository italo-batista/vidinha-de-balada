
library(dplyr)

# http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/dados-abertos-cota-parlamentar
urlCamara <- "http://www.camara.leg.br/cotas/"


# Download e descompactacao dos dados do site da Camara dos Deputados
# Verba - Cota de Exercicio para Atividade Parlamentar
download.ano = function() {
  gastos2014 <- "Ano-2014.csv.zip"
  download.file(url = paste(urlCamara, "Ano-2014.csv.zip", sep = ""), destfile = gastos2014,
                mode='wb', cacheOK=FALSE)
  unzip(gastos2014)
   
  gastos2015 <- "Ano-2015.csv.zip"
  download.file(url = paste(urlCamara, "Ano-2015.csv.zip", sep = ""), destfile = gastos2015,
                mode='wb', cacheOK=FALSE)
  unzip(gastos2015)
  
  gastos2016 <- "Ano-2016.csv.zip"
  download.file(url = paste(urlCamara, "Ano-2016.csv.zip", sep = ""), destfile = gastos2016,
                mode='wb', cacheOK=FALSE)
  unzip(gastos2016)
  
  gastos2017 <- "Ano-2017.csv.zip"
  download.file(url = paste(urlCamara, "Ano-2017.csv.zip", sep = ""), destfile = gastos2017,
                mode='wb', cacheOK=FALSE)
  unzip(gastos2017)
}
# download.ano()



# Leitura e organizacao dos dados baixados
leitura.concat = function() {
  gastos2014 <- read.csv("Ano-2014.csv", sep = ";")
  gastos2015 <- read.csv("Ano-2015.csv", sep = ";")
  gastos2016 <- read.csv("Ano-2016.csv", sep = ";")
  gastos2017 <- read.csv("Ano-2017.csv", sep = ";")
  
  # return(rbind(gastos2014, gastos2015, gastos2016, gastos2017))
  
  gastoMandato = gastos2014 %>%
    rbind(gastos2015,
          gastos2016,
          gastos2017)
  
  return(gastoMandato)
  
}
# gastoMandato <- leitura.concat()


novas.categorias = function(gastoMandato){
  gastoMandato$nossas_categorias = NA

  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR"] = "Escritório"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "SERVIÇOS POSTAIS"] = "Serviços Postais"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao %in% c("LOCAÇÃO OU FRETAMENTO DE VEÍCULOS AUTOMOTORES", "LOCAÇÃO OU FRETAMENTO DE AERONAVES", "LOCAÇÃO OU FRETAMENTO DE EMBARCAÇÕES", "LOCAÇÃO DE VEÍCULOS AUTOMOTORES OU FRETAMENTO DE EMBARCAÇÕES")] = "Locação de veículos"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "COMBUSTÍVEIS E LUBRIFICANTES."] = "Combustíveis"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao %in% c("PASSAGENS AÉREAS", "Emissão Bilhete Aéreo")] = "Passagens aéreas"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "TELEFONIA"] = "Telefonia"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR."] = "Divulgação de atividade parlamentar"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR"] = "Alimentação"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL."] = "Hospedagem"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "SERVIÇO DE TÁXI, PEDÁGIO E ESTACIONAMENTO"] = "Locomoção"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "CONSULTORIAS, PESQUISAS E TRABALHOS TÉCNICOS."] = "Consultoria"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "ASSINATURA DE PUBLICAÇÕES"] = "Revistas/Jornais"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "TELEFONIA"] = "Telefonia"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "SERVIÇO DE SEGURANÇA PRESTADO POR EMPRESA ESPECIALIZADA."] = "Segurança particular"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "PASSAGENS TERRESTRES, MARÍTIMAS OU FLUVIAIS"] = "Passagens (exceto aéreas)"
  gastoMandato$nossas_categorias[gastoMandato$txtDescricao == "PARTICIPAÇÃO EM CURSO, PALESTRA OU EVENTO SIMILAR"] = "Cursos e palestras"
  
  return(gastoMandato)
}


# write.csv(gastoMandato, file = "gastosMandato.csv", row.names = FALSE)
