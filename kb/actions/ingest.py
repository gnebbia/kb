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
    t = tar.getmembers()[0]       # GET TAR METADATA STORED IN PAX HEADERS
    tar.extractall(Path(config["PATH_KB"]))
    tar.close()

    """
    Version 1 (pre 0.1.6 multi kb version) export files don't contain any metadata. 
    This means that the original export files assume that the destination is ".kb"
    
    This will not work in post 0.1.6. Therefore, they need to be moved to fit in with 
    this schema.
    
    For 0.1.6 and above exports, a simple untar will work.

    NOTE THAT THE EXPORTS ARE NOT BACKWARDLY COMPATIBLE.

    """

    if t.pax_headers.get('kb-export-format-version','1') == '1':
          # Version 1 import file detected
          kb_path_base = kb_path_base = config["PATH_KB"]

          # Move data, templates and db into newly created directory (and optionally recent.hist)
          fs.move_file(str(Path(kb_path_base,'.kb','data')),str(Path(kb_path_base,'data')))
          fs.move_file(str(Path(kb_path_base,'.kb','templates')),str(Path(kb_path_base,'templates')))
          fs.move_file(str(Path(kb_path_base,'.kb','kb.db')),str(Path(kb_path_base,'kb.db')))
          fs.move_file(str(Path(kb_path_base,'.kb','recent.hist')),str(Path(kb_path_base,'recent.hist')))
          fs.remove_directory(str(Path(kb_path_base,'.kb')))

    else:
          # Version 2 import file detected
          pass

    return -200
