import os

from predictimoveis import app
from predictimoveis.forms import FormRegistro, FormSistema

from flask import render_template, url_for

from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

import numpy as np




@app.route("/")
def home():
	return render_template("home.html")

@app.route("/registro")
def registro():
	form = FormRegistro()
	return render_template("registro.html", form=form)

@app.route("/sistema")
def sistema():

	carrega_modelo = joblib.load(os.path.join(app.root_path, 'saves/modelo_final.sav'))	
	medida_x = joblib.load(os.path.join(app.root_path,'saves/x_test.sav'))
	medida_y = joblib.load(os.path.join(app.root_path,'saves/y_test.sav'))

	form = FormSistema()

	if form.validate_on_submit():
		#return redirect('/success')


		return render_template("sistema.html", form=form)