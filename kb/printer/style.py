# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer style module for constants

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import List
import kb.styler as styler
from kb.entities.artifact import Artifact

ALT_BGROUND = styler.set_bg('#303030')
BOLD = styler.set_style('bold')
UND = styler.set_style('underlined')
RESET = styler.reset()
