import os

from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)

#não colocar /localhost na hora de exportar a variavel

app.config['SECRET_KEY'] = '833d1a8d188e94730cb6af5b9fcc9786'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///predict_imoveis"
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#db.create_all()

from predictimoveis import routes

