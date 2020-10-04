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
import sys
sys.path.append('kb')

from typing import Dict
import kb.filesystem as fs
from kb.actions.erase import eraseAction

def erase(eraseOnlyDB, config: Dict[str, str]):
    """
    Erase the entire kb knowledge base (or only the database).

    Arguments:
    args:           - a string containing what it to be deleted
                      if "db" then only the database will be deleted
                      elsee everthing will be deleted
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """

    response = eraseAction(eraseOnlyDB,config)
    
    return(response)
