# -*- encoding: utf-8 -*-
# kb v0.1.2
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

    if args["id"]:
        for i in args["id"]:
            delete_by_id(i, config)

    elif args["title"]:
        delete_by_name(args["title"], args["category"], config)


def delete_by_id(id: int, config: Dict[str, str]):
    """
    Edit the content of an artifact by id.

    Arguments:
    id:             - the ID (the one you see with kb list)
                      associated to the artifact to delete
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    conn = db.create_connection(config["PATH_KB_DB"])
    artifact_id = history.get_artifact_id(config["PATH_KB_HIST"], id)
    artifact = db.get_artifact_by_id(conn, artifact_id)

    if not artifact:
        return

    db.delete_artifact_by_id(conn, artifact_id)

    category_path = Path(config["PATH_KB_DATA"], artifact.category)

    try:
        Path(category_path, artifact.title).unlink()
    except FileNotFoundError:
        pass

    if fs.count_files(category_path) == 0:
        fs.remove_directory(category_path)

    print("Artifact {category}/{title} removed!".format(
        category=artifact.category, title=artifact.title))


def delete_by_name(title: str, category: str, config: Dict[str, str]):
    """
    Edit the content of an artifact by name, that is title/category

    Arguments:
    title:          - the title assigned to the artifact to delete
    category:       - the category assigned to the artifact to delete
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    conn = db.create_connection(config["PATH_KB_DB"])
    artifacts = db.get_artifacts_by_filter(conn, title=title,
                                            category=category,
                                            is_strict=True)
    if len(artifacts) == 1:
        artifact = artifacts.pop()
        db.delete_artifact_by_id(conn, artifact.id)
        print("Artifact {}/{} removed!".format(artifact.category, artifact.title))
    elif len(artifacts) > 1:
        print(
            "There is more than one artifact with that title, please specify a category")
    else:
        print(
            "There is no artifact with that name, please specify a correct artifact name")
