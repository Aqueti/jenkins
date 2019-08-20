from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.config import *

app = Flask(__name__)

app.config.update(mail_config)

login = LoginManager(app)
login.login_view = 'login'

mail = Mail(app)

from app import views

app.config.from_object(Config)
