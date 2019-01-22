import os
import io
import locale

from predictimoveis import app
from predictimoveis.forms import FormRegistro, FormSistema

from flask import render_template, url_for

from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

import numpy as np

np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/registro")
def registro():
	form = FormRegistro()
	return render_template("registro.html", form=form)



def clear():
	return redirect(url_for('sistema'))

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

		areas = [[dorms, banhos, vagas, area]]
		
		a = carrega_modelo.predict(areas)
		print(a)
		#estimado2 = (str(a)[1:-1])
		#estimado = ('R$ ') + (''.join(map(str, a)))
	
		#estimado = locale.format("%1.2f",a,1)

		locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
		
		valor = locale.currency(a, grouping=True, symbol=None)
		
		estimado = ('R$ %s' % valor)


		mse = mean_squared_error(medida_y, carrega_modelo.predict(medida_x))

		np.sqrt(mse)

		porc = carrega_modelo.score(medida_x, medida_y)
		
		precisao = format(porc*100, '.2f') + '%'
		#flash('Editado com sucesso!')


	return render_template("sistema.html", form=form, estimado=estimado, precisao=precisao)