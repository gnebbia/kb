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
from pathlib import Path
from typing import Dict

from kb.actions.list import list_categories, list_tags, list_templates
from kb.api.constants import MIME_TYPE, API_VERSION
from kb.config import construct_config,BASE
import kb.db as db
import kb.filesystem as fs
import kb.initializer
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


def remove_base_from_list(name:str, data:str):
    """
    Gets a list of active knowledgebases.

    Arguments:
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """

    output_list = []
    for base in data["bases"]:
        if base["name"] != name:
            base_info = dict()
            base_info['name'] = base['name']
            base_info['description'] = base['description']
            output_list.append(base_info)
    return (output_list)


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


def new_base(args: Dict[str, str], config: Dict[str, str]):
    """
    Implementation of creation of new knowledge bases

    Arguments:
    args        -   contains the name and description of the knowledge base to create
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
 
    initial_bases_path = config["PATH_KB_INITIAL_BASES"]
    name = args.get("name","")
    description = args.get("description","")

    # Cannot use the reserved term "default"
    if name == 'default':
        return -1
       
    # Check to see if the knowledge base already exists - cannot create it otherwise
    if does_base_exist(name,config):
        return -2
    
    data = toml.load(config["PATH_KB_INITIAL_BASES"])
    data['current'] = name
    data['bases'].append({'name':name,'description':description})
    
    # Write the new information to the main bases.toml file.
    with open(initial_bases_path, 'w') as dkb:
        dkb.write(toml.dumps(data))

    # Create new configuration file to initialise the knowledge base with
    # and initialise it
    new_config = construct_config(BASE)
    kb.initializer.init(new_config) 

    return 0


def delete_base(args: Dict[str, str], config: Dict[str, str]):
    """
    Implementation of delete a knowledge bases

    Arguments:
    args        -   contains the name of the knowledge base to delete
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """    

    initial_bases_path = config["PATH_KB_INITIAL_BASES"]
    name = args.get("name","")
    
    # Get bases.tooml file
    data = toml.load(initial_bases_path)
    current = data['current']

    if current == name:
        return -1 # Cannot delete current knowledgebase

    if not does_base_exist(name,config):
        return -2 # Cannot delete a knowledgebase if it doesn't exist
    
    
    base_path = str(Path(config["PATH_BASE"],name))

    data['bases'] = remove_base_from_list(name,data)


    # Write bases.toml file without the removed base
    with open(initial_bases_path, 'w') as dkb:
        dkb.write(toml.dumps(data))

    # remove the directory with the artifacts etc in...
    fs.remove_directory(base_path)
    return 0      
