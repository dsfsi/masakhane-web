from core.resources.translate import TranslateResource, AddResource, SaveResource, HomeResource

from flask import Flask
from flask import request, render_template, current_app


from flask_migrate import Migrate
from flask_cors import CORS
from core.extensions import db
from core.config import Config, DevelopmentConfig, ProductionConfig, StagingConfig

from core.model_load import MasakhaneModelLoader


# this is only for debug purpose
# import ipdb
import os
from flask_restful import Api


def create_app(saved_models):

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


    register_extensions(app)
    register_resources(app, saved_models)

    # db = SQLAlchemy(app)

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



def load_model(src_language, trg_language, domain):   
    model_loader = MasakhaneModelLoader(
                                    available_models_file=os.environ.get('MODEL_ALL_FILE',
                                        './available_models.tsv'))

    # Download currently supported languages
    model_loader.download_model(src_language=src_language, 
                    trg_language=trg_language, domain=domain)
    
    model_dir = model_loader.load_model(src_language=src_language, 
                    trg_language=trg_language, domain=domain)

    return model_dir


# if __name__=='__main__' or __name__=='core':
    
models = {}

# Always start with English-Swahili (This will be revised in the future)
# models["en-sw"] = load_model("sw")


masakhane = create_app(models)


masakhane.models = models

# our_db.create_all()

#     masakhane.run(host='0.0.0.0', port=5001)


# for lan in Language.query.all():
#     print(lan.to_json())
#     print(masakhane.models)
#     models[f"{lan['source']}-{lan['target']}"] = load_model(f"{lan['target']}")