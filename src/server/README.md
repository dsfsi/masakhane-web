
# The Backend 
The server contains the methods and extensions to support Masakhane Web

## Table of contents
- [API](#api)
  - [**Endpoints**](#endpoints)
    - [**GET**](#get)
    - [**POST**](#post)
- [Manage CLI](#manage-cli)
- [Tests](#tests)

# API
This is the REST API of the Masakhane Web App.

API for [Masakhane-MT](https://github.com/masakhane-io/masakhane-mt) machine translation models for African languages to translate

## **Endpoints**

The server is running on http://localhost:5000  

### **GET**

<table style='width:100%;'>
<tr>
<th> Endpoint </th><th> Description </th><th> Returns (on success) </th> 
</tr>
<td>

`/`

</td><td> The base endpoint </td>
<td> 

```json
{
    "message": "welcome Masakhane Web" 
}
```

</td> 
<tr>
<td> 

`/translate` 

</td><td> Lists the saved models </td>
<td> 

```json
[
    {
        "type": "source",
        "name": "English",
        "value": "en",
        "targets": [
            {
                "name": "Swahili",
                "value": "sw"
            }
        ]
    }
]
```

</td> 
</tr>
<tr>
<td>

`/update`

</td><td> Updates the local database with the newly loaded models </td>
<td> 

```json
{
    "message": "models updated" 
}
```

</td> 
</tr>
</table>

### **POST**

<table style='width:100%;'>
<tr>
<th> Endpoint </th><th> Description </th><th> Example Body </th><th> Returns (on success) </th> 
</tr>
<tr>
<td>

`/translate`

</td><td> Returns the translated text </td>
<td> 

```json
{
  "src_lang": "english",
  "tgt_lang": "swahili",
  "input":    "how are you?"
}
```

</td> 
<td> 

```json
{
    "src_lang": "english",
    "tgt_lang": "swahili",
    "input": "Hello, how are you?",
    "output": "kwa ukunjufu"
}
```

</td>
</tr>
<tr>
<td>

`/save`

</td><td> Saves the translation feedback </td>
<td> 

```json
{
  "srcX_lang": "english",
  "tgt_lang": "swahili",
  "input": "Hello, how are you?",
  "review": "translation correction",
  "stars": "translation confidence",
  "token": "user auth (bool)"
}
```

</td> 
<td> 

```json
{
    "message": "Review saved",
}
```

</td>
</tr>
<tr></tr>
</table>

# Manage CLI
There is a cli program for managing the server - it is in [src/server/manage.py]()

The command format is: 
```bash 
python manage.py command optional_parameter
```

| Command | Parameter | Description |
| ------- | --------- | ----------- |
| `create_db` | none | Creates database tables for the db models Language & Feedback
| `all_languages` | none | Lists the model info stored in the Language table
| `add_language` | `name_tag` | Adds a language with a given name_tag, ie - `en-sw-JW300 OR en-tiv-`|
| `remove_language` | `name_tag`| Removes a language with a given name_tag |
| `clean` | none | Deletes and recreates an empty database |
| `tests` | none | Runs the backend tests |

# Tests

**TODO**