# Common SetUp errors and Debugging

## Table of Contents
- [Common SetUp errors and Debugging](#common-setup-errors-and-debugging)
  - [Table of Contents](#table-of-contents)
- [Errors during setup](#errors-during-setup)
  - [**Errors with Docker**](#errors-with-docker)
    - [**gcsfuse** - Noted on Mac M1 (Dec 2022)](#gcsfuse---noted-on-mac-m1-dec-2022)
    - [**failed to solve** - Noted on Mac M1 (Dec 2022)](#failed-to-solve---noted-on-mac-m1-dec-2022)
  - [**Errors with stand alone setup**](#errors-with-stand-alone-setup)
    - [**PyICU/Polyglot** - Noted on Linux/Ubuntu (Jun 2022)](#pyicupolyglot---noted-on-linuxubuntu-jun-2022)
- [Checking the client, server/api \& database](#checking-the-client-serverapi--database)
  - [**Check the client**](#check-the-client)
  - [**Check the api**](#check-the-api)
    - [**Notable API endpoints to test using GET:**](#notable-api-endpoints-to-test-using-get)
    - [**Notable API endpoints to test using POST:**](#notable-api-endpoints-to-test-using-post)
  - [**Check the database**](#check-the-database)
    - [**With Docker**](#with-docker)
    - [**With Stand alone backend**](#with-stand-alone-backend)


# Errors during setup

## **Errors with Docker**
### **gcsfuse** - Noted on Mac M1 (Dec 2022)
Seems to be a architecture issue, resolved by running the command:
```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```
[solution reference](https://github.com/GoogleCloudPlatform/gcsfuse/issues/586)

### **failed to solve** - Noted on Mac M1 (Dec 2022)
Full err message:  
```
failed to solve: rpc error: code = Unknown desc = failed to solve with frontend dockerfile.v0: failed to create LLB definition: failed to authorize: rpc error: code = Unknown desc = failed to fetch anonymous token: Get "https://auth.docker.io/token?scope=repository%3Alibrary%2Fnode%3Apull&service=registry.docker.io": dial tcp: lookup auth.docker.io on 192.168.0.1:53: no such host
```

This is a ad-hoc error, possible solutions:
- Sign in to docker hub and docker cli ```docker signin```  
- Sign in to docker hub  
- Within `Docker hub>Settings>Docker Engine`,set  `buildkit` to `false`   

[solution signin reference](https://stackoverflow.com/questions/65361083/docker-build-failed-to-fetch-oauth-token-for-openjdk) | [solution buildkit reference](https://stackoverflow.com/questions/64221861/an-error-failed-to-solve-with-frontend-dockerfile-v0)

**Note** Running these commands is not advisable: 
```bash 
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
``` 
This will invalidate the GCSFuse fix for Mac M1.

## **Errors with stand alone setup**

### **PyICU/Polyglot** - Noted on Linux/Ubuntu (Jun 2022)

Resolved by running the commands:
```bash
apt-get update
```

Then either - from apt directly : https://packages.debian.org/source/stable/pyicu:
```bash 
apt-get install python3-icu
```
OR - from source:
```bash
apt-get install pkg-config libicu-dev
pip install --no-binary=:pyicu: pyicu
```

# Checking the client, server/api & database
## **Check the client**
The client should be running on http://localhost:3000.

Check the terminal (standalone), inspect the webpage or view the docker logs for error output.
## **Check the api**
The API should be running on http://localhost:5000 and return the following output:
```json
{  
    "message": "welcome Masakhane Web"
}
```
Check the terminal (standalone) or view the docker logs for error output.

### **Notable API endpoints to test using GET:**
Make get requests by going to the web endpoint in your browser
| Endpoint |  Description | 
| -------- |  ----------- |
| http://localhost:5000/update | Updates the local database with the newly loaded models | 
| http://localhost:5000/translate | Lists the saved models |  



### **Notable API endpoints to test using POST:**
Use a developer tool such as [Postman](https://www.postman.com/) to make POST requests
| Endpoint | Description | Example Body |
| ------ | --------- | --------- |
| http://localhost:5000/translate | Returns the translated text  | <pre lang="json">{<br>  "src_lang": "english",<br>  "tgt_lang": "swahili",<br>  "input":    "Hello, how are you?"<br>}</pre>|

## **Check the database**
Docker makes use of a postgreSQL database  
The stand alone app uses sqlite, so there is an different method for access.

### **With Docker**  
The 'db-1' image in docker contains the database using PostgreSQL, you can access the DB system running on the image with the command:
```
docker-compose -f docker-compose.yml exec db psql --username=masakhane --dbname=masakhane
```

List all databases:
```
\l
```

Connect to the masakhane database: 
```
\c masakhane
```

List relations
```
\dt
```

See saved information in a relation:
```
select * from language;
```

Quit the database:
```
\q
```

### **With Stand alone backend**  

Within the `src/server/core/` directory, run this command to start the python interpreter:
```
python
``` 

Use the code below to check what is saved in the database

```python
import sqlite3, os

conn = sqlite3.connect("masakhane.db")
c = conn.cursor()

for row in c.execute('SELECT * FROM feedback'):
print(row)

for row in c.execute('SELECT * FROM language'):
print(row)
```
