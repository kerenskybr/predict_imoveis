import os

from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '833d1a8d188e94730cb6af5b9fcc9786'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predict_imoveis.db'


db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from predictimoveis import routes