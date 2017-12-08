#! /bin/bash

# geracao dos arquivos para o banco
Rscript gera_csvs.R > "log/geracao.log"

mysql "vidinha_balada" < "banco/vidinha-banco.sql" > "log/criacaobanco.log"
mysql "vidinha_balada" < "banco/popula-banco.sql" > "log/popula.log"
