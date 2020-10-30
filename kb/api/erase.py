# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb erase API module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

from flask import make_response

from kb.actions.erase import erase_kb
from kb.api.constants import MIME_TYPE


def erase(component, config: Dict[str, str]):
    """
    Erase the entire kb knowledge base (or only the database).

    Arguments:
    component:      - a string containing what it to be deleted
                      if "db" then only the database will be deleted
                      otherwise everything will be deleted
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """

    component = component.lower()
    if component == 'db' or component == 'all':
        if component == 'db':
            erase_what = "db"
            erase_what_text = "database"
        else:
            erase_what = "all"
            erase_what_text = "whole knowledgebase"
        results = erase_kb(erase_what, config)
        if results == -404:
            response = make_response(({'Error': 'The ' + erase_what_text + ' has not been erased.'}), 404)
        else:
            response = make_response(({'OK': 'The ' + erase_what_text + ' has been erased.'}), 200)
    else:
        response = make_response(({'Error': 'Invalid Parameter'}), 406)  # 'Not Acceptable'
        response.allow = ['all', 'db']
    response.mimetype = MIME_TYPE['json']    
    return response
