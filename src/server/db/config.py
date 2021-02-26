import os

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL = "../../models/joeynmt/"
    TEMP = "temp/"
    MODEL_ALL_FILE = "../../data/external/available_models.tsv"
    JSON = "../../data/external/languages.json"
    
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://masakhane:masakhane@localhost/masakhane'

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MODEL = os.environ.get('MODEL')

class StagingConfig(Config):
    """
    This is an imitation of the production environment for 
    testing purpose. 
    """
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MODEL = os.environ.get('MODEL')