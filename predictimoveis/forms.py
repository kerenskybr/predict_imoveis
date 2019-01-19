from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_login import current_user, AnonymousUserMixin

class FormRegistro(FlaskForm):
	nome = StringField('Nome Fantasia', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	senha = PasswordField('Senha', validators=[DataRequired()])
	confirma_senha = PasswordField('Repetir Senha', validators=[DataRequired(), EqualTo('senha')])
	submit = SubmitField('Registrar')