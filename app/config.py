import os


class BaseConfig(object):
    SITE_NAME = 'Dashboard-PBX'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Gox0Agv8KS')

    MYSQL_DATABASE_USER = 'pbx-dashboard'
    MYSQL_DATABASE_PASSWORD = 'password'
    MYSQL_DATABASE_DB = 'asteriskcdrdb'
    MYSQL_DATABASE_HOST = 'pbx.dfb.com.do'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
                            MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD,
                            MYSQL_DATABASE_HOST, MYSQL_DATABASE_DB)
    SUPPORTED_LOCALES = ['es']


class DevConfig(BaseConfig):
    """Development configuration options."""
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False
    TESTING = False


class TestConfig(BaseConfig):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False
