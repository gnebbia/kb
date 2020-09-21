# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb database module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import sqlite3
from pathlib import Path
from typing import List, Optional
import attr

from kb.entities.artifact import Artifact

DB_CREATE_QUERY = """CREATE TABLE IF NOT EXISTS artifacts (
                         id integer PRIMARY KEY,
                         title text NOT NULL,
                         category text NOT NULL,
                         path text NOT NULL,
                         tags text,
                         status text,
                         author text);
                     CREATE TABLE IF NOT EXISTS tags (
                         artifact_id integer,
                         tag text,
                         FOREIGN KEY(artifact_id)
                           REFERENCES artifacts(id)
                           ON DELETE CASCADE);
                  """


def create_connection(db_file: str):
    """
    Create a database connection to the SQLite database
    specified by db_file

    Arguments:
    db_file         -  database file

    Returns:
    An sqlite3 connection object or None in case of error
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as err:
        print("Connection Failed: {error}".format(error=err))

    return conn


def create_table(conn, create_table_sql: str) -> None:
    """
    Create a table from the create_table_sql statement
    or show an error message in case of failure

    Arguments:
    conn              - Connection object
    create_table_sql  - A 'CREATE TABLE' statement
    """
    try:
        cursor = conn.cursor()
        cursor.executescript(create_table_sql)
    except Exception as err:
        print("Table Creation Failed: {error}".format(error=err))


def create_kb_database(kb_db_path: str) -> None:
    """
    Create an empty sqlite database for kb
    at the specified path or return an error
    if the creation is not possible

    Arguments:
    kb_db_path      - the path where the kb database will be stored
    """
    conn = create_connection(kb_db_path)

    if conn is not None:
        create_table(conn, DB_CREATE_QUERY)
    else:
        print("Error! cannot create the database connection.")


def is_artifact_existing(conn, title: str, category: str) -> bool:
    """
    Checks if an artifact with the provided title and category
    already exists in the database

    Arguments:
    conn            - the sqlite3 connection object
    title           - the title of the artifact
    category        - the category of the artifact

    Returns:
    True if the artifact already exists in the database,
    otherwise False
    """
    cur = conn.cursor()
    cur.execute("""SELECT title,category
                   FROM artifacts
                   WHERE title=? AND category=?""", [title, category])

    result = cur.fetchone()
    return result is not None


def insert_artifact(conn, artifact: Artifact) -> None:
    """
    Inserts in the database the provided artifact

    Arguments:
    conn            - An sqlite connection object representing
                      the database on which data will be inserted
    artifact        - an artifact object

    Returns:
    Returns an error if there was a failure in the insertion operation
    """
    # Convert tags to a string with ';' separating tags
    tags_list = []
    if artifact.tags:
        tags_list = list(set(artifact.tags.split(';')))

    path = ""
    if artifact.path:
        path = artifact.path
    else:
        path = str(Path(artifact.category, artifact.title))

    cur = conn.cursor()
    if is_artifact_existing(conn, artifact.title, artifact.category):
        print("Error: the specified artifact already exists in kb!")
        print("Run `kb update -h` to understand how to update an artifact")
        return

    sql = '''INSERT INTO artifacts
             (title,category,path,tags,author,status)
             VALUES(?,?,?,?,?,?)'''
    args = (artifact.title, artifact.category,
            path, artifact.tags, artifact.author, artifact.status)

    cur.execute(sql, args)
    last_artifact_id = cur.lastrowid

    for tag in tags_list:
        sql = '''INSERT INTO tags
                 (artifact_id,tag)
                 VALUES(?,?)'''
        args = (last_artifact_id, tag)
        cur.execute(sql, args)

    conn.commit()


def delete_artifact_by_id(conn, artifact_id: int) -> None:
    """
    Deletes the artifact corresponding to the provided
    artifact ID

    Arguments:
    conn                - the sqlite3 connection object
    artifact_id         - the ID associated to the artifact to remove
    """
    cur = conn.cursor()
    sql_query = "DELETE FROM artifacts WHERE id = ?"

    cur.execute(sql_query, [artifact_id])
    conn.commit()


def delete_artifact_by_name(conn, title: str, category: str) -> None:
    """
    Deletes the artifact corresponding to the provided
    artifact name, that is title and category

    Arguments:
    conn                - the sqlite3 connection object
    artifact_id         - the ID associated to the artifact to remove
    """
    cur = conn.cursor()
    sql_query = "DELETE FROM artifacts WHERE title = ? AND category = ?"

    cur.execute(sql_query, [title, category])
    conn.commit()


def get_artifact_by_id(conn, artifact_id: int) -> Artifact:
    """
    Get the artifact corresponding to the provided
    artifact ID

    Arguments:
    conn                - the sqlite3 connection object
    artifact_id         - the ID associated to the artifact to retrieve
    """
    cur = conn.cursor()
    sql_query = "SELECT * FROM artifacts WHERE id = ?"
    cur.execute(sql_query, [artifact_id])

    result = cur.fetchone()
    if result:
        return Artifact(*result)


def get_artifacts_by_filter(
        conn,
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None,
        status: Optional[str] = None,
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts by applying a generic filter
    on title, category and tags.

    Arguments:
    conn                - the sqlite3 Connection object
    title               - the title string to match in the database
    category            - the category string to match in the database
    tags                - the tag list to match in the database
    author              - the author to match
    status              - the status to match
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a list of the artifacts matching the provided filter that
    has been found
    """
    artifact_id_list = list()

    if title is not None:
        artifacts_by_title = get_artifacts_by_title(
            conn, query_string=title, is_strict=is_strict)
        artifact_id_list.append({art.id for art in artifacts_by_title})
    if category is not None:
        artifacts_by_cat = get_artifacts_by_category(
            conn, query_string=category, is_strict=is_strict)
        artifact_id_list.append({art.id for art in artifacts_by_cat})
    if tags:
        artifacts_by_tags = get_artifacts_by_tags(
            conn, tags=tags, is_strict=is_strict)
        artifact_id_list.append({art.id for art in artifacts_by_tags})
    if author:
        artifacts_by_author = get_artifacts_by_author(
            conn, query_string=author, is_strict=is_strict)
        artifact_id_list.append({art.id for art in artifacts_by_author})
    if status:
        artifacts_by_status = get_artifacts_by_status(
            conn, query_string=status, is_strict=is_strict)
        artifact_id_list.append({art.id for art in artifacts_by_status})

    if len(artifact_id_list) == 0:
        return None

    # Perform an intersection on collected artifact IDs
    resulting_set = artifact_id_list.pop()
    for art_id in artifact_id_list:
        resulting_set.intersection_update(art_id)

    artifacts = []
    for result_id in resulting_set:
        artifacts.append(get_artifact_by_id(conn, result_id))

    return artifacts


