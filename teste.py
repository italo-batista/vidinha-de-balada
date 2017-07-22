import ConfigParser  
import sqlalchemy
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
    partido = mysql.Column(mysql.String(20))
    uf = mysql.Column(mysql.String(2))
    foto = mysql.Column(mysql.String(30))
    twitter = mysql.Column(mysql.String(10))
    telefone = mysql.Column(mysql.String(15))
    email = mysql.Column(mysql.String(20))
    dataNsc = mysql.Column(mysql.DateTime)
    
    def __repr__(self):
        return '<Deputado (%s, %s, %s, %s, %s, %s, %s, %s) >' % (self.id, self.nome, self.partido, self.uf, self.foto, self.twitter, self.telefone, self.email, self.dataNsc)

class Gasto(mysql.Model):  
    __tablename__ = 'gastos'
    
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

    idDeputado = mysql.Column(mysql.String(7), nullable=False)    
    mes = mysql.Column(mysql.Integer)
    ano = mysql.Column(mysql.Integer)
    idCategoria = mysql.Column(mysql.String(10), nullable=False)
    
    def __repr__(self):
        return '<SelosDeputado (%s, %s, %s, %s) >' % (self.idDeputado, self.mes, self.ano, self.idCategoria)

class Empresa(mysql.Model):  
    __tablename__ = 'empresas'

    cnpj = mysql.Column(mysql.String(15))    
    nome = mysql.Column(mysql.String(10))
    
    def __repr__(self):
        return '<Empresa (%s, %s) >' % (self.idDeputado, self.mes)


# Routes
@app.route("/")
def hello():  
    return "Hello Worldddd!"

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
    

if __name__ == "__main__":  
    app.run(debug=True)
