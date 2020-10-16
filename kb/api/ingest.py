# -*- encoding: utf-8 -*-
# kb v0.1.4
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb import command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""
import sys
sys.path.append('kb')

import tarfile
from pathlib import Path
from typing import Dict
import kb.filesystem as fs
from kb.actions.ingest import ingest_kb

import os
from werkzeug.utils import secure_filename

def ingest(file,args: Dict[str, str], config: Dict[str, str]):
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
    print (args["file"])
    if args["file"].endswith(".tar.gz"):
        filename = secure_filename(file.filename)
        home_path = Path(config["PATH_KB"]+'/')
        print("made dir")
        home_path.mkdir(parents=True, exist_ok=True)
        print("saving file")
        print (str(home_path))  
        print(filename)
        file.save(os.path.join(home_path, filename))
        print ("saved file")
        print (home_path)
        print (filename)
        args["file"] = str(home_path) + "/" + str(filename)
        print (args["file"])
        results = ingest_kb(args,config)
        if results == -200:
            return -200
    else:
        return -415