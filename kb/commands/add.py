# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb add command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""
import sys
sys.path.append('kb')

import shlex
import sys
from pathlib import Path
from subprocess import call
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.filesystem as fs
from kb.entities.artifact import Artifact

from kb.actions.add import add_artifact
from kb.actions.add import add_file_to_kb as add_file_to_kb

import tempfile

def add(args: Dict[str, str], config: Dict[str, str]):
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
    # Check if the add command has proper arguments/options
    is_valid_add = args["file"] or args["title"]
    if not is_valid_add:
        print("Please, either specify a file or a title for the new artifact")
        sys.exit(1)

    # Check initialization
    initializer.init(config)

    conn = db.create_connection(config["PATH_KB_DB"])

    if args["file"]:
        for fname in args["file"]:
            if fs.is_directory(fname):
                continue
            add_file_to_kb(conn, args, config, fname)
    else:
        # Get title for the new artifact
        # title = args["title"]

        # Assign a "default" category if not provided
        # category = args["category"] or "default"

        # Create "category" directory if it does not exist
        # category_path = Path(config["PATH_KB_DATA"], category)
        # category_path.mkdir(parents=True, exist_ok=True)

        if not db.is_artifact_existing(conn, args["title"], args["category"]):
            # If a file is provided, copy the file to kb directory
            # otherwise open up the editor and create some content
            #artifact_path = str(Path(category_path, title))
            #if args["body"]:
            #    with open(artifact_path, "w+") as art_file:
            #        body = args["body"].replace("\\n", "\n")
            #        art_file.write(body)
            pass
        else:
            with tempfile.NamedTemporaryFile(delete=True) as f:
                shell_cmd = shlex.split(
                    config["EDITOR"]) + [f]
                call(shell_cmd)
                args["temp_file"] = f
                result = add_artifact(conn,args,config)
        return(result)