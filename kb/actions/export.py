# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb export action module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import time
import tarfile
from typing import Dict

import sys
sys.path.append('kb')

from kb import __version__

def export_kb(args: Dict[str, str], config: Dict[str, str]):
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
    if args.get("only_data") == 'True':
        with tarfile.open(fname, mode='w:gz') as archive:
            archive.add(config["PATH_KB_DATA"], arcname="kb", recursive=True)
     
    else:
        # V1 format export
        # with tarfile.open(fname, mode='w:gz') as archive:
        #    archive.add(config["PATH_KB"], arcname=".kb",recursive=True)
        """
        V2 format export
        Place metadata in the export file so that the import function determine 
        whether this is in the original format for exprt files or the new multi-kb format
        """
        pax = { 'kb-export-format-version' : '2',
                'kb-version' : __version__ }
        with tarfile.open(fname, "w:gz",format=tarfile.PAX_FORMAT, pax_headers=pax) as archive:
            archive.add(config["PATH_KB"], arcname=".",recursive=True)
        
    return(fname)


               