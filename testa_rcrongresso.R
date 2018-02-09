install.packages("rcongresso")

vignette("introducao-rcongresso", package="rcongresso")
vignette("purrr-e-rcongresso", package="rcongresso")

library(rcongresso)
library(dplyr)
library(jsonlite)


get_all_proposicoes = function() {
  require(jsonlite)

  first_link = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio=2015-01-01&pagina=1&itens=100"
  temp = fromJSON(first_link)
  last_link = temp$links[4, 2]
  next_link = temp$links[2, 2]
  
  df = data.frame()
  df = rbind(df, temp$dados)
  
  while (next_link != last_link) {
    temp = fromJSON(next_link)
    df = rbind(df, temp$dados)
    last_link = temp$links[4, 2]
    next_link = temp$links[2, 2]
    last_link = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio=2015-01-01&pagina=10&itens=100"
    
  }
  
  temp = fromJSON(next_link)
  df = rbind(df, temp$dados)
  
  # alguns dados de proposições vêm com ano = 0
  df = df %>%
    filter(ano != 0)
  
  return(df)
}

get_all_votacoes = function(ids_proposicoes) {
  require(jsonlite)
  
  all_votacoes = data.frame(id = numeric())
  
  for (id in ids_proposicoes) {
    query = paste(paste("https://dadosabertos.camara.leg.br/api/v2/proposicoes/", id, sep=""), "/votacoes", sep="")
    votacao = fromJSON(query)
    all_votacoes = rbind(all_votacoes, votacao$dados$id, row.names=NULL)
  }
  
  return(all_votacoes)
}

proposicoes = get_all_proposicoes()

m_votacoes = get_all_votacoes(proposicoes$id)
m_votacoes = m_votacoes %>%
  mutate(id = X100000367L) %>%
  select(id)


