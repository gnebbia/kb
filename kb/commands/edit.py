# -*- encoding: utf-8 -*-
# kb v0.1.0
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb edit command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import shlex
from pathlib import Path
from subprocess import call
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.history as history


def edit(args: Dict[str, str], config: Dict[str, str]):
    """
    Edit the content of an artifact.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> the IDs (the one you see with kb list)
                        associated to the artifact we want to edit
                      title -> the title assigned to the artifact(s)
                      category -> the category assigned to the artifact(s)
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    initializer.init(config)

    conn = db.create_connection(config["PATH_KB_DB"])
    # if an ID is specified, load artifact with that ID
    if args["id"]:
        artifact = history.get_artifact(
            conn, config["PATH_KB_HIST"], args["id"])

        category_path = Path(config["PATH_KB_DATA"], artifact.category)

        shell_cmd = shlex.split(config["EDITOR"]) + [Path(category_path, artifact.title)]
        call(shell_cmd)

    # else if a title is specified
    elif args["title"]:
        artifacts = db.get_artifacts_by_filter(conn, title=args["title"],
                                               category=args["category"],
                                               is_strict=True)

        if len(artifacts) == 1:
            artifact = artifacts.pop()
            category_path = Path(config["PATH_KB_DATA"], artifact.category)
            shell_cmd = shlex.split(config["EDITOR"]) + [Path(category_path, artifact.title)]
            call(shell_cmd)
        elif len(artifacts) > 1:
            print(
                "There is more than one artifact with that title, please specify a category")
        else:
            print(
                "There is no artifact with that name, please specify a correct artifact name")
