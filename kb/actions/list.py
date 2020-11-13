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
    return category_list


def list_templates(config: Dict[str, str]):
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

    template_list = dict()
    template_list = sorted(fs.list_files(config["PATH_KB_TEMPLATES"]))
    return template_list


def list_tags(conn, config):
    """
    Returns a list of tags within the knowledge base.

    Arguments:

    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """

    tags_list = dict()
    tags_list = db.ldb_tags(conn)
    return tags_list
