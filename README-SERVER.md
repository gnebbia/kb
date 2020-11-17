<p align="center">
    <img src="img/kbAPILogo.png?raw=true" width="200"/>
</p>

# kbAPI Server


> **This document refers to the Alpha  deployment of the kbAPI  server which  is NOT complete and should NOT be used in production environments.**

## What is the kbAPI Server ?

The kbAPI server is a component of the kb project which exposes the knowledge base as a REST API.

It does this by wrapping the core functionality of kb using the [Flask framework](https://flask.palletsprojects.com/en/1.1.x/)

## Starting the server (MacOS and Linux)

To start the kbAPI server, simply navigate to the directory containing the `server.py` module and type

`python3 server.py`

or, to run it in the background as a detached process (thus allowing you to have the server running in the background)

`python3 server.py &`

## Starting the server (Windows)

TODO

## DOCKER container

The kbAPI serer is also available as a DOCKER container. To construct the image, use:

`docker-compose -f docker-compose-server.yml build  --force-rm`

once the image is built, it can be run with:

`docker run -p 5000:5000 -ti kb_kb  sh -c "sh"`

## Security

The server is protected by a small security framework which required login details to be passed in each call (as per REST convention).
In this initial release, there is a simple user defined: `kbuser`  with a password of `kbuser`. This will be expanded in future releases.

In order to use the server, some examples would be:

```curl 
curl --location --request GET 'http://<hostname>:<port>//list' --header 'Authorization: Basic a2J1c2VyOmtidXNlcg=='
``` 

Note that the **a2J1c2VyOmtidXNlcg==** indicates the credentials for **kbuser/kbuser**

an alternative curl call would be :
```curl
curl -u kbuser:kbuser -i http://<hostname>:<port>/list
```
A Python example using  the well-known Requests library:

```python
import requests
url = "http://<hostname>:<port>//list"
payload = {}
headers = {
  'Authorization': 'Basic a2J1c2VyOmtidXNlcg=='
}
response = requests.request("GET", url, headers=headers, data = payload)
print(response.text.encode('utf8'))

```

## Production Servers

The Docker image supplied uses the default Flask WSGI server. This is not recommended for use in production environments.
Several options are out there to replace the default server, but a recommended option is 

[![alt text][1]][2]

[1]: img/gunicornlogo.png
[2]: https://gunicorn.org/

To deploy kb-API as a gunicorn-based server, simply use:

```gunicorn -w 4 server:kbapi_app --bind "localhost:5000"```

>Note that following the gunicorn documentation, you can configure the number of worker threads, bind address, memory usage etc.

## Endpoints

| Endpoint                                     | Method | Description|
|----------------------------------------------|-------|-------------|
| `http://<hostname>/add`                      | POST | Adds a new artifact to the knowledgebase |
| `http://<hostname>/delete/id/<id>`           | POST | Delete a specific Artifact by ID |
| `http://<hostname>/delete/ids/<id,id,id>`    | POST | Delete specific Artifacts by ID |
| `http://<hostname>/delete/<name>`            | POST | Delete a specific Artifact by name |
| `http://<hostname>/erase/db`                 | POST | Erase just the knowledgebase database |
| `http://<hostname>/erase/all`                | POST | Erase all of the knowledgebase as well as files |
| `http://<hostname>/export/all`               | GET  | Export ALL the data (including files) from the knowledgebase |
| `http://<hostname>/export/kb`                | GET  | Export JUST the data from the knowledgebase |
| `http://<hostname>/grep/<regex>`             | GET  | Returns ALL of the artifacts in the knowledgebase using the regex|
| `http://<hostname>/import   `                | POST | Remove the existing knowledgebase and replace with the content of the  import file |
| `http://<hostname>/list`                     | GET  | Returns ALL of the artifacts in the knowledgebase |
| `http://<hostname>/list/category/<category>` | GET  | Returns artifacts in the knowledgebase in the requested category |
| `http://<hostname>/list/tags/<tags>`         | GET  | Returns artifacts in the knowledgebase which have the requested tags |
| `http://<hostname>/stats`                    | GET  | Return a JSON string of information about the knowledgebase |
| `http://<hostname>/tags `                    | GET  | Return a JSON string of all the tags in the knowledgebase |
| `http://<hostname>/templates`                | GET  | Return a list of all the templates available |
| `http://<hostname>/template/<query>`         | GET  | Returns the list of templates that comply with the query specified as a regex |
| `http://<hostname>/template/add/<template>`  | POST | Create a new template with the content specified in the file uploaded with it |
| `http://<hostname>/template/apply/<template>`| GET  | Apply the template to a set of artifacts whose criteria meet those 
| `http://<hostname>/template/delete/<template>`| POST  | Delete the specified template |
| `http://<hostname>/template/get/<template>`  | GET  | Returns the named template specified in the body of the HTTP request |
| `http://<hostname>/template/new/<template>`  | POST | Create a new named template containing the default template  |
| `http://<hostname>/template/update/<template>`| PUT  | Update the specified template |
| `http://<hostname>/update/<id>`              | PUT  | Updates an artifact by ID |
| `http://<hostname>/view/<id>`                | GET  | View an artifact by ID  |
| `http://<hostname>/view/<title>`             | GET  | View an artifact by title  |
| `http://<hostname>/view/<category>/<name>`   | GET  | View an artifact by its name  |
| `http://<hostname>/version`                  | GET  | Returns the version of the kb software in use  |

## Endpoints which do NOT exist

The following endpoints **look like they should exist but do NOT**

| Endpoint                               | Description      |
|----------------------------------------|------------------|
| `http://<hostname>/template/edit.....` | Edit an artifact |
| `http://<hostname>/edit.....`          | Edit a template  |


All of these endpoints will return a 
```json
{
  "Method Never Allowed"
}
```

with an HTTP response code of `405`

This is due to the paradigm of the kb-API being different to the CLI-based kb i.e. there is nowhere to edit an artifact or template. The "edit" operation is effected by using a combination of `get` and `update` methods.

## API Documentation (Postman)

The complete API documentation can be found [here](https://documenter.getpostman.com/view/12840256/TVRrWQnq#intro)


## Things to be aware of

Since kb uses SQLite to store artifacts, there are small limitations which should be noted:

> 1 - SQLite can support multiple users at once. It does however lock the whole database when writing, so if there are lots of concurrent writes it is not a suitable database for the application (usually the time the database is locked is a few  milliseconds - so for most uses this does not matter). But it is very well tested and very stable (and widely used) so it can be trusted.
This means that there **may** be occasions when a write operation will fail, so this should be catered for in any application using this REST API

> 2 - If the `.../import` method is used, and the knowledgebase is being used as a multi-user scenario, then ALL the artifacts will be removed, and the knowledgebase will be reset to whatever is in the import file for **everyone** 
