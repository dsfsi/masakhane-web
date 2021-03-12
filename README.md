==============================

# Masakhane WEB




## How to run

## Install Docker and Docker-compose 

Run the following command to check if you have `docker` and `docker-compose` installed in your computer :
    - `docker --version`
    - `docker-compose --version`

If you get the information about the version and not an error you can skeep the details below and just to the Using Docker section. 


### Install Docker 



### Using Docker 

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

### Admin command 

- check the available models in memory `sudo docker-compose exec server python manage.py all_language`
- add a new language `sudo docker-compose exec server python manage.py add_language en-sw`
- delete a language `sudo docker-compose exec server python manage.py remove_language en-sw`


