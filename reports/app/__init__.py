from flask import Flask
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'

from app import views

app.config.from_object(Config)
