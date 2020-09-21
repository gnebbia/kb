# -*- encoding: utf-8 -*-
# kb v0.1.2
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
    fname = args["file"] or time.strftime("%d_%m_%Y-%H%M%S")
    archive_ext = ".kb.tar.gz"
    if not fname.endswith(archive_ext):
        fname = fname + archive_ext

    if args["only_data"]:
        with tarfile.open(fname, mode='w:gz') as archive:
            archive.add(config["PATH_KB_DATA"], arcname="kb", recursive=True)
    else:
        with tarfile.open(fname, mode='w:gz') as archive:
            archive.add(config["PATH_KB"], arcname=".kb", recursive=True)
