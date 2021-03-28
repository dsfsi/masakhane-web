==============================

# Masakhane WEB

TODO : description of the project 


## How to run

### As a stand alone app 

#### Backend 
- Install requiered packages 
    -  `pip install -r requirements.txt`
- run the app :
    - move to the server directory : `cd src/server/`
    - `export FLASK_APP=core/__init__.py`
    - `python manage.py run`

Note: The stand alone app uses sqlite as db instead of postgress like our live app, you then need to run the command bellow to create initialise and create the datbase 

- Create table relations
    - `python manage.py create_db`
- Add languages 
    - `python manage.py add_language en-sw-JW300`
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

To delete an existing sqlite db `rm core/masakhane.db`

#### Frontend 
TODO : Need to be completed by Cate 




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

#### Add, Delete and Updaate supported languages  

- check the available models in memory `sudo docker-compose exec server python manage.py all_language`
- add a new language, 
    - e.g English-Swahili (note: we are using JW300 shortform) `sudo docker-compose exec server python manage.py add_language en-sw`curre
    - (English-Yoruba) `sudo docker-compose exec server python manage.py add_language en-yo`
- delete a language `sudo docker-compose exec server python manage.py remove_language en-sw`
- run this on the production server to update the models `curl --request GET 'http://127.0.0.1:5000/update'`


<!-- ### Mount GCB

gcloud auth application-default login
gcloud auth login

mkdir bucket/
gcsfuse maskhane-web-test bucket/
GOOGLE_APPLICATION_CREDENTIALS=./json.json gcsfuse maskhane-web-test bucket/

fusermount -u  bucket/ -->