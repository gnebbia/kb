# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for module for printers which don't fit anywhere else

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import os
from typing import List, Dict

from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_list(
        args: Dict[str, str],
        data: Dict[str, str],
        label: str):
    """
    Generates kb lists .

    Arguments:
    args            - a Dictionary string of arguments
    data            - a Dictionary string of data to be printed

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    label = "{label}".format(label=label.ljust(9))
    if not args["no_color"]:
        label = UND + BOLD + label + RESET

    print(label)
    print()
    for i in data:
        line = "{label}".format(label=i)
        if not args["no_color"]:
            label = BOLD + line + RESET
        print(line)
