#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# kb test suite
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
To reload modules
import imp
imp.reload(kb)
imp.reload(kb.db)
imp.reload(kb.filesystem)
"""

import attr
import kb
import kb.db as db
import kb.filesystem as fs
import sqlite3
import pytest
from pathlib import Path
from kb.entities.artifact import Artifact


@pytest.fixture()
def db_connect():
    conn = sqlite3.connect(Path("tests","data","mydb.db"))
    return conn

def _list_tables(conn):
    """
    Return the list of tables currently in the database
    at the moment kb is based on a single table
    called "artifacts", but this may change in the future.

    Arguments:
    conn            -   the sqlite3 Connection object

    Returns:
    A list of strings representing the list of tables
    in the kb database
    """
    cur = conn.cursor()
    sql_query = """SELECT name FROM sqlite_master
                   WHERE type='table'
                   ORDER BY name;"""
    cur.execute(sql_query)
    rows = cur.fetchall()
    return rows


def test_create_connection():
    ok_db_path = Path("tests","data",".kb","kb.db")
    assert db.create_connection(ok_db_path) is not None
    ok_db_path.unlink()
    

def test_create_connection_2():
    failing_db_path = Path("tests","data","non_existing","kb.db")
    assert db.create_connection(failing_db_path) is None

def test_create_connection_3():
    ok_db_path = ":memory:"
    assert db.create_connection(ok_db_path) is not None

def test_list_tables_blank():
    db_path = Path("tests","data","empty.db")
    conn = db.create_connection(db_path)
    assert _list_tables(conn) == []
    db_path.unlink()

def test_list_tables():
    sql_create_table_query = """CREATE TABLE IF NOT EXISTS testtable1 (
                                    id integer PRIMARY KEY,
                                    author text
                                 );
                                CREATE TABLE IF NOT EXISTS testtable2 (
                                    id integer PRIMARY KEY,
                                    author text
                                );
                             """

    db_path = Path("tests","data","two_tables.db")
    conn = db.create_connection(db_path)
    try:
        c = conn.cursor()
        c.executescript(sql_create_table_query)
    except Exception as e:
        print(e)

    assert len(_list_tables(conn)) == 2
    db_path.unlink()


def test_create_table(db_connect):
    sql_db_create_query = """CREATE TABLE IF NOT EXISTS artifacts (
                                id integer PRIMARY KEY,
                                title text NOT NULL,
                                category text NOT NULL,
                                path text NOT NULL,
                                tags text,
                                status text,
                                author text);
                          """

    db_path =  Path("tests","data","mydb.db")
    conn = db.create_connection(db_path)
    if conn is not None:
        db.create_table(conn, sql_db_create_query)
    else:
        print("Error! cannot create the database connection.")

    assert len(_list_tables(conn)) == 1
    db_path.unlink()

def test_create_table_2(db_connect):
    sql_db_create_query = """CREATE TABLE artifacts (
                                id integer PRIMARY KEY,
                                title text NOT NULL,
                                category text NOT NULL,
                                path text NOT NULL,
                                tags text,
                                status text,
                                author text);
                          """

    db_path =  Path("tests","data","mydb.db")
    conn = db.create_connection(db_path)
    if conn is not None:
        db.create_table(conn, sql_db_create_query)
        db.create_table(conn, sql_db_create_query)
    else:
        print("Error! cannot create the database connection.")

    assert len(_list_tables(conn)) == 1
    db_path.unlink()
    
def test_create_kb_database_table():
    db_path = Path("tests","data","mydb.db")
    db.create_kb_database(db_path)

    conn = db.create_connection(db_path)
    try:
        c = conn.cursor()
    except Exception as e:
        print(e)

    # Make sure, the database has the correct number of tables
    kb_tables = _list_tables(conn)
    assert len(kb_tables) == 2
    assert kb_tables == [("artifacts",),("tags",)]
    db_path.unlink()



def test_insert_artifact():
    db_path = Path("tests","data","newdb.db")
    db.create_kb_database(db_path)
    conn = db.create_connection(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="pentest/smb", title="pentest_smb", category="procedure", 
            tags='pt;smb', status="OK", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="protocol/ftp", title="ftp", category="cheatsheet", 
            status="Draft", author="elektroniz"))

    kb_tables = _list_tables(conn)
    assert len(kb_tables) == 2
    assert kb_tables == [("artifacts",),("tags",)]

    sql = "SELECT * FROM artifacts;"
    cur = conn.cursor()
    cur.execute(sql)
   
    rows = cur.fetchall()
    print(rows)
    assert set(rows) == {(1, 'pentest_smb', 'procedure',
                        'pentest/smb', 'pt;smb', 'OK', 'gnc'),
                         (2, 'ftp', 'cheatsheet', 'protocol/ftp', None,
                        'Draft', 'elektroniz')}

    db_path.unlink()

def test_is_artifact_existing():
    db_path = Path("tests","data","newdb.db")
    db.create_kb_database(db_path)
    conn = db.create_connection(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="pentest/smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="OK", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="protocol/ftp", title="ftp",
            category="cheatsheet", status="Draft", author="elektroniz"))
    
    assert db.is_artifact_existing(conn,title="pentest_smb",
                                   category="procedure")
    assert db.is_artifact_existing(conn,title="ftp",
                                   category="cheatsheet")
    assert not db.is_artifact_existing(conn,title="pentest_smb",
                                       category="nonexist")
    assert not db.is_artifact_existing(conn,title="nonexist",
                                       category="procedure")
    assert not db.is_artifact_existing(conn,title="",
                                       category="cheatsheet")
    assert not db.is_artifact_existing(conn,title="", category="")


    db_path.unlink()


def test_delete_artifact_by_id():
    db_path = Path("tests","data","newdb.db")
    db.create_kb_database(db_path)
    conn = db.create_connection(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="pentest/smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="OK", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="protocol/ftp", title="ftp",
            category="cheatsheet", status="Draft", author="elektroniz"))
    
    db.delete_artifact_by_id(conn, 1)

    sql = "SELECT * FROM artifacts;"
    cur = conn.cursor()
    cur.execute(sql)
   
    rows = cur.fetchall()
    assert len(rows) == 1
    assert set(rows) == {(2, 'ftp', 'cheatsheet', 'protocol/ftp', None,
                        'Draft', 'elektroniz')}

    db.delete_artifact_by_id(conn,2)

    sql = "SELECT * FROM artifacts;"
    cur = conn.cursor()
    cur.execute(sql)
   
    rows = cur.fetchall()

    assert len(rows) == 0

    db_path.unlink()


def test_delete_artifact_by_name():
    db_path = Path("tests","data","newdb.db")
    db.create_kb_database(db_path)
    conn = db.create_connection(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="pentest/smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="OK", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="protocol/ftp", title="ftp",
            category="cheatsheet", status="Draft", author="elektroniz"))

    db.delete_artifact_by_name(conn, title="pentest_smb", category="")
    sql = "SELECT * FROM artifacts;"
    cur = conn.cursor()
    cur.execute(sql)
   
    rows = cur.fetchall()
    assert len(rows) == 2

    db.delete_artifact_by_name(conn, title="pentest_smb", category="procedure")
    sql = "SELECT * FROM artifacts;"
    cur = conn.cursor()
    cur.execute(sql)
   
    rows = cur.fetchall()
    assert len(rows) == 1
    assert set(rows) == {(2, 'ftp', 'cheatsheet', 'protocol/ftp', None,
                          'Draft', 'elektroniz')}

    db_path.unlink()




def test_get_artifacts_by_tags():
    db_path = Path("tests","data","kb_art_tags.db")
    conn = db.create_connection(db_path)
    db.create_kb_database(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="ok", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/ftp", title="ftp", category="cheatsheet", 
            status="draft", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/http", title="http", category="cheatsheet", 
            status="OK", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/irc", title="irc", category="cheatsheet", 
            tags="protocol", status="draft", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_ftp", title="pentest_ftp", category="cheatsheet", 
            tags="pt", status="draft", author="elektroniz"))

    rows = db.get_artifacts_by_tags(conn, tags=["pt"], is_strict=False)
    assert len(rows) == 2

    rows = db.get_artifacts_by_tags(conn, tags=["p"], is_strict=False)
    assert len(rows) == 3

    rows = db.get_artifacts_by_tags(conn, tags=["pt"], is_strict=True)
    assert len(rows) == 2

    db_path.unlink()

def test_get_artifacts_by_title():
    db_path = Path("tests","data","kb_filter_title.db")
    conn = db.create_connection(db_path)
    db.create_kb_database(db_path)
    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="ok", author="gnc"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/ftp", title="ftp", category="cheatsheet", 
            status="draft", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/http", title="http", category="cheatsheet", 
            status="OK", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="guides/irc", title="irc", category="cheatsheet", 
            tags="protocol", status="draft", author="elektroniz"))
    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_ftp", title="pentest_ftp", category="cheatsheet", 
            tags="pt", status="draft", author="elektroniz"))

    rows = db.get_artifacts_by_title(conn, query_string="", is_strict=False)
    assert len(rows) == 5
    
    rows = db.get_artifacts_by_title(conn, query_string="", is_strict=True)
    assert len(rows) == 0

    db_path.unlink()

def test_get_artifacts_by_category():
    db_path = Path("tests","data","kb_filter_cat.db")

    conn = db.create_connection(db_path)
    db.create_kb_database(db_path)

    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_smb", title="pentest_smb",
            category="procedure", tags='pt;smb', status="ok", author="gnc"))

    db.insert_artifact(conn, Artifact(id=None, path="guides/ftp", title="ftp",
            category="cheatsheet",
            status="draft", author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="guides/http", title="http",
            category="cheatsheet", status="OK", author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="guides/irc", title="irc",
                       category="cheatsheet", tags="protocol", status="draft",
                       author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="cheatsheet/pentest_ftp", title="pentest_ftp",
                       category="cheatsheet", tags="pt", status="draft",
                       author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="sheet/math", title="math_formulas",
                       category="sheet", tags="math", status="draft",
                       author="gnc"))

    db.insert_artifact(conn, Artifact(id=None, path="sheet/math2", title="geometry_formulas",
                       category="sheet", tags="math", status="draft",
                       author="gnc"))

    rows = db.get_artifacts_by_category(conn, query_string="", is_strict=False)
    assert len(rows) == 7

    rows = db.get_artifacts_by_category(conn, query_string="", is_strict=True)
    assert len(rows) == 0

    rows = db.get_artifacts_by_category(conn, query_string="sheet", is_strict=True)
    assert len(rows) == 2


    db_path.unlink()


def test_get_artifacts_by_filter():
    db_path = Path("tests","data","kb_filter.db")
    conn = db.create_connection(db_path)
    db.create_kb_database(db_path)

    db.insert_artifact(conn, Artifact(id=None, path="", title="pentest_smb",
            category="procedure", tags='pt;smb', status="ok", 
            author="gnc"))

    db.insert_artifact(conn, Artifact(id=None, path="", title="ftp",
            category="cheatsheet", tags="protocol", status="draft",
            author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="", title="pentest_ftp",
            category="procedure", tags="pt;ftp", status="draft",
            author="elektroniz"))

    db.insert_artifact(conn, Artifact(id=None, path="general/CORS", title="CORS",
            category="general", tags="web", status="draft",
            author="elektroniz"))

    rows = db.get_artifacts_by_filter(conn, title="pentest",
                                      category="cheatsheet",
                                      tags=["pt"], is_strict=False)

    assert len(rows) == 0

    rows = db.get_artifacts_by_filter(conn, category="procedure",
                                      tags=["pt"], is_strict=False)
    assert set(rows) == {Artifact(1,"pentest_smb","procedure","procedure/pentest_smb","pt;smb","ok","gnc", None),
                         Artifact(3,"pentest_ftp","procedure","procedure/pentest_ftp","pt;ftp","draft", "elektroniz", None)}


    rows = db.get_artifacts_by_filter(conn, title="OR")
    assert set(rows) == {Artifact(4,"CORS","general","general/CORS","web", "draft","elektroniz", None)}


    rows = db.get_artifacts_by_filter(conn, category="cheatsheet",
                                      is_strict=False)
    assert set(rows) == {Artifact(2,"ftp","cheatsheet","cheatsheet/ftp","protocol", "draft", "elektroniz", None)}


    rows = db.get_artifacts_by_filter(conn, category="sheet",
                                      is_strict=False)
    assert set(rows) == {Artifact(2,"ftp","cheatsheet","cheatsheet/ftp","protocol", "draft", "elektroniz", None)}

    rows = db.get_artifacts_by_filter(conn, category="cheatsheet",
                                      is_strict=True)
    assert set(rows) == {Artifact(2,"ftp","cheatsheet","cheatsheet/ftp","protocol", "draft", "elektroniz", None)}

    rows = db.get_artifacts_by_filter(conn, category="sheet",
                                      is_strict=True)
    assert len(rows) == 0


    db_path.unlink()
