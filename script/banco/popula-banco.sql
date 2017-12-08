USE vidinha_balada;

load data local infile '../../data/dados_gerados/tabela_info_deputados.csv' into table deputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (id, nome, partidoAtual, uf, foto, twitter, telefone, email);


load data local infile '../../data/dados_gerados/empresas.csv' into table empresas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (cnpj, nome, idEmpresa);


load data local infile '../../data/dados_gerados/sessoes_mensal.csv' into table sessoesMes fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, quantidadeSessoes);


load data local infile '../../data/final/cota_por_estado.csv' into table cotas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (uf, cota);


load data local infile '../../data/dados_gerados/tabela_final_votacoes.csv' into table sessoesMesDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, idDeputado, quantidadeParticipacoes);


load data local infile '../../data/dados_gerados/tabela_gastos_empresas.csv' into table gastos fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, anoEmissao, mesEmissao, idEmpresa, cnpj, nomeFornecedor, nomeCategoria, valor, id);

load data local infile '../../data/dados_gerados/ganhadores_selos.csv' into table selosDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, mes, ano, idCategoria);


load data local infile '../../data/dados_gerados/tabela_selos_cota.csv' into table selosCota fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, ano, mes, selo);


load data local infile '../../data/dados_gerados/tabela_selos_presencas.csv' into table selosPresenca fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, mes, ano, selo);
