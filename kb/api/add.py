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


from pathlib import Path
from typing import Dict
from kb.entities.artifact import Artifact
import kb.actions.add as actions

# Get the configuration for the knowledgebase
from kb.config import DEFAULT_CONFIG

# Use the flask framework
from flask import jsonify

import os
from werkzeug.utils import secure_filename
#import urllib.request


def addArtifact(args: Dict[str, str],file,config: Dict[str, str]):
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

    if file :
        # Create "category" directory if it does not exist
        category_path = Path(DEFAULT_CONFIG["PATH_KB_DATA"], args["category"])
        category_path.mkdir(parents=True, exist_ok=True)

        # Get the filename
        filename = secure_filename(file.filename)
        category_path = Path(DEFAULT_CONFIG["PATH_KB_DATA"], args["category"])
        file.save(os.path.join(category_path, filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        
    result = actions.add(args,config=DEFAULT_CONFIG)
    return (result)

