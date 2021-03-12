from core.resources.translate import TranslateResource, DeleteResource, AddResource, SaveResource, HomeResource

from flask import Flask
from flask import request, render_template

from core.models.feedback import Feedback
from core.models.language import Language, language_list

from flask_migrate import Migrate
from core.extensions import db
from core.config import Config, DevelopmentConfig, ProductionConfig, StagingConfig

from core.model_load import MasakhaneModelLoader

from flask_sqlalchemy import SQLAlchemy


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
    app.config.from_object(config_str)


    register_extensions(app)
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



def load_model(model_short_name):   
    model_loader = MasakhaneModelLoader(
                                    available_models_file="./available_models.tsv")

    # Download currently supported languages
    model_loader.download_model(model_short_name)
    
    model_dir = model_loader.load_model(model_short_name)

    return model_dir
    # model_dir, config, lc = model_loader.load_model(model_short_name)
    # return {"model_dir": model_dir, "config": config, "lc": lc}




# print(models["en-sw"])

# import psycopg2
# try: 
#     conn = psycopg2.connect(database="masakhane", user="masakhane",  
#     password="masakhane", host="localhost")
#     print("connected")

#     mycursor =conn.cursor()
#     mycursor.execute("SELECT * FROM language")
#     data = mycursor.fetchall()

#     print(data)

# except:
#     print ("I am unable to connect to the database")

# print(Language.query.all())


models = {}
# models["en-sw"] = load_model("sw")

# for lan in Language.query.all():
#     print(lan.to_json())
#     models[f"{lan['source']}-{lan['target']}"] = load_model("sw")

masakhane = create_app(models)
# db.create_all()
# db.session.commit()

masakhane.models = models

# if __name__=='__main__':
#     masakhane.run(host='0.0.0.0', port=5001)