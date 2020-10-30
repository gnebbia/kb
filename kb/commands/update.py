# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb edit command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import shlex
from subprocess import call
from typing import Dict
from pathlib import Path
import kb.db as db
import kb.initializer as initializer
import kb.history as history
import kb.filesystem as fs
from kb.entities.artifact import Artifact


def update(args: Dict[str, str], config: Dict[str, str]):
    """
    Update artifact properties within the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> a list of IDs (the ones you see with kb list)
                        associated to the artifact to update
                      title -> the title to be assigned to the artifact
                        to update
                      category -> the category to be assigned to the
                        artifact to update
                      tags -> the tags to be assigned to the artifact
                        to update
                      author -> the author to be assigned to the artifact
                        to update
                      status -> the status to be assigned to the artifact
                        to update
                      template -> the template to be assigned to the artifact
                        to update
                      edit_content -> a boolean, if True -> also open the
                        artifact to edit the content
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
        old_artifact = history.get_artifact(conn,
                                            config["PATH_KB_HIST"], args["id"])
        if not old_artifact:
            print("The artifact you are trying to update does not exist! "
                  "Please insert a valid ID...")
            return None
        response = update_artifact(old_artifact, args, config, attachment)
    # else if a title is specified
    elif args["title"]:
        artifact = db.get_uniq_artifact_by_filter(conn, title=args["title"],
                                                  category=args["category"],
                                                  author=args["author"],
                                                  status=args["status"],
                                                  is_strict=True)

        if artifact:
            category_path = Path(config["PATH_KB_DATA"], artifact.category)
        else:
            print(
                "There is none or more than one artifact with that title, please specify a category")

    if args["edit_content"] or args["body"]:
        if args["title"]:
            artifact_path = str(Path(category_path, artifact.title))
            shell_cmd = shlex.split(config["EDITOR"]) + [artifact_path]
        elif args["id"]:
            artifact_path = str(Path(config["PATH_KB_DATA"])
                                / old_artifact.category
                                / old_artifact.title)
            shell_cmd = shlex.split(config["EDITOR"]) + [artifact_path]

        if args["body"]:
            args["body"] = args["body"].replace("\\n", "\n")
            with open(artifact_path, 'w') as art_file:
                art_file.write(args["body"])
        else:
            call(shell_cmd)
