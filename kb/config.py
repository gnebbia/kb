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

DEFAULT_CONFIG = {
    "PATH_KB": str(Path(Path.home(), ".kb")),
    "PATH_KB_DB": str(Path(Path.home(), ".kb", "kb.db")),
    "PATH_KB_HIST": str(Path(Path.home(), ".kb", "recent.hist")),
    "PATH_KB_DATA": str(Path(Path.home(), ".kb", "data")),
    "PATH_KB_GIT": str(Path(Path.home(), ".kb", ".git")),
    "PATH_KB_CONFIG": str(Path(Path.home(), ".kb", "kb.conf.py")),  # for future use
    "PATH_KB_TEMPLATES": str(Path(Path.home(), ".kb", "templates")),
    "PATH_KB_DEFAULT_TEMPLATE": str(Path(Path.home(), ".kb", "templates", "default")),
    "DB_SCHEMA_VERSION": 1,
    "EDITOR": os.environ.get("EDITOR", "vim"),
    "INITIAL_CATEGORIES": ["default",]
}


DEFAULT_TEMPLATE = {
    "TITLES": ("^#.*", "blue"),
    "WARNINGS": ("^!.*", "yellow"),
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
