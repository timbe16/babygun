# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~

    Babymailgun tests
"""

from app import app, db
import flask_testing
import os


class TestCase(flask_testing.TestCase):
    
    """
    Base TestClass for app.
    """
    def create_app(self):
        # app = create_app(TestConfig())
        # self.twill = Twill(app, port=3000)
        return app
        # return app(self)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.dirname(os.path.abspath(__file__)) + '/app_test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

