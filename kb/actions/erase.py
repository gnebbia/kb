# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb erase command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
import kb.filesystem as fs


def erase_kb(erase_what, config: Dict[str, str]):
    """
    Erase the entire kb knowledge base (or only the database).

    Arguments:
    eraseOnlyDB:    - a string containing the following fields:
                      if "db", only the database will be deleted
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """

    if erase_what == "db":
            try:
                fs.remove_file(config["PATH_KB_DB"])
                fs.remove_file(config["PATH_KB_HIST"])
                response = 200
            except FileNotFoundError:
                response= 404
    else:
            try:
                fs.remove_directory(config["PATH_KB"])
                response = 200
            except FileNotFoundError:
                response = 404
    return(response)