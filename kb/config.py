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
from pathlib import Path
from sys import platform

import toml


def seed_default_knowledge_base():
    """
    Set name for default knowledge base

    Returns a string containing the default knowledge base
    """
    return ('default')


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


def get_current_base(BASE: Path):
    """
    Get current base knowledgebase file

    Arguments:
    BASE      - the path to the toml bases.toml file

    Returns name of the current KB (or "seed_default_knowledge_base()")
    """
    bases_config = str(Path(BASE,".kb", "bases.toml"))
    try:
        bases_data = toml.load(bases_config)
        current_base = bases_data['current']
        return current_base
    except toml.TomlDecodeError:
        print("Error: The bases file is not in the toml format")
    except FileNotFoundError:
        return(seed_default_knowledge_base())


def construct_config(BASE: Path, current: str):
    """
    Assemble the configuration file

    Arguments:
    BASE      - the path to the toml bases.toml file

    Returns DEFAULT_CONFIG with correct values.
    """
    if current == '':
        this_base = get_current_base(BASE)    
    else:
        this_base = current

    KB_BASE = Path(BASE,".kb",this_base)

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
    return DEFAULT_CONFIG

# Home base for the user
BASE = Path.home()

# Get configuration
DEFAULT_CONFIG = construct_config(BASE,'')

# Initial values for default template
DEFAULT_TEMPLATE = {
    "TITLES": ("^#.*", "blue"),
    "WARNINGS": ("^!.*", "yellow"),
}

# Default knowledge base name
DEFAULT_KNOWLEDGEBASE = seed_default_knowledge_base()

# Initial data for multi-knowledge base file
INITIAL_KNOWLEDGEBASE = {
    'current':DEFAULT_KNOWLEDGEBASE,
    'bases': [{'name': DEFAULT_KNOWLEDGEBASE, 'description': 'Default knowledgebase'}]
    }
