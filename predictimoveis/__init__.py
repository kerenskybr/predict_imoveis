import os

from flask import Flask

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)

#não colocar /localhost na hora de exportar a variavel

app.config['SECRET_KEY'] = '833d1a8d188e94730cb6af5b9fcc9786'

#Uncomment to local
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///predict_imoveis"

#Uncommentd  to heroku
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://datchrzllffhbj:8d0984b3db5c18ffee687484ad97a88ad1a2f7af9cfbb05bfbfdfa5501818b49@ec2-107-20-230-70.compute-1.amazonaws.com:5432/d5ld8ffclmf9h"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#comment before send to heroku
#db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#db.create_all()

from predictimoveis import routes

