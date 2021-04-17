from flask_testing import TestCase
from core.extensions import db
from core import masakhane, load_model


class BaseTestCase(TestCase):
    def create_app(self):
        masakhane.config.from_object('project.config.TestingConfig')
        return masakhane

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()