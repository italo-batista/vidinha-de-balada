
DROP DATABASE IF EXISTS vidinha_balada;

CREATE DATABASE vidinha_balada;

USE vidinha_balada;

CREATE TABLE deputado (

	id VARCHAR(7) NOT NULL,
	nome VARCHAR(40),
	partidoAtual VARCHAR(15),
	uf CHAR(2),
	foto VARCHAR(60),
	twitter VARCHAR(20),
	telefone VARCHAR(15),
	email VARCHAR(30),
	PRIMARY KEY (id)
);

CREATE TABLE sessoesMes (

	mes INT(2),
	ano INT(4),
	quantidadeSessoes INT,
	PRIMARY KEY (mes, ano)
);


CREATE TABLE empresas (

	cnpj VARCHAR(15),
	nome VARCHAR(20),
	id VARCHAR(10),

  PRIMARY KEY (id),
	CONSTRAINT unique_obs UNIQUE (cnpj, nome)
);


CREATE TABLE cotas (

	uf CHAR(2),
	cota FLOAT,
	PRIMARY KEY(uf)
);

CREATE TABLE sessoesMesDeputado (

	mes INT(2),
	ano INT(4),
	idDeputado VARCHAR(7) NOT NULL,
	quantidadeParticipacoes INT,
	
	PRIMARY KEY (mes, ano, idDeputado),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
);

CREATE TABLE emendasPropostasDeputado (

	mes INT(2),
	ano INT(4),
	idDeputado VARCHAR(7) NOT NULL,
	quantidade INT,
	
	PRIMARY KEY (mes, ano, idDeputado),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
);


CREATE TABLE gastos (

	idDeputado VARCHAR(7) NOT NULL,
	anoEmissao INT,
	mesEmissao INT,
	cnpj VARCHAR(20),
	nomeFornecedor VARCHAR(15) NOT NULL,
	nomeCategoria VARCHAR(30) NOT NULL,
	valor FLOAT,
	id VARCHAR(10)
	
	PRIMARY KEY (id),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
);

CREATE TABLE selosDeputado (

	idDeputado VARCHAR(7) NOT NULL,
	mes INT(2),
	ano INT(4),
	idCategoria VARCHAR(10) NOT NULL,

	PRIMARY KEY (idDeputado, mes, ano, idCategoria),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
);
