library(readr)
library(dplyr)

dados_t = read_csv("gasto_mensal_por_deputado.csv", col_names = TRUE)

dados = dados %>% filter(ano > 2016)

filtro = dados %>% group_by(txNomeParlamentar) %>% summarise(total = sum(total))
filtro = as.data.frame(filtro)
filtro = filtro[ order( filtro[,"total"]), ]
filtro = filtro %>% filter(total > 177225.5)

filtrados = filter( dados_t%txNomeParlamentar %in% filtro$txNomeParlamentar )

write.table(filtrado, file = "mais_dps_2016.csv", row.names=FALSE, col.names=TRUE, sep=",")