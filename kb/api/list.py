# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb list api module

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
import kb.actions.list as ls
from kb.api.constants import MIME_TYPE
import kb.db as db
import kb.filesystem as fs


def list_cats(config: Dict[str, str]):
    """
    List the categories.

    Arguments:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DATA           - the main path of the DATA
    """

    categories = ls.list_categories(config)
    response = make_response(({'Categories': categories}), 200)
    response.mimetype = MIME_TYPE['json']
    print(response)
    return response


def list_all_tags(config: Dict[str, str]):
    """
    List the tags.

    Arguments:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DATA           - the main path of the DATA
    """
    conn = db.create_connection(config["PATH_KB_DB"])
    tags = ls.list_tags(conn, config)
    response = make_response(({'Tags': tags}), 200)
    response.mimetype = MIME_TYPE['json']
    return response
