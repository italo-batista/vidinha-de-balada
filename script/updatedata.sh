#! /bin/bash

# geracao dos arquivos para o banco
Rscript gera_csvs.R

mysql -u root -p vidasofrida vidinha_balada < /banco/vidinha-banco.sql
mysql -u root -p vidasofrida vidinha_balada < /banco/popula-banco.sql
