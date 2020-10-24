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


def get_templates(templates_path: str) -> List[str]:
    """
    Get the list of available templates.

    Arguments:
    templates_path      - the path where all templates are stored

    Returns:
    A list of strings representing the available templates
    """
    return fs.list_files(templates_path)


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
    return(get_templates(config["PATH_KB_TEMPLATES"]))
    

def apply_on_set(args: Dict[str, str], config: Dict[str, str]):
    """
    Apply the specified template to all the filtered artifacts
    """
    # Check initialization
    initializer.init(config)

    tags_list = None
    if args["tags"] and args["tags"] != "":
        tags_list = args["tags"].split(';')

    conn = db.create_connection(config["PATH_KB_DB"])
    is_query_strict = not args["extended_match"]
    rows = db.get_artifacts_by_filter(
        conn,
        title=args["title"],
        category=args["category"],
        tags=tags_list,
        status=args["status"],
        author=args["author"],
        is_strict=is_query_strict)
    rows_updated = 0
    for artifact in rows:
        rows_updated = rows_updated + 1
        updated_artifact = Artifact(
            id=artifact.id,
            title=artifact.title,
            category=artifact.category,
            tags=artifact.tags,
            author=artifact.author,
            status=artifact.status,
            template=args["template"])
        db.update_artifact_by_id(conn, artifact.id, updated_artifact)
    if rows_updated == 0:
        resp_content = '{"Error":"' + "No matching artifacts to apply template" + '"}'
        resp = make_response((resp_content), 404)
    else:
        resp_content = '{"OK":"' + str(rows_updated) + " artifacts updated" + '"}'
        resp = make_response((resp_content), 200)
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
    print(template_path)
    if fs.is_file(template_path):
        resp_content = '{"Error":"' + "Template already exists" + '"}'
        resp = make_response((resp_content), 409)
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
    attachment      - The template file itself
    """

    # Get the filename
    templates_path = Path(config["PATH_KB_TEMPLATES"])
    template_path = str(Path(config["PATH_KB_TEMPLATES"]) + "/" + title)
    if not fs.is_file(template_path):
        resp_content = '{"Error":"' + "Template does not exist" + '"}'
        resp = make_response((resp_content), 404)
        resp.mimetype = 'application/json'
        return(resp)

    filecontent.save(os.path.join(templates_path, title))
    resp_content = '{"OK":"' + "Template successfully updated" + '"}'
    resp = make_response((resp_content), 200)
    resp.mimetype = 'application/json'
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
    template_name = (Path(config["PATH_KB_TEMPLATES"]) / args["title"])
    if not fs.is_file(template_name):
        return(-404)
    else:
        fs.remove_file(Path(template_name))
        return(-200)


def get_template(template, DEFAULT_CONFIG):
    """
    Retrieve a template

    Arguments:
    args:           - template name
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES - directory where the templates are located
    """

    # Default response is an error
    response = -404
    template_name = (Path(DEFAULT_CONFIG["PATH_KB_TEMPLATES"]) / template)
    if not fs.is_file(template_name):
        return(resp)

    with open(template_name, "rb") as tp_file:
        encoded_string = base64.b64encode(tp_file.read())
    return(encoded_string)


def edit(args: Dict[str, str], config: Dict[str, str]):
    """
    Edit a template from the kb templates.

    Arguments:
    args:           - a dictionary containing the following fields:
                      template -> the name of the template to edit
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_TEMPLATES  - the path to where the templates of KB
                                           are stored
                      EDITOR             - the editor program to call
    """
    template_path = str(Path(config["PATH_KB_TEMPLATES"]) / args["template"])

    if not fs.is_file(template_path):
        print("ERROR: The template you want to edit does not exist. "
              "Please specify a valid template to edit or create a new one")
        sys.exit(1)

    shell_cmd = shlex.split(
        config["EDITOR"]) + [template_path]
    call(shell_cmd)
