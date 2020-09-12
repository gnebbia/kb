# -*- encoding: utf-8 -*-
# kb v0.1.0
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

    conn = db.create_connection(config["PATH_KB_DB"])

    if args["id"]:
        artifact_id = history.get_artifact_id(
            config["PATH_KB_HIST"], args["id"])

        artifact = db.get_artifact_by_id(conn, artifact_id)

        category_path = Path(config["PATH_KB_DATA"], artifact.category)
        artifact_path = Path(category_path, artifact.title)

        if args["editor"]:
            with tempfile.NamedTemporaryFile() as tmpfname:
                fs.copy_file(artifact_path, tmpfname.name)
                call([config["EDITOR"], tmpfname.name])
            sys.exit(0)

        # View File
        if fs.is_text_file(artifact_path):
            markers = get_markers(config["PATH_KB_MARKERS"])
            color_mode = not args["no_color"]
            viewer.view(artifact_path, markers, color=color_mode)
        else:
            opener.open_non_text_file(artifact_path)

    elif args["title"]:
        artifact = db.get_uniq_artifact_by_filter(conn, title=args["title"],
                                                  category=args["category"],
                                                  is_strict=True)
        if artifact:
            category_path = Path(config["PATH_KB_DATA"], artifact.category)
            artifact_path = Path(category_path, artifact.title)

            content = ""
            if args["editor"]:
                call([config["EDITOR"], artifact_path])
                sys.exit(0)

            # View File
            if fs.is_text_file(artifact_path):
                markers = get_markers(config["PATH_KB_MARKERS"])
                color_mode = not args["no_color"]
                viewer.view(artifact_path, markers, color=color_mode)
            else:
                opener.open_non_text_file(artifact_path)
        else:
            print(
                "There is no artifact with that title, please specify a category")
