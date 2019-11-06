import os
import unittest
from flask import current_app
from app import create_app
from app import db
from config import basedir


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        print('Setting Up')
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(os.path.join(basedir, 'test.db'))
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
