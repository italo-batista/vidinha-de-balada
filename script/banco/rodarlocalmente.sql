USE vidinha_balada;

load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/script/tabela_info_deputados.csv' into table deputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (id, nome, partidoAtual, uf, foto, twitter, telefone, email);


load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/script/empresas.csv' into table empresas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (cnpj, nome, idEmpresa);


load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/script/sessoes_mensal.csv' into table sessoesMes fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, quantidadeSessoes);


load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/data/final/cota_por_estado.csv' into table cotas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (uf, cota);


load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/script/tabela_final_votacoes.csv' into table sessoesMesDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, idDeputado, quantidadeParticipacoes);


load data local infile '/home/leticiawanderley/Documents/Projects/vidinha-de-balada/script/tabela_gastos_empresas.csv' into table gastos fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, anoEmissao, mesEmissao, cnpj, nomeFornecedor, nomeCategoria, idEmpresa, valor, id);


/*
load data local infile 'xxx' into table emendasPropostasDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (mes, ano, idDeputado, quantidade);


load data local infile 'xxx' into table selosDeputado fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
    (idDeputado, mes, ano, idCategoria);
*/
