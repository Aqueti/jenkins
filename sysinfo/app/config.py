import os

class Config(object):
    SECRET_KEY = "test" #os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = "test"