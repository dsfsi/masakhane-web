import os
import unittest

from flask import current_app
from flask_testing import TestCase

from core import masakhane


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('core.config.DevelopmentConfig')
        return masakhane

    def test_app_is_development(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "super-secret-key")
        self.assertFalse(current_app is None)
        self.assertTrue(
            masakhane.config['SQLALCHEMY_DATABASE_URI'] == 
                os.getenv('DATABASE_TEST_URL', "sqlite:///masakhane.db")
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('core.config.StagingConfig')
        return masakhane

    def test_app_is_testing(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "key_testing")
        self.assertTrue(masakhane.config['TESTING'])
        self.assertTrue(
            masakhane.config['SQLALCHEMY_DATABASE_URI'] == 
                os.getenv('DATABASE_TEST_URL', "sqlite:///masakhane.db")
        )

class TestProductionConfig(TestCase):
    def create_app(self):
        masakhane.config.from_object('core.config.ProductionConfig')
        return masakhane

    def test_app_is_production(self):
        self.assertTrue(masakhane.config['SECRET_KEY'] == "key_production")
        self.assertFalse(masakhane.config['TESTING'])

if __name__ == '__main__':
    unittest.main()