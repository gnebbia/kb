#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# kb test suite
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

import os
import kb
import kb.filesystem as fs
from pathlib import Path


def test_list_files():
    # Test number of files found
    files_kb = fs.list_files(Path("tests", "data", ".kb", "data"))
    assert len(files_kb) == 4

    files_kb2 = fs.list_files(Path("tests", "data", ".kb2", "data"))
    assert len(files_kb2) == 8
    assert not len(files_kb2) == 7


    # Test if files picked are right
    kb_list_of_files = ["pt_tls",
                        "pt_ipmi",
                        "pth",
                        "pt_wifi_tips"]

    assert set(files_kb) == set(kb_list_of_files)
    
    kb2_list_of_files = [str(Path("dir2","dir3","pt_wifi2")),
                         str(Path("dir2","pt_wifi_tips")),
                         str(Path("pt_tls")),
                         str(Path("pt_ipmi")),
                         str(Path("pth")),
                         str(Path("dir1","pt_ipmi")),
                         str(Path("dir1","pth")),
                         str(Path("pt_wifi_tips"))]

    assert set(files_kb2) == set(kb2_list_of_files)

def test_list_dirs():
    # Test number of directories found
    dir_kb = fs.list_dirs(Path("tests", "data", ".kb", "data"))
    assert len(dir_kb) == 0

    dir_kb2 = fs.list_dirs(Path("tests", "data", ".kb2", "data"))
    assert len(dir_kb2) == 3


    # Test if files picked are right
    kb_list_of_dirs =  []

    assert set(dir_kb) == set(kb_list_of_dirs)
    
    kb2_list_of_dirs = [str(Path("dir2")),
                        str(Path("dir2/dir3")),
                        str(Path("dir1"))]

    assert set(dir_kb2) == set(kb2_list_of_dirs)



def test_copy_file():
    filename_src = Path("tests","data","sample_data")
    filename_dst = Path("tests","data","sample_data_dest")

    with open(filename_src, 'w') as f:
        f.write('sample data\n')
    assert os.path.exists(filename_src)

    fs.copy_file(filename_src, filename_dst)
    assert os.path.exists(filename_dst)

def test_move_file():
    filename = Path("tests","data","sample_data")
    with open(filename, 'w') as f:
        f.write('sample data\n')

    assert os.path.exists(filename)

    filename_new = Path("tests","data","new_sample_data")
    fs.move_file(filename, filename_new )
    assert not os.path.exists(filename)
    assert os.path.exists(filename_new)


def test_remove_file():
    filename = Path("tests","data","sample_data")
    with open(filename, 'w') as f:
        f.write('sample data\n')

    assert os.path.exists(filename)

    fs.remove_file(filename)
    assert not os.path.exists(filename)

def test_get_basename():
    filename = Path("tests","data","sample_data")
    with open(filename, 'w') as f:
        f.write('sample data\n')
    assert "sample_data" == fs.get_basename(filename)

