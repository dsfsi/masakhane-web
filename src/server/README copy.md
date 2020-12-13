==============================

# RESTApi 

## Endpoints 

- Get all the available languages : `http GET http://127.0.0.1:5000/translate`
- Get a translation given a source and target language : 

    ```http POST http://127.0.0.1:5000/translate  source="en" target="ln" input="I am speaking with cate"```