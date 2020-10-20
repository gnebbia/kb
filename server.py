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

# Import system libraries
import sys
import os
import io
import tempfile
import base64
import urllib.request
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter


# Use the flask framework, as well as the authentication framework
from flask import Flask, abort, make_response, request, send_file
from flask_httpauth import HTTPBasicAuth

# Import the API functions

from kb.api.add import add
from kb.api.erase import erase
from kb.api.delete import delete
from kb.api.export import export
from kb.api.grep import grep
from kb.api.ingest import ingest
from kb.api.search import search
from kb.api.update import update
from kb.api.view import view_by_id, view_by_title, view_by_name
from kb import db
from kb import __version__

# Get the configuration for the knowledgebase
from kb.config import DEFAULT_CONFIG


class ListConverter(BaseConverter):
    """
    Custom class to convert a list from a RESTful URL into a Python list
    """
    def to_python(self, value):
        print(value)
        return value.split(',')


# Initialisation

# Initiate the Flask app
kbapi_app = Flask(__name__)
kbapi_app.url_map.converters['list'] = ListConverter  # Add custom converter for lists

# Initiate the authentication framework
auth = HTTPBasicAuth()

# Set Flask application parameters
DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

# Methods allowed:
ALLOWED_METHODS = ['add', 'delete', 'erase', 'export', 'search', 'update', 'version', 'view']

parameters = dict(id="", title="", category="", query="", tags="", author="", status="", no_color=False, verbose=False)
# query -> filter for the title field of the artifact
# category -> filter for the category field of the artifact
# tags -> filter for the tags field of the artifact
# author -> filter for the author field of the artifact
# status -> filter for the status field of the artifact
# no_color -> determines whether  a color output is needed
# verbose -> determines if a verbose output is needed


def toJson(self):
    """
    This function converts an Artifact object to a Json document

    Arguments:
    self   - Artifact object

    Returns:
    A Json document
    """
    record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s""status":"%s""author":"%s","template":"%s"}' % \
        (self.id, self.title, self.category, self.path, self.tags, self.status, self.author, self.template)
    return record


def constructResponse(results):
    """
        This function constructs a response from thee results obtained by a core function
        Arguments:
        result   - Set of results

        Returns:
        Fully fledged Json response

    """
    response = '['
    for result in results:
        response = response + toJson(result) + ','
    response = response[:-1] + ']'
    return response


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


@kbapi_app.route('/template', methods=['GET', 'POST'])
@auth.login_required
def methods_not_implemented_yet():
    response = make_response(({'Error': 'Method Not Allowed Yet'}), 405)
    response.allow = ALLOWED_METHODS
    return(response)


@kbapi_app.route('/add', methods=['POST'])
@auth.login_required
def add_item():
    parameters["title"] = request.form.get("title", "")
    parameters["category"] = request.form.get("category", "")
    parameters["author"] = request.form.get("author", "")
    parameters["status"] = request.form.get("status", "")
    parameters["tags"] = request.form.get("tags", "")
    parameters["file"] = ""

    attachment = request.files['file']
    resp = add(args=parameters, config=DEFAULT_CONFIG, file=attachment)
    if resp is None:
        return (make_response(({'Error': 'There was an issue adding the artifact'}), 404))
    if resp <= 0:
        return (make_response(({'Error': 'There was an issue adding the artifact'}), 404))
    else:
        return (make_response(({'Added': resp}), 200))


