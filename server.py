import sys
sys.path.append('kb')

from bottle import get, run

from kb.commands.search import search
from kb.entities.artifact import Artifact
from kb.config import DEFAULT_CONFIG

parameters = dict(id="",
                    title = "",
                    category = "",
                    query = "",
                    tags = "",
                    author = "",
                    status = "",
                    no_color = False,
                    verbose = False,
                    response = True)
# query -> filter for the title field of the artifact
# category -> filter for the category field of the artifact
# tags -> filter for the tags field of the artifact
# author -> filter for the author field of the artifact
# status -> filter for the status field of the artifact
# no_color -> determines whether  a color output is needed
# verbose -> determines if a verbose output is needed
# response -> determines whether any data is required to be returned

def constructResponse(results):
    response = '['
    for result in results:
        response = response + result.toJson() + ','
    response =  response[:-1].replace("\"","\"") + ']'
    return response

@get('/list')
def getAll():
    results = search( parameters, config=DEFAULT_CONFIG)    
    return {'knowledge': constructResponse(results) }


@get('/list/category/<category>')
def getCategory(category=''):
    parameters["category"]=category
    results = search( parameters, config=DEFAULT_CONFIG)
    return {'knowledge': constructResponse(results) }

run(host='localhost', port=8080, debug=True,reloader=True)
