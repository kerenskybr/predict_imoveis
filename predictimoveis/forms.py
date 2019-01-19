from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_login import current_user, AnonymousUserMixin

class FormRegistro(FlaskForm):
	nome = StringField('Nome Fantasia', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	senha = PasswordField('Senha', validators=[DataRequired()])
	confirma_senha = PasswordField('Repetir Senha', validators=[DataRequired(), EqualTo('senha')])
	submit = SubmitField('Registrar')

class FormSistema(FlaskForm):
	dorms = IntegerField('Dormitórios', validators=[DataRequired(), Length(min=0, max=10)])
	banho = IntegerField('Banhos', validators=[DataRequired(), Length(min=0, max=10)])
	vagas = IntegerField('Vagas', validators=[DataRequired(), Length(min=0, max=4)])
	area = FloatField('Área Total', validators=[DataRequired(),Length(min=10, max=1000)])
	submit = SubmitField('Calcular')