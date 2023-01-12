# **Project Details**
The requirements of Masakhane Web is to faciliate translations for African languages using different machine translation models. There is also an feauture to provide feedback and correction to inaccurate translations. 

## **Table of Contents**
- [**Tech Stack**](#tech-stack)
  - [**Frontend**](#frontend)
    - [**React**](#react)
    - [**Webpack**](#webpack)
  - [**Backend**](#backend)
    - [**Python**](#python)
    - [**Database**](#database)
    - [**Flask**](#flask)
- [**File Structure**](#file-structure)



# **Tech Stack**

## **Frontend** 
Review the [client readme](../../src/client/README.md) for more information.

### **React**
The frontend is written using [React](https://reactjs.org/).

### **Webpack**
The frontend also makes use of [Webpack](https://webpack.js.org/), a static module bundler for modern JavaScript applications.

-  **Webpack DevServer & Proxy**  
    The [devServer](https://webpack.js.org/configuration/dev-server/) runs on http://translate.masakhane.io:80.  
    The [proxy](https://webpack.js.org/configuration/dev-server/#devserverproxy) allows you to send requests to http://translate.masakhane.io/translate and have it hit the backen at http://localhost:5000/translate. 


## **Backend**
Review the [server readme](../../src/server/README.md) for more information

### **Python**
The backend is written using [Python](https://www.python.org/)

### **Database**
The backend database is predominantly PostgreSQL on Docker, but there is an option to use SQLite when running a stand-alone backend.

### **Flask**
The backend also makes use of [Flask](https://flask.palletsprojects.com/en/2.2.x/), which is for web development in Python. 

- **App**  
    Masakhane Web makes use of the Flask [application factory](https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/) pattern in `src/core/__init__.py` 

- **API**  
    The API uses [flask_restful](https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing) and is defined in `src/core/resources/translate.py`.  
    It is initialised along with the app in `src/core/__init__.py`.  

- **Database**  
  The application interacts with the database using [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) and is defined in `src/core/extensions.py`.  
    It is initialised along with the app in `src/core/__init__.py`. (Note the `.env.dev` for database config)

# **File Structure**

```
.masakhane-web
|-- docker-compose.yml              # Docker compose for local instance
|-- docker-compose.prod.yml         # Docker compose for production instance
|-- entrypoint.sh
|-- environment.yaml
`-- src
    |-- client                      # IDK much about the frontend, update required
    |   |-- Dockerfile                              
    |   |-- package-lock.json                     
    |   |-- package.json                                
    |   |-- public                                      
    |   |-- src                                   
    |   |   |-- App.js
    |   |   |-- App.test.js                       
    |   |   |-- components
    |   |   |   |-- translateCard.js
    |   |   |   `-- *others*
    |   |   |-- images
    |   |   |-- index.css                         
    |   |   |-- index.js
    |   |   |-- logo.svg
    |   |   |-- pages
    |   |   |   |-- About.js
    |   |   |   |-- Faq.js
    |   |   |   `-- Home.js
    |   |   |-- reportWebVitals.js
    |   |   |-- setupProxy.js                           
    |   |   `-- setupTests.js
    |   `-- webpack.config.js
    `-- server
        |-- __init__.py                                        
        |-- available_models.tsv    # TSV file containing available models     
        |-- languages.json          # JSON file containing language information (names, etc)
        |-- Dockerfile
        |-- entrypoint.sh           # Docker entrypoint for Dockerfile
        |-- Dockerfile.prod
        |-- entrypoint.prod.sh      # Docker entrypoint for Dockerfile.prod
        |-- requirements.txt        # Python dependencies
        |-- manage.py               # Manage CLI 
        |-- core
        |   |-- __init__.py         # Flask app factory & init
        |   |-- resources     
        |   |   `-- translate.py    # Flask API
        |   |-- extensions.py       # Flask_SQLAlchemy init
        |   |-- models
        |   |   |-- feedback.py     # Feedback DB Model
        |   |   |-- language.py     # Language DB Model
        |   |   |-- predict.py      # I think this is in the wrong place, does the translation
        |   |   `-- translation.py  # Translation object
        |   |-- model_load.py       # Class to manage the download and loading of different translation models 
        |   |-- config.py           # Different config states for dev enviroments
        |   |-- languages.json      # Duplicate of ../languages.json
        |   |-- tests           
        |   |   |-- __init__.py
        |   |   |-- base.py         # Test create app
        |   |   |-- test_app.py     # Test API
        |   |   `-- test_config.py  # Dev tests
        |   |-- utils.py
        |   `-- utils_bucket
        |       |-- bucket.py
        |       `-- upload_download.py
        |-- models  # Translation models are stored here
        |   `-- joeynmt
        |       |-- en-sw-JW300     # File struct of a complete model for English to Swahili
        |       |   |-- config.yaml
        |       |   |-- config_orig.yaml
        |       |   |-- model.ckpt
        |       |   |-- src.bpe.model
        |       |   |-- src_vocab.txt
        |       |   |-- trg.bpe.model
        |       |   `-- trg_vocab.txt
        `-- nginx
            |-- Dockerfile
            `-- nginx.conf
```