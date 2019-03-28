import os
import io
import locale

from flask_login import current_user, logout_user, login_required, login_user

from predictimoveis import db, app
from predictimoveis.forms import FormRegistro, FormSistema, FormLogin
from predictimoveis.models import Usuarios, Colaboradores, Consultas, DadosNovos

from flask import render_template, url_for, flash, redirect

from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

import numpy as np


@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('sistema'))

	form = FormLogin()
	if form.validate_on_submit():
		nome = Usuarios.query.filter_by(email=form.email.data).first()
		if nome:
			login_user(nome, remember=form.lembrarme.data)
			return redirect(url_for('sistema'))
	else:
		flash('Erro. Nome de usuário ou senha inválido', 'danger')

	return render_template("login.html", title='Login', form=form)


@app.route("/registro", methods=['GET', 'POST'])
def registro():

	form = FormRegistro()

	if form.validate_on_submit():

		grava = Usuarios(nome=form.nome.data, email=form.email.data, senha=form.senha.data)

		db.session.add(grava)
		db.session.commit()

		flash(f'Sua conta foi criada. Você pode agora se logar {form.nome.data}!', 'success')

		return redirect(url_for('login'))

	return render_template("registro.html", title='Registro', form=form)


@app.route("/logout")
def logout():
	logout_user()

	return render_template("home.html", title="Início")
'''

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('sistema'))
	formulario = FormDeLogin()
	if formulario.validate_on_submit():
		nome = Usuario.query.filter_by(email=formulario.email.data).first()
		if nome and bcrypt.check_password_hash(nome.senha, formulario.senha.data):
			login_user(nome, remember=formulario.lembrarme.data)
			return redirect(url_for('sistema'))
		else:
			flash('Erro. Nome de usuario ou senha inválido.', 'danger')
	return render_template('login.html', title='login', formulario=formulario)

'''


@app.route("/sistema", methods=['GET', 'POST'])
#@login_required
def sistema():
	query = Consultas.query.filter_by(id_usuario=current_user.id)

	#Carrega o modelo de machine learning treinado
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

		a = a.round()

		locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

		valor = locale.currency(a, grouping=True, symbol=None)

		valor_string = str(valor)

		estimado = ('R$ %s' % valor)


		mse = mean_squared_error(medida_y, carrega_modelo.predict(medida_x))

		np.sqrt(mse)

		porc = carrega_modelo.score(medida_x, medida_y)

		precisao = format(porc*100, '.2f') + '%'
		flash(f'Resultado gerado com sucesso!', 'success')

		#Abaixo, grava a consulta efetuada no banco de dados

		consulta = Consultas(dorms=dorms, banhos=banhos, vagas=vagas,area=area,
								desc=desc, valor=valor_string, id_usuario=1)
		db.session.add(consulta)
		db.session.commit()


	return render_template("sistema.html", form=form, estimado=estimado,
							precisao=precisao, query=query, title='Sistema')


@app.route("/sistema/<item_id>/deletar", methods=['GET', 'POST'])
#@login_required
def deletar(item_id):
	query = Consultas.query.get_or_404(item_id)
	'''
	if query.id_usuario != current_user:
		abort(403)
	'''
	db.session.delete(query)
	db.session.commit()
	flash('Apagado com sucesso', 'warning')

	return redirect(url_for('sistema'))