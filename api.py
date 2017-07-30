#!/usr/bin/python
# coding: utf-8
import json
import ConfigParser
import sqlalchemy
import datetime
import sys, os
import operator
from unidecode import unidecode
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

# needed to install:
# 	sudo apt-get install python-mysqldb
#	sudo pip install mysql-python

# use this material:
# http://blog.cloudoki.com/getting-started-with-restful-apis-using-the-flask-microframework-for-python/

# other links:
#	http://www.roblayton.com/2015/04/creating-python-flask-crud-api-with.html
#	http://www.roblayton.com/2015/04/connecting-python-script-to-mysql.html
#	https://github.com/jigyasa-grover/RESTful-API-using-Python-Flask-MySQL

#oi bb
# Config --------------------------------------------------------------

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/vidinha_balada?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mysql = SQLAlchemy(app)
mysql.init_app(app)
with app.app_context():
	mysql.create_all()


reload(sys)
sys.setdefaultencoding('utf8')

def force_decode(string, codecs=['utf8', 'cp1252']):
    for i in codecs:
        try:
            return string.decode(i)
        except:
            pass

# Init ----------------------------------------------------------------

now = datetime.datetime.now()
if now.month == 1:
	mesPassado = 12
	ano = now.year - 1
else:
	mesPassado = now.month - 1
	ano = now.year

	mesPassado = 03
	ano = 2016

categoria_alimentacao = 'Alimentação'
categoria_escritorio = 'Escritório'
categoria_divulgacao = 'Divulgação de atividade parlamentar'
categoria_locacao = 'Locação de veículos'
categoria_combustivel = 'Combustíveis'
categoria_passagens = 'Passagens aéreas'

def init():
	pass

# Models --------------------------------------------------------------

class Cota(mysql.Model):
    __tablename__ = 'cotas'
    uf = mysql.Column(mysql.String(2), primary_key=True)
    cota = mysql.Column(mysql.Integer, nullable=False)

    def __init__(self, uf, cota):
        self.uf = uf
        self.cota = cota

    def __repr__(self):
        return '<Cotas (%s, %s) >' % (self.uf, self.cota)

class Deputado(mysql.Model):
    __tablename__ = 'deputado'

    id = mysql.Column(mysql.String(7), primary_key=True)
    nome = mysql.Column(mysql.String(15))
    partidoAtual = mysql.Column(mysql.String(20))
    uf = mysql.Column(mysql.String(2))
    foto = mysql.Column(mysql.String(30))
    twitter = mysql.Column(mysql.String(10))
    telefone = mysql.Column(mysql.String(15))
    email = mysql.Column(mysql.String(20))

    def __repr__(self):
        return '<Deputado (%s, %s, %s, %s, %s, %s, %s, %s) >' % (self.id, self.nome, self.partidoAtual, self.uf, self.foto, self.twitter, self.telefone, self.email)

class Gasto(mysql.Model):
    __tablename__ = 'gastos'

    idDeputado = mysql.Column(mysql.String(7), nullable=False)
    mesEmissao = mysql.Column(mysql.Integer)
    anoEmissao = mysql.Column(mysql.Integer)
    cnpj = mysql.Column(mysql.String(15))
    nomeFornecedor = mysql.Column(mysql.String(15), nullable=False)
    nomeCategoria = mysql.Column(mysql.String(10), nullable=False)
    idEmpresa = mysql.Column(mysql.String(10), nullable=False)
    valor = mysql.Column(mysql.Float)
    id = mysql.Column(mysql.String(10), primary_key=True)

    def __repr__(self):
        return '<Gasto (%s, %s, %s, %s, %s, %s, %s, %s, %s) >' % (self.idDeputado, self.mesEmissao, self.anoEmissao, self.nomeCategoria, self.nomeFornecedor, self.valor, self.cnpj, self.id, self.idEmpresa)

class SessoesMes(mysql.Model):
    __tablename__ = 'sessoesMes'

    mes = mysql.Column(mysql.Integer, primary_key=True)
    ano = mysql.Column(mysql.Integer, primary_key=True)
    quantidadeSessoes = mysql.Column(mysql.Integer)

    def __repr__(self):
        return '<SessoesMes (%s, %s, %s) >' % (self.mes, self.ano, self.quantidadeSessoes)

class SessoesMesDeputado(mysql.Model):
    __tablename__ = 'sessoesMesDeputado'

    mes = mysql.Column(mysql.Integer, primary_key=True)
    ano = mysql.Column(mysql.Integer, primary_key=True)
    idDeputado = mysql.Column(mysql.String(7), primary_key=True)
    quantidadeParticipacoes = mysql.Column(mysql.Integer)

    def __repr__(self):
        return '<SessoesMesDeputado (%s, %s, %s, %s) >' % (self.mes, self.ano, self.idDeputado, self.quantidadeParticipacoes)

