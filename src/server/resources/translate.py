from flask import request, jsonify, make_response
from flask_restful import Resource
from http import HTTPStatus
from utils import model_load
from models.predict import Predicter

from models.translation import Translation
import json

class TranslateResource(Resource):

    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()

        available_models_file = '../../data/external/available_models.tsv'

        model_loader = model_load.MasakhaneModelLoader(
                            available_models_file=available_models_file)

        if data['target'] not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        model_dir, config, lc = model_loader.download_model(data['target'])

        translation_result = Predicter().predict_translation(data['input'], model_dir, lc)
        
        trans = Translation(source=data['source'],
                                target=data['target'],
                                    input=data['input'],
                                    output=translation_result)
        

        return trans.data, HTTPStatus.CREATED

    
    def get(self):
        available_models_file = '../../data/external/available_models.tsv'

        model_loader = model_load.MasakhaneModelLoader(
                            available_models_file=available_models_file)
        
        path_to_json = '../../data/external/languages.json'

        available_json = {}
        temp_dict = {}

        with open(path_to_json, 'r') as f:
            distros_dict = json.load(f)

        for distro in distros_dict:
            temp_dict[distro['language_short']] = distro['language_en']


        for lang in model_loader.models.keys():
            available_json[temp_dict[lang]] = lang

        return available_json, HTTPStatus.OK        