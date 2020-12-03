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
from kb.actions.base import base_list,get_current_kb_details,does_base_exist,switch_base
from kb.printer.base import generate_current_kb,generate_bases_output

def list_bases(args: Dict[str, str], config: Dict[str, str]):
    """
    Gets a list of active knowledgebases.

    Arguments:
    args        -   contains any switches and flags that need to be applied
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    bases = base_list(config)
    if "no_color" in args:
        color_mode = not args["no_color"]
    else:
        color_mode = False
    generate_bases_output(bases, color_mode)
    return True


def get_current(args: Dict[str, str], config: Dict[str, str]):
    """
    Get information about the current knowledgebase.

    Arguments:
    args        -   contains any switches and flags that need to be applied
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    current_kb=get_current_kb_details(config)
    if "no_color" in args:
        color_mode = not args["no_color"]
    else:
        color_mode = False
    generate_current_kb(current_kb,color_mode)
    return current_kb


def switch(args: Dict[str, str], config: Dict[str, str]):
    print("Switch to ", args["kb"])
    target = args["kb"]
    if does_base_exist(target,config):
        print("exists")
        switch_base(target,config)
    else:
        print("doesnt exist")
    return True

def nowt(args: Dict[str, str], config: Dict[str, str]):
    return True

COMMANDS = {
    'add': nowt,
    'switch': switch,
    'current':get_current,
    'delete': nowt,
    'edit': nowt,
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
