from flask import request, jsonify, make_response
from flask_restful import Resource
from http import HTTPStatus
from utils import model_load
from models.predict import Predicter

import os
import sqlite3

from models.translation import Translation

import json

class TranslateResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.selected_models_file = '../../data/external/selected_models.tsv'

    def post(self):
        """
        Translate a sentence
        """

        data = request.get_json()


        model_loader = model_load.MasakhaneModelLoader(
                            available_models_file=self.selected_models_file)

        if data['target'] not in model_loader.models.keys():
            return {'message' :'language not found'}, HTTPStatus.NOT_FOUND

        model_dir, config, lc = model_loader.download_model(data['target'])

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

        # if (int(data['review'])>=4) :
        sqlite_entry(db, data['source'], data['target'], \
                        data['input'], data['review'], data['stars'])
            
        return trans.data, HTTPStatus.CREATED

    
    def get(self):

        model_loader = model_load.MasakhaneModelLoader(
                            available_models_file=self.selected_models_file)
        
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