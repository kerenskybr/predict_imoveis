from flask import Flask

from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '833d1a8d188e94730cb6af5b9fcc9786'



login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from predictimoveis import routes