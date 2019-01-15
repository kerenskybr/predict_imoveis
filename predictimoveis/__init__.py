from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '833d1a8d188e94730cb6af5b9fcc9786'



from predictimoveis import routes