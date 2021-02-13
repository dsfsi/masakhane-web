# test_hello.py
from app import create_app
from flask import json, jsonify
# import unittest

def test_home_page():
    "Test the home endpoint"
    app = create_app()
    response = app.test_client().get('/')

    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == "welcome Masakhane Web"

# TODO We will need to have a dump database to check this 
def test_translation():
    app = create_app()
    response = app.test_client().post(
        '/translate',
        data = json.dumps({
            "src_lang":"en",
            "tgt_lang":"sw",
            "input":"How are you doing today ?",
            "review":"Translation in Swahili for : How are you doing today ?",
            "stars":"5"}),
            content_type='application/json',
            )

    data = response.get_json()

    assert response.status_code == 201 # created

    # Givent that we can't know exactly the output of the translation
    # we can test that some result are return 
    assert data['output'] != ""  
    
def test_save():
    """
    Test the save endpoint by checking the status code 
    and the responce message.
    """
    app = create_app()
    response = app.test_client().post(
                    '/save',
                    data = json.dumps({
                        "src_lang":"en",
                        "tgt_lang":"sw",
                        "input":"How are you doing today ?",
                        "review":"Test Saving",
                        "stars":"5",
                        "token":"ww2wki&idjj11yyy"}),
                        content_type='application/json',
                        )


    assert response.status_code == 201
    
    assert b"Review saved" in response.data