from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_login import current_user, AnonymousUserMixin

class FormRegistro(FlaskForm):
	nome = StringField('Nome Fantasia, nome imobiliária', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	senha = PasswordField('Senha', validators=[DataRequired()])
	confirma_senha = PasswordField('Repetir Senha', validators=[DataRequired(), EqualTo('senha')])
	submit = SubmitField('Registrar')

#Validação para verificar se o usuario ja existe
def validate_username(self, nome):
    
    usuario = Usuarios.query.filter_by(nome=nome.data).first()

    if usuario:
        raise ValidationError("Esse nome de usuario já existe. Favor escolha outro.")

def validate_email(self, email):
    
    usuario = Usuarios.query.filter_by(email=email.data).first()

    if usuario:
        raise ValidationError("Esse email já foi usado. Favor escolha outro.") 

class FormLogin(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Email()])
	senha = PasswordField('Senha', validators=[DataRequired()])
	lembrarme = BooleanField('Lembre-me')
	submit = SubmitField('Logar')

class FormSistema(FlaskForm):
	dorms = IntegerField('Dormitórios', validators=[DataRequired()])
	banhos = IntegerField('Banhos', validators=[DataRequired()])
	vagas = IntegerField('Vagas', validators=[DataRequired()])
	area = FloatField('Área Total', validators=[DataRequired()])
	valor = StringField('Valor')
	descr = StringField('Descrição')
	submit = SubmitField('Calcular')

class FormDeAtualizarConta(FlaskForm):
	nome = StringField('Nome de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	imagem = FileField('Atualizar Imagem da Conta.', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Atualizar')

class FormDadosNovos(FlaskForm):
	bairro = StringField('Bairro/Distrito', validators=[DataRequired(), Length(min=2, max=20)])
	cidade = StringField('Cidade', validators=[DataRequired(), Length(min=2, max=20)])
	cond = StringField('Condomínio')
	valor = StringField('Valor')
	submit = SubmitField('Enviar')
	'''
	bairro = db.Column(db.String(100), nullable=False)
	dorms = db.Column(db.Integer, nullable=False)
	banhos = db.Column(db.Integer, nullable=False)
	vagas = db.Column(db.Integer, nullable=False)
	area = db.Column(db.Integer, nullable=False)
	cond =  db.Column(db.String(10), nullable=False)
	valor = db.Column(db.Integer, nullable=False)
	cidade = db.Column(db.String(60), nullable=False)
	'''