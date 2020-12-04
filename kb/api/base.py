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

from kb.actions.base import base_list,get_current_kb_details,does_base_exist,switch_base
from kb.api.constants import MIME_TYPE


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
        resp = (make_response(({'Switched': "The current knowledge base is now : '" + target + "'"}), 200))
    else:
        resp = (make_response(({'Error': "The knowledge base '" + target + "' does not exist"}), 404))
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
