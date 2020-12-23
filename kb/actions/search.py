# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb search action module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict

import kb.db as db
import kb.initializer as initializer
import kb.actions.list as ls


def search_kb(args: Dict[str, str], config: Dict[str, str]):
    """
    Search artifacts within the knowledge base of kb.

    Arguments:
    args:           - a dictionary containing the following fields:
                      query -> filter for the title field of the artifact
                      category -> filter for the category field of the artifact
                      tags -> filter for the tags field of the artifact
                      author -> filter for the author field of the artifact
                      status -> filter for the status field of the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    # Check initialization
    initializer.init(config)


    conn = db.create_connection(config["PATH_KB_DB"])
    
    categories = ls.list_categories(config)
    print(categories)

    # List all categories
    if args.get("all_categories", False) is True:
        categories = ls.list_categories(config)
        return categories
    
    # List all categories
    if args.get("all_tags", False) is True:
        all_tags = ls.list_tags(conn, config)
        return all_tags

    tags_list = None
    if args.get("tags",False) is True:
        if args["tags"] and args["tags"] != "":
            tags_list = args["tags"].split(';')

    rows = db.get_artifacts_by_filter(
        conn,
        title=args.get("query",''),
        category=args.get("category",''),
        tags=tags_list,
        status=args.get("status",''),
        author=args.get("author",''))

    
    artifacts = sorted(rows, key=lambda x: x.title)
    return artifacts
