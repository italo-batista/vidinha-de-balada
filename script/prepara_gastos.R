# --------
#     Este script é responsável pelo download dos arquivos do site da cãmara. 
#     Os arquivos sao baixados um a um e renomeados de acordo com seus anos.
#     A saída deste script é um dataframe contando com os gastos dos deputados nos anos baixados.
# --------


library(readr)
library(dplyr)
options(scipen = 50)

le_csv_zip = function(link, nome){
  temp = tempfile()
  download.file(link, temp)
  data = read_delim(unz(temp, nome), delim = ";" )
  unlink(temp)
  return(data)
}


prepara_tabela_final = function(dados){
  
  dados$ano = as.numeric(format(as.Date(dados$datEmissao), "%Y"))
  dados$mes = as.numeric(format(as.Date(dados$datEmissao), "%m"))
  dados$vlrLiquido = gsub(",", ".", dados$vlrLiquido) %>% 
    as.numeric()
  
  return(dados)
}

# Download dos dados do site da Camara dos Deputados.
# Cria/unifica as categorias de gastos semelhantes afim de diminuir
#   a quantidade de categorias e facilitar o entendimento.
# Leitura e organizacao em um unico objeto dos dados baixados
cria_data_frame_2015_2017 = function(){
  ano_2015 = le_csv_zip("http://www.camara.leg.br/cotas/Ano-2015.csv.zip", "Ano-2015.csv")
  ano_2016 = le_csv_zip("http://www.camara.leg.br/cotas/Ano-2016.csv.zip", "Ano-2016.csv")
  ano_2017 = le_csv_zip("http://www.camara.leg.br/cotas/Ano-2017.csv.zip", "Ano-2017.csv")
  ano_2018 = le_csv_zip("http://www.camara.leg.br/cotas/Ano-2018.csv.zip", "Ano-2018.csv")
  dados_completos = ano_2015 %>%
    rbind(ano_2016,
          ano_2017,
          ano_2018)
  
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
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "SERVIÇO DE SEGURANÇA PRESTADO POR EMPRESA ESPECIALIZADA."] = "Segurança particular"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "PASSAGENS TERRESTRES, MARÍTIMAS OU FLUVIAIS"] = "Passagens (exceto aéreas)"
  dados_completos$nossas_categorias[dados_completos$txtDescricao == "PARTICIPAÇÃO EM CURSO, PALESTRA OU EVENTO SIMILAR"] = "Cursos e palestras"
  
  dados_completos = prepara_tabela_final(dados_completos) %>%
                    filter(!is.na(idecadastro))
  
  return(dados_completos)
}


# write.csv(dados_completos, file = "gastosGerais", row.names = FALSE)
