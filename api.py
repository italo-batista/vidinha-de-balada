# coding: utf-8
import ConfigParser  
import sqlalchemy
import datetime
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


app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Pesquisas@localhost/vidinha_balada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mysql = SQLAlchemy(app)
mysql.init_app(app)
with app.app_context():
	mysql.create_all()


# Init

now = datetime.datetime.now()
if now.month == 1:
	mesPassado = 12
	ano = now.year - 1
else:
	mesPassado = now.month - 1
	ano = now.year
	
categoria_alimentacao = 'Alimentação'
categoria_escritorio = 'Escritório'
categoria_divulgacao = 'Divulgação de atividade parlamentar'
categoria_locacao = 'Locação de veículos'
categoria_combustivel = 'Combustível'
categoria_passagens = 'Passagens aéreas'

#categoria_alimentacao = 'Alimentaca'
#categoria_escritorio = 'Escritório'
#categoria_divulgacao = 'Divulgação'
#categoria_locacao = 'Locação de'
#categoria_combustivel = 'Combustíve'
#categoria_passagens = 'Passagens'
	
def init():
	pass

# Models
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
    
    idDocumento = mysql.Column(mysql.String(10), primary_key=True)
    idDeputado = mysql.Column(mysql.String(7), nullable=False)
    mesEmissao = mysql.Column(mysql.Integer)
    anoEmissao = mysql.Column(mysql.Integer)
    idCategoria = mysql.Column(mysql.String(10), nullable=False)
    nomeFornecedor = mysql.Column(mysql.String(15), nullable=False)
    valor = mysql.Column(mysql.Float)
    cnpj = mysql.Column(mysql.String(15))
    
    def __repr__(self):
        return '<Gasto (%s, %s, %s, %s, %s, %s, %s) >' % (self.idDeputado, self.mesEmissao, self.anoEmissao, self.idCategoria, self.nomeFornecedor, self.valor, self.cnpj)

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
    idCategoria = mysql.Column(mysql.String(10), primary_key=True)
    
    def __repr__(self):
        return '<SelosDeputado (%s, %s, %s, %s) >' % (self.idDeputado, self.mes, self.ano, self.idCategoria)

class Empresa(mysql.Model):  
    __tablename__ = 'empresas'

    cnpj = mysql.Column(mysql.String(15), primary_key=True)    
    nome = mysql.Column(mysql.String(10))
    
    def __repr__(self):
        return '<Empresa (%s, %s) >' % (self.cnpj, self.nome)


# Routes
@app.route("/")
def hello():  
    return "Hello World!"

#/gasto_anual?ano=
@app.route('/gasto_anual')
def getGasto(ano):
	pass
    
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

def somaGastos(query_gasto_categoria):
	gastoTotal = 0
	for gasto in query_gasto_categoria:
		gastoTotal = gastoTotal + gasto.valor
	return gastoTotal
	
@app.route('/deputados/<id>', methods=['GET'])
def getDeputado(id):
			
	deputado = Deputado.query.filter_by(id=id).first()	
	query_gasto_alimentacao = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_alimentacao).all()
	query_gasto_escritorio = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_escritorio).all()
	query_gasto_divulgacao = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_divulgacao).all()
	query_gasto_locacao = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_locacao).all()
	query_gasto_combustivel = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_combustivel).all()
	query_gasto_passagens = Gasto.query.filter_by(idDeputado=id, mesEmissao=mesPassado, anoEmissao=ano, idCategoria=categoria_passagens).all()
	presencas_deputado = SessoesMesDeputado.query.filter_by(idDeputado=id, mes=mesPassado, ano=ano).first()
	presencas_total = SessoesMes.query.filter_by(mes=mesPassado, ano=ano).first()
	
	gasto_alimentacao = somaGastos(query_gasto_alimentacao)
	gasto_escritorio = somaGastos(query_gasto_escritorio)
	gasto_divulgacao = somaGastos(query_gasto_divulgacao)
	gasto_locacao = somaGastos(query_gasto_locacao)
	gasto_combustivel = somaGastos(query_gasto_combustivel)
	gasto_passagens = somaGastos(query_gasto_passagens)
	
	## o total dos gastos é a soma dos gastos das categorias anteriores ou envolvem outros gastos?
	total_gastos = gasto_alimentacao + gasto_escritorio + gasto_divulgacao + gasto_locacao + gasto_combustivel + gasto_passagens
		
	json = {
	'Nome' : deputado.nome,
	'urlfoto' : deputado.foto,
	'Alimentação' : gasto_alimentacao,
	'Escritório' : gasto_escritorio,
	'Divulgação de atividade parlamentar' : gasto_divulgacao,
	'Locação de veículos' : gasto_locacao,
	'Combustível' : gasto_combustivel,
	'Passagens aéreas' : gasto_passagens,
	'presencas' : presencas_deputado.quantidadeParticipacoes,
	'total_sessoes' : presencas_total.quantidadeSessoes,
	'Total' : total_gastos
	}
	
	return jsonify(json)    

if __name__ == "__main__":  
    app.run(debug=True)
