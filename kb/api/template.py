# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb template api module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import shlex
import sys
import os
import toml
from pathlib import Path
from subprocess import call
from typing import Dict, List
import kb.db as db
import kb.initializer as initializer
import kb.filesystem as fs
import kb.config as conf
from kb.entities.artifact import Artifact
from flask import jsonify, make_response
import kb.printer.template as printer
from werkzeug.utils import secure_filename
import base64
from kb.actions.template import delete as delete_template
from kb.actions.template import update_template as update_a_template
from kb.actions.template import get_templates
from kb.actions.template import apply_on_set as apply_templates


def search(args: Dict[str, str], config: Dict[str, str]):
    """
    Search templates installed in kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      query -> filter for the title field of the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES     - the path to where the templates of KB
                                              are stored
    """
    template_list = get_templates(config["PATH_KB_TEMPLATES"])
    if not template_list:
        resp = make_response(({'Error': 'No Templates Exist'}), 404)
        resp.mimetype = 'application/json'
        return (resp)

    if args.get("query", "") == "":
        resp = make_response(jsonify(template_list), 200)
        resp.mimetype = 'application/json'
        return (resp)

    if args["query"]:
        template_list = [x for x in template_list if args["query"] in x]
        resp = make_response(jsonify(template_list), 200)
        resp.mimetype = 'application/json'
        return (resp)


def apply_on_set(args: Dict[str, str], config: Dict[str, str]):
    """
    Apply the specified template to all the filtered artifacts
    """
    rows_updated = apply_templates(args, config)
    if rows_updated == 0:
        resp_content = '{"Error":"' + "No matching artifacts to apply template" + '"}'
        resp = make_response((resp_content), 404)
        resp.mimetype = 'application/json'
    else:
        resp_content = '{"OK":"' + str(rows_updated) + " artifacts updated" + '"}'
        resp = make_response((resp_content), 200) 
        resp.mimetype = 'application/json'
    return(resp)


def new(args: Dict[str, str], config: Dict[str, str]):
    """
    Create a new template from scratch starting from the default template.

    Arguments:
    args:           - a dictionary containing the following fields:
                      template -> the name of the new template to create
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES         - the path to where the templates of KB
                                                  are stored
                      PATH_KB_DEFAULT_TEMPLATE  - the path to where the default template of KB
                                                  is stored
                      EDITOR                    - the editor program to call
    """

    template_path = str(Path(config["PATH_KB_TEMPLATES"]) / args["template"])
    if fs.is_file(template_path):
        resp_content = '{"Error":"' + "Template already exists" + '"}'
        resp = make_response((resp_content), 409)
        resp.mimetype = 'application/json'
        return(resp)

    #    print("ERROR: The template you inserted corresponds to an existing one. ",
    #          "Please specify another name for the new template")
    #    sys.exit(1)

    fs.create_directory(Path(template_path).parent)

    with open(template_path, 'w') as tmplt:
        tmplt.write("# This is an example configuration template\n\n\n")
        tmplt.write(toml.dumps(conf.DEFAULT_TEMPLATE))

    # shell_cmd = shlex.split(
    #    config["EDITOR"]) + [template_path]
    # call(shell_cmd)
    resp_content = '{"OK":"' + "Default template content added" + '"}'
    resp = make_response((resp_content), 200)
    resp.mimetype = 'application/json'
    return(resp)


def add(args: Dict[str, str], config: Dict[str, str], filecontent):
    """
    Add a new template to the templates available in kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> the path to the template to include in kb templates
                      title -> the title to assign to the kb template added
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES         - the path to where the templates of KB
                                                  are stored
    """

    # Get the filename
    templates_path = Path(config["PATH_KB_TEMPLATES"])
    template_path = str(Path(config["PATH_KB_TEMPLATES"]) / args["title"])
    if fs.is_file(template_path):
        resp_content = '{"Error":"' + "Template already exists" + '"}'
        resp = make_response((resp_content), 409)
        return(resp)

    filecontent.save(os.path.join(templates_path, args["title"]))
    resp = jsonify({'OK': 'Template successfully uploaded'})
    resp.status_code = 200
    return (resp)


def update_template(title: str, config: Dict[str, str], filecontent):
    """
    Updates an existing template.

    Arguments:
    title:           - a string containing the title of the existing kb template
    config:         - a configuration dictionary containing at least
                      the following key:
                      PATH_KB_TEMPLATES         - the path to where the templates of KB
                                                  are stored
    filecontent      - The template file itself
    """
    resp = update_a_template(title, config, filecontent)
    return (resp)


def delete(args: Dict[str, str], config: Dict[str, str]):
    """
    Delete a template from the kb templates.

    Arguments:
    args:           - a dictionary containing the following fields:
                      template -> the name of the template to remove
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES         - the path to where the templates of KB
                                                  are stored
    """
    results = delete_template(args, config)
    if results == -404:
        resp_content = '{"Error":"' + "Template does not exist" + '"}'
        resp = make_response((resp_content), 404)
        resp.mimetype = 'application/json'
        return(resp)
    if results == -200:
        resp_content = '{"OK":"' + "Template Removed" + '"}'
        resp = make_response((resp_content), 200)
        resp.mimetype = 'application/json'
        return(resp)


def get_template(template, DEFAULT_CONFIG):
    """
    Retrieve a template

    Arguments:
    args:           - template name
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES - directory where the templates are located
    """

    results = get_template(template_name)
    if results == -404:
        resp_content = '{"Error":"' + "Template does not exist" + '"}'
        resp = make_response((resp_content), 404)
        resp.mimetype = 'application/json'
        return(resp)
    else:
        record = '{"Template":"' + template + '","Content":"' + str(encoded_string) + '"}'
        resp = (make_response((record), 200))
        resp.mimetype = 'text/plain;charset=UTF-8'
        return(resp)

