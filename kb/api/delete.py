# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb delete command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import sys
# sys.path.append('kb')

import sys
from typing import Dict
from pathlib import Path
import kb.db as db
import kb.initializer as initializer
import kb.history as history
import kb.filesystem as fs
from kb.actions.delete import delete_artifacts
from flask import make_response


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
    """
    initializer.init(config)

    results = delete_artifacts(args, config, True)

    if results == -404:
        response = (make_response(({'Error': 'There is no artifact with that ID, please specify a correct artifact ID'}), 404))
    if results == -301:
        response = (make_response(({'Error': 'There is more than one artifact with that title, please specify a category'}), 301))
    if results == -302:
        response = (make_response(({'Error': 'There are no artifacts with that title, please specify a title'}), 302))
    if results >= 0:
        response = (make_response(({'Deleted': results}), 200))
    return response
