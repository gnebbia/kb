# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb export command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import time
import tarfile
from pathlib import Path
from typing import Dict
from kb.actions.export import export_kb



def export(args: Dict[str, str], config: Dict[str, str]):
    """
    Export the entire kb knowledge base.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> a string representing the wished output
                        filename
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
    """
    fname=export_kb(args, config=config)

    return(fname)
    
