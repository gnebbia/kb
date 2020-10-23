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
    # template_list = fs.list_files(config["PATH_KB_TEMPLATES"])
    template_list = get_templates(config["PATH_KB_TEMPLATES"])
    if not template_list:
        return (make_response(({'Error': 'No Templates Exist'}), 404))

    if args.get("query", "") == "":
        return make_response(jsonify(template_list), 200)

    if args["query"]:
        template_list = [x for x in template_list if args["query"] in x]
        return make_response(jsonify(template_list), 200)

    # color_mode = not args["no_color"]
    # printer.print_template_search_result(template_list, color_mode)


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

    for artifact in rows:
        updated_artifact = Artifact(
            id=artifact.id,
            title=artifact.title,
            category=artifact.category,
            tags=artifact.tags,
            author=artifact.author,
            status=artifact.status,
            template=args["template"])
        db.update_artifact_by_id(conn, artifact.id, updated_artifact)


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

    # template_path = Path(config["PATH_KB_DATA"], args["title"])
    filecontent.save(os.path.join(templates_path, args["title"]))
    # os.rename(os.path.join(template_path, filename), os.path.join(template_path, args["title"]))
    resp = jsonify({'OK': 'Template successfully uploaded'})
    resp.status_code = 200
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
        resp_content = '{"Error":"' + "Template does not exist" + '"}'
        resp = make_response((resp_content), 404)
        return(resp)
    else:
        fs.remove_file(Path(template_name))
        resp_content = '{"OK":"' + "Template Removed" + '"}'
        resp = make_response((resp_content), 200)
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

    # Default response is an error
    resp = (make_response(({'Error': 'Template does not exist'}), 404))

    template_name = (Path(DEFAULT_CONFIG["PATH_KB_TEMPLATES"]) / template)
    if not fs.is_file(template_name):
        resp_content = '{"Error":"' + "Template does not exist" + '"}'
        resp = make_response((resp_content), 404)
        return(resp)

    with open(template_name, "rb") as tp_file:
        encoded_string = base64.b64encode(tp_file.read())
    record = '{"Template":"' + template + '","Content":"' + str(encoded_string) + '"}'
    response = (make_response((record), 200))

    return(response)


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
