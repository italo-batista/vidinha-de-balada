
DROP DATABASE IF EXISTS vidinha_balada;

CREATE DATABASE vidinha_balada
  CHARACTER SET utf8
  COLLATE utf8_general_ci;

USE vidinha_balada;

CREATE TABLE deputado (

	id VARCHAR(7) NOT NULL,
	nome VARCHAR(40),
	partidoAtual VARCHAR(15),
	uf CHAR(2),
	foto VARCHAR(60),
	twitter VARCHAR(20),
	telefone VARCHAR(15),
	email VARCHAR(50),
	sexo VARCHAR(20),
	PRIMARY KEY (id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE sessoesMes (

	mes INT(2),
	ano INT(4),
	quantidadeSessoes INT,
	PRIMARY KEY (mes, ano)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE empresas (

	cnpj VARCHAR(20),
	nome VARCHAR(60),
	idEmpresa VARCHAR(10),
	PRIMARY KEY (idEmpresa),
	CONSTRAINT unique_obs UNIQUE (cnpj, nome)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE cotas (

	uf CHAR(2),
	cota FLOAT,
	PRIMARY KEY(uf)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE sessoesMesDeputado (

	mes INT(2),
	ano INT(4),
	idDeputado VARCHAR(7) NOT NULL,
	quantidadeParticipacoes INT,

	PRIMARY KEY (mes, ano, idDeputado),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE emendasPropostasDeputado (

	mes INT(2),
	ano INT(4),
	idDeputado VARCHAR(7) NOT NULL,
	quantidade INT,

	PRIMARY KEY (mes, ano, idDeputado),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE gastos (

	idDeputado VARCHAR(7) NOT NULL,
	anoEmissao INT,
	mesEmissao INT,
	idEmpresa VARCHAR(10),
	cnpj VARCHAR(20),
	nomeFornecedor VARCHAR(60) NOT NULL,
	nomeCategoria VARCHAR(40) NOT NULL,
	valor FLOAT,
	id VARCHAR(10),

	PRIMARY KEY (id),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE selosDeputado (

	idDeputado VARCHAR(7) NOT NULL,
	mes INT(2),
	ano INT(4),
	idCategoria VARCHAR(40) NOT NULL,

	PRIMARY KEY (idDeputado, mes, ano, idCategoria),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE usuariosInscritos (

	idCadastro INT(4) NOT NULL AUTO_INCREMENT,
	nome VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
	idDeputado VARCHAR(7) NOT NULL,

	PRIMARY KEY (idCadastro),
	FOREIGN KEY (idDeputado) REFERENCES deputado(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


CREATE TABLE selosCota (

	id INT(4) NOT NULL AUTO_INCREMENT,
	idDeputado VARCHAR(7) NOT NULL,
	ano VARCHAR(4) NOT NULL,
	mes VARCHAR(4) NOT NULL,
	selo VARCHAR(10) NOT NULL,

	PRIMARY KEY (id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE selosPresenca (

	id INT(4) NOT NULL AUTO_INCREMENT,
	idDeputado VARCHAR(7) NOT NULL,
	mes VARCHAR(4) NOT NULL,	
	ano VARCHAR(4) NOT NULL,
	selo VARCHAR(10) NOT NULL,

	PRIMARY KEY (id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

