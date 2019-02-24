import os
import io
import locale

from predictimoveis import db, app
from predictimoveis.forms import FormRegistro, FormSistema
from predictimoveis.models import Usuarios, Colaboradores, Consultas, DadosNovos

from flask import render_template, url_for, flash

from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

import numpy as np

#np.set_printoptions(formatter={'float': '{: 0.2f}'.format})


@app.route("/")
def home():
	return render_template("home.html")


@app.route("/registro")
def registro():
	form = FormRegistro()

	if form.validate_on_submit():



		nome = StringField('Nome Fantasia, nome imobiliária', validators=[DataRequired(), Length(min=5, max=20)])
		email = StringField('Email',validators=[DataRequired(), Email()])
		senha = PasswordField('Senha', validators=[DataRequired()])
		confirma_senha = PasswordField('Repetir Senha', validators=[DataRequired(), EqualTo('senha')])
		submit 

	return render_template("registro.html", form=form)

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/sistema", methods=['GET', 'POST'])
def sistema():

	carrega_modelo = joblib.load(os.path.join(app.root_path, 'saves/modelo_final.sav'))	
	medida_x = joblib.load(os.path.join(app.root_path,'saves/x_test.sav'))
	medida_y = joblib.load(os.path.join(app.root_path,'saves/y_test.sav'))

	form = FormSistema()

	estimado = 0

	precisao = 0

	if form.validate_on_submit():

		dorms = int(form.dorms.data)
		banhos = int(form.banhos.data)
		vagas = int(form.vagas.data)
		area = float(form.area.data)
		desc = form.desc.data

		areas = [[dorms, banhos, vagas, area]]
		
		a = carrega_modelo.predict(areas)

		locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
		
		valor = locale.currency(a, grouping=True, symbol=None)
		
		estimado = ('R$ %s' % valor)


		mse = mean_squared_error(medida_y, carrega_modelo.predict(medida_x))

		np.sqrt(mse)

		porc = carrega_modelo.score(medida_x, medida_y)
		
		precisao = format(porc*100, '.2f') + '%'
		flash(f'Previsão gerada com sucesso!', 'success')


	return render_template("sistema.html", form=form, estimado=estimado, precisao=precisao)