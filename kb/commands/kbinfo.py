# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb stats command module

:Copyright: © 2020, alshaptons.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

from actions.kbinfo import kb_stats
from config import DEFAULT_CONFIG

def kbinfo():
    """
    Get statistics about the database

    Arguments:
    None

    """

    print(kb_stats(DEFAULT_CONFIG))
    #return(kb_stats(DEFAULT_CONFIG))

