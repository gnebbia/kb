# -*- encoding: utf-8 -*-
# kb v0.1.0
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb delete command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import sys
from typing import Dict
from pathlib import Path
import kb.db as db
import kb.initializer as initializer
import kb.history as history
import kb.filesystem as fs


def delete(args: Dict[str, str], config: Dict[str, str]):
    """
    Delete a list of artifacts from the kb knowledge base.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> a list of IDs (the ones you see with kb list)
                        associated to the artifacts we want to delete
                      title -> the title assigned to the artifact(s)
                      category -> the category assigned to the artifact(s)
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
    """
    initializer.init(config)

    conn = db.create_connection(config["PATH_KB_DB"])

    if args["id"]:
        for i in args["id"]:
            artifact_id = history.get_artifact_id(config["PATH_KB_HIST"], i)
            artifact = db.get_artifact_by_id(conn, artifact_id)

            db.delete_artifact_by_id(conn, artifact_id)

            category_path = Path(config["PATH_KB_DATA"], artifact.category)

            Path(category_path, artifact.title).unlink()
            if fs.count_files(category_path) == 0:
                fs.remove_directory(category_path)

            print("Artifact {category}/{title} removed!".format(
                category=artifact.category, title=artifact.title))
        sys.exit(0)

    # else if a title is specified
    elif args["title"]:
        artifacts = db.get_artifacts_by_filter(conn, title=args["title"],
                                               category=args["category"],
                                               is_strict=True)
        if len(artifacts) == 1:
            artifact = artifacts.pop()
            db.delete_artifact_by_id(conn, artifact.id)
            print("Artifact {}/{} removed!".format(artifact.category, artifact.title))
        else:
            print(
                "There is more than one artifact with that title, please specify a category")