class EmendasPropostasDeputado(mysql.Model):
    __tablename__ = 'emendasPropostasDeputado'

    mes = mysql.Column(mysql.Integer, primary_key=True)
    ano = mysql.Column(mysql.Integer, primary_key=True)
    idDeputado = mysql.Column(mysql.String(7), primary_key=True)
    quantidade = mysql.Column(mysql.Integer)

    def __repr__(self):
        return '<EmendasPropostasDeputado (%s, %s, %s, %s) >' % (self.mes, self.ano, self.idDeputado, self.quantidade)

class SelosDeputado(mysql.Model):
    __tablename__ = 'selosDeputado'

    idDeputado = mysql.Column(mysql.String(7), primary_key=True)
    mes = mysql.Column(mysql.Integer, primary_key=True)
    ano = mysql.Column(mysql.Integer, primary_key=True)
    idCategoria = mysql.Column(mysql.String(40), primary_key=True)

    def __repr__(self):
        return '<SelosDeputado (%s, %s, %s, %s) >' % (self.idDeputado, self.mes, self.ano, self.idCategoria)

class Empresa(mysql.Model):
    __tablename__ = 'empresas'

    cnpj = mysql.Column(mysql.String(15))
    nome = mysql.Column(mysql.String(10))
    idEmpresa = mysql.Column(mysql.Integer, primary_key=True)

    def __repr__(self):
        return '<Empresa (%s, %s, %d) >' % (self.cnpj, self.nome, self.idEmpresa)


# Routes --------------------------------------------------------------

@app.route("/")
def hello():
    return "Hello World!"

#@app.route('/gasto_anual')
#def getGasto(ano):
#	pass

gastos_anos = {}
f = open('data/gerados-hackfest/gasto_total_anos.csv')
f.readline()

for line in f:
    gasto_anual = line.split(",")
    valores = [float(gasto_anual[1]), float(gasto_anual[2])]
    gastos_anos[gasto_anual[0]] = valores

f.close()


#/gasto_anual?ano=
@app.route('/gasto_anual')
def anual():
    key =request.args.get('ano').lower()
    return json.dumps(gastos_anos[key], ensure_ascii=False).encode('utf-8')

@app.route('/cotas', methods=['GET'])
def getCotas():
    data = Cota.query.all()

    data_all = []

    for cota in data:
        data_all.append([cota.uf, cota.cota])

    return jsonify(cotas=data_all)

@app.route('/cota/<uf>', methods=['GET'])
def getCota(uf):
	cota = Cota.query.filter_by(uf=uf).first_or_404()
	data_all = [cota.uf, cota.cota]
	return jsonify(cotas=data_all)


# Perfil
def getDeputadoSelos(query_selos):
	json = []
	for selo in query_selos:
		json.append([selo.idDeputado, selo.mes, selo.ano, selo.idCategoria])
	return json

@app.route('/selosDeputado/<id>', methods=['GET'])
def getSelos(id):
	q_selos = SelosDeputado.query.filter_by(idDeputado = id).all()
	selos = getDeputadoSelos(q_selos)
	return jsonify(selos)


@app.route('/buscaDeputado', methods=['GET'])
def getDeputado():
	nome = request.args.get('nome')
	data = Deputado.query.all()

	data_all = []

	for deputado in data:
		if(unidecode(nome.upper()) in unidecode(deputado.nome.upper())):
			data_all.append({'nome' : deputado.nome, 'id': deputado.id})

	return jsonify(deputadosId=data_all)

@app.route('/empresasParceiras/<id>', methods=['GET'])
def getEmpresasParceiras(id):

	data = Gasto.query.filter_by(idDeputado = id).all()


	data_all = {}
	categorias = {}

	for gasto in data:
		chave = gasto.idEmpresa
		if(chave not in data_all.keys()):
			data_all[chave] = gasto.valor
			categorias[chave] = [gasto.nomeCategoria]
		else:
			data_all[chave] += gasto.valor
			if(gasto.nomeCategoria not in categorias[chave]):
				categorias[chave].append(gasto.nomeCategoria)

	parceiras = []
	n = 0
	while (n < 10 and len(data_all) > 0):
		max_val = max(data_all.iteritems(), key=operator.itemgetter(1))[0]
		parceiras.append({'id':max_val, 'valor': data_all[max_val], 'categorias': categorias[max_val]})
		data_all.pop(max_val)
		n += 1

	return jsonify(parceiras)

