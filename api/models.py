from api import mysql


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
    anoEmissao = mysql.Column(mysql.Integer)
    mesEmissao = mysql.Column(mysql.Integer)
    idEmpresa = mysql.Column(mysql.String(10), nullable=False)
    cnpj = mysql.Column(mysql.String(15))
    nomeFornecedor = mysql.Column(mysql.String(15), nullable=False)
    nomeCategoria = mysql.Column(mysql.String(10), nullable=False)
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


class SelosCota(mysql.Model):
    __tablename__ = 'selosCota'

    id = mysql.Column(mysql.Integer, primary_key=True)
    idDeputado = mysql.Column(mysql.String(7))
    ano = mysql.Column(mysql.Integer)
    mes = mysql.Column(mysql.Integer)
    selo = mysql.Column(mysql.String(10))

    def __repr__(self):
        return '<SelosCota (%s, %s, %s, %s, %s) >' % (self.id, self.idDeputado, self.mes, self.ano, self.selo)


class SelosPresenca(mysql.Model):
    __tablename__ = 'selosPresenca'

    id = mysql.Column(mysql.Integer, primary_key=True)
    idDeputado = mysql.Column(mysql.String(7))
    mes = mysql.Column(mysql.Integer)
    ano = mysql.Column(mysql.Integer)
    selo = mysql.Column(mysql.String(40))

    def __repr__(self):
        return '<SelosPresenca (%s, %s, %s, %s, %s) >' % (self.id, self.idDeputado, self.mes, self.ano, self.selo)


class Empresa(mysql.Model):
    __tablename__ = 'empresas'

    cnpj = mysql.Column(mysql.String(15))
    nome = mysql.Column(mysql.String(10))
    idEmpresa = mysql.Column(mysql.Integer, primary_key=True)

    def __repr__(self):
        return '<Empresa (%s, %s, %d) >' % (self.cnpj, self.nome, self.idEmpresa)
