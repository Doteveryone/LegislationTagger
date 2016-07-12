import os

class Config(object):
    DEBUG = False
    MONGODB_DB = os.environ.get('MONGODB_DB', None)
    MONGODB_HOST = os.environ.get('MONGODB_HOST', None)
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 0))
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', None)
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', None)
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    SECURITY_REGISTERABLE = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER', None)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', None)
    SECURITY_SEND_REGISTER_EMAIL = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'not-a-secret'
    SECURITY_PASSWORD_SALT = 'not-secure'
    MONGODB_DB = os.environ.get('MONGODB_DB', 'legicert')
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))


class TestConfig(DevelopmentConfig):
    TESTING = True
    MONGODB_DB = os.environ.get('MONGODB_DB', 'legicert_test')
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))