# -*- encoding: utf-8 -*-
# kb v0.1.3
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
from pathlib import Path
from subprocess import call
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.filesystem as fs
from kb.entities.artifact import Artifact
import kb.printer.template as printer



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
    template_list = fs.list_files(config["PATH_KB_TEMPLATES"])
    if args["query"]:
        template_list = [x for x in template_list if args["query"] in x]
    color_mode = not args["no_color"]
    printer.print_template_search_result(template_list, color_mode)


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
        print("ERROR: The template you inserted corresponds to an existing one. "
                "Please specify another name for the new template")
        sys.exit(1)

    
    fs.create_directory(Path(template_path).parent)
    fs.copy_file(config["PATH_KB_DEFAULT_TEMPLATE"], template_path)

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
    template_name = args["template"]
    fs.remove_file(Path(config["PATH_KB_TEMPLATES"], template_name))


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


COMMANDS = {
    'add': add,
    'delete': delete,
    'edit': edit,
    'list': search,
    'new': new,
}


def template(args: Dict[str, str], config: Dict[str, str]):
    """
    Manage templates for kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      template_command -> the sub-command to execute for templates
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

    COMMANDS[args["template_command"]](args, config)
