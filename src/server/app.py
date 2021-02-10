from flask import Flask
from flask import request, render_template

from flask_migrate import Migrate
from extensions import db
from db import Config


# this is only for debug purpose
# import ipdb
import os
from flask_restful import Api

from utils import model_load
from models.predict import Predicter
from resources.translate import TranslateResource, DeleteResource, AddResource, SaveResource, Home

def create_app():

    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        config_str = Config.ProductionConfig
    else:
        config_str = Config.DevelopmentConfig 

    app = Flask(__name__)
    app.config.from_object(config_str)
    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)
    api.add_resource(TranslateResource, '/translate')
    api.add_resource(DeleteResource, '/delete')
    api.add_resource(AddResource, '/add')
    api.add_resource(SaveResource, '/save')


if __name__=='__main__':
    # masakhane.run(port=5000, debug=True)
    masakhane = create_app()
    masakhane.run(port=5000, debug=True)
