
DROP DATABASE IF EXISTS vidinha_balada;

CREATE DATABASE vidinha_balada;

USE vidinha_balada;


CREATE TABLE deputado (

	id VARCHAR(7) NOT NULL,
	nome VARCHAR(30),
	partidoAtual VARCHAR(20),
	uf CHAR(2),
	foto VARCHAR(30),
	twitter VARCHAR(10),
	telefone VARCHAR(15),
	email VARCHAR(20),
	PRIMARY KEY (id)
);

CREATE TABLE sessoesMes (

	mes INT(2),
	ano INT(4),
	quantidadeSessoes INT,
	PRIMARY KEY (mes, ano)
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

	idDocumento VARCHAR(10) NOT NULL,
	idDeputado VARCHAR(7) NOT NULL,
	mesEmissao INT,
	anoEmissao INT,
	idCategoria VARCHAR(10) NOT NULL,
	nomeFornecedor VARCHAR(15) NOT NULL,
	valor FLOAT,
	cnpj VARCHAR(15),

	PRIMARY KEY (idDocumento),
	CONSTRAINT unique_obs UNIQUE (idDeputado, mesEmissao, anoEmissao, idCategoria),
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

		
CREATE TABLE empresas (

	cnpj VARCHAR(15),
	nome VARCHAR(10),

	CONSTRAINT unique_obs UNIQUE (cnpj, nome)
);


CREATE TABLE cotas (

	uf CHAR(2),
	cota FLOAT,
	PRIMARY KEY(uf)
);
