from flask import Flask, jsonify, request
from flask_cors import CORS
import logging


logger = logging.getLogger(__name__)

def create_app(model_handler):
    app = Flask(__name__, static_url_path="")
    CORS(app)

    @app.route("/predict", methods=["GET", "POST"])
    def predict():
        request_data = request.get_json()
        logger.debug("REST Request: %s", request)
        response = model_handler.predict_raw(request_data)

        json_response = jsonify(response)
        if (
            isinstance(response, dict)
            and "status" in response
            and "code" in response["status"]
        ):
            json_response.status_code = response["status"]["code"]

        logger.debug("REST Response: %s", response)
        return json_response

    return app
