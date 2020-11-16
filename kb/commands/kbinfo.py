# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb stats command module

:Copyright: © 2020, alshaptons.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
from kb.printer.stats import generate_stats_header, generate_sizes, generate_lists,generate_def_config
from kb.actions.kbinfo import kb_stats


def kbinfo(args: Dict[str, str], config: Dict[str, str]):
    """
    Get statistics about the database

    Arguments:
    args        -   A dictionary containing the command line arguments
    config      -   A dictionary containing the current configuration
    """
    statistics = kb_stats(config)
    generate_stats_header(statistics, args.get("no_color", ""))
    if args["stats_verbose"]:
        print()
        generate_sizes(statistics, args.get("no_color", ""))
        print()
        generate_lists(statistics, args.get("no_color", ""))
        print()
        generate_def_config(statistics, args.get("no_color", ""))
    

