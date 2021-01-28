from flask import request, jsonify, make_response
from flask_restful import Resource
from http import HTTPStatus
from utils import model_load
from models.predict import Predicter

import os
import sqlite3
import shutil

from models.translation import Translation

import json

class TranslateResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.selected_models_file = '../../data/external/selected_models.tsv'
        self.model_path = '../../models/joeynmt/'

    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()

        model = self.model_path+data['source']+'-'+data['target']
        
        if not os.path.exists(model):
            return {'message' :'model not found'}, HTTPStatus.NOT_FOUND 

        else : 
            model_loader = model_load.MasakhaneModelLoader(
                                available_models_file=self.selected_models_file)

            if data['target'] not in model_loader.models.keys():
                return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

            model_dir, config, lc = model_loader.load_model(data['target'])

            translation_result = Predicter().predict_translation(data['input'], model_dir, lc)
            
            trans = Translation(source=data['source'],
                                    target=data['target'],
                                        input=data['input'],
                                        output=translation_result)
            
            cur_dir = os.path.dirname(__file__)
            db = os.path.join(cur_dir, 'masakhane.sqlite')

            def sqlite_entry(path, source, target, 
                                    original_text, translation_suggested, stars):
                conn = sqlite3.connect(path)
                c = conn.cursor()
                c.execute("INSERT INTO masakhane (Date, Source, Target,  \
                                        OriginalText, TranslationSuggested, Stars)"\
                " VALUES (DATETIME('now'), ?, ?,  ?, ?, ?)", (source, target, \
                                            original_text, translation_suggested, stars))
                conn.commit()
                conn.close()

            # TODO: Need to work on when to save the feedback

            # if (int(data['review'])>=4) :
            # sqlite_entry(db, data['source'], data['target'], \
            #                 data['input'], data['review'], data['stars'])
                
            return trans.data, HTTPStatus.CREATED

    
    def get(self):
        return os.listdir(self.model_path), HTTPStatus.OK        

class DeleteResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.selected_models_file = '../../data/external/selected_models.tsv'
        self.model_path = '../../models/joeynmt/'

    def delete(self):
        """
        Translate a sentence
        """

        data = request.get_json()

        try:

            shutil.rmtree(self.model_path+data['lag'])
            
            # os.rmdir(self.model_path+data['lag'])
            return data['lag'], HTTPStatus.OK

        except OSError as e:
            print("Error: %s : %s" % (self.model_path+data['lag'], e.strerror))
            return HTTPStatus.NOT_FOUND
       
class AddResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.selected_models_file = '../../data/external/available_models.tsv'
        self.model_path = '../../models/joeynmt/'
        self.path_to_json = '../../data/external/languages.json'


    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()

        model_loader = model_load.MasakhaneModelLoader(
                            available_models_file=self.selected_models_file)

        if data['target'] not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        model_loader.download_model(data['target'])

        
        # available_json = {}
        # temp_dict = {}

        # with open(self.path_to_json, 'r') as f:
        #     distros_dict = json.load(f)

        # for distro in distros_dict:
        #     temp_dict[distro['language_short']] = distro['language_en']


        return {'message' :f"language {data['target']} downloaded"}, HTTPStatus.CREATED       