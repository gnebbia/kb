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
import filesystem as fs
import initializer
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
 
   # Check initialization
    initializer.init(config)

    conn = db.create_connection(config["PATH_KB_DB"])

 
    augmented_config = dict()
    versions_config = dict()
    current_stats_config = dict()
    sizes_config = dict()

    augmented_config["DEFAULT_CONFIG"] = config

    versions_config["KB_VERSION"] = str(__version__)
    versions_config["KB_API_VERSION"] = str(API_VERSION)
    augmented_config["VERSIONS"] = versions_config

    current_stats_config["KB_CATEGORIES"] = fs.count_files(config["PATH_KB_DATA"])
    current_stats_config["KB_TEMPLATES"] = fs.count_files(config["PATH_KB_TEMPLATES"])
    current_stats_config["KB_TAGS"] = db.count_tags(conn)

    sizes_config["KB_DB_BYTES"] = fs.get_file_size(config["PATH_KB_DB"])
    sizes_config["KB_TOTAL_BYTES"] = fs.get_complete_size(config["PATH_KB"])
    sizes_config["KB_TEMPLATE_BYTES"] = fs.get_complete_size(config["PATH_KB_TEMPLATES"])
    sizes_config["KB_ARTIFACT_BYTES"] = fs.get_complete_size(config["PATH_KB_DATA"])
    current_stats_config["SIZES"] = sizes_config


    current_stats_config["KB_ARTIFACTS"] = db.count_artifacts(conn)
    augmented_config["CURRENT_STATS"] = current_stats_config

    print(augmented_config)
    return(augmented_config)
