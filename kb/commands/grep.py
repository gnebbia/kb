# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb grep command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import sys
from pathlib import Path
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.printer.grep as printer
import kb.history as history
import kb.filesystem as fs


def grep(args: Dict[str, str], config: Dict[str, str]):
    """
    Grep through the list of artifacts of the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      regex -> the regex to search for
                      case_insensitive -> a boolean, if true,
                        the search will be case insensitive
                      matches -> a boolean, if true, only the raw
                        matches will be shown
                      verbose -> a boolean, if true, a verbose
                        output is produced on screen
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
    """
    initializer.init(config)

    conn = db.create_connection(config["PATH_KB_DB"])

    # Get all artifacts
    rows = db.get_artifacts_by_filter(conn, title="")

    # Get all the file paths related to the artifacts in the database
    file_list = [Path(config["PATH_KB_DATA"], r.category, r.title)
                 for r in rows]

    # Grep in the files
    results = fs.grep_in_files(
        file_list,
        args["regex"],
        args["case_insensitive"])

    # Get the list of artifact tuples in the form (category,title)
    artifact_names = [fs.get_filename_parts_wo_prefix(
        res[0], config["PATH_KB_DATA"]) for res in results]

    # If user specied --matches -> just show matching lines and exit
    if args["matches"]:
        printer.print_grep_matches(artifact_names)
        sys.exit(0)

    # Get the set of uniq artifacts
    uniq_artifact_names = set(artifact_names)

    # Get the number of matches (hits) for each path found
    filecounts = get_hits_per_artifact_name(artifact_names)

    grep_result = list()

    for art in uniq_artifact_names:
        artifact = db.get_artifacts_by_filter(
            conn, category=art[0], title=art[1])[0]
        if artifact:
            no_of_hits = filecounts[art]
            grep_result.append((artifact, no_of_hits))

    # Sort by number of hits, the largest -> the first
    grep_result.sort(key=lambda x: x[1], reverse=True)

    grep_artifacts = [r[0] for r in grep_result]
    grep_hits = [r[1] for r in grep_result]

    # Write to history file
    history.write(config["PATH_KB_HIST"], grep_artifacts)

    color_mode = not args["no_color"]
    if args["verbose"]:
        printer.print_grep_result_verbose(
            grep_artifacts, grep_hits, color_mode)
    else:
        printer.print_grep_result(grep_artifacts, grep_hits, color_mode)


def get_hits_per_artifact_name(artifact_name_list):
    """
    Get the dictionary related to the number of hits
    for each artifact name found.

    Arguments:
    artifact_name_list  - a list of tuples, where each
                        tuple is (category, title)
    Returns:
    A dictionary having as key the tuple (category,title)
    and as value the number of hits of that
    """
    namecounts = dict()
    for artname in artifact_name_list:
        if artname in namecounts:
            namecounts[artname] += 1
        else:
            namecounts[artname] = 1
    return namecounts
