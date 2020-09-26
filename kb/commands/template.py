# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb template command module

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


def template(args: Dict[str, str], config: Dict[str, str]):
    """
    Manage templates for kb

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
    is_valid_template = args["list"] or args["add"] or args["new"] or args["delete"] or args["edit"]
    if not is_valid_template:
        print("Please, specify a valid template command")
        sys.exit(1)

    # Check initialization
    initializer.init(config)

    if args["list"]:
        template_list = fs.list_files(config["PATH_KB_TEMPLATES"])
        print(template_list)
    elif args["new"]:
        template_name = input("Specify a name for the new template: ")
        
        if not template_name:
            sys.exit(1)

        print(template_name.split('/'))
        template_path = str(Path(*[config["PATH_KB_TEMPLATES"]] + template_name.split('/')))
        print(template_path)

        if fs.is_file(template_path):
            print("ERROR: The template you inserted corresponds to an existing one. "
                  "Please specify another name for the new template")
            sys.exit(1)

        fs.copy_file(config["PATH_KB_MARKERS"], template_path)

        shell_cmd = shlex.split(
            config["EDITOR"]) + [template_path]
        call(shell_cmd)

    elif args["add"]:
        template_path = args["add"]
        fs.copy_file(template_path, config["PATH_KB_TEMPLATES"])

    elif args["delete"]:
        template_name = args["delete"]
        fs.remove_file(Path(config["PATH_KB_TEMPLATES"], template_name))

    elif args["edit"]:
        template_name = args["edit"]
        template_path = str(Path(*[config["PATH_KB_TEMPLATES"]] + template_name.split('/')))

        shell_cmd = shlex.split(
            config["EDITOR"]) + [template_path]
        call(shell_cmd)

    else:
        print("Please specify a correct template command")


def add_template_to_kb(
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
    template = args["template"] or "default"

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
        status=args["status"], author=args["author"], template=template)
    db.insert_artifact(conn, new_artifact)