@app.route('/timelineDeputado/<id>', methods=['GET'])
def getTimelineDeputado(id):
	deputado = Deputado.query.filter_by(id=id).first()

	timeline = {}

	query_gastos = Gasto.query.filter_by(idDeputado=id).all()
	query_presencas = SessoesMesDeputado.query.filter_by(idDeputado=id).all()
	cota = Cota.query.filter_by(uf=deputado.uf).first()
	query_sessoes = SessoesMes.query.all()

	for gasto in query_gastos:
		chave = str(gasto.anoEmissao) + "/" + str(gasto.mesEmissao)
		if(chave not in timeline.keys()):
			timeline[chave] = [gasto.valor]
		else:
			timeline[chave][0] += gasto.valor

	for presenca in query_presencas:
		chave = str(presenca.ano) + "/" + str(presenca.mes)

		if(chave not in timeline.keys()):
			timeline[chave] = [0, presenca.quantidadeParticipacoes]
		else:
			timeline[chave].append(presenca.quantidadeParticipacoes)

	for sessao in query_sessoes:
		chave = str(sessao.ano) + "/" + str(sessao.mes)

		if(chave != "0/0"):
			if(chave not in timeline.keys()):
				timeline[chave] = [0,0, sessao.quantidadeSessoes, cota.cota]
			else:
				if(len(timeline[chave]) == 1):
					timeline[chave].append(0)
				timeline[chave].append(sessao.quantidadeSessoes)
				timeline[chave].append(cota.cota)

	for mes in timeline:
		if (len(timeline[mes]) == 1):
			timeline[mes].append("-")
			timeline[mes].append("-")
			timeline[mes].append(cota.cota)

	timelineDeputado = []

	for i in timeline:
		timelineDeputado.append({"data": i, "total_gasto": timeline[i][0], "total_presenca": timeline[i][1], "sessoes_total": timeline[i][2], "cota": timeline[i][3]})

	return jsonify(timelineDeputado)

def somaGastosTotais(query_gasto_categoria):
	gastoTotal = 0
	for gasto in query_gasto_categoria:
		gastoTotal = gastoTotal + gasto.valor
	return gastoTotal

def somaPresencasDeputado(query_presencas):
	presencas = 0
	for presenca in query_presencas:
		presencas = presencas + presenca.quantidadeParticipacoes
	return presencas

def somaPresencas(query_presencas):
	presencas = 0
	for presenca in query_presencas:
		presencas = presencas + presenca.quantidadeSessoes
	return presencas

@app.route('/deputados/<id>', methods=['GET'])
def getPerfilDeputado(id):

	deputado = Deputado.query.filter_by(id=id).first()
	query_gasto_alimentacao = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_alimentacao, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_gasto_escritorio = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_escritorio, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_gasto_divulgacao = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_divulgacao, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_gasto_locacao = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_locacao, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_gasto_combustivel = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_combustivel, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_gasto_passagens = Gasto.query.filter_by(idDeputado=id, nomeCategoria=categoria_passagens, mesEmissao=mesPassado, anoEmissao=ano).all()
	query_presencas_deputado = SessoesMesDeputado.query.filter_by(idDeputado=id).all()
	query_sessoes_total = SessoesMes.query.all()

	gasto_alimentacao = somaGastosTotais(query_gasto_alimentacao)
	gasto_escritorio = somaGastosTotais(query_gasto_escritorio)
	gasto_divulgacao = somaGastosTotais(query_gasto_divulgacao)
	gasto_locacao = somaGastosTotais(query_gasto_locacao)
	gasto_combustivel = somaGastosTotais(query_gasto_combustivel)
	gasto_passagens = somaGastosTotais(query_gasto_passagens)
	presencas_deputado = somaPresencasDeputado(query_presencas_deputado)
	sessoes_total = somaPresencas(query_sessoes_total)

	## o total dos gastos é a soma dos gastos das categorias anteriores ou envolvem outros gastos?
	total_gastos = gasto_alimentacao + gasto_escritorio + gasto_divulgacao + gasto_locacao + gasto_combustivel + gasto_passagens

	cota_uf = Cota.query.get(deputado.uf).cota

	json = {
	'Nome' : deputado.nome,
	'urlfoto' : deputado.foto,
	'Id' : deputado.id,
	'Partido' : deputado.partidoAtual,
	'UF' : deputado.uf,
	'Cota' : cota_uf,

	'Total gastos' : total_gastos,

	'Alimentação' : gasto_alimentacao,
	'Escritório' : gasto_escritorio,
	'Divulgação de atividade parlamentar' : gasto_divulgacao,
	'Locação de veículos' : gasto_locacao,
	'Combustível' : gasto_combustivel,
	'Passagens aéreas' : gasto_passagens
	}

	return jsonify(json)


# TOP 10

