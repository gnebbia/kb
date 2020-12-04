# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb search command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""
import sys
from typing import Dict

from kb.actions.search import search_kb
import kb.history as history
import kb.printer.search as printer
import kb.printer.others as others


def search(args: Dict[str, str], config: Dict[str, str]):
    """
    Search artifacts within the knowledge base of kb and display the output on the terminal.

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

    result = search_kb(args, config)

    # List all categories
    if args.get("all_categories", False) is True:
        others.generate_list(args, result, 'Categories')
        sys.exit(0)

    # List all tags
    if args.get("all_tags", False) is True:
        others.generate_list(args, result, 'Tags')
        sys.exit(0)

    # Write to history file
    history.write(config["PATH_KB_HIST"], result)

    # Print resulting list
    color_mode = not args["no_color"]
    if args["verbose"]:
        printer.print_search_result_verbose(result, color_mode)
    else:
        printer.print_search_result(result, color_mode)
