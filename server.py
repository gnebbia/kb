import sys
sys.path.append('kb')

import json
from kb.main import dispatch
from bottle import get, run

from kb.commands.search import search
from kb.entities.artifact import Artifact
from kb.config import DEFAULT_CONFIG

@get('/list')
def getAll():
    # allKnowledge=[{'item':'knowledge'}]
    # query -> filter for the title field of the artifact
    # category -> filter for the category field of the artifact
    # tags -> filter for the tags field of the artifact
    # author -> filter for the author field of the artifact
    # status -> filter for the status field of the artifact
    # no_color -> determines whether  a color output is needed
    # verbose -> determines if a verbose output is needed
    # response -> determines whether any data is required to be returned
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

    k = search( parameters, config=DEFAULT_CONFIG)
    for a in k:
        response = a.toJson()
    return {'knowledge': response }


run(host='localhost', port=8080, debug=True,reloader=True)
