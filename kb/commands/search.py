# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb search command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.printer.search as printer
import kb.history as history


def search(args: Dict[str, str], config: Dict[str, str]):
    """
    Search artifacts within the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      query -> filter for the title field of the artifact
                      category -> filter for the category field of the artifact
                      tags -> filter for the tags field of the artifact
                      author -> filter for the author field of the artifact
                      status -> filter for the status field of the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    # Check initialization
    initializer.init(config)

    tags_list = None
    if args["tags"] and args["tags"] != "":
        tags_list = args["tags"].split(';')

    conn = db.create_connection(config["PATH_KB_DB"])
    rows = db.get_artifacts_by_filter(
        conn,
        title=args["query"],
        category=args["category"],
        tags=tags_list,
        status=args["status"],
        author=args["author"])

    # rows.sort(key=lambda x: x[1])
    artifacts = sorted(rows, key=lambda x: x.title)

    # Write to history file
    history.write(config["PATH_KB_HIST"], artifacts)

    # Print resulting list
    color_mode = not args["no_color"]
    if args["verbose"]:
        printer.print_search_result_verbose(artifacts, color_mode)
    else:
        printer.print_search_result(artifacts, color_mode)
