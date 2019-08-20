import os

class Config(object):
    SECRET_KEY = "test" #os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = "test"

mail_config = dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'aqueti.test@gmail.com',
    MAIL_PASSWORD = '')

RLIST= ['astepenko@aqueti.com']