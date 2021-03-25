from flask_restful import Resource
from http import HTTPStatus

import ipdb
import os
import sqlite3

from core.model_load import MasakhaneModelLoader
from core.models.predict import Predicter
from core.models.feedback import Feedback

import json

from core.models.language import Language, language_list
from core.models.translation import Translation

from flask import request, current_app

def load_model(model_short_name):   
    model_loader = MasakhaneModelLoader(
                                    available_models_file="./available_models.tsv")

    # Download currently supported languages
    model_loader.download_model(model_short_name)
    
    model_dir = model_loader.load_model(model_short_name)

    return model_dir
    # model_dir, config, lc = model_loader.load_model(model_short_name)
    # return {"model_dir": model_dir, "config": config, "lc": lc}

class TranslateResource(Resource):
    def __init__(self, saved_models):
        # self.model_path = current_app.config['MODEL']
        # self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        self.models = saved_models
        # self.models = current_app.models
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

        # print(self.models)

        for couple in list(self.models.keys()):
            src, tgt = couple.split("-")
            output.append(
                {
                    "type": "source", "name" : self.languages_short_to_full[src].capitalize(), "value" : src
                }
            )
            output.append(
                {
                    "type": "target", "name" : self.languages_short_to_full[tgt].capitalize(), "value" : tgt
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
       
class AddResource(Resource):
    def __init__(self, saved_models):
        self.selected_models_file = current_app.config['MODEL_ALL_FILE']
        # self.models = current_app.models
        self.models = saved_models

    def get(self):

        print(self.models)

        now = list(self.models.keys())

        db_pairs = []

        # Update model form the db when doing the get call 
        for lan in Language.query.all():
            language_pair = lan.to_json()
            db_pair = f"{language_pair['source']}-{language_pair['target']}"
            
            # check if the model is not already loaded
            if db_pair not in now: 

                print(f"db_pair : {db_pair} \n now : {now}")

                self.models[db_pair] = load_model(f"{language_pair['target']}")
                db_pairs.append(db_pair)

        # To make sure that the model in memory are some with the one in the db
        for pair in now:
            if pair not in db_pairs:
                 del self.models[pair]

        return {'message': "Models updated"}, HTTPStatus.OK


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
                        accurate_translation = data['accurate_translation'], 
                        know_src_lang = data['know_src_lang'], 
                        know_tgt_lang = data['know_tgt_lang'], 
                        own_translation = data['own_translation'], 
                        text = data['text'], 
                        translation = data['translation'], 
                        understand_translation = data['understand_translation'], 
                        feedbackToken = data['feedbackToken'])

        feedback.save()

        return {'message' :"Review saved"}, HTTPStatus.CREATED
          

class HomeResource(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        return {'message': "welcome Masakhane Web"}, HTTPStatus.OK
        