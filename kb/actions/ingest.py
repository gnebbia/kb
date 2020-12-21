# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb import action module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import tarfile
from pathlib import Path
from typing import Dict

import kb.filesystem as fs


def ingest_kb(args: Dict[str, str], config: Dict[str, str]):
    """
    Import an entire kb knowledge base.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> a string representing the path to the archive
                        to be imported
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
    """

    tar = tarfile.open(args["file"], "r:gz")
    tar.extractall(Path(config["PATH_KB"]))
    tar.close()

    return -200
