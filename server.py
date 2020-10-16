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

# Use the flask framework, as well as the authentication framework
from flask import Flask, jsonify, abort, make_response, request,send_file
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


# Import the API functions
from kb.api.search import search
from kb.api.add import add
from kb.api.erase import erase
from kb.api.delete import delete
from kb.api.export import export
from kb.api.ingest import ingest
from kb import __version__

from kb import db

# Get the configuration for the knowledgebase
from kb.config import DEFAULT_CONFIG 


import os
from werkzeug.utils import secure_filename
import urllib.request
import tempfile
import io
import base64


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
    
    return str(record.replace('\\',''))


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

"""
    Security framework 
"""
@auth.get_password
def get_password(username):
    if username == 'kbuser':
        return 'kbuser'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized access'}), 401)
"""
    Security framework 
"""

@app.route('/version', methods=['GET'])
@auth.login_required
def return_version():
    return (make_response(jsonify({'Version': str(__version__)})), 200)


@app.route('/list', methods=['GET'])
@auth.login_required
def getAll():
    results = search(parameters, config=DEFAULT_CONFIG)    
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts within the knowledgebase.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))

        

@app.route('/list/category/<category>', methods=['GET'])
@auth.login_required
def getCategory(category = ''):

    parameters["category"]=category

    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with this category.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))

@app.route('/list/tags/<tags>', methods=['GET'])
@auth.login_required
def getTags(tags = ''):
    parameters["tags"]=tags
    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with these tags.'}), 404))
    else:
        return (make_response(jsonify({'Knowledge': constructResponse(results)}), 200))


@app.route('/add', methods=['POST'])
@auth.login_required
def addItem():
    parameters["title"] = request.form.get("title","")
    parameters["category"] = request.form.get("category","")
    parameters["author"]= request.form.get("author","")
    parameters["status"] = request.form.get("status","")
    parameters["tags"] = request.form.get("tags","")
    parameters["file"] = ""

    attachment = request.files['file']
    resp = add(args=parameters,config=DEFAULT_CONFIG,file=attachment)
    if resp is None:
        return (make_response(jsonify({'Error': 'There was an issue adding the artifact'}), 404))

    if resp  <= 0 :
        return (make_response(jsonify({'Error': 'There was an issue adding the artifact'}), 404))
    else:
        return (make_response(jsonify({'Added': resp}), 200))



@app.route('/erase/<component>', methods=['POST'])
@auth.login_required
def eraseDB(component = 'all'):
    if component == 'db':
        erase_what = "db"
        erase_what_text = "database"
    else:
        erase_what = "all"
        erase_what_text = "whole knowledgebase"

    results = erase(erase_what, config=DEFAULT_CONFIG)

    if results == -404:
        return (make_response(jsonify({'Error': 'The ' + erase_what_text + ' has not been erased.'}), 404))

    else:
        return (make_response(jsonify({'OK': 'The ' + erase_what_text + ' has been erased.'}), 200))



@app.route('/delete/id/<id>', methods=['POST'])
@auth.login_required
def deleteItemByID(id = ''):
    parameters["id"] = id 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == -404:
        return (make_response(jsonify({'Error': 'There is no artifact with that ID, please specify a correct artifact ID'}), 404))
    if results == -301:
            return (make_response(jsonify({'Error': 'There is more than one artifact with that title, please specify a category'}), 301))
    if results == -302:
            return (make_response(jsonify({'Error': 'There are no artifacts with that title, please specify a title'}), 301))
    return (make_response(jsonify({'Deleted': results}), 200))


@app.route('/delete/ids/<ids>', methods=['POST'])
@auth.login_required
def deleteItemsByID(ids = ''):
    deleted = []      
    list_of_IDs = ids.split(",")
    for item in list_of_IDs:
        parameters["id"] = item
        results = delete(parameters, config=DEFAULT_CONFIG)
        if results == item:
            deleted.append(item)

    if len(deleted) == 0:
        return (make_response(jsonify({'Error': 'There are no artifacts with any of those IDs'}), 404))
    if len(deleted) != len(list_of_IDs):
        return (make_response(jsonify({'Error': 'These are the only artifacts that were deleted: '+ ', '.join(deleted)}), 200))
    else:
        return (make_response(jsonify({'Deleted': 'All artifacts were deleted: '+ ', '.join(deleted)}), 200))
     
@app.route('/delete/name/<title>', methods=['POST'])
@auth.login_required
def deleteItemByName(title = ''):
    parameters["title"] = title 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == -404:
        return (make_response(jsonify({'Error': 'There are no artifacts with that title'}), 404))
    else:
        return (make_response(jsonify({'Deleted': title}), 200))


@app.route('/edit', methods=['GET','POST'])
@app.route('/grep', methods=['GET'])
@app.route('/template', methods=['GET','POST'])
@app.route('/update', methods=['GET','POST'])
@auth.login_required
def methods_not_implemented():
    response = make_response(jsonify({'Error': 'Method Not Allowed'}), 405)
    response.allow=['add','delete','erase','export','search','version']
    return(response)



@app.route('/view/<id>', methods=['GET'])
@auth.login_required
def artifact(id):
    parameters["id"] = id 
    #results = delete(parameters, config=DEFAULT_CONFIG)
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    artifact = db.get_artifact_by_id(conn, id)
    # with tempfile.NamedTemporaryFile(delete=True) as f:
    #    parms = dict()
    #    parms["file"] = f.name
    #    parms["only_data"] = "True" 
    #    results = export(parms, config=DEFAULT_CONFIG)
    #    with open(results, 'rb') as bites:
    #        return send_file(
    #                io.BytesIO(bites.read()),
    #                as_attachment=True,
    #                attachment_filename=results,
    #                mimetype='application/gzip'
    #        )
    category_path = Path(str(DEFAULT_CONFIG["PATH_KB_DATA"]), str(artifact.category))
    artifact_file = Path(str(category_path), str(artifact.title))

    with open(artifact_file, "rb") as artifact_file:
        encoded_string = base64.b64encode(artifact_file.read())

  
   
    record = "{" + toJson(artifact)  + "{" + "content:" + str(encoded_string) + "}"
    return (make_response(jsonify(record), 200))



@app.route('/export/data', methods=['GET'])
@auth.login_required
def exportKnowledgebaseDATA():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        parms["only_data"] = "True" 
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, 'rb') as bites:
            return send_file(
                    io.BytesIO(bites.read()),
                    as_attachment=True,
                    attachment_filename=results,
                    mimetype='application/gzip'
            )
        
@app.route('/export/all', methods=['GET'])
@auth.login_required
def exportKnowledgebaseALL():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, 'rb') as bites:
            return send_file(
                    io.BytesIO(bites.read()),
                    as_attachment=True,
                    attachment_filename=results,
                    mimetype='application/gzip'
            )

@app.route('/import', methods=['POST'])
@auth.login_required
def ingestKnowledgebase():
        parms = dict()
        print("here")
        print (request.files)
        file = request.files['f']

        parms["file"] =  file.filename
        print (parms["file"])
        results = ingest(file,parms, config=DEFAULT_CONFIG)
        if results == -200:
            return (make_response(jsonify({'Imported': file.name}), 200))
        if results == -415:
           return (make_response(jsonify({'Error': file.name + " is not a valid kb export file."}), 415))
     
# Start the server
if __name__ == '__main__':
    app.run(debug = DEBUG, host = '0.0.0.0', port = PORT)