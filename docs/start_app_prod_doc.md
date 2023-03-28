# **Running the App In Production**
To run the app locally, see [here](start_app_locally_doc.md)

## **Table of Contents**
  - [**Docker Setup**](#docker-setup)
  - [**Running the app**](#running-the-app)
    - [**Building the App**](#building-the-app)
    - [**Shut down the app**](#shut-down-the-app)
    - [**Add, Update, \& Delete Languages**](#add-update--delete-languages)
    - [**Running tests**](#running-tests)
 

## **Docker Setup**

Ensure you have `docker` & `docker-compose` installed on your computer, you can check with the following commands:
```bash
docker --version
docker-compose --version
```

If the above commands return an error, please install [Docker](https://docs.docker.com/engine/install/) and [Docker-compose](https://docs.docker.com/compose/install/).

## **Running the app**
###  **Building the App**
To build the app, from the root project directory, run the following command:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### **Shut down the app**
To shut down the app, run the following command to remove the docker container:
```bash
docker-compose -f docker-compose.prod.yml down
```

### **Add, Update, & Delete Languages**
**Add a Language**
```bash
docker-compose -f docker-compose.yml exec api python manage.py add_language en-sw-JW300
```
The language code parameter `en-sw-JW300` represents {src-lang}-{tgt-lang}-{shortform}  
So `en-sw-JW300` represents English-Swahili using JW300 shortform  
**Note** - A code parameter example without shortform is `en-tiv-`

Download available languages csv [here](https://zenodo.org/record/7417644/files/masakhane-mt-current-models.csv) 

**Update Langugaes**
```bash
curl --request GET 'http://127.0.0.1:5000/update'
```

**Check available languages**
```bash
docker-compose -f docker-compose.prod.yml exec api python manage.py all_languages
```

**Remove a language**
```bash
docker-compose -f docker-compose.prod.yml exec api python manage.py remove_language en-sw-JW300
```

### **Running tests**
```bash
docker-compose -f docker-compose.prod.yml exec api python manage.py tests
```