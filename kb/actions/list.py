# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb list action module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

import kb.db as db
import kb.initializer as initializer
import kb.filesystem as fs

def list_categories(config: Dict[str, str]):
    """
    Returns a list of categories within the knowledge base.

    Arguments:

    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """

    category_list = dict()
    category_list = sorted(fs.list_dirs(config["PATH_KB_DATA"]))
    # artifacts = sorted(rows, key=lambda x: x.title)
    return category_list
