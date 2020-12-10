from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import model_load
from models.predict import Predicter

from models.translation import Translation


class TranslateResource(Resource):
    # def get(Self):
    #     """
    #     Get all the recipes
    #     """
    #     data = []

    #     for recipe in recipe_list:
    #         if recipe.is_publish is True:
    #             data.append(recipe.data)

    #     return {'data': data}, HTTPStatus.OK

    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()

        available_models_file = 'data/available_models.tsv'

        model_loader = model_load.MasakhaneModelLoader(available_models_file=available_models_file)

        if data['target'] not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        model_dir, config, lc = model_loader.download_model(data['target'])

        translation_result = Predicter().predict_translation(data['input'], model_dir, lc)
        
        trans = Translation(source=data['source'],
                                target=data['target'],
                                    input=data['input'],
                                    # output=data['input'])
                                    output=translation_result)
        

        return trans.data, HTTPStatus.CREATED