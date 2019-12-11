class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sikret'
    CSRF_ENABLED = True 
    USER_ENABLE_EMAIL = False
    USER_APP_NAME = 'Ogłoszenia'