# Back End

## Flask RESTApi

API for [Masakhane-MT](https://github.com/masakhane-io/masakhane-mt) machine translation models for African languages to translate

## Create a database

Run Python at your terminal

```sh
bash db.sh
```

Inside Python run the following command to see the content of the database (Make sure you're in the folder that contains the db).

```sh
import sqlite3,os
conn = sqlite3.connect("masakhane.sqlite")
c = conn.cursor()
for row in c.execute('SELECT * FROM masakhane'):
    print(row)
```

## Testing 

`py.test -v --ignore=lib`

## Create and Migrate database
```bash
flask db init
flask db migrate
flask db upgrade 
```