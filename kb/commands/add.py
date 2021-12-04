# -*- encoding: utf-8 -*-
# kb v0.1.6
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
import kb.filesystem as fs
import kb.initializer as initializer
from kb.entities.artifact import Artifact


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
                print("Error:", fname, "is a directory, ignored.")
                continue
            add_file_to_kb(conn, args, config, fname)
    else:
        # Get title for the new artifact
        title = args["title"]

        # Assign a "default" category if not provided
        category = args["category"] or "default"

        # Create "category" directory if it does not exist
        category_path = Path(config["PATH_KB_DATA"], category)
        category_path.mkdir(parents=True, exist_ok=True)

        is_stdin_empty = sys.stdin.isatty()

        if not db.is_artifact_existing(conn, title, category):
            # If a file is provided, copy the file to kb directory
            # otherwise open up the editor and create some content
            artifact_path = str(Path(category_path, title))
            if args["body"]:
                with open(artifact_path, "w+") as art_file:
                    body = args["body"].replace("\\n", "\n")
                    art_file.write(body)
            elif not is_stdin_empty:
                with open(artifact_path, "w+") as art_file:
                    body_lines = sys.stdin.readlines()
                    art_file.writelines(body_lines)
            else:
                shell_cmd = shlex.split(config["EDITOR"]) + [artifact_path]
                call(shell_cmd)

        new_artifact = Artifact(
            id=None,
            title=title,
            category=category,
            path="{category}/{title}".format(category=category, title=title),
            tags=args["tags"],
            status=args["status"],
            author=args["author"],
            template=args["template"],
        )
        db.insert_artifact(conn, new_artifact)


def validate(args):
    """
    Validate arguments for the add command

    Arguments:
    args        - the dictionary of arguments
                  passed to the add command

    Returns:
    A boolean, True if the add command is valid
    """
    return bool(args["file"] or args["title"])


def add_file_to_kb(
    conn, args: Dict[str, str], config: Dict[str, str], fname: str
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
    # Title
    title = args["title"] or fs.get_basename(fname)
    dest_fname = (
        title  # enable artifact to have a title different from the corresponding file
    )

    # Template
    if args["template"]:
        template = args["template"]
    elif fs.is_md_file(fname):
        template = "markdown"
        if args["title"] is None:
            title = Path(fname).stem
    else:
        template = "default"

    # Category
    category = args["category"] or "default"
    category_path = Path(config["PATH_KB_DATA"], category)
    category_path.mkdir(parents=True, exist_ok=True)

    # Copy

    if db.is_artifact_existing(conn, title, category):
        print(
            "Error: The specified artifact {title} already exist!".format(title=title)
        )
        sys.exit(1)

    if fs.is_file(Path(category_path, dest_fname)):
        print(
            "Error: The destination file {dest_fname} already exist!".format(
                dest_fname=dest_fname
            )
        )
        sys.exit(1)

    try:
        fs.copy_file(fname, Path(category_path, dest_fname))
    except FileNotFoundError:
        print("Error: The specified file {fname} does not exist!".format(fname=fname))
        sys.exit(1)

    # ???
    # if not db.is_artifact_existing(conn, title, category):
    #     fs.copy_file(fname, Path(category_path, title))

    new_artifact = Artifact(
        id=None,
        title=title,
        category=category,
        path="{category}/{title}".format(category=category, title=title),
        tags=args["tags"],
        status=args["status"],
        author=args["author"],
        template=template,
    )
    db.insert_artifact(conn, new_artifact)
