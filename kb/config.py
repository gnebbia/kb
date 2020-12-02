# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb config module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import os
from sys import platform
from pathlib import Path
import toml

# Home base for the user
BASE = Path.home()

# Insert directory with specific knowledgebase in (picked up from global options file)
KB_BASE = Path(BASE,".kb","home")


DEFAULT_CONFIG = {
    "PATH_BASE": str(Path(BASE, ".kb")),
    "PATH_KB": str(Path(KB_BASE)),
    "PATH_KB_DB": str(Path(KB_BASE, "kb.db")),
    "PATH_KB_HIST": str(Path(KB_BASE, "recent.hist")),
    "PATH_KB_DATA": str(Path(KB_BASE, "data")),
    "PATH_KB_CONFIG": str(Path(KB_BASE,  "kb.conf.py")),  # for future use
    "PATH_KB_TEMPLATES": str(Path(KB_BASE,  "templates")),
    "PATH_KB_DEFAULT_TEMPLATE": str(Path(KB_BASE, "templates", "default")),
    "PATH_KB_INITIAL_BASES": str(Path(BASE,".kb", "bases.toml")),
    "DB_SCHEMA_VERSION": 1,
    "EDITOR": os.environ.get("EDITOR", "vim"),
    "INITIAL_CATEGORIES": ["default", ]
}


DEFAULT_TEMPLATE = {
    "TITLES": ("^#.*", "blue"),
    "WARNINGS": ("^!.*", "yellow"),
}

INITIAL_KNOWLEDGEBASE = {
    'current':'default',
    'bases': [{'name': 'default', 'description': 'Default knowledgebase'},
    {'name': 'work', 'description': 'Work Stuff'}]
    }

def get_markers(markers_path: str):
    """
    Load markers file

    Arguments:
    markers_path    - the path to the toml markers file

    Returns a dictionary containing markers
    """
    try:
        return toml.load(markers_path)
    except toml.TomlDecodeError:
        print("Error: The provided file is not in the toml format")
    except FileNotFoundError:
        print("Error: The provided file does not exist or cannot be accessed")
