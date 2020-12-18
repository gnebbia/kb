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


def write_base_list(initial_bases_path:str,data:str):
    """
    Write a list of active knowledge bases to the bases.toml file.

    Arguments:
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """

    # Write the information to the main bases.toml file.
    with open(initial_bases_path, 'w') as dkb:
        dkb.write(toml.dumps(data))
    return True


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


def add_base_to_list(name:str, description:str, data:str):
    """
    Adds a new knowledge base into the list.

    Arguments:
    name        -   name of the knowledge base to add
    description -   description of the new knowledge base.
    data        -   existing list
    """

    data['bases'].append({'name':name,'description':description})
    return(data)


def remove_base_from_list(name:str, data:str):
    """
    Gets a list of active knowledgebases.

    Arguments:
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """

    print(data)
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
    write_base_list(config["PATH_KB_INITIAL_BASES"],current)


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
    add_base_to_list(name,description,data) 

    write_base_list(initial_bases_path,data)

    # Create new configuration file to initialise the knowledge base with
    # and initialise it
    new_config = construct_config(BASE,name)
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
    
    write_base_list(initial_bases_path,data)

    # remove the directory with the artifacts etc in...
    fs.remove_directory(base_path)
    return 0    


def rename_base(args: Dict[str, str], config: Dict[str, str]):
    """
    Implementation of renaming a knowledge bases

    Arguments:
    args        -   contains the name and description of the knowledge base to create
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    old = args.get("old",'')
    new = args.get("new",'')
    current = get_current_kb_details(config)["name"]
    
    description = args.get("description",'')
    if old == '':
        return -1 # No old base supplied
    if new == '':
        return -2 # No new base supplied
    if old == new:
        return -3 # Old base name same as new base name
    if not does_base_exist(old,config):
        return -4 # Old base does not exist
    if does_base_exist(new,config):
        return -5 # New base already exists
    if new == 'default':
        return -6 # Cannot use 'default' as a kb name
    if old == 'default':
        return -7 # Cannot use 'default' as a kb name
    if old == current:
        return -8 # Cannot rename the current knowledge base
    if new == current:
        return -9 # Cannot rename to the current knowledge base

    # Manipulate the bases.toml file to effect the rename
    # but hold the data in memory
    data = toml.load(config["PATH_KB_INITIAL_BASES"])               # Get the bases.toml file
    data_with_new_base = add_base_to_list(new,description,data)     # Add the new base + description
    data_final = remove_base_from_list(old,data_with_new_base)      # Remove the old name
    final_toml = {  'current': current,                             # Re-assemble the toml file
                    'bases': data_final
                    }

    old_path = str(Path(config["PATH_BASE"],old))
    new_path = str(Path(config["PATH_BASE"],new))

    # Write toml file
    with open(str(Path(config["PATH_BASE"],'bases.toml')), 'w') as bases:
        bases.write(toml.dumps(final_toml))
        
    # need to lock old directory first ?????
    # Rename kb
    fs.rename_directory(str(old_path),str(new_path))

    return 0
