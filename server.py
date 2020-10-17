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
from flask import Flask, abort, make_response, request,send_file
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


# Import the API functions

from kb.api.add import add
from kb.api.erase import erase
from kb.api.delete import delete
from kb.api.export import export
from kb.api.ingest import ingest
from kb.api.search import search
from kb.api.view import view_by_id,view_by_title,view_by_name
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
HOST = '0.0.0.0'

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
    return make_response(({'Error': 'Unauthorized access'}), 401)
"""
    Security framework 
"""

@app.route('/version', methods=['GET'])
@auth.login_required
def return_version():
    return (make_response(({'Version': str(__version__)})), 200)


@app.route('/list', methods=['GET'])
@auth.login_required
def getAll():
    results = search(parameters, config=DEFAULT_CONFIG)    
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts within the knowledgebase.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))

        

@app.route('/list/category/<category>', methods=['GET'])
@auth.login_required
def getCategory(category = ''):

    parameters["category"]=category

    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts with this category.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))

@app.route('/list/tags/<tags>', methods=['GET'])
@auth.login_required
def getTags(tags = ''):
    parameters["tags"]=tags
    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts with these tags.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))


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
        return (make_response(({'Error': 'There was an issue adding the artifact'}), 404))

    if resp  <= 0 :
        return (make_response(({'Error': 'There was an issue adding the artifact'}), 404))
    else:
        return (make_response(({'Added': resp}), 200))



@app.route('/erase/<string:component>', methods=['POST'])
@auth.login_required
def eraseDB(component = 'all'):
    if component == 'db':
        erase_what = "db"
        erase_what_text = "database"
    else:
        erase_what = "all"
        erase_what_text = "whole knowledgebase"
    # VALIDATE all/db and issue error messgage if not there
    results = erase(erase_what, config=DEFAULT_CONFIG)

    if results == -404:
        return (make_response(({'Error': 'The ' + erase_what_text + ' has not been erased.'}), 404))

    else:
        return (make_response(({'OK': 'The ' + erase_what_text + ' has been erased.'}), 200))



@app.route('/delete/id/<id>', methods=['POST'])
@auth.login_required
def deleteItemByID(id = ''):
    parameters["id"] = id 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == -404:
        return (make_response(({'Error': 'There is no artifact with that ID, please specify a correct artifact ID'}), 404))
    if results == -301:
            return (make_response(({'Error': 'There is more than one artifact with that title, please specify a category'}), 301))
    if results == -302:
            return (make_response(({'Error': 'There are no artifacts with that title, please specify a title'}), 301))
    return (make_response(({'Deleted': results}), 200))


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
        return (make_response(({'Error': 'There are no artifacts with any of those IDs'}), 404))
    if len(deleted) != len(list_of_IDs):
        return (make_response(({'Error': 'These are the only artifacts that were deleted: '+ ', '.join(deleted)}), 200))
    else:
        return (make_response(({'Deleted': 'All artifacts were deleted: '+ ', '.join(deleted)}), 200))
     
@app.route('/delete/name/<title>', methods=['POST'])
@auth.login_required
def deleteItemByName(title = ''):
    parameters["title"] = title 
    results = delete(parameters, config=DEFAULT_CONFIG)
    if results == -404:
        return (make_response(({'Error': 'There are no artifacts with that title'}), 404))
    else:
        return (make_response(({'Deleted': title}), 200))



@app.route('/grep', methods=['GET'])
@app.route('/template', methods=['GET','POST'])
@app.route('/update', methods=['GET','POST'])
@auth.login_required
def methods_not_implemented():
    response = make_response(({'Error': 'Method Not Allowed'}), 405)
    response.allow=['add','delete','erase','export','search','version','view']
    return(response)

@app.route('/edit', methods=['GET'])
@auth.login_required
def methods_never_implemented():
    response = make_response(({'Error': 'Method Never Allowed'}), 405)
    response.allow=['add','delete','erase','export','search','version','view']
    return(response)


@app.route('/view/<int:id>', methods=['GET'])
@auth.login_required
def view_artifact_by_id(id):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_id(conn,id,DEFAULT_CONFIG))


@app.route('/view/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_title(title):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_title(conn,title,DEFAULT_CONFIG))  


@app.route('/view/<string:category>/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_name(category,title):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_name(conn,title,category,DEFAULT_CONFIG))  



        
@app.route('/export/all', methods=['GET'])
@auth.login_required
def exportKnowledgebaseALL():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, "rb") as export_file:
            encoded_string = base64.b64encode(export_file.read())

        export_content = '{"Export":"' + str(encoded_string) + '"}"'
        return (make_response((export_content), 200))

@app.route('/export/data', methods=['GET'])
@auth.login_required
def exportKnowledgebaseDATA():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        parms["only_data"] = "True" 
        results = export(parms, config=DEFAULT_CONFIG)
        with open(results, "rb") as export_file:
            encoded_string = base64.b64encode(export_file.read())

        export_content = '{"Export":"' + str(encoded_string) + '"}"'
        return (make_response((export_content), 200))
        

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
            return (make_response(({'Imported': file.name}), 200))
        if results == -415:
           return (make_response(({'Error': file.name + " is not a valid kb export file."}), 415))
     
# Start the server
if __name__ == '__main__':
    app.run(debug = DEBUG, host = HOST, port = PORT)