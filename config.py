import os

basedir = os.path.abspath(os.path.dirname(__file__))
w1_sensor_directory = '/sys/bus/w1/devices/'


class Config:
    def __init__(self):
        pass

    SECRET_KEY = 'cheesecake'
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'cheese cake'
    # JWT_ALGORITHM = 'SH256'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        print('INITIALIZING', app.config['FLASK_CONFIG'])
        print('INITIALIZING', app.config['SQLALCHEMY_DATABASE_URI'])
        pass


class TestingConfig(Config):
    print('TestingConfig')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # SERVER_NAME = "Dicks"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    APP_SLOW_DB_QUERY_TIME = 1


class DevelopmentConfig(Config):
    print('DevelopmentConfig')
    # INTERNAL_URL = '127.0.0.1:5000'
    DEBUG = True
    # SERVER_NAME = '0.0.0.0:5000'
    FEATURE_FLAGS = {
        'firebase': True,
        'manage': False,
        'inventory': False,
        'finance': False,
        'about': False,
        'reports': True,
        'show_tables_firebase': True,

    }

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'username'  # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'password'  # os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = 'mysql://gpamfilis:mysqliscool123@gpamfilis.mysql.pythonanywhere-services.com/gpamfilis$epoptis_production'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test1.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:mysqliscool123@localhost/development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    # "pythonanywhere": PythonAnywhereConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    #     # 'production': ProductionConfig,
    #     # 'default': DevelopmentConfig,
}
