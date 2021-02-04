from flask import Flask
from flask import request, render_template
# this is only for debug purpose
# import ipdb
import os
from flask_restful import Api

from utils import model_load
from models.predict import Predicter
from resources.translate import TranslateResource, DeleteResource, AddResource, SaveResource, Home

masakhane = Flask(__name__)

api = Api(masakhane)

api.add_resource(Home, '/')
api.add_resource(TranslateResource, '/translate')
api.add_resource(DeleteResource, '/delete')
api.add_resource(AddResource, '/add')
api.add_resource(SaveResource, '/save')


if __name__=='__main__':
    masakhane.run(port=5000, debug=True)
