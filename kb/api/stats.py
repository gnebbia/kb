# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb stats api module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

from flask import make_response

from kb.actions.kbinfo import kb_stats
from kb.api.constants import MIME_TYPE


def stats(config: Dict[str, str]):
    """
    Get statistics about the database

    Argument:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
    """

    stats_content = kb_stats(config)
    resp = make_response(stats_content, 200)
    resp.mimetype = MIME_TYPE['json']
    return(resp)
