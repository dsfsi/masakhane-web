# **Running the App Locally**

The app can be run as a standalone or using Docker, unless you are working on an machine running linux/ubuntu, it is adviseable to use Docker.

To run the app in production, see [here](start_app_prod_doc.md).

For any errors during setup, please see the [debugging doc](debugging_setup.md).

Review the [project details doc](project_details.md) for more information on the technology stack.  
Take note of the [Client](../../src/client/README.md) and [Server](../../src/server/README.md) README's.

## **Table of Contents**
- [**Using Docker ( Preferred )**](#using-docker--preferred-)
  - [**Docker Setup**](#docker-setup)
  - [**Running the app**](#running-the-app)
    - [**Building the App**](#building-the-app)
    - [**Shut down the app**](#shut-down-the-app)
    - [**Add, Update, \& Delete Languages**](#add-update--delete-languages)
    - [**Running tests**](#running-tests)
    - [**The Database**](#the-database)
- [**As a stand-alone app**](#as-a-stand-alone-app)
  - [**Backend Setup**](#backend-setup)
  - [**Run the server:**](#run-the-server)
    - [**The Database**](#the-database-1)
    - [**Add, Update, \& Delete Languages**](#add-update--delete-languages-1)
    - [**Running tests**](#running-tests-1)
  - [**Frontend Setup**](#frontend-setup)
  - [**Run the client:**](#run-the-client)
- [**Errors during setup**](#errors-during-setup)


# **Using Docker ( Preferred )**

The better/easier way to run the app is to use Docker, which will build both the frontend and the backend with the correct enviroment setup.

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
docker-compose -f docker-compose.yml up -d --build
```

Docker should create a container named 'masakhane-web' with the images 'db-1', 'server-1', and 'client-1'.  
The server should be active on http://localhost:5000 and the client on http://localhost:3000  
Look [here](debugging_setup.md#checking-the-client-serverapi--database) for checking these services manually.

### **Shut down the app**
To shut down the app, run the following command to remove the docker container:
```bash
docker-compose -f docker-compose.yml down
```

### **Add, Update, & Delete Languages**
**Add a Language**
```bash
docker-compose -f docker-compose.yml exec server python manage.py add_language en-sw-JW300
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
docker-compose -f docker-compose.yml exec server python manage.py all_languages
```

**Remove a language**
```bash
docker-compose -f docker-compose.yml exec server python manage.py remove_language en-sw-JW300
```

### **Running tests**
```bash
docker-compose -f docker-compose.yml exec server python manage.py tests
```

### **The Database**
Look [here](debugging_setup.md#with-docker) for more information about accessing the database

# **As a stand-alone app**
In order to run the app, we need to set up the backend and frontend seperately.  
**Note** It is advisable to be working on an linux/ubuntu machine.

## **Backend Setup**

First, ensure you are running [Python 3.6.9](https://www.python.org/downloads/release/python-369/)

Within the `src/server` directory of the project

**Install required packages:**
```bash
pip install -r requirements.txt
```

**Run the following commands:**
```bash
export FLASK_APP=core/__init__.py
export FLASK_ENV=development
```

## **Run the server:**
To start the API and database services, run the command:
```bash
python manage.py run
```

### **The Database**
Look [here](debugging_setup.md#with-stand-alone-backend) for more information about accessing the database

### **Add, Update, & Delete Languages**
**Add a Language**
```bash
python manage.py add_language en-sw-JW300
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
python manage.py all_languages
```

**Remove a language**
```bash
python manage.py remove_language en-sw-JW300
```

### **Running tests**
```bash
python manage.py tests
```

The API is available at `http://localhost:5000`, see notable API endpoints [here](debugging_setup.md#check-the-api)

## **Frontend Setup**

Ensure you have [node.js](https://nodejs.org/en/) and [yarn](https://classic.yarnpkg.com/en/docs/install) installed

Within the `src/client/` directory of the project:
**Install required packages:**
```bash
npm install --legacy-peer-deps
```

**Run the following commands:**
```bash
npm i webpack webpack-cli --legacy-peer-deps
npm i @babel/core @babel/preset-env @babel/preset-react babel-loader --legacy-peer-deps
```

## **Run the client:**
To start the client , run the command:
```bash
npm run develop
```

The client is available at `http://localhost:3000`

# **Errors during setup**
If there was a problem during setup, review [this doc](debugging_setup.md) for possible errors and solutions.

