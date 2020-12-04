# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kbAPI server module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

# Import system libraries
import os
import tempfile
from pathlib import Path

# Use the flask framework, as well as the authentication framework
from flask import Flask, make_response, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.routing import BaseConverter

# Import the API functions
from kb.api.add import add
from kb.api.base import base as base_list
from kb.api.base import get_current,switch
from kb.api.list import list_cats, list_all_tags
from kb.api.erase import erase
from kb.api.delete import delete, delete_list_of_items_by_ID
from kb.api.export import export
from kb.api.grep import grep
from kb.api.ingest import ingest
from kb.api.search import search
from kb.api.stats import stats
from kb.api.template import search as search_templates
from kb.api.template import add as add_template
from kb.api.template import new as new_template
from kb.api.template import delete as delete_template
from kb.api.template import apply_on_set as apply_template
from kb.api.template import get_template, update_template
from kb.api.update import update
from kb.api.view import view_by_id, view_by_title, view_by_name

# Import supporting functions
from kb.api.constants import MIME_TYPE
from kb import db
from kb import __version__

# Get the configuration for the knowledgebase
#from kb.config import DEFAULT_CONFIG, get_current_base, KB_BASE, BASE
from kb.config import get_current_base, KB_BASE, BASE


class ListConverter(BaseConverter):
    """
    Custom class to convert a list from a RESTful URL into a Python list
    """
    def to_python(self, value):
        """
        Split on commas
        """
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
ALLOWED_METHODS = ['add', 'base', 'delete', 'erase', 'export', 'get', 'grep', 'ingest' 'search', 'stats', 'template', 'update', 'version', 'view']


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
    Convert an artifct object to a JSON string
    """
    record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s","status":"%s","author":"%s","template":"%s"}' % \
        (self.id, self.title, self.category, self.path, self.tags, self.status, self.author, self.template)

    return record


def constructResponse(results):
    """
    Constructs a response from the results obtained by a core function
    """
    response = '['
    for result in results:
        response = response + toJson(result) + ','
    response = response[:-1] + ']'
    response = response.replace('"', "'")
    return response


def construct_search_response(results, error_text):
    """
    Constructs a good/badresponse from the results obtained by a search function
    """
    if len(results) == 0:
        response = make_response(({'Error': error_text}), 404)
    else:
        response = make_response(({'Knowledge': constructResponse(results)}), 200)
    response.mimetype = MIME_TYPE['json']
    return(response)


"""
Security framework
"""


@auth.get_password
def get_password(username):
    """
    Return password for username (default).
    """
    if username == 'kbuser':
        return 'kbuser'
    return None


@auth.error_handler
def unauthorized():
    """
    Unauthorised access to the API.
    """
    resp = make_response(({'Error': 'Unauthorized access'}), 401)
    resp.mimetype = MIME_TYPE['json']
    return (resp)


"""
Error Handling
"""


@kbapi_app.errorhandler(404)
@kbapi_app.errorhandler(500)
def not_found(error):
    """
    Generic Error Handlers
    """
    error_texts = {
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    error_text = error_texts.get(error.code, 'Unknown Error')
    resp = make_response(({'Error': error_text}), error.code)
    resp.mimetype = MIME_TYPE['json']
    return (resp)


"""
Pre-request tooling
"""

@kbapi_app.before_request
def for_each_request():
    """
    Ensure the current knowledgebase is referred to
    """
    global DEFAULT_CONFIG

    # Home base for the user
    BASE = Path.home()

    # Get the current kb or 'default'

    KB_BASE = Path(BASE,".kb",get_current_base(BASE))

    DEFAULT_CONFIG = {
        "PATH_BASE": str(Path(BASE, ".kb")),
        "PATH_KB": str(Path(KB_BASE)),
        "PATH_KB_DB": str(Path(KB_BASE, "kb.db")),
        "PATH_KB_HIST": str(Path(KB_BASE, "recent.hist")),
        "PATH_KB_DATA": str(Path(KB_BASE, "data")),
        "PATH_KB_CONFIG": str(Path(KB_BASE,  "kb.conf.py")),  # for future use
        "PATH_KB_TEMPLATES": str(Path(KB_BASE,  "templates")),
        "PATH_KB_DEFAULT_TEMPLATE": str(Path(KB_BASE, "templates", "default")),
        "PATH_KB_INITIAL_BASES": str(Path(BASE,".kb", "bases.toml")),
        "DB_SCHEMA_VERSION": 1,
        "EDITOR": os.environ.get("EDITOR", "vim"),
        "INITIAL_CATEGORIES": ["default", ]
    }


"""
Routing for URLs
"""


@kbapi_app.route('/edit', methods=['GET', 'PUT', 'POST'])
@kbapi_app.route('/template/edit', methods=['GET', 'PUT', 'POST'])
@auth.login_required
def method_never_implemented():
    """
    Methods from the command line NEVER to be implemented as the do not fit the paradigm of an API
    """
    response = make_response(({'Error': 'Method Never Allowed'}), 405)
    response.allow = ALLOWED_METHODS
    response.mimetype = MIME_TYPE['json']
    return(response)


@kbapi_app.route('/add', methods=['POST'])
@auth.login_required
def add_item():
    """
    Add a new artifact to the knowledge base.
    """
    parameters["title"] = request.form.get("title", "")
    parameters["category"] = request.form.get("category", "")
    parameters["author"] = request.form.get("author", "")
    parameters["status"] = request.form.get("status", "")
    parameters["tags"] = request.form.get("tags", "")
    parameters["file"] = ""
    attachment = request.files['file']
    resp = add(args=parameters, config=DEFAULT_CONFIG, file=attachment)
    return(resp)


@kbapi_app.route('/base/current', methods=['GET'])
@auth.login_required
def list_current_base():
    """
    Return the current knowledgebase
    """
    results = get_current(config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/base/list', methods=['GET'])
@auth.login_required
def list_all_bases():
    """
    List all  the knowledgebases
    """
    results = base_list(config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/base/switch/<string:target>', methods=['PUT'])
@auth.login_required
def switch_base(target='default'):
    """
    Switch to a knowledge base
    """
    results = switch(target,config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/categories', methods=['GET'])
@auth.login_required
def list_categories():
    """
    List all  the categories
    """
    results = list_cats(config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/delete/<int:id>', methods=['POST'])
@auth.login_required
def delete_item_by_ID(id=''):
    """
    Delete a single artifact from the kb knowledge base.
    """
    parameters["id"] = id
    results = delete(parameters, config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/delete/<list:ids>', methods=['POST'])
@auth.login_required
def delete_items_by_ID(ids=''):
    """
    Delete a list of artifacts from the kb knowledge base.
    """
    return(delete_list_of_items_by_ID(ids, config=DEFAULT_CONFIG))


@kbapi_app.route('/delete/name/<string:title>', methods=['POST'])
@auth.login_required
def delete_item_by_name(title=''):
    """
    Delete an artifact from the knowledgebase by name.
    """
    parameters["title"] = title
    results = delete(parameters, config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/erase/<string:component>', methods=['POST'])
@auth.login_required
def erase_db(component='all'):
    """
    Erase the whole knowledgebase
    """
    results = erase(component, config=DEFAULT_CONFIG)
    return(results)


@kbapi_app.route('/export/all', methods=['GET'])
@auth.login_required
def export_kb_all():
    """
    Export the whole knowledgebase to a file
    """
    with tempfile.NamedTemporaryFile(delete=True) as f:
        params = dict()
        params["file"] = f.name
        results = export(params, config=DEFAULT_CONFIG)
        return(results)


@kbapi_app.route('/export/data', methods=['GET'])
@auth.login_required
def export_kb_data():
    """
    Export just the data to a file
    """
    with tempfile.NamedTemporaryFile(delete=True) as f:
        params = dict()
        params["file"] = f.name
        params["only_data"] = "True"
        results = export(params, config=DEFAULT_CONFIG)
        return(results)


@kbapi_app.route('/grep/<string:regex>', methods=['GET'])
@auth.login_required
def grep_artifacts(regex):
    """
    Grep the whole knowledgebase
    """
    params = dict()
    params["regex"] = regex
    params["case_insensitive"] = False
    params["no_color"] = False
    params["verbose"] = True
    results = grep(params, config=DEFAULT_CONFIG)
    response = make_response(constructResponse(results), 200)
    response.mimetype = MIME_TYPE['json']
    return(response)


@kbapi_app.route('/import', methods=['POST'])
@auth.login_required
def ingest_kb():
    """
    Import a kb export file
    """
    params = dict()
    f = request.files['file']
    return (ingest(f, params, config=DEFAULT_CONFIG))


@kbapi_app.route('/list', methods=['GET'])
@auth.login_required
def get_all():
    """
    List all  the artifacts in the knowledgebase
    """
    parameters = dict()
    results = search(parameters, config=DEFAULT_CONFIG)
    print(results)
    response = construct_search_response(results, 'There are no artifacts in the knowledgebase.')
    return(response)


@kbapi_app.route('/list/<queries>', methods=['GET'])
@auth.login_required
def get_query(queries=''):
    """
    List the artifacts matching the query
    """
    parameters["query"] = queries
    results = search(parameters, config=DEFAULT_CONFIG)
    response = construct_search_response(results, 'There are no matching artifacts.')
    return(response)


@kbapi_app.route('/list/category/<category>', methods=['GET'])
@auth.login_required
def get_category(category=''):
    """
    List the artifacts in a category
    """
    parameters["category"] = category
    results = search(parameters, config=DEFAULT_CONFIG)
    response = construct_search_response(results, 'There are no artifacts with this category.')
    return(response)


@kbapi_app.route('/list/tags/<tags>', methods=['GET'])
@auth.login_required
def get_tags(tags=''):
    """
    List the artifacts with the given tags
    """
    parameters["tags"] = tags
    results = search(parameters, config=DEFAULT_CONFIG)
    response = construct_search_response(results, 'There are no artifacts with these tags.')
    return(response)


@kbapi_app.route('/stats', methods=['GET'])
@auth.login_required
def return_stats():
    """
    Returns statistics about the knowledgebase
    """
    response = stats(DEFAULT_CONFIG)
    response.mimetype = MIME_TYPE['json']
    return(response)


@kbapi_app.route('/tags', methods=['GET'])
@auth.login_required
def list_db_tags():
    """
    List all  the tags
    """
    results = list_all_tags(config=DEFAULT_CONFIG)
    return (results)


@kbapi_app.route('/templates', methods=['GET'])
@auth.login_required
def list_all_templates():
    """
    List all the available templates
    """
    params = dict()
    return(search_templates(params, DEFAULT_CONFIG))


@kbapi_app.route('/templates/<string:templates>', methods=['GET'])
@auth.login_required
def kb_query_templates(templates):
    """
    List the templates matching a query string
    """
    params = dict()
    params["query"] = templates
    return(search_templates(params, DEFAULT_CONFIG))


@kbapi_app.route('/template/apply/<string:title>', methods=['PUT'])
@auth.login_required
def kb_apply_template(title):
    """
    Apply a template to specific artifacts
    """
    params = dict()
    params["title"] = request.form.get("title", "")
    params["category"] = request.form.get("category", "")
    params["author"] = request.form.get("author", "")
    params["status"] = request.form.get("status", "")
    params["tags"] = request.form.get("tags", "")
    params["extended_match"] = request.form.get("extended_match", "")
    return (apply_template(params, DEFAULT_CONFIG))


@kbapi_app.route('/template/new/<string:template>', methods=['POST'])
def kb_new_template(template):
    """
    Create a new template with the default template content
    """
    params = dict()
    params["template"] = template
    return(new_template(params, DEFAULT_CONFIG))


@kbapi_app.route('/template/add/<string:title>', methods=['POST'])
@auth.login_required
def kb_add_template(title):
    """
    Add a new template with custom content
    """
    params = dict()
    params["title"] = title
    attachment = request.files['file']
    return(add_template(params, DEFAULT_CONFIG, attachment))


@kbapi_app.route('/template/delete/<string:template>', methods=['POST'])
def kb_delete_template(template):
    """
    Delete a named template
    """
    params = dict()
    params["title"] = template
    return(delete_template(params, DEFAULT_CONFIG))


@kbapi_app.route('/template/get/<string:title>', methods=['GET'])
@kbapi_app.route('/template/view/<string:title>', methods=['GET'])
@auth.login_required
def kb_get_template(title):
    """
    Get/View a template
    """
    return (get_template(title, DEFAULT_CONFIG))


@kbapi_app.route('/template/update/<string:title>', methods=['PUT'])
@auth.login_required
def kb_update_template(title):
    """
    Update a named template (with content)
    """
    attachment = request.files['file']
    return (update_template(title, DEFAULT_CONFIG, attachment))


@kbapi_app.route('/update/<int:id>', methods=['PUT'])
@auth.login_required
def update_artifact(id):
    """
    Update an artifact
    """
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
    """
    Returns current version of the kb software
    """
    response = make_response(({'Version': str(__version__)}), 200)
    response.mimetype = MIME_TYPE['json']
    return(response)


@kbapi_app.route('/view/<int:id>', methods=['GET'])
@kbapi_app.route('/get/<int:id>', methods=['GET'])
@auth.login_required
def view_artifact_by_id(id):
    """
    Get/View an artifact by ID
    """
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_id(conn, id, DEFAULT_CONFIG))


@kbapi_app.route('/view/<string:title>', methods=['GET'])
@kbapi_app.route('/get/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_title(title):
    """
    Get/View an artifact by title
    """
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_title(conn, title, DEFAULT_CONFIG))


@kbapi_app.route('/view/<string:category>/<string:title>', methods=['GET'])
@kbapi_app.route('/get/<string:category>/<string:title>', methods=['GET'])
@auth.login_required
def view_artifact_by_name(category, title):
    """
    Get/View an artifact by category/title
    """
    conn = db.create_connection(DEFAULT_CONFIG["PATH_KB_DB"])
    return (view_by_name(conn, title, category, DEFAULT_CONFIG))


# Start the server
if __name__ == '__main__':
    kbapi_app.run(debug=DEBUG, host=HOST, port=PORT)
