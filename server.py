# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kbAPI server module

:Copyright: © 2020, alshaptons.
:License: GPLv3 (see /LICENSE).
"""

import sys
sys.path.append('kb')

import io

# Use the flask framework
from flask import Flask, jsonify, abort, make_response, request,send_file

# Import the API functions
from kb.api.search import search
from kb.api.add import addArtifact
from kb.api.erase import eraseAction
from kb.api.delete import delete
from kb.api.export import export

# Get the configuration for the knowledgebase
from kb.config import DEFAULT_CONFIG 


import os
from werkzeug.utils import secure_filename
import urllib.request
import tempfile
import io

from pathlib import Path

app = Flask(__name__)

# Set Flask parameters
DEBUG = True
PORT = 5000

parameters = dict(id="",
                    title = "",
                    category = "",
                    query = "",
                    tags = "",
                    author = "",
                    status = "",
                    no_color = False,
                    verbose = False)
# query -> filter for the title field of the artifact
# category -> filter for the category field of the artifact
# tags -> filter for the tags field of the artifact
# author -> filter for the author field of the artifact
# status -> filter for the status field of the artifact
# no_color -> determines whether  a color output is needed
# verbose -> determines if a verbose output is needed

"""

    This function converts an Artifact object to a Json document

    Arguments:
    self   - Artifact object

    Returns:
    A Json document
"""

def toJson(self):
    record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s""status":"%s""author":"%s","template":"%s"}' % (self.id,self.title,self.category,self.path,self.tags,self.status, self.author,self.template)
    return record


"""
    This function constructs a response from thee results obtained by a core function
    
    Arguments:
    result   - Set of results

    Returns:
    Fully fledged Json response

"""

def constructResponse(results):
    response = '['
    for result in results:
        response = response + toJson(result) + ','
    response =  response[:-1] + ']'
    return response

# -----------------------------------------------
"""
    Application router for server functions 
    Arguments:
        Variable

    Returns:
        JSON document or informationl message in HTTP responses

"""

@app.route('/list', methods=['GET'])
def getAll():
    results = search(parameters, config=DEFAULT_CONFIG)    
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts within the knowledgebase.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))

        

@app.route('/list/category/<category>', methods=['GET'])
def getCategory(category = ''):

    parameters["category"]=category

    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with this category.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))

@app.route('/list/tags/<tags>', methods=['GET'])
def getTags(tags = ''):
    parameters["tags"]=tags
    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with these tags.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))

@app.route('/add', methods=['POST'])
def addItem():
    parameters["title"] = request.form.get("title","")
    parameters["category"] = request.form.get("category","")
    parameters["author"]= request.form.get("author","")
    parameters["status"] = request.form.get("status","")
    parameters["tags"] = request.form.get("tags","")
    parameters["file"] = ""

    attachment= request.files['file']
    resp = addArtifact(args=parameters,config=DEFAULT_CONFIG,file=attachment)
    if resp is None:
        return (make_response(jsonify({'Error': 'There was an issue adding the artifact'}), 404))
    else:
        return (make_response(jsonify({'Added': resp}), 200))



@app.route('/erase/<component>', methods=['POST'])
def eraseDB(component = 'all'):
    if component == 'db':
        eraseWhat="db"
        eraseWhatText="database"
    else:
        eraseWhat="all"
        eraseWhatText="whole knowledgebase"

    results = eraseAction(eraseWhat, config=DEFAULT_CONFIG)

    if results == "404":
        return (make_response(jsonify({'Error': 'The ' + eraseWhatText + ' has not been erased.'}), 404))

    else:
        return (make_response(jsonify({'OK': 'The ' + eraseWhatText + ' has been erased.'}), 200))



@app.route('/delete/id/<id>', methods=['POST'])
def deleteItemByID(id = ''):
    parameters["id"]=id 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == "404":
        return (make_response(jsonify({'Error': 'There is no artifact with that ID, please specify a correct artifact ID'}), 404))
    if results == "301Multi":
            return (make_response(jsonify({'Error': 'There is more than one artifact with that title, please specify a category'}), 301))
    if results == "301None":
            return (make_response(jsonify({'Error': 'There are no artifacts with that title, please specify a title'}), 301))
    return (make_response(jsonify({'Deleted': results}), 200))


@app.route('/delete/ids/<ids>', methods=['POST'])
def deleteItemsByID(ids = ''):
    deleted=[]      
    listofIDs = ids.split(",")
    for item in listofIDs:
        parameters["id"]=item
        results = delete(parameters, config=DEFAULT_CONFIG)
        if results == item:
            deleted.append(item)

    if len(deleted) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with any of those IDs'}), 404))
    if len(deleted) != len(listofIDs):
        return (make_response(jsonify({'Error': 'These are the only artifacts that were deleted: '+ ', '.join(deleted)}), 200))
    else:
        return (make_response(jsonify({'Deleted': 'All artifacts were deleted: '+ ', '.join(deleted)}), 200))
     
@app.route('/delete/name/<title>', methods=['POST'])
def deleteItemByName(title = ''):
    parameters["title"]=title 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == "404":
        return (make_response(jsonify({'Error': 'There are no artifacts with that title'}), 404))
    else:
        return (make_response(jsonify({'Deleted': title}), 200))


@app.route('/export/data', methods=['GET'])
def exportKnowledgebaseDATA():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms=dict()
        parms["file"]=f.name
        parms["only_data"]="True" 
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, 'rb') as bites:
            return send_file(
                    io.BytesIO(bites.read()),
                    as_attachment=True,
                    attachment_filename=results,
                    mimetype='application/gzip'
            )
        
@app.route('/export/all', methods=['GET'])
def exportKnowledgebaseALL():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms=dict()
        parms["file"]=f.name
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, 'rb') as bites:
            return send_file(
                    io.BytesIO(bites.read()),
                    as_attachment=True,
                    attachment_filename=results,
                    mimetype='application/gzip'
            )

# Start the server
if __name__ == '__main__':
    app.run(debug = DEBUG, host = '0.0.0.0', port = PORT)