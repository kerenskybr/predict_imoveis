from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from predictimoveis import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_usuario):
	return Usuarios.query.get(int(id_usuario))

class Usuarios(db.Model, UserMixin):

	__tablename__ = 'usuarios'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	senha = db.Column(db.String(10), nullable=False)
	imagem_perfil = db.Column(db.String(20), nullable=False, default='default.jpg')

	def _repr__(self):
		return f"Usuarios('{self.nome}', '{self.email}', '{self.senha}', '{self.imagem_perfil}')"


class Colaboradores(db.Model):

	__tablename__ = 'colaboradores'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	senha = db.Column(db.String(10), nullable=False)

	def _repr__(self):
		return f"Colaboradores('{self.nome}', '{self.email}', '{self.senha}')"


class Consultas(db.Model):

	__tablename__ = 'consultas'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	dorms = db.Column(db.Integer, nullable=False)
	banhos = db.Column(db.Integer, nullable=False)
	vagas = db.Column(db.Integer, nullable=False)
	area = db.Column(db.Integer, nullable=False)
	descr = db.Column(db.String(30), nullable=False)
	data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
	valor = db.Column(db.String, nullable=False)

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

	#usuario = db.relationship('Usuario', backref=db.backref('usuarios', lazy=True))

	def _repr__(self):
		return f"Consultas('{self.dorms}','{self.banhos}','{self.vagas}','{self.area}','{self.desc}','{self.data}')"


class DadosNovos(db.Model):

	__tablename__ = 'dados_novos'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	bairro = db.Column(db.String(100), nullable=False)
	dorms = db.Column(db.Integer, nullable=False)
	banhos = db.Column(db.Integer, nullable=False)
	vagas = db.Column(db.Integer, nullable=False)
	area = db.Column(db.Float, nullable=False)
	cond =  db.Column(db.String(10), nullable=False)
	valor = db.Column(db.String(10), nullable=False)
	cidade = db.Column(db.String(60), nullable=False)

	def _repr__(self):
		return f"DadosNovos('{self.bairro}','{self.dorms}','{self.banhos}','{self.vagas}','{self.area}','{self.cond}', '{self.valor}', '{self.cidade}')"
