library(readr)
library(dplyr)

dados = read_csv("gasto_mensal_por_deputado.csv", col_names = TRUE)

um_ponto = dados %>%
  group_by(txNomeParlamentar) %>% 
  summarise(N = n()) %>%
  filter(N < 10)

dados = dados %>% filter(txNomeParlamentar %in% um_ponto$txNomeParlamentar)

filtro = dados %>% group_by(txNomeParlamentar) %>% summarise(total = sum(total))
filtro = as.data.frame(filtro)
filtro = filtro[ order( filtro[,"total"]), ]

min_sum = min(filtro$total)
max_sum = max(filtro$total)
#med_sum = median(filtro$total)

sem_min = filtro %>% filter(total != min_sum)
med_sum = median(sem_min$total)

strategy_values = c(min_sum, med_sum, max_sum)
strategy_name = filtro %>% filter(total %in% strategy_values)
filtrados = dados %>% filter(txNomeParlamentar %in% strategy_name$txNomeParlamentar)

write.table(filtrados, file = "mais_dps_2016.csv", row.names=FALSE, col.names=TRUE, sep=",")