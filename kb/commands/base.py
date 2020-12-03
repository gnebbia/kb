# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb template command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import shlex
import sys
import toml
from pathlib import Path
from subprocess import call
from typing import Dict, List

import kb.config as conf
import kb.db as db
import kb.filesystem as fs

import kb.initializer as initializer
from kb.entities.artifact import Artifact
import kb.printer.template as printer
from kb.actions.template import edit as edit_template
from kb.actions.template import delete as delete_template
from kb.actions.base import base_list,get_current_kb_details
from kb.printer.base import generate_current_kb,generate_bases_output

def list_bases(args: Dict[str, str], config: Dict[str, str]):
    bases = base_list(config)
    if "no_color" in args:
        color_mode = not args["no_color"]
    else:
        color_mode = False
    generate_bases_output(bases, color_mode)
    return True

def get_current(args: Dict[str, str], config: Dict[str, str]):
    current_kb=get_current_kb_details(config)
    if "no_color" in args:
        color_mode = not args["no_color"]
    else:
        color_mode = False
    generate_current_kb(current_kb,color_mode)
    return current_kb

def switch(args: Dict[str, str], config: Dict[str, str]):
    return True

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
        return

    if args["query"]:
        template_list = [x for x in template_list if args["query"] in x]
    color_mode = not args["no_color"]
    printer.print_template_search_result(template_list, color_mode)



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

    if fs.is_file(template_path):
        print("ERROR: The template you inserted corresponds to an existing one. "
                "Please specify another name for the new template")
        sys.exit(1)

    fs.create_directory(Path(template_path).parent)
    # fs.copy_file(config["PATH_KB_DEFAULT_TEMPLATE"], template_path)

    with open(template_path, 'w') as tmplt:
        tmplt.write("# This is an example configuration template\n\n\n")
        tmplt.write(toml.dumps(conf.DEFAULT_TEMPLATE))

    shell_cmd = shlex.split(
        config["EDITOR"]) + [template_path]
    call(shell_cmd)


def add(args: Dict[str, str], config: Dict[str, str]):
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
    template_path = args["file"]
    if args["title"]:
        dest_path = str(Path(config["PATH_KB_TEMPLATES"]) / args["title"])
    else:
        dest_path = config["PATH_KB_TEMPLATES"]
    fs.copy_file(template_path, dest_path)


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
        print("ERROR: The template you want to delete does not exist. "
              "Please specify a valid template to edit or create a new one")
        sys.exit(1)


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
    edit_template(args, config)

COMMANDS = {
    'add': add,
    'base': switch,
    'current':get_current,
    'delete': delete,
    'edit': edit,
    'list': list_bases
}


def base(args: Dict[str, str], config: Dict[str, str]):
    """
    Manage knowledge bases for kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      command -> the sub-command to execute for templates
                                          that can be: "add", "delete", "edit",
                                          "list" or "new".
                      file -> used if the command is add, representing the template
                              file to add to kb
                      template -> used if the command is "delete", "edit" or "new" 
                                  to represent the name of the template
                      query -> used if the command is "list"
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DEFAULT_TEMPLATE - the path to the kb default template
                      PATH_KB_TEMPLATES        - the path to kb templates
                      EDITOR                   - the editor program to call
    """

    # Check initialization
    initializer.init(config)
    COMMANDS[args["base_command"]](args, config)
