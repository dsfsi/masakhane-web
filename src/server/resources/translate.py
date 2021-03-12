from flask_restful import Resource
from http import HTTPStatus

import ipdb
from model_load import MasakhaneModelLoader
from models.predict import Predicter
from models.feedback import Feedback

import os
import shutil
import json


from models.translation import Translation

from flask import request, current_app

class TranslateResource(Resource):
    def __init__(self, saved_models):
        # self.model_path = current_app.config['MODEL']
        # self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        self.models = saved_models
        # self.path_to_json = current_app.config['JSON']

        with open(current_app.config['JSON'], 'r') as f:
            distros_dict = json.load(f)

        self.languages_short_to_full = {}
        self.languages_full_to_short = {}

        for distro in distros_dict:
            self.languages_short_to_full[distro['language_short'].lower()] = distro['language_en'].lower()
            self.languages_full_to_short[distro['language_en'].lower()] = distro['language_short'].lower()

    def post(self):
        """
        Translate a sentence
        """

        # global models 
        data = request.get_json()

        source_language = data['src_lang'].lower()
        target_language = data['tgt_lang'].lower()

        source_language_short = self.languages_full_to_short[source_language]
        target_language_short = self.languages_full_to_short[target_language] 
        
        input_model = source_language_short+'-'+target_language_short

        if input_model not in self.models.keys():
            return {'message' :'model not found'}, HTTPStatus.NOT_FOUND         

        else : 
            translation_result = Predicter().translate(
                data['input'], model=self.models[input_model]['model'],
                src_vocab=self.models[input_model]['src_vocab'],
                trg_vocab=self.models[input_model]['trg_vocab'],
                preprocess=self.models[input_model]['preprocess'],
                postprocess=self.models[input_model]['postprocess'],
                logger=self.models[input_model]['logger'],
                beam_size=self.models[input_model]['beam_size'],
                beam_alpha=self.models[input_model]['beam_alpha'],              
                level=self.models[input_model]['level'],
                lowercase=self.models[input_model]['lowercase'],
                max_output_length=self.models[input_model]['max_output_length'],
                use_cuda=self.models[input_model]['use_cuda'],
                )
            
            trans = Translation(src_lang=data['src_lang'],
                                    tgt_lang=data['tgt_lang'],
                                        input=data['input'],
                                        output=translation_result)
            
            return trans.data, HTTPStatus.CREATED
    
    def get(self):

        output = []
        for couple in list(self.models.keys()):
            src, tgt = couple.split("-")
            output.append(
                {
                    "id": "source", "name" : self.languages_short_to_full[src].capitalize(), "value" : src
                }
            )
            output.append(
                {
                    "id": "target", "name" : self.languages_short_to_full[tgt].capitalize(), "value" : tgt
                }
            )

        output = list({v['name']:v for v in output}.values())

        return output, HTTPStatus.OK         

def load_model(model_short_name):   
    model_loader = MasakhaneModelLoader(
                                    available_models_file=current_app.config['MODEL_ALL_FILE'])

    # Download currently supported languages
    model_loader.download_model(model_short_name)
    
    model_dir = model_loader.load_model(model_short_name)

    return model_dir

class DeleteResource(Resource):
    def __init__(self, saved_models) -> None:
        super().__init__()
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        self.model_path = current_app.config['MODEL']
        self.models = saved_models

    def delete(self):
        """
        Translate a sentence
        """
        data = request.get_json()

        try:
            # shutil.rmtree(self.model_path+data['tgt_lang']) 
            # os.rmdir(self.model_path+data['lag'])

            result = self.models.pop(data['tgt_lang'], None)

            if result != None:
                return data['tgt_lang'], HTTPStatus.OK
            else:
                raise Exception('This model does not exist in memory')

        except Exception as e:
            return {'message' :"Model doesn't exist in memory"}, HTTPStatus.NOT_FOUND
       
class AddResource(Resource):
    def __init__(self, saved_models):
        super().__init__()
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']

        self.models = saved_models

        with open(current_app.config['JSON'], 'r') as f:
            distros_dict = json.load(f)

        self.languages_short_to_full = {}
        self.languages_full_to_short = {}

        for distro in distros_dict:
            self.languages_short_to_full[distro['language_short'].lower()] = distro['language_en'].lower()
            self.languages_full_to_short[distro['language_en'].lower()] = distro['language_short'].lower()


    def post(self):
        """
        Translate a sentence
        """
        data = request.get_json()

        source_language = data['src_lang'].lower()
        target_language = data['tgt_lang'].lower()

        source_language_short = self.languages_full_to_short[source_language]
        target_language_short = self.languages_full_to_short[target_language] 

        model_loader = MasakhaneModelLoader(
                            available_models_file=self.selected_models_file)

        # print(model_loader)
        if target_language_short not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        self.models[source_language_short+'-'+target_language_short] = load_model(target_language_short)
        
        return {'message' :f"language {target_language_short} downloaded"}, HTTPStatus.CREATED       

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
        print('l')
        return {'message': "welcome Masakhane Web"}, HTTPStatus.OK
        