# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb import api module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""
import sys
import os
import tarfile
from pathlib import Path
from typing import Dict

from werkzeug.utils import secure_filename

from flask import make_response

from kb.actions.ingest import ingest_kb
from kb.api.constants import MIME_TYPE
import kb.filesystem as fs


def ingest(f, args: Dict[str, str], config: Dict[str, str]):
    """
    Import an entire kb knowledge base.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> a string representing the path to the archive
                        to be imported
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
    """

    if f.filename.endswith(".tar.gz"):
        home_path = Path(config["PATH_KB"]+'/')
        home_path.mkdir(parents=True, exist_ok=True)
        f.save(os.path.join(home_path, f.filename))
        args["file"] = str(home_path) + "/" + str(f.filename)

        try:
            fs.remove_directory(config["PATH_KB_DATA"])
        except FileNotFoundError:
            pass
        try:
            fs.remove_directory(config["PATH_KB_TEMPLATES"])
        except FileNotFoundError:
            pass
        try:
            fs.remove_file(config["PATH_KB_DB"])
        except FileNotFoundError:
            pass
        try:
            fs.remove_file(config["PATH_KB_HIST"])
        except FileNotFoundError:
            pass
        try:
            fs.remove_file(config["PATH_KB_CONFIG"])
        except FileNotFoundError:
            pass

        results = ingest_kb(args, config)

        try:
            fs.remove_file(Path(args["file"]))
        except FileNotFoundError:
            pass

        if results == -200:
            response = make_response(({'Imported': f.filename}), 200)
            response.mimetype = MIME_TYPE['json']
            return response
    else:
        response = make_response(({'Error': f.filename + " is not a valid kb export file."}), 415)
        response.mimetype = MIME_TYPE['json']
        return response