def get_artifacts_by_title(
        conn,
        query_string: str = "",
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts matching the string to search,
    if the string is empty, it will retrieve all artifacts

    Arguments:
    conn                - the sqlite3 Connection object
    query_string        - the string to match in the database
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a list of the artifacts matching the provided string that
    have been found
    """
    if not is_strict:
        query_string = "%" + query_string + "%"
    cur = conn.cursor()
    sql_query = """
                SELECT *
                FROM artifacts
                WHERE title LIKE ?
                COLLATE NOCASE
                """
    cur.execute(sql_query, [query_string])
    artifacts = [Artifact(*row) for row in cur.fetchall()]
    return artifacts


def get_uniq_artifact_by_filter(
        conn,
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None,
        status: Optional[str] = None,
        is_strict: bool = False
) -> Artifact:
    """
    Get the artifact with the specified query string
    if the result is unique or None otherwise

    Arguments:
    conn                - the sqlite3 Connection object
    title               - the title string to match in the database
    category            - the category string to match in the database
    tags                - the tag list to match in the database
    author              - the author to match
    status              - the status to match
    is_strict           - if True, the pattern matching is
                          on exact strings
    Returns:
    This function can return either:
    - the Artifact object matching the string to search, if the
      result is unique
    - None if there is more than one artifact matching the
    query string or no artifact matched at all
    """
    artifacts = get_artifacts_by_filter(conn, title=title,
                                        category=category,
                                        tags=tags,
                                        author=author,
                                        status=status,
                                        is_strict=is_strict)
    if len(artifacts) == 1:
        return artifacts.pop()


def get_artifacts_by_status(
        conn,
        query_string: str = "",
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts matching the status string provided,
    if the string is empty, it will retrieve all artifacts

    Arguments:
    conn                - the sqlite3 Connection object
    query_string        - the status string to match in the database
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a list of the artifacts matching the provided status string that
    have been found
    """
    if not is_strict:
        query_string = "%" + query_string + "%"
    cur = conn.cursor()
    sql_query = """
                SELECT *
                FROM artifacts
                WHERE status LIKE ?
                COLLATE NOCASE
                """
    cur.execute(sql_query, [query_string])

    artifacts = [Artifact(*row) for row in cur.fetchall()]
    return artifacts


def get_artifacts_by_author(
        conn,
        query_string: str = "",
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts matching the string to search,
    if the string is empty, it will retrieve all artifacts

    Arguments:
    conn                - the sqlite3 Connection object
    query_string        - the author string to match in the database
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a set of the artifacts matching the provided author that
    have been found
    """
    if not is_strict:
        query_string = "%" + query_string + "%"
    cur = conn.cursor()
    sql_query = """
                SELECT *
                FROM artifacts
                WHERE author LIKE ?
                COLLATE NOCASE
                """
    cur.execute(sql_query, [query_string])
    artifacts = [Artifact(*row) for row in cur.fetchall()]
    return artifacts


def get_artifacts_by_category(
        conn,
        query_string: str = "",
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts of the category matching the string to search,
    if the string is empty, it will retrieve all artifacts

    Arguments:
    conn                - the sqlite3 Connection object
    query_string        - the string to match in the database
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a set of the artifacts matching the provided string that
    have been found
    """
    if not is_strict:
        query_string = "%" + query_string + "%"

    sql_query = """SELECT *
                   FROM artifacts
                   WHERE category LIKE ?
                   COLLATE NOCASE"""

    cur = conn.cursor()
    cur.execute(sql_query, [query_string])

    artifacts = [Artifact(*row) for row in cur.fetchall()]
    return artifacts


def get_artifacts_by_tags(
        conn,
        tags: List[str] = [],
        is_strict: bool = False
) -> List[Artifact]:
    """
    Returns artifacts matching the provided list of tags,
    if no tags are provided, it will retrieve all artifacts

    Arguments:
    conn                - the sqlite3 Connection object
    query_string        - the list of tags (strings) provided
    is_strict           - if True, the pattern matching is
                          on exact strings

    Returns:
    a list of the found artifacts matching the provided tags
    """
    rows = list()
    if not is_strict:
        tags = ["%" + tag + "%" for tag in tags]

    cur = conn.cursor()
    for tag in tags:
        sql_query = """
                    SELECT *
                    FROM artifacts INNER JOIN tags ON tags.artifact_id = artifacts.id
                    WHERE tag LIKE ?
                    COLLATE NOCASE
                    """
        cur.execute(sql_query, [tag])
        rows += cur.fetchall()

    # We discard the last two fields in result rows
    # since we are only interested in artifact data
    rows = [r[:-2] for r in list(set(rows))]

    artifacts = [Artifact(*row) for row in rows]
    return artifacts


def update_artifact_by_id(
        conn,
        artifact_id: int,
        artifact: Artifact
) -> None:
    """
    Update an artifact in the database

    Arguments:
    conn            - An sqlite connection object representing
                      the database on which data will be inserted
    artifact_id     - the ID associated to the artifact to update
    artifact        - an artifact object which contains the attributes
                      to update

    Returns:
    Returns an error if there was a failure in the update operation
    """
    current_artifact = get_artifact_by_id(conn, artifact_id)
    if not current_artifact:
        return None

    update_record = (artifact_id, artifact.title, artifact.category,
                     artifact.path, artifact.tags, artifact.author,
                     artifact.status, None)

    new_record = list()
    for i, elem in enumerate(attr.astuple(current_artifact)):
        new_record.append(update_record[i] or elem or None)

    delete_artifact_by_id(conn, artifact_id)
    updated_artifact = Artifact(None, *new_record[1:])
    insert_artifact(conn, updated_artifact)
