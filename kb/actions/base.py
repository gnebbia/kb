# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb base action module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import toml
from typing import Dict

from kb.actions.list import list_categories, list_tags, list_templates
from kb.api.constants import MIME_TYPE, API_VERSION
import kb.db as db
import kb.filesystem as fs
from kb import __version__

def base_list(config:Dict[str, str]):
    """
    Gets a list of active knowledgebases.

    Arguments:
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    list_of_bases = []
    data = toml.load(config["PATH_KB_INITIAL_BASES"])
    for base in data["bases"]:
        base_info = dict()
        base_info['name'] = base['name']
        base_info['description'] = base['description']
        list_of_bases.append(base_info)
    return (list_of_bases)

def does_base_exist(target:str, config:Dict[str, str]):
    """
    Check to see if a specific knowledge base exists

    Arguments:
    base        -   the knowledgebase to check for
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    list_of_bases = base_list(config)
    for base in list_of_bases:
        if base["name"] == target:
            return True
    return False

def get_current_kb_details(config:Dict[str, str]):
    """
    Get information about the current knowledgebase.

    Arguments:
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    ckb = dict()
    data = toml.load(config["PATH_KB_INITIAL_BASES"])
    ckb["name"] = data["current"]
    bases = data["bases"]
    for base in bases:
        if base['name'] == data['current']:
            ckb['description'] = base['description']
    return (ckb)

def switch_base(target:str,config:Dict[str, str]):
    """
    Switch the current knowledge base to the one supplied.

    Arguments:
    target      -   the desired knowledge base.
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """

    current = toml.load(config["PATH_KB_INITIAL_BASES"])
    current["current"] = target
    # Write the .toml file back - thereby switching the knowledge base
    with open(config["PATH_KB_INITIAL_BASES"], 'w') as switched:
        switched.write(toml.dumps(current))