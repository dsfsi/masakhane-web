from flask import Flask
from flask import request,render_template


import ipdb
import os
from flask_restful import Api

from utils import model_load
from models.predict import Predicter
from resources.translate import TranslateResource

app = Flask(__name__)

api = Api(app)

api.add_resource(TranslateResource, '/translate')

if __name__=='__main__':
    app.run(port=5000, debug=True)
