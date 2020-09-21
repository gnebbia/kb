# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb view command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import os
import platform
import sys
import shlex
import tempfile
from subprocess import call
from pathlib import Path
from typing import Dict
import kb.db as db
import kb.filesystem as fs
import kb.history as history
import kb.initializer as initializer
import kb.opener as opener
import kb.viewer as viewer
from kb.config import get_markers


def view(args: Dict[str, str], config: Dict[str, str]):
    """
    View an artifact contained in the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> the IDs (the one you see with kb list)
                        associated to the artifact to view
                      title -> the title of the artifact to view
                      category -> the category of the artifact to view
                      editor -> a boolean, if True the file will
                        be opened in a text editor as a temporary file
                        hence the original will not be affected
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      PATH_KB_MARKERS   - the file associated to the markers
                      EDITOR            - the editor program to call
    """
    # Check initialization
    initializer.init(config)


    color_mode = not args["no_color"]
    if args["id"]:
        view_by_id(args["id"], config, args["editor"], color_mode)
    elif args["title"]:
        view_by_name(args["title"], args["category"], config, args["editor"], color_mode)


def view_by_id(id: int, config: Dict[str, str], open_editor: bool, color_mode: bool):
    """
    View the content of an artifact by id.

    Arguments:
    id:             - the ID (the one you see with kb list)
                      associated to the artifact we want to edit
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    open_editor     - a boolean, if True it will open the artifact as
                      a temporary copy in editor
    color_mode      - a boolean, if True the colors on screen will be
                      enabled when printed on stdout
    """
    conn = db.create_connection(config["PATH_KB_DB"])
    artifact_id = history.get_artifact_id(
        config["PATH_KB_HIST"], id)

    artifact = db.get_artifact_by_id(conn, artifact_id)

    if not artifact:
        sys.exit(1)

    category_path = Path(config["PATH_KB_DATA"], artifact.category)
    artifact_path = Path(category_path, artifact.title)

    if open_editor:
        with tempfile.NamedTemporaryFile() as tmpfname:
            fs.copy_file(artifact_path, tmpfname.name)

            shell_cmd = shlex.split(config["EDITOR"]) + [tmpfname.name]
            call(shell_cmd)

        sys.exit(0)

    # View File
    if fs.is_text_file(artifact_path):
        markers = get_markers(config["PATH_KB_MARKERS"])
        viewer.view(artifact_path, markers, color=color_mode)
    else:
        opener.open_non_text_file(artifact_path)


def view_by_name(title: str, category: str, config: Dict[str, str], open_editor: bool, color_mode: bool):
    """
    View the content of an artifact by name, that is title/category

    Arguments:
    title:          - the title assigned to the artifact(s)
    category:       - the category assigned to the artifact(s)
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    open_editor     - a boolean, if True it will open the artifact as
                      a temporary copy in editor
    color_mode      - a boolean, if True the colors on screen will be
                      enabled when printed on stdout
    """
    conn = db.create_connection(config["PATH_KB_DB"])
    artifacts = db.get_artifacts_by_filter(conn, title=title,
                                                category=category,
                                                is_strict=True)
    if len(artifacts) == 1:
        artifact = artifacts.pop()
        category_path = Path(config["PATH_KB_DATA"], artifact.category)
        artifact_path = Path(category_path, artifact.title)

        if open_editor:
            with tempfile.NamedTemporaryFile() as tmpfname:
                fs.copy_file(artifact_path, tmpfname.name)

                shell_cmd = shlex.split(config["EDITOR"]) + [tmpfname.name]
                call(shell_cmd)
            sys.exit(0)

        # View File
        if fs.is_text_file(artifact_path):
            markers = get_markers(config["PATH_KB_MARKERS"])
            viewer.view(artifact_path, markers, color=color_mode)
        else:
            opener.open_non_text_file(artifact_path)
    elif len(artifacts) > 1:
        print(
            "There is more than one artifact with that title, please specify a category")
    else:
        print(
            "There is no artifact with that name, please specify a correct artifact name")
