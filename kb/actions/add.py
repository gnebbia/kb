# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb add command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import shlex
import sys
from pathlib import Path
from subprocess import call
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.filesystem as fs
from kb.entities.artifact import Artifact

import os
from werkzeug.utils import secure_filename


def add_artifact(conn, args: Dict[str, str], config: Dict[str, str]):
    """
    Adds a list of artifacts to the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> a list of files to add to kb
                      title -> the title assigned to the artifact(s)
                      category -> the category assigned to the artifact(s)
                      tags -> the tags assigned to the artifact(s)
                      author -> the author to assign to the artifact
                      status -> the status to assign to the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      EDITOR            - the editor program to call
    """

    response = -404

    # Check initialization
    initializer.init(config)
    # Get title for the new artifact
    title = args["title"]

    # Assign a "default" category if not provided
    category = args["category"] or "default"

    # Create "category" directory if it does not exist
    category_path = Path(config["PATH_KB_DATA"], category)
    category_path.mkdir(parents=True, exist_ok=True)
    artifact_path = str(Path(category_path, title))

    if 'body' in args:
        with open(artifact_path, "w+") as art_file:
            body = args["body"].replace("\\n", "\n")
            art_file.write(body)

    if 'temp_file' in args:
        for fname in args["temp_file"]:
            os.rename(fname, artifact_path)
            add_file_to_kb(conn, args, config, artifact_path)

    if 'file' in args:
        for fname in args["file"]:
            if fs.is_directory(fname):
                continue
            add_file_to_kb(conn, args, config, fname)

    new_artifact = Artifact(
        id=None, title=title, category=category,
        path="{category}/{title}".format(category=category, title=title),
        tags=args["tags"],
        status=args["status"], author=args["author"])
    response = db.insert_artifact(conn, new_artifact)
    print(response)
    return(response)


def add_file_to_kb(
        conn,
        args: Dict[str, str],
        config: Dict[str, str],
        fname: str
) -> None:
    """
    Adds a file to the kb knowledge base.

    Arguments:
    conn        -   the connection to the database object
    args        -   the args dictionary passed to the add command,
                    it must contain at least the following keys:
                        title, category, tags, status, author
    config      -   the configuration dictionary that must contain
                    at least the following key:
                    PATH_KB_DATA, the path to where artifact are stored
    fname       -   the path of the file to add to kb
    """
    title = args["title"] or fs.get_basename(fname)
    category = args["category"] or "default"

    category_path = Path(config["PATH_KB_DATA"], category)
    category_path.mkdir(parents=True, exist_ok=True)

    fs.copy_file(fname, Path(category_path, title))

    if not db.is_artifact_existing(conn, title, category):
        fs.copy_file(fname, Path(category_path, title))

    new_artifact = Artifact(
        id=None,
        title=title, category=category,
        path="{category}/{title}".format(category=category, title=title),
        tags=args["tags"],
        status=args["status"], author=args["author"])
    db.insert_artifact(conn, new_artifact)
