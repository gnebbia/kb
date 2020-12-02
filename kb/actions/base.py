# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb base action module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import toml
from typing import Dict

from kb.actions.list import list_categories, list_tags, list_templates
from kb.api.constants import MIME_TYPE, API_VERSION
import kb.db as db
import kb.filesystem as fs
from kb import __version__

def base_list(config:Dict[str, str]):
    list_of_bases = []
    data = toml.load(config["PATH_KB_INITIAL_BASES"])
    for base in data["bases"]:
        base_info = dict()
        base_info['name'] = base['name']
        base_info['description'] = base['description']
        list_of_bases.append(base_info)
    print(list_of_bases)
    return (list_of_bases)

