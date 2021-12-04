# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb opener module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import os
import platform
import subprocess


def open_non_text_file(filename):
    """
    Open a non-text file
    """
    if platform.system() == "Darwin":
        subprocess.Popen(["open", filename])
    elif platform.system() == "Windows":
        os.startfile(filename)
    else:
        subprocess.Popen(["xdg-open", filename])
