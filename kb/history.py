# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb history module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import List
from kb.entities.artifact import Artifact
import kb.db as db


def get_artifact_id(hist_file_path: str, list_id: int) -> int:
    """
    Get the database ID related to an artifact based
    on the list ID (ID shown by kb list).
    This function is based on the history file path
    that is used to retrieve the correspondence between
    list ID and database artifact ID

    Arguments:
    hist_file_path      - the path to the history file,
                          this is generally in
                          $HOME/.kb/recent.hist
    list_id             - the ID shown by kb list

    Returns:
    The database ID corresponding to the artifact or
    None in case of non-valid list ID
    """
    with open(hist_file_path, 'r') as hfile:
        for line in hfile:
            items = line.split(",")
            if items[0] == list_id:
                return items[1]
        return None


def write(hist_file_path: str, search_result: List) -> None:
    """
    Write the kb history file with the results of
    a search/list operation.

    Arguments:
    hist_file_path      - the path to the history file,
                          this is generally in
                          $HOME/.kb/recent.hist
    search_result       - the results returned from
                          a DB query
    """
    with open(hist_file_path, "w") as hfile:
        hfile.write('view_id,db_id\n')
        for view_id, result in enumerate(search_result):
            hfile.write("{},{}\n".format(view_id, result.id))


def get_artifact(conn, hist_file_path: str, list_id: int) -> Artifact:
    """
    Get an artifact based on the list ID (ID shown by kb list).
    This function is based on the history file path
    that is used to retrieve the correspondence between
    list ID and database artifact ID

    Arguments:
    hist_file_path      - the path to the history file,
                          this is by default in
                          $HOME/.kb/recent.hist
    list_id             - the ID shown by kb list

    Returns:
    The artifact corresponding to list_id shown by kb list
    None in case of non-valid list ID
    """
    artifact_id = get_artifact_id(
        hist_file_path, list_id)

    return db.get_artifact_by_id(conn, artifact_id)
