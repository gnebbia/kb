# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb update api module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
from pathlib import Path

from kb.actions.update import update_artifact
import kb.db as db
from kb.db import get_artifact_by_id
from kb.entities.artifact import Artifact
import kb.filesystem as fs
import kb.initializer as initializer


# Use the flask make_response function
from flask import make_response


def update(args: Dict[str, str], config: Dict[str, str], attachment):
    """
    Update artifact properties within the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      id -> an id of an artifact - note - the ACTUAL db_id
                      title -> the title to be assigned to the artifact
                        to update
                      category -> the category to be assigned to the
                        artifact to update
                      tags -> the tags to be assigned to the artifact
                        to update
                      author -> the author to be assigned to the artifact
                        to update
                      status -> the status to be assigned to the artifact
                        to update
                      template -> the template to be assigned to the artifact
                        to update
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
    attachment:     - new file content
"""
    initializer.init(config)

    template_name = args.get("template", "")
    if template_name != "":
        templates_path = Path(config["PATH_KB_TEMPLATES"])
        template_path = str(Path(config["PATH_KB_TEMPLATES"]) / args["title"])
        if not fs.is_file(template_path):
            resp_content = '{"Error":"' + "Named template does not exist" + '"}'
            resp = make_response((resp_content), 404)
            resp.mimetype = 'application/json'
            return(resp)

    conn = db.create_connection(config["PATH_KB_DB"])
    # if an ID is specified, load artifact with that ID
    if args["id"]:
        id = args["id"]
        old_artifact = get_artifact_by_id(conn, id)
        if old_artifact is None:
            resp = make_response(({'Error': 'The artifact does not exist'}), 404)
            resp.mimetype = 'application/json'
            return(resp)
            response = update_artifact(conn, old_artifact, args, config, attachment)
            if resp == -200:
                resp = make_response(({'Updated': id}), 200)
                resp.mimetype = 'application/json'
            else:
                resp = make_response(({'Error': id + " artifact not updated"}), 400)
                resp.mimetype = 'application/json'

    return(resp)
