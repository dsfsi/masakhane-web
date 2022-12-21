import os
# external imports
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
# internal imports
from core.resources.translate import TranslateResource, AddResource, SaveResource, HomeResource
from core.extensions import db
from core.config import Config, DevelopmentConfig, ProductionConfig, StagingConfig



#application factory
def create_app(saved_models):
    """Flask application factory to config and init app"""
    env = os.environ.get('ENV', 'Development')
    if env == 'Production':
        config_str = ProductionConfig()
    elif env == 'Staging':
        config_str = StagingConfig()
    else:
        config_str = DevelopmentConfig()

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_str)
    # database init
    register_extensions(app)
    # api init
    register_resources(app, saved_models)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app, saved_models):
    api = Api(app)
    api.add_resource(HomeResource, '/') 
    api.add_resource(TranslateResource, '/translate', resource_class_kwargs={'saved_models': saved_models})
    # TODO need to find a better way to updte the current app information whithout exposing to the public
    api.add_resource(AddResource, '/update', resource_class_kwargs={'saved_models': saved_models})
    api.add_resource(SaveResource, '/save')
  
models = {}
masakhane = create_app(models)
masakhane.models = models