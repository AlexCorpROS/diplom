import os

class Config(object):    
    # блок отвечающий за определение места хранения изображений аватаров пользовталей
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER', 'coder')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'coder')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5532)
    DB = os.environ.get('POSTGRES_DB', 'mydb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://coder:coder@localhost:5532/mydb'
    SECRET_KEY = '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = True