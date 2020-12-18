# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb base api module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

from flask import make_response
from markupsafe import escape 

from kb.actions.base import base_list,get_current_kb_details,does_base_exist,switch_base,new_base,delete_base
from kb.api.constants import MIME_TYPE
from kb.config import DEFAULT_KNOWLEDGEBASE


def base(config: Dict[str, str]):
    """
    Get information about the available knowledge bases

    Argument:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PAPATH_KB_INITIAL_BASESTH_KB - the main path of KB information
    """

    bases = base_list(config)
    bases_json = '{"knowledge_bases":'+str(bases)+'}'
    resp = make_response(bases_json.replace("'",'"'), 200)    
    resp.mimetype = MIME_TYPE['json']
    return(resp)

def switch(target:str, config: Dict[str, str]):
    if does_base_exist(target,config):
        switch_base(target,config)
        resp = (make_response(({'Switched': "The current knowledge base is now : '" + escape(target) + "'"}), 200))
    else:
        resp = (make_response(({'Error': "The knowledge base '" + escape(target) + "' does not exist"}), 404))
    resp.mimetype = MIME_TYPE['json']
    return resp

def get_current(config: Dict[str, str]):
    """
    Return the current knowledge bases

    Argument:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PAPATH_KB_INITIAL_BASESTH_KB - the main path of KB information
    """

    current = get_current_kb_details(config)
    json_current = '{"current_knowledge_base":'+str(current)+'}'
    resp = make_response(json_current.replace("'",'"'), 200)    
    resp.mimetype = MIME_TYPE['json']
    return(resp)


def make_new_base(args: Dict[str, str], config: Dict[str, str]):
    """
    Command implementation of creation of new knowledge base

    Arguments:
    args        -   contains the name and description of the knowledge base to create
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """
    name = args.get("name","")
    results = new_base(args,config)

    # Can't use the name contained in DEFAULT_KNOWLEDGEBASE
    if results == -1:
        resp = make_response({"Error":"The knowledge base '" + DEFAULT_KNOWLEDGEBASE + "' is reserved, and therefore, not allowed"}, 404)    
        resp.mimetype = MIME_TYPE['json']
        return resp 
    
    # Check to see if the knowledge base already exists - cannot create it otherwise
    if results == -2:
        resp = make_response({"Error":"The knowledge base '" + name + "' already exists"}, 404)    
        resp.mimetype = MIME_TYPE['json']
        return resp 
        
    # Return success message
    if results == 0:
        resp = make_response({"OK":"The knowledge base '" + name + "' has been created"}, 200)    
        resp.mimetype = MIME_TYPE['json']
        return resp   


def delete_a_base(name, config: Dict[str, str]):
    """
    Implementation of delete a knowledge bases

    Arguments:
    args        -   contains the name of the knowledge base to delete
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_INITIAL_BASES, the path to where the .toml file containing kb information is stored
    """    

    parameters = dict()
    parameters["name"] = name
    results = delete_base(parameters,config)
    if results == 0:
        resp = make_response({"OK":"The knowledge base '" + name + "' has been deleted"}, 200)    
        resp.mimetype = MIME_TYPE['json']        
        return resp
    if results == -1:
        resp = make_response({"Error":"Cannot delete the current knowledge base"}, 404)    
        resp.mimetype = MIME_TYPE['json']
        return resp 
    if results == -2:
        resp = make_response({"Error":"The knowledge base '" + name + "' does not exist"}, 404)    
        resp.mimetype = MIME_TYPE['json']
        return resp
    if results == -3:
        resp = make_response({"Error":"The knowledge base '"+DEFAULT_KNOWLEDGEBASE + "' is reserved, and therefore, cannot be deleted"}, 404)    
        resp.mimetype = MIME_TYPE['json']
        return resp
