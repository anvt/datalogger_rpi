# from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# TODO: find a way to bypass the CORS package.
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
bootstrap = Bootstrap()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'

    app.config['FLASK_CONFIG'] = config_name

    CORS(app, headers=['Content-Type'])
    # FlaskMustache(app)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    csrf.init_app(app)

    db.init_app(app)

    # login_manager.init_app(app)
    bootstrap.init_app(app)
    # ftable.init_app(app)
    #
    # Blueprints

    # TODO: organize the blueprints, rename
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # from app.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    # from .api.v1.datalogger import api as api_v1_datalogger_blueprint
    # app.register_blueprint(api_v1_datalogger_blueprint, url_prefix='/api/v1/datalogger')

    return app

# links
# http://stackoverflow.com/questions/21509728/flask-restful-post-fails-due-csrf-protection-of-flask-wtf#21509994
# https://github.com/lepture/flask-wtf/issues/111
