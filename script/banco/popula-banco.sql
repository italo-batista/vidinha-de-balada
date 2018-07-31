USE vidinha_balada;

load data local infile '/home/ubuntu/vidinha-de-balada/data/cota_por_estado.csv' into table cotas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (uf, cota);


load data local infile '/home/ubuntu/vidinha-de-balada/data/1-tabela_final_votacoes.csv' into table sessoesMesDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, idDeputado, quantidadeParticipacoes);


load data local infile '/home/ubuntu/vidinha-de-balada/data/2-sessoes_mensal.csv' into table sessoesMes fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, quantidadeSessoes);


load data local infile '/home/ubuntu/vidinha-de-balada/data/3-empresas.csv' into table empresas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (cnpj, nome, idEmpresa);


load data local infile '/home/ubuntu/vidinha-de-balada/data/4-tabela_gastos_empresas.csv' into table gastos fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, anoEmissao, mesEmissao, idEmpresa, cnpj, nomeFornecedor, nomeCategoria, valor, id);


load data local infile '/home/ubuntu/vidinha-de-balada/data/5-tabela_info_deputados.csv' into table deputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (id, nome, partidoAtual, uf, foto, twitter, telefone, email);


load data local infile '/home/ubuntu/vidinha-de-balada/data/6-ganhadores_selos.csv' into table selosDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, mes, ano, idCategoria);


load data local infile '/home/ubuntu/vidinha-de-balada/data/7-tabela_selos_presencas.csv' into table selosPresenca fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, mes, ano, selo);


load data local infile '/home/ubuntu/vidinha-de-balada/data/8-tabela_selos_cota.csv' into table selosCota fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, ano, mes, selo);