def somaGastosCategoria(query_gasto_categoria):
	gastoTotal = 0
	for gasto in query_gasto_categoria:
		gastoTotal = gastoTotal + gasto.valor
	return gastoTotal

def maisGastadores10(query_gastos):
	deputados_id = []
	gastos = []

	for gasto in query_gastos:

		if (gasto.idDeputado in deputados_id):
			index = deputados_id.index(gasto.idDeputado)
			gastos[index] = gastos[index] + gasto.valor
		else:
			deputados_id.append(gasto.idDeputado)
			gastos.append(gasto.valor)

	tam = len(deputados_id)
	deputadoGasto = []

	for i in xrange(tam):
		tupla = (gastos[i], deputados_id[i])
		deputadoGasto.append(tupla)

	tops = sorted(deputadoGasto, key=lambda x: x[0], reverse=True)
	top10 = []
	for i in range(10):
		top10.append(tops[i])

	return top10

@app.route("/top10", methods=['GET'])
def top10():
	query_gastos = Gasto.query.filter_by(mesEmissao=mesPassado, anoEmissao=ano).all()
	top10 = maisGastadores10(query_gastos)

	json = []

	for i in range(len(top10)):
		deputado = top10[i]

		# info deputado

		deputado_id = deputado[1]
		deputado_gasto_total = deputado[0]
		deputado_posicao = i + 1

		deputado_obj = Deputado.query.get(deputado_id)

		deputado_nome = deputado_obj.nome
		deputado_partido = deputado_obj.partidoAtual
		deputado_foto = deputado_obj.foto
		deputado_uf = deputado_obj.uf
		deputado_cota_uf = Cota.query.get(deputado_uf).cota

		deputado_presencas = SessoesMesDeputado.query.filter_by(idDeputado=deputado_id, mes=mesPassado, ano=ano).first().quantidadeParticipacoes
		sessoes_totais = SessoesMes.query.filter_by(mes=mesPassado, ano=ano).first().quantidadeSessoes

		# gastos categorias

		query_gasto_alimentacao = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_alimentacao, mesEmissao=mesPassado, anoEmissao=ano).all()
		query_gasto_escritorio = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_escritorio, mesEmissao=mesPassado, anoEmissao=ano).all()
		query_gasto_divulgacao = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_divulgacao, mesEmissao=mesPassado, anoEmissao=ano).all()
		query_gasto_locacao = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_locacao, mesEmissao=mesPassado, anoEmissao=ano).all()
		query_gasto_combustivel = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_combustivel, mesEmissao=mesPassado, anoEmissao=ano).all()
		query_gasto_passagens = Gasto.query.filter_by(idDeputado=deputado_id, nomeCategoria=categoria_passagens, mesEmissao=mesPassado, anoEmissao=ano).all()

		gasto_alimentacao = somaGastosCategoria(query_gasto_alimentacao)
		gasto_escritorio = somaGastosCategoria(query_gasto_escritorio)
		gasto_divulgacao = somaGastosCategoria(query_gasto_divulgacao)
		gasto_locacao = somaGastosCategoria(query_gasto_locacao)
		gasto_combustivel = somaGastosCategoria(query_gasto_combustivel)
		gasto_passagens = somaGastosCategoria(query_gasto_passagens)

		gastos_categorias = {
		categoria_alimentacao : gasto_alimentacao,
		categoria_combustivel : gasto_combustivel,
		categoria_divulgacao : gasto_divulgacao,
		categoria_escritorio : gasto_escritorio,
		categoria_locacao : gasto_locacao,
		categoria_passagens : gasto_passagens
		}

		meus_gastos = [(categoria_alimentacao, gasto_alimentacao),
		(categoria_combustivel, gasto_combustivel),
		(categoria_divulgacao, gasto_divulgacao),
		(categoria_escritorio, gasto_escritorio),
		(categoria_locacao, gasto_locacao),
		(categoria_passagens, gasto_passagens)
		]

		maior_gasto = sorted(meus_gastos, key=lambda x: x[1], reverse=True)[0]

		deputado_json = {
		'Id' : deputado_id,
		'Nome': deputado_nome,
		'urlfoto' : deputado_foto,
		'presencas' : deputado_presencas,
		'total_sessoes': sessoes_totais,
		'Total' : deputado_gasto_total,
		'Posicao': deputado_posicao,
		'Partido' : deputado_partido,
		'UF' : deputado_uf,
		'Cota_UF' : deputado_cota_uf,
		'Gastos' : gastos_categorias,
		'Maior_gasto_categoria' : maior_gasto[0],
		'Maior_gasto_valor' : maior_gasto[1]
		}

		json.append(deputado_json)

	return jsonify(json)

if __name__ == "__main__":
    app.run(debug=True)
