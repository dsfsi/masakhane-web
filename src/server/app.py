from flask import Flask
from flask import request, render_template
# this is only for debug purpose
# import ipdb
import os
from flask_restful import Api

from utils import model_load
from models.predict import Predicter
from resources.translate import TranslateResource, DeleteResource, AddResource

app = Flask(__name__)

api = Api(app)

api.add_resource(TranslateResource, '/translate')
api.add_resource(DeleteResource, '/delete')
api.add_resource(AddResource, '/add')

if __name__=='__main__':
    app.run(port=5000, debug=True)
