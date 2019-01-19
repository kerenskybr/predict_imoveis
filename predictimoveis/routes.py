from predictimoveis import app

from flask import render_template

from predictimoveis.forms import FormRegistro

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/registro")
def registro():
	form = FormRegistro()
	return render_template("registro.html", form=form)

@app.route("/sistema")
def sistema():
	return render_template("sistema.html")