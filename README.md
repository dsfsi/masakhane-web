# Masakhane WEB - A Machine Translation Web Platform for African Languages
<div align="center">
<img src="https://pbs.twimg.com/profile_images/1255858628986384384/d7Lk9I-w_400x400.jpg" >
</div>

[**Masakhane**](https://www.masakhane.io/) meaning ‘we build together’,  is a research effort for machine translation for African languages which is open source and online. So far, the community has built translation models based on [Joey NMT](https://github.com/joeynmt/joeynmt) for over 38 African languages. As such, **Masakhane Web** is a platform that aims to host the already trained models from the community and allow contributions from users to create new data for retraining. The objective of this web application is to provide access to an open-source platform that makes available relatively accurate translations for languages across Africa. If you can't find your language and/or would like to train your own machine translation model in your language, see https://github.com/masakhane-io/masakhane-mt on how you can contribute.
   

**Disclaimer:**  This system is for research purposes only and should be taken as work in progress. None of the trained models are suitable for production usage.

### Table of Contents

- [How to run](#how-to-run)
    - [As a stand alone app](#stand-alone)
        - [Backend](#bakend)
        - [Frontend](#frontend)
    - [Using Docker (Prefered)](#using-docker-(prefered))
- [Contributing](#contributing)
- [Contributors](#contributors)
- [Contact Us](#contact-us)
- [Acknowledgements](#acknowledgements)



## How to run

### As a stand alone app 

#### Backend 
- Install required packages 
    -  `pip install -r requirements.txt`
- run the app :
    - move to the server directory : `cd src/server/`
    - `export FLASK_APP=core/__init__.py`
    - `python manage.py run`

Note: The stand alone app uses sqlite as db instead of postgreSQL like our live app, you then need to run the command below to create and initialize the datbase. 

- Create table relations
    - `python manage.py create_db`
- Add languages 
    - `python manage.py add_language en-sw`
- Check available languages
    - `python manage.py all_language`
- Update known languages 
    - `curl --request GET 'http://127.0.0.1:5000/update'`

You can check content saved in the dabase using the code below :

```
import sqlite3, os

conn = sqlite3.connect("masakhane.db")
c = conn.cursor()

for row in c.execute('SELECT * FROM feedback'):
    print(row)

for row in c.execute('SELECT * FROM language'):
    print(row)
```

#### Frontend 
- install the following: \
    - [node.js](https://nodejs.org/en/)
    - [yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable)

- To run:
    - move to the client directory : `cd src/client/` 
    - run `yarn start`


This runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

View [https://github.com/dsfsi/masakhane-web/tree/master/src/client](https://github.com/dsfsi/masakhane-web/tree/master/src/client) on how you can contribute to improve the look of the website.

### Using Docker (Prefered)

The better way to run the app is to use Docker, which will take care of running both the `frontend` and `backend` easily.

#### Install Docker and Docker-compose 

Run the following command to check if you have `docker` and `docker-compose` installed in your computer :
    - `docker --version`
    - `docker-compose --version`

If you get the information about the version and not an error you can skeep the details below and just to the Using Docker section. 

- Docker : `https://docs.docker.com/engine/install/`
- Docker-compose : `https://docs.docker.com/compose/install/`

To make sure that it is well installed you can run the code above to check the version of the installed `docker` and `docker-compose`

#### Run the App

- run the app 
    * `sudo docker-compose up -d --build` from the root project. 
- shutdown the app
    * `sudo docker-compose down` 

- create_db
    * `sudo docker-compose exec server python manage.py create_db`

- check the database
    * `sudo docker-compose exec db psql --username=masakhane --dbname=masakhane`
        * list databases`\l`
        * connect to the masakhane database`\c masakhane`
        * list relations `\dt`
        * to quit `\q`
        * to see saved information in a relation `select * from language;`
        or 
        * to see feedbacks in a relation `select * from feedback;`

#### Add, Delete and Update supported languages  
- The
- check the available models in memory `sudo docker-compose exec server python manage.py all_language`
- add a new language, 
    - e.g English-Swahili (note: we are using JW300 shortform) `sudo docker-compose exec server python manage.py add_language en-sw`curre
    - (English-Yoruba) `sudo docker-compose exec server python manage.py add_language en-yo`
- delete a language `sudo docker-compose exec server python manage.py remove_language en-sw`
- run this on the production server to update the models `curl --request GET 'http://127.0.0.1:5000/update'`




# Contributing

## Options
- *Can't see your language as one of the supported languages: Visit [Masakhane:Building your first machine translation model](https://github.com/masakhane-io/masakhane-mt#building-your-first-machine-translation-model) to learn more about how you can train a model for your language.*
- *I have an idea or a new feature: Create a new issue first, assign it to yourself and then fork the repo*
- *I want to help in improving the accuracy of the models: Check out below on how you can reach out to us*

## Submitting Changes[Pull Request]
- See [https://opensource.com/article/19/7/create-pull-request-github](https://opensource.com/article/19/7/create-pull-request-github)

# Contributors
<a href="https://github.com/dsfsi/masakhane-web/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dsfsi/masakhane-web" />
</a>

Made with [contributors-img](https://contrib.rocks).


# Contact Us
- Vukosi Marivate - vukosi.marivate@cs.up.ac.za
- Abiodun Modupe  - abiodun.modupe@cs.up.ac.za
- Salomon Kabongo - skabenamualu@aimsammi.org 
- Catherine Gitau - cgitau@aimsammi.org

# License
[MIT](https://mit-license.org/)

## Citing the project
**On a visualisation/notebook/webapp:**

> Data Science for Social Impact Research Group @ University of Pretoria, Masakhane NLP, *Masakhane WEB - A Machine Translation Web Platform for African Languages* Available on: [https://github.com/dsfsi/masakhane-web](https://github.com/dsfsi/masakhane-web).

**In a publication**

Software

> @software{marivate_vukosi_2021_4745501,
  author       = {Marivate, Vukosi and
                  Gitau, Catherine and
                  Kabenamualu, Salomon and
                  Modupe, Abiodun and
                  Masakhane NLP},
  title        = {{Masakhane WEB - A Machine Translation Web Platform 
                   for Solely African Languages}},
  month        = may,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {0.9},
  doi          = {10.5281/zenodo.4745501},
  url          = {[https://doi.org/10.5281/zenodo.4745501](https://doi.org/10.5281/zenodo.4745501)}
}

# Acknowledgements

We want to acknowledge support from the following organisations
- [Mozilla](https://www.mozilla.org/en-US/moss/)  
- [Google Cloud Platfrom](https://cloud.google.com/)


<!-- ### Mount GCB

gcloud auth application-default login
gcloud auth login

mkdir bucket/
gcsfuse maskhane-web-test bucket/
GOOGLE_APPLICATION_CREDENTIALS=./json.json gcsfuse maskhane-web-test bucket/

fusermount -u  bucket/ -->
