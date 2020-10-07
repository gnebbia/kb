# kbAPI Server


> **This   document refers to the Alpha  deployment
of the kbAPI  server which  is NOT complete and
should  NOT be used in production environments.**

## What is the kbAPI Server ?

The kbAPI server is a component of the kb project which exposes the knowledge base as a REST API.

It does this by wrapping the core functionality of kb using the [Bottle framework](http://bottlepy.org)

## Starting the server (MacOS and Linux)

To start the kbAPI server, simply navigate to the  directory containing the server.py module and type

`python3 server.py`

or, to run it in the background  as a detached process (thus allowing you to log out and have the server running in the background)

`nohup python3 server.py &`

## Starting the server (Windows)

TODO

## DOCKER container

The kbAPI serer is also available as a DOCKER container. To construct the image, use:

`docker-compose -f docker-compose-server.yml build  --force-rm`

once the image is built, it can be run with:

`docker run -p 5000:5000 -ti kb_kb  sh -c "sh"`



## Endpoints

| Endpoint | Description|
|----------|------------|
| `http://hostname/list` | Returns ALL of the artifacts in the knowledgebase as a JSON document|
|`http://hostname/list/category/<category>`|Returns artifacts in the knowledgebase as a JSON document which are of the requested category|
|`http://hostname/add`|Adds a new artifact to the knowledgebase|
|`http://hostname/erase/db`|Erase just the knowledgebase database|
|`http://hostname/erase/all`|Erase all of the knowledgebase as well as files|
|`http://hostname/delete/id/<id>`|Delete a specific Artifact by ID|

## Things to be aware of

Since kb uses SQLite to store artifacts, there is a small limitation which should
be noted:

> SQLite can support multiple users at once. It does however lock the whole database
when writing, so if there are lots of concurrent writes it is not a suitable
database for the application (usually the time the database is locked is a few
milliseconds - so for most uses this does not matter). But it is very well tested
and very stable (and widely used) so it can be trusted.

This means that there **may** be occasions when a write operation will fail,
so this should be catered for in any application using this REST API
