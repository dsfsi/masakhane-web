#External modules
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from collections import defaultdict
import os, json
#Internal modules
from core.model_load import MasakhaneModelLoader
from core.models.predict import Predicter
from core.models.feedback import Feedback
from core.models.language import Language
from core.models.translation import Translation


class TranslateResource(Resource):
    """ TranslateResource
        -----------------
        #### User-Defined Flask API Resource accepting GET & POST\n
        GET - List's available models\\
        POST - Performs translation from srg lang to tgt lang, review the server ReadMe for more info.
    """
    def __init__(self, saved_models):
        self.models = saved_models

        # load languages.json into distros_dict
        json_file = os.environ.get('JSON','./languages.json')
        with open(json_file, 'r') as f:
            distros_dict = json.load(f)
        # init empty dicts to store full_name to short_name bindings
        self.languages_short_to_full = {}
        self.languages_full_to_short = {}

        for distro in distros_dict:
            self.languages_short_to_full[distro['language_short'].lower(
            )] = distro['language_en'].lower()
            self.languages_full_to_short[distro['language_en'].lower(
            )] = distro['language_short'].lower()
        # Example: languages_short_to_full['sw'] = 'swahili'
        # Example: languages_full_to_short['Swahili'] = 'sw'

    def post(self):
        """POST method to translate a given input
        ---

        ### Request Body
        ```json 
        {
            "src_lang" : "src_lang_full",
            "tgt_lang" : "tgt_lang_full",
            "input": "input_text",
        }
        ```
        ### Returns a Translation Object defined in `src/server/core/models/translation.py`
        ```json 
        {
            "src_lang" : "src_lang_full",
            "tgt_lang" : "tgt_lang_full",
            "input": "input_text",
            "output": "translation_result"
        }
        ```
        """
        # Get req body
        data = request.get_json()

        source_language = data['src_lang'].lower()
        target_language = data['tgt_lang'].lower()

        #Get short_name from self.language_dicts
        source_language_short = self.languages_full_to_short[source_language]
        target_language_short = self.languages_full_to_short[target_language]

        #model key to provide translation
        input_model = source_language_short+'-'+target_language_short

        if input_model not in self.models.keys():
            return {'message': 'model not found'}, HTTPStatus.NOT_FOUND
        else:
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
        """GET Method to list available models in memory
        ---

        Returns a json list, ie
        ```json
        [
            {
                "type": "source",
                "name": "src_lang_full",
                "value": "src_lang_short",
                "targets": [
                    {
                        "name": "tgt_lang_full",
                        "value": "tgt_lang_short"
                    }
                ]
            }
        ]
        ```
        """

        dict_output = defaultdict(lambda: [])
        #for each src-tgt key in model dict 
        for couple in list(self.models.keys()):
            src, tgt = couple.split("-")
            dict_output[src].append(
                {
                    'name': self.languages_short_to_full[tgt].capitalize(),
                    'value': tgt
                }
            )

        output = []
        for source in dict_output:
            output.append(
                {
                    "type": "source",
                    "name": self.languages_short_to_full[source].capitalize(),
                    "value": source,
                    'targets': dict_output[source]
                }
            )

        return output, HTTPStatus.OK


class AddResource(Resource):
    """ AddResource
        -----------------
        #### User-Defined Flask API Resource accepting GET\n
        GET - Updates the models based on the model info stored in the Language table
    """
    def __init__(self, saved_models):
        self.models = saved_models
        # Load file path to avialable_models.tsv which has all the github & google drive links that store the model files
        self.selected_models_file = os.environ.get('MODEL_ALL_FILE',
                                                   "./available_models.tsv")

    def get(self):
        """GET Method to update the available models
            ---
            Returns a json Object, ie
            ```json
            {
                "message": "Models updated"
            }
            ```
        """
        model_loader = MasakhaneModelLoader(available_models_file=os.environ.get('MODEL_ALL_FILE',
                                             './available_models.tsv'))
        db_pairs = []
        if not os.path.exists(filePath):
            os.makedirs('./models/joeynmt')
        downloaded_models = os.listdir('./models/joeynmt')
        #loads model info from the Language table
        for lan in Language.query.all():
            language_pair = lan.to_json()
            src_language =language_pair['source']
            tgt_language = language_pair['target']
            domain = language_pair['domain']
            db_pair = f"{language_pair['source']}-{language_pair['target']}"
            # check if the model is not already loaded in memory
            if db_pair not in list(self.models.keys()):
                name_tag = src_language+"-"+tgt_language+"-"+domain
                # check if the model is not already downloaded
                if name_tag not in downloaded_models:
                    print("Downloading model for "+name_tag)
                    model_loader.download_model(src_language, tgt_language, domain)
                # Attempts to download model and store in self.models
                self.models[db_pair] = model_loader.load_model(src_language, tgt_language, domain)
                print(f"db_pair : {db_pair} \n now : {list(self.models.keys())}")

            # keep all the pairs in the db
            db_pairs.append(db_pair)

        # Remove models from memory that are not listed in the DB Language table 
        for pair in list(self.models.keys()):
            if pair not in db_pairs:
                del self.models[pair]

        return {'message': "Models updated"}, HTTPStatus.OK


class SaveResource(Resource):
    """ SaveResource
        ------------
        #### User-Defined Flask API Resource accepting POST\n
        POST - saves feedback/correction information into the Feedback database
    """
    def __init__(self):
        super().__init__()

    def post(self):
        """POST Method to save feeback into the DB Feedback table
        ---
        ### Request Body
        ```json 
        {
            "src_lang" : "src_lang_full",
            "tgt_lang" : "tgt_lang_full",
            "input": "input_text",
            "review": "translation_correction",
            "stars": "translation_confidence",
            "token": "user_auth(bool)",
        }
        ```
        ### Returns a Translation Object defined in `src/server/core/models/translation.py
        ```json 
        {
            "message": "Review saved"
        }
        """

        data = request.get_json()

        feedback = Feedback(
            src_lang=data['src_lang'],
            tgt_lang=data['tgt_lang'],
            accurate_translation=data['accurate_translation'],
            know_src_lang=data['know_src_lang'],
            know_tgt_lang=data['know_tgt_lang'],
            own_translation=data['own_translation'],
            text=data['text'],
            translation=data['translation'],
            understand_translation=data['understand_translation'],
            feedbackToken=data['feedbackToken'])

        feedback.save()

        return {'message': "Review saved"}, HTTPStatus.CREATED


class HomeResource(Resource):
    """ HomeResource
        ------------
        User-Defined Flask API Resource accepting GET\n
        GET - returns {'message': "welcome Masakhane Web"}
    """
    def __init__(self):
        super().__init__()

    def get(self):
        return {'message': "welcome Masakhane Web"}, HTTPStatus.OK
