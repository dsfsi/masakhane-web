from flask import Flask, json, request
from flask import jsonify
# from flask import request,render_template
# import json as json


from utils import model_load
from models.predict import Predicter


from flask_cors import CORS, cross_origin
# from predict import Predicter
import os

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# pred = Predicter()

@app.route('/translate',methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type', 'Authorization'])
def sentiment():
    available_models_file = 'data/available_models.tsv'

    model_loader = model_load.MasakhaneModelLoader(available_models_file=available_models_file)

    model_dir, config, lc = model_loader.download_model('twi')
    # model_dir, config, lc = model_loader.download_model('ln')

    print(request)
    
    if request.method =='POST':
        #sentence = request.body.sentence

        data = request.data
        print(json.loads(data))

        #print(jsonify(request.data))
        # sentence = request.form['feedback']
        #sentence = "Hello \t me"
        sentence = json.loads(data)

        sentiment = Predicter().predict_translation(sentence, model_dir, lc)

        
        # feedback = {'feedback': 'this is feedback'}
        return json_response(sentiment)

    return json_response({'error': 'kudo not found'}, 404)
    #     return render_template('index.html',feedback=sentiment,sentiment_value=sentiment, predict=True)

    # return render_template('index.html', predict=False)

def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})