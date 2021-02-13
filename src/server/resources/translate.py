from flask_restful import Resource
from http import HTTPStatus
from model_load import MasakhaneModelLoader
from models.predict import Predicter
from models.feedback import Feedback
import os
import shutil

from models.translation import Translation

from flask import request, current_app

class TranslateResource(Resource):
    def __init__(self):
        self.model_path = current_app.config['MODEL']
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']

    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()
        
        model = self.model_path+data['src_lang']+'-'+data['tgt_lang']
        
        if not os.path.exists(model):
            return {'message' :'model not found'}, HTTPStatus.NOT_FOUND 

        else : 
            model_loader = MasakhaneModelLoader(
                                available_models_file=self.selected_models_file)

            model_dir, config, lc = model_loader.load_model(data['tgt_lang'])

            translation_result = Predicter().predict_translation(data['input'], model_dir, lc)
            
            trans = Translation(src_lang=data['src_lang'],
                                    tgt_lang=data['tgt_lang'],
                                        input=data['input'],
                                        output=translation_result)
            
            return trans.data, HTTPStatus.CREATED
    
    def get(self):
        return os.listdir(self.model_path), HTTPStatus.OK        

class DeleteResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        self.model_path = current_app.config['MODEL']

    def delete(self):
        """
        Translate a sentence
        """
        data = request.get_json()

        try:
            shutil.rmtree(self.model_path+data['tgt_lang']) 
            # os.rmdir(self.model_path+data['lag'])
            return data['tgt_lang'], HTTPStatus.OK

        except OSError as e:
            print("Error: %s : %s" % (self.model_path+data['tgt_lang'], e.strerror))
            return HTTPStatus.NOT_FOUND
       
class AddResource(Resource):
    def __init__(self):
        super().__init__()
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        self.model_path = current_app.config['MODEL']
        print(current_app.config)
        self.path_to_json = current_app.config['JSON']


    def post(self):
        """
        Translate a sentence
        """
        data = request.get_json()

        model_loader = MasakhaneModelLoader(
                            available_models_file=self.selected_models_file)

        if data['tgt_lang'] not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        model_loader.download_model(data['tgt_lang'])


        return {'message' :f"language {data['tgt_lang']} downloaded"}, HTTPStatus.CREATED       

class SaveResource(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        """
        Save into the database

        params:
        -------
            - data['src_lang']    : The source language 
            - data['tgt_lang']    : The target language
            - data['input']     : The input setence
            - data['review']    : The suggested translation correction
            - data['stars']     : The confidence of the suggested translation
            - data['token'] : User authorisation to collect data token (Boolean value)
        """          

        data = request.get_json()

        feedback = Feedback(
                        src_lang = data['src_lang'], 
                        tgt_lang = data['tgt_lang'], 
                        input = data['input'], 
                        review = data['review'], 
                        stars = data['stars'], 
                        token = data['token'])

        feedback.save()

        return {'message' :"Review saved"}, HTTPStatus.CREATED
          

class HomeResource(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        return {'message': "welcome Masakhane Web"}, HTTPStatus.OK
        