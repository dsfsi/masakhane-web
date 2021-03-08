import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL = "./models/joeynmt/"
    TEMP = "./temp/"
    MODEL_ALL_FILE = "./available_models.tsv"
    JSON = "./languages.json"
    
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super-secret-key'    
    basedir = os.path.abspath(os.path.dirname(__file__))

class StagingConfig(Config):
    """
    This is an imitation of the production environment for 
    testing purpose. 
    """
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', "sqlite://")
    MODEL = os.getenv('MODEL', "./")

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY', "sqlite://")
    MODEL = os.getenv('MODEL', "./")

