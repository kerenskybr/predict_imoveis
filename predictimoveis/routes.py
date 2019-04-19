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

@app.route("/contato")
def contato():
	return render_template("contato.html")


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

def salva_imagem(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125) #redimensionando imagens salva espaço e ganha performance
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/minha_conta", methods=['GET', 'POST'])
@login_required
def minha_conta():
	form = FormDeAtualizarConta()
	if form.validate_on_submit():
		if form.imagem.data:
			arquivo_imagem = salva_imagem(form.imagem.data)
			current_user.imagem_perfil = arquivo_imagem
		current_user.nome = form.nome.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Sua conta foi atualizada com sucesso.', 'success')
		return redirect(url_for('minha_conta'))

	elif request.method == 'GET':
		form.nome.data = current_user.nome
		form.email.data = current_user.email
	imagem_perfil = url_for('static', filename='profile_pics/' + current_user.imagem_perfil)
	return render_template('minha_conta.html', title='Minha Conta', imagem_perfil=imagem_perfil, form=form)


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
								desc=desc, valor=valor_string, id_usuario=current_user.id)
		db.session.add(consulta)
		db.session.commit()


	return render_template("sistema.html", form=form, estimado=estimado,
							precisao=precisao, query=query, title='Sistema')


@app.route("/sistema/<item_id>/deletar", methods=['GET', 'POST'])
#@login_required
def deletar(item_id):
	query = Consultas.query.get_or_404(item_id)
	
	if query.id_usuario != current_user.id:
		abort(403)
	
	db.session.delete(query)
	db.session.commit()
	flash('Apagado com sucesso', 'warning')

	return redirect(url_for('sistema'))