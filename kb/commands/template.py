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



def search(args, config):
    template_list = fs.list_files(config["PATH_KB_TEMPLATES"])
    if args["query"]:
        template_list = [x for x in template_list if args["query"] in x]
    color_mode = not args["no_color"]
    printer.print_template_search_result(template_list, color_mode)


def new(args, config):
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


def add(args, config):
    template_path = args["file"]
    fs.copy_file(template_path, config["PATH_KB_TEMPLATES"])

def delete(args, config):
    template_name = args["template"]
    fs.remove_file(Path(config["PATH_KB_TEMPLATES"], template_name))


def edit(args, config):
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
                      title -> the title assigned to the artifact(s)
                      category -> the category assigned to the artifact(s)
                      tags -> the tags assigned to the artifact(s)
                      author -> the author to assign to the artifact
                      status -> the status to assign to the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      EDITOR            - the editor program to call
    """

    # Check initialization
    initializer.init(config)

    COMMANDS[args["template_command"]](args, config)
