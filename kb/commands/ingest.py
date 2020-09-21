# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb import command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import tarfile
from pathlib import Path
from typing import Dict
import kb.filesystem as fs


def ingest(args: Dict[str, str], config: Dict[str, str]):
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
    if args["file"].endswith(".tar.gz"):
        answer = input("You are about to import a whole knowledge base "
                       "are you sure you want to wipe your previous "
                       " kb data ? [YES/NO]")
        if answer.lower() == "yes":
            print("Previous kb knowledge base data wiped...")
            try:
                fs.remove_directory(config["PATH_KB"])
            except FileNotFoundError:
                pass
            tar = tarfile.open(args["file"], "r:gz")
            tar.extractall(Path.home())
            tar.close()
            print("kb archive {fname} imported".format(fname=args["file"]))
    else:
        print("Please provide a file exported through kb with kb.tar.gz extension")
