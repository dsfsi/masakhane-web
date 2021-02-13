from resources.translate import TranslateResource, DeleteResource, AddResource, SaveResource, HomeResource

from flask import Flask
from flask import request, render_template

from flask_migrate import Migrate
from extensions import db
from db.config import Config, DevelopmentConfig, ProductionConfig, StagingConfig


# this is only for debug purpose
# import ipdb
import os
from flask_restful import Api


def create_app():

    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        config_str = ProductionConfig()
    
    elif env == 'Staging':
        config_str = StagingConfig()
    
    else:
        config_str = DevelopmentConfig()

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
    api.add_resource(HomeResource, '/')
    api.add_resource(TranslateResource, '/translate')
    api.add_resource(DeleteResource, '/delete')
    api.add_resource(AddResource, '/add')
    api.add_resource(SaveResource, '/save')


if __name__=='__main__':
    masakhane = create_app()
    masakhane.run()