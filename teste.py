import ConfigParser  
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy  
from flask import Flask, jsonify, request

# needed to install: 
# 	sudo apt-get install python-mysqldb
#	sudo pip install mysql-python 

# use this material:
# http://blog.cloudoki.com/getting-started-with-restful-apis-using-the-flask-microframework-for-python/


app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Pesquisas@localhost/vidinha_balada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mysql = SQLAlchemy(app)
mysql.init_app(app)
with app.app_context():
	mysql.create_all()

# map models
class Cotas(mysql.Model):  
    __tablename__ = 'cotas'
    uf = mysql.Column(mysql.String(2), primary_key=True)
    cota = mysql.Column(mysql.Integer, nullable=False)

    def __repr__(self):
        return '<Cotas (%s, %s) >' % (self.uf, self.cota)

@app.route("/")
def hello():  
    return "Hello Worldddd!"
    
    
@app.route('/cotas', methods=['GET'])
def getCotas():  
    data = Cotas.query.all()

    data_all = []

    for cota in data:
        data_all.append([cota.uf, cota.cota])

    return jsonify(cotas=data_all)
    
@app.route('/cotas/<uf>', methods=['GET'])
def getCota(uf):
	cota = Cotas.query.filter_by(uf=uf).first_or_404()
	data_all = [cota.uf, cota.cota]
	return jsonify(cotas=data_all)
    
if __name__ == "__main__":  
    app.run(debug=True)
