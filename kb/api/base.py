# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb base api module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

from flask import make_response

from kb.actions.base import base_list
from kb.api.constants import MIME_TYPE


def base(config: Dict[str, str]):
    """
    Get information about the available knowledge bases

    Argument:
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PAPATH_KB_INITIAL_BASESTH_KB - the main path of KB information
    """

    bases = base_list(config)
    resp = make_response(str(bases).replace("'",'"'), 200)    
    resp.mimetype = MIME_TYPE['json']
    return(resp)
