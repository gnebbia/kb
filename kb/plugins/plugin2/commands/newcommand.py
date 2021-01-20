# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Example newcommand.py plugin template

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

"""
This module will contain the CLI interface to the actions


"""

from typing import Dict
from ..actions.newcommand import newcommand as nc

# Add/modify this to include your new plugin's functionality
def newcommand(args: Dict[str, str], config: Dict[str, str]): 
    results = nc(args, config)
    print(results)
    return 0
