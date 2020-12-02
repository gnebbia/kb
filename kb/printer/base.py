# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for base command module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import os
from typing import List
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_bases_output(
        bases: str,
        color: bool = True):
    """
    Generates kb base results header.

    Arguments:
    stats           - a Dictionary string of knowledgebase info
    color           - a boolean, True if color is enabled

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    header = "{name}           {description}".format(
        name='Name',
        description='Description')

    if color:
        header = UND + BOLD + header + RESET
    print(header)

    for base in bases:
        summary = "{name}          {description}".format(
            kb_version=base["name"].ljust(20),
            api_version=base["name"].ljust(40))
        if color:
            summary = UND + BOLD + summary + RESET
        print(summary)
        
