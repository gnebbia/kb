# -*- encoding: utf-8 -*-
# kb v0.1.2
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
            print("The artifact you are trying to update does not exist! "\
                   "Please insert a valid ID...")
            return None

        updated_artifact = Artifact(
            id=None,
            title=args["title"],
            category=args["category"],
            tags=args["tags"],
            author=args["author"],
            status=args["status"])

        db.update_artifact_by_id(conn, old_artifact.id, updated_artifact)
        # If either title or category has been changed, we must move the file
        if args["category"] or args["title"]:
            old_category_path = Path(
                config["PATH_KB_DATA"],
                old_artifact.category)
            new_category_path = Path(
                config["PATH_KB_DATA"],
                args["category"] or old_artifact.category)
            fs.create_directory(new_category_path)

            fs.move_file(Path(old_category_path, old_artifact.title), Path(
                new_category_path, args["title"] or old_artifact.title))
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
                "There is more than one artifact with that title, please specify a category")

    if args["edit_content"]:
        shell_cmd = shlex.split(config["EDITOR"]) + [Path(category_path, artifact.title)]
        call(shell_cmd)
