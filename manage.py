import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

import app.events
from app import create_app, db
from app.models import User

import logging
from logging.handlers import RotatingFileHandler
from flask import request
from time import strftime
import traceback

env = os.getenv('FLASK_CONFIG')
print('USING ENVIRONMENT VARIABLE: ', env)
app = create_app(env or 'testing')  # development testing, linux_development pythonanywhere
migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method,
#                  request.scheme, request.full_path, response.status)
#     return response
#
#
# @app.errorhandler(Exception)
# def exceptions(e):
#     tb = traceback.format_exc()
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method,
#                  request.scheme, request.full_path, tb)
#     return e.status_code


if __name__ == '__main__':
    # handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    # logger = logging.getLogger('tdm')
    # logger.setLevel(logging.ERROR)
    # logger.addHandler(handler)
    manager.run()
