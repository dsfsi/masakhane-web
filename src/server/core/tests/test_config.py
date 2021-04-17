import os
import unittest

from flask import current_app
from flask_testing import TestCase

from core import masakhane


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('project.config.DevelopmentConfig')
        return masakhane

    def test_app_is_development(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "my_precious")
        self.assertFalse(current_app is None)
        self.assertTrue(
            masakhane.config['SQLALCHEMY_DATABASE_URI'] == 
                os.environ.get('DATABASE_URL')
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('project.config.TestingConfig')
        return masakhane

    def test_app_is_testing(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "my_precious")
        self.assertTrue(masakhane.config['TESTING'])
        self.assertFalse(masakhane.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            masakhane.config['SQLALCHEMY_DATABASE_URI'] == 
                os.environ.get('DATABASE_TEST_URL')
        )

class TestProductionConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('project.config.ProductionConfig')
        return masakhane

    def test_app_is_production(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "my_precious")
        self.assertTrue(masakhane.config['TESTING'])

if __name__ == '__main__':
    unittest.main()