@kbapi_app.route('/delete/<int:id>', methods=['POST'])
@auth.login_required
def delete_item_by_ID(id=''):
    parameters["id"] = id
    results = delete(parameters, config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/delete/<list:ids>', methods=['POST'])
@auth.login_required
def delete_items_by_ID(ids=''):
    deleted = []
    for item in ids:
        parameters["id"] = item
        results = delete(parameters, config=DEFAULT_CONFIG)
        if results == item:
            deleted.append(item)
    if len(deleted) == 0:
        return (make_response(({'Error': 'There are no artifacts with any of those IDs'}), 404))
    if len(deleted) != len(ids):
        return (make_response(({'Error': 'These are the only artifacts that were deleted: ' + ', '.join(deleted)}), 200))
    else:
        return (make_response(({'Deleted': 'All artifacts were deleted: ' + ', '.join(deleted)}), 200))


@kbapi_app.route('/delete/name/<string:title>', methods=['POST'])
@auth.login_required
def delete_item_by_name(title=''):
    parameters["title"] = title
    results = delete(parameters, config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/edit', methods=['GET'])
@auth.login_required
def methods_never_implemented():
    response = make_response(({'Error': 'Method Never Allowed'}), 405)
    response.allow = ALLOWED_METHODS
    return(response)


@kbapi_app.route('/erase/<string:component>', methods=['POST'])
@auth.login_required
def erase_db(component='all'):
    results = erase(component, config=DEFAULT_CONFIG)
    return(results)


@kbapi_app.route('/export/all', methods=['GET'])
@auth.login_required
def export_kb_all():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        results = export(parms, config=DEFAULT_CONFIG)
        return(results)


@kbapi_app.route('/export/data', methods=['GET'])
@auth.login_required
def export_kb_data():
    with tempfile.NamedTemporaryFile(delete=True) as f:
        parms = dict()
        parms["file"] = f.name
        parms["only_data"] = "True"
        results = export(parms, config=DEFAULT_CONFIG)
        return(results)


@kbapi_app.route('/grep/<string:regex>', methods=['GET'])
@auth.login_required
def grep_artifacts(regex):
    parms = dict()
    parms["regex"] = regex
    parms["case_insensitive"] = False
    parms["no_color"] = False
    parms["verbose"] = True
    
    results = grep(parms, config=DEFAULT_CONFIG)
    return(make_response(constructResponse(results)), 200)


@kbapi_app.route('/list', methods=['GET'])
@auth.login_required
def get_all():
    results = search(parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts within the knowledgebase.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))


@kbapi_app.route('/list/<queries>', methods=['GET'])
@auth.login_required
def get_query(queries=''):
    print(queries)
    parameters["query"] = queries
    results = search(parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no matching artifacts.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))


@kbapi_app.route('/list/category/<category>', methods=['GET'])
@auth.login_required
def get_category(category=''):
    parameters["category"] = category
    results = search(parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts with this category.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))


@kbapi_app.route('/list/tags/<tags>', methods=['GET'])
@auth.login_required
def get_tags(tags=''):
    parameters["tags"] = tags
    results = search(parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        return (make_response(({'Error': 'There are no artifacts with these tags.'}), 404))
    else:
        return (make_response(({'Knowledge': constructResponse(results)}), 200))


@kbapi_app.route('/update/<int:id>', methods=['PUT'])
@auth.login_required
def update_artifact(id):
    parameters["title"] = request.form.get("title", "")
    parameters["category"] = request.form.get("category", "")
    parameters["author"] = request.form.get("author", "")
    parameters["status"] = request.form.get("status", "")
    parameters["tags"] = request.form.get("tags", "")
    parameters["file"] = ""
    parameters["id"] = id
    attachment = request.files['file']
    resp = update(args=parameters, config=DEFAULT_CONFIG, attachment=attachment)
    return(resp)


@kbapi_app.route('/version', methods=['GET'])
@auth.login_required
def return_version():
    return (make_response(({'Version': str(__version__)})), 200)


@kbapi_app.route('/view/<int:id>', methods=['GET'])
@auth.login_required
def view_artifact_by_id(id):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_id(conn, id, DEFAULT_CONFIG))


@kbapi_app.route('/view/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_title(title):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_title(conn, title, DEFAULT_CONFIG))


@kbapi_app.route('/view/<string:category>/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_name(category, title):
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_name(conn, title, category, DEFAULT_CONFIG))


@kbapi_app.route('/import', methods=['POST'])
@auth.login_required
def ingest_kb():
    parms = dict()
    print("here")
    print(request.files)
    file = request.files['f']
    parms["file"] = file.filename
    print(parms["file"])
    results = ingest(file, parms, config=DEFAULT_CONFIG)
    if results == -200:
        return (make_response(({'Imported': file.name}), 200))
    if results == -415:
        return (make_response(({'Error': file.name + " is not a valid kb export file."}), 415))


# Start the server
if __name__ == '__main__':
    kbapi_app.run(debug=DEBUG, host=HOST, port=PORT)
