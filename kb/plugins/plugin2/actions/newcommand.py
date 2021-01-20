# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Example low-level actions newcommand.py plugin template

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

"""
This module will contain the main functions for the plugin.

It will be shared between the CLI and the API, so should not 
output anything to the screen, simply return data.

"""

from typing import Dict

# Add/modify this to include your new plugin's functionality
def newcommand(args: Dict[str, str], config: Dict[str, str]): 
    return "New Command"
