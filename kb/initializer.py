# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb initializer module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import os
from pathlib import Path
import toml
import kb.db as db
import kb.filesystem as fs
import kb.config as conf


def init(config):
    """
    Initialize kb with the provided configuration.

    Arguments:
    config  - a dictionary containing the following keys:
                PATH_KB                 - the path to kb
                                            (~/.kb by default)
                PATH_KB_DB              - the path to kb database
                                            (~/.kb/kb.db by default)
                PATH_KB_DATA            - the path to kb data
                                            (~/.kb/data/ by default)
                PATH_KB_DEFAULT_TEMPLATE - the path to kb markers
                                            (~/.kb/templates/default by default)
    """
    if not is_initialized(config):
        create_kb_files(config)


def create_kb_files(config):
    """
    Create the kb files and infrastructure

    Arguments:
    config  - a dictionary containing the following keys:
                PATH_KB                   - the path to kb
                                            (~/.kb by default)
                PATH_KB_DB                - the path to kb database
                                            (~/.kb/kb.db by default)
                PATH_KB_DATA              - the path to kb data
                                            (~/.kb/data/ by default)
                INITIAL_CATEGORIES        - a list containing the initial
                                            categories contained within kb
                PATH_KB_TEMPLATES         - the path to kb templates
                                            (~/.kb/templates/ by default)
                DB_SCHEMA_VERSION         - the database schema version
    """
    # Get paths for kb from configuration
    kb_path = config["PATH_KB"]
    db_path = config["PATH_KB_DB"]
    data_path = config["PATH_KB_DATA"]
    initial_categs = config["INITIAL_CATEGORIES"]
    templates_path = config["PATH_KB_TEMPLATES"]
    schema_version = config["DB_SCHEMA_VERSION"]
    default_template_path = str(Path(templates_path) / "default")

    # Create main kb
    fs.create_directory(kb_path)

    # Create kb database
    if not os.path.exists(db_path):
        db.create_kb_database(db_path, schema_version)

    # Check schema version
    conn = db.create_connection(db_path)
    current_schema_version = db.get_schema_version(conn)

    if current_schema_version == 0:
        db.migrate_v0_to_v1(conn)

    # Create "data" directory
    fs.create_directory(data_path)

    # Create "templates" directory
    fs.create_directory(templates_path)

    # Create kb initial categories directories
    for category in initial_categs:
        category_path = Path(data_path, category)
        fs.create_directory(category_path)

    # Create markers file
    with open(default_template_path, "w") as cfg:
        cfg.write(toml.dumps(conf.DEFAULT_TEMPLATE))


def is_initialized(config) -> bool:
    """
    Check if kb is correctly initialized,
    ensure that:
    1 - the .kb directory exists
    2 - the kb database exists
    3 - the kb data directory exists

    Arguments:
    config  - a dictionary containing the following keys:
                PATH_KB         - the path to kb
                                    (~/.kb by default)
                PATH_KB_DB      - the path to kb
                                    (~/.kb/kb.db by default)
                PATH_KB_DATA    - the path to kb
                                    (~/.kb/data/ by default)
    Returns:
    True is kb is correctly initialized, False otherwise
    """
    kb_path = config["PATH_KB"]
    db_path = config["PATH_KB_DB"]
    data_path = config["PATH_KB_DATA"]
    templates_path = config["PATH_KB_TEMPLATES"]

    for path in [kb_path, db_path, data_path, templates_path]:
        if not os.path.exists(path):
            return False

    conn = db.create_connection(db_path)
    return db.is_schema_updated_to_version(conn, config["DB_SCHEMA_VERSION"])
