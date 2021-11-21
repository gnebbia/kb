# -*- encoding: utf-8 -*-
# kb v0.1.6
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

# from sys import platform
from pathlib import Path

import toml

BASE_PATH = Path(
    os.environ.get("XDG_DATA_HOME", Path(Path.home(), ".local", "share")), "kb"
)


DEFAULT_CONFIG = {
    "PATH_KB": str(Path(BASE_PATH)),
    "PATH_KB_DB": str(Path(BASE_PATH, "kb.db")),
    "PATH_KB_HIST": str(Path(BASE_PATH, "recent.hist")),
    "PATH_KB_DATA": str(Path(BASE_PATH, "data")),
    "PATH_KB_GIT": str(Path(BASE_PATH, ".git")),
    # for future use
    "PATH_KB_CONFIG": str(Path(BASE_PATH, "kb.conf.py")),
    "PATH_KB_TEMPLATES": str(Path(BASE_PATH, "templates")),
    "PATH_KB_DEFAULT_TEMPLATE": str(Path(BASE_PATH, "templates", "default")),
    "PATH_KB_MARKDOWN_TEMPLATE": str(Path(BASE_PATH, "templates", "markdown")),
    "DB_SCHEMA_VERSION": 1,
    "EDITOR": os.environ.get("EDITOR", "vim"),
    "INITIAL_CATEGORIES": [
        "default",
    ],
}


DEFAULT_TEMPLATE = {
    "TITLES": ("^#.*", "blue"),
    "WARNINGS": ("^!.*", "yellow"),
}

MARKDOWN_TEMPLATE = {
    "MARKDOWN": "rich",
    "STYLE": "paraiso-dark",
    "JUSTIFY": "full",
    "HYPERLINKS": False,
    "PAGER": True,
    "PAGER_COLOR": True,
    "PADDING_VERTICAL": 0,
    "PADDING_HORIZONTAL": 4,
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
