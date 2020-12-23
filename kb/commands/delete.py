# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb delete command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import sys
from typing import Dict
from pathlib import Path

from kb.actions.delete import delete_artifacts
import kb.db as db
import kb.history as history
import kb.initializer as initializer
import kb.filesystem as fs



def delete(args: Dict[str, str], config: Dict[str, str]):
    """
    Delete a list of artifacts from the kb knowledge base.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> a list of IDs (the ones you see with kb list)
                        associated to the artifacts we want to delete
                      title -> the title assigned to the artifact(s)
                      category -> the category assigned to the artifact(s)
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
    db_id:          - True if this is a raw DB id, 
                      False if this is a viewed artifact IDs
    """
    initializer.init(config)

    response = delete_artifacts(args, config, False)

    if response == -200:
        print("Artifact removed.")
    
    if response == -301:
        print("There is more than one artifact with that title, please specify a category")
    
    if response == -302:
        print("There is no artifact with that name, please specify a correct artifact name")

