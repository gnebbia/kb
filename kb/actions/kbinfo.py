# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb stats action module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
import kb.filesystem as fs
from kb.actions.list import list_categories, list_tags, list_templates
from kb.api.constants import MIME_TYPE, API_VERSION
import db
from kb import __version__


def kb_stats(config: Dict[str, str]):
    """
    Get useful statistics for the knowledge basee.

    Arguments:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_HIST      - the history menu path of KB
    """
 
    conn = db.create_connection(config["PATH_KB_DB"])

    augmented_config = dict()
    versions_config = dict()
    current_stats_config = dict()
    sizes_config = dict()
    categories = dict()
    artifacts = dict()
    current_categories = dict()
    current_tags = dict()
    tags = dict()
    templates = dict()

    augmented_config["DEFAULT_CONFIG"] = config

    versions_config["kb"] = str(__version__)
    versions_config["kbAPI"] = str(API_VERSION)
    augmented_config["Versions"] = versions_config

    current_categories = list_categories(config)
    categories["Current"] = current_categories
    categories["Total"] = fs.count_files(config["PATH_KB_DATA"])
    current_stats_config["Categories"] = categories

    current_templates = list_templates(config)
    templates["Current"] = current_templates
    templates["Total"] = fs.count_files(config["PATH_KB_TEMPLATES"])
    current_stats_config["Templates"] = templates

    current_tags = list_tags(conn, config)
    tags["Current"] = current_tags
    tags["Total"] = len(current_tags)
    current_stats_config["Tags"] = tags

    sizes_config["Database"] = fs.get_file_size(config["PATH_KB_DB"])
    sizes_config["Total"] = fs.get_complete_size(config["PATH_KB"])
    sizes_config["Templates"] = fs.get_complete_size(config["PATH_KB_TEMPLATES"])
    sizes_config["Artifacts"] = fs.get_complete_size(config["PATH_KB_DATA"])
    current_stats_config["Sizes"] = sizes_config

    artifacts["Total"] = db.count_artifacts(conn)
    current_stats_config["Artifacts"] = artifacts
    augmented_config["lastUpdate"] = fs.get_last_modified_time(config["PATH_KB_DB"])
    augmented_config["CurrentStatistics"] = current_stats_config

    return(augmented_config)
