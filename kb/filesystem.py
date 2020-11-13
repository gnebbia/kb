# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb filesystem module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import List
from datetime import datetime


def list_files(directory: str) -> List[str]:
    """
    List all files contained in a directory recursively,
    similarly to the "find" UNIX command

    Args:
    directory       - a string representing the target directory

    Returns:
    A list of strings representing the path of files contained
    in the directory
    """

    # Get kbdir path
    dirpath = Path(directory)

    # Get list of files in the form: file1, dir1/file2, ...
    files = [str(f.relative_to(dirpath))
             for f in dirpath.rglob("*") if f.is_file()]
    return files


def list_dirs(directory: str) -> List[str]:
    """
    List all sub-directories contained in a directory

    Args:
    directory       - a string representing the path to a directory

    Returns:
    A list of strings representing the path of directories contained
    in the provided directory
    """
    # Get kbdir path
    dirpath = Path(directory)

    # Get list of files in the form: file1, dir1/file2, ...
    files = [str(f.relative_to(dirpath))
             for f in dirpath.rglob("*") if f.is_dir()]
    return files


def get_file_size(filename):
    """
    Get the size of a named file

    Args:
    filename       - a string representing the path to the required file

    Returns:
    A value in bytes (or zero if the file does not exist or cannot be opened)
    """
    file_size = 0
    try:
        st = os.stat(filename)
    except:
        file_size = 0
    finally:
        file_size = st.st_size
    return file_size


def get_complete_size(root='.'):
    """
    Get the size of the whole knowledgebase (including data, templates, artifacts etc)

    Args:
    root       - a string representing the root of the knowledgebase

    Returns:
    A value in bytes (or zero if the knowledgebase does not exist or cannot be opened)
    """

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def touch_file(filename: str):
    """
    Creates a new empty file, in the style of the UNIX
    touch program.

    Arguments:

    filename    - a path to a filename
    """
    Path(filename).touch()


def get_basename(filename: str) -> str:
    """
    Get basename for a file

    Arguments:
    filename    - a path to a filename

    Returns:
    The basename of the provided file
    """
    return Path(filename).name


def copy_file(source: str, dest: str) -> None:
    """
    Copies a file to the provided destination

    Arguments:
    source    - the path to the source file to copy
    dest      - the destination path of the copy
    """
    shutil.copy2(Path(source), Path(dest))


def remove_file(filename: str) -> None:
    """
    Removes a file from the filesystem

    Arguments:
    filename    - the file to remove from the kb directory
    """
    try:
        Path(filename).unlink()
    except FileNotFoundError:
        pass


def remove_directory(directory: str) -> None:
    """
    Removes a directory from the filesystem

    Arguments:
    directory    - the directory to remove from the kb system
    """
    shutil.rmtree(directory)


def create_directory(directory: str) -> None:
    """
    Create a directory if it does not exist.

    Arguments:
    directory    - the directory path to be created
    """
    os.makedirs(Path(directory), exist_ok=True)


def is_directory(path: str) -> bool:
    """
    Checks if the provided path is a directory.

    Arguments:
    path        - the path to check

    Returns:
    A boolean, if true, the path corresponds to a directory
    """
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    """
    Checks if the provided path corresponds to a regular file.

    Arguments:
    path        - the path to check

    Returns:
    A boolean, if true, the path corresponds to a regular file
    """
    return os.path.isfile(path)


def count_files(directory: str) -> int:
    """
    Count the number of files in a directory

    Arguments:
    directory    - the directory where to count files

    Returns:
    the number of files contained in the directory
    """
    return len(list(Path(directory).iterdir()))


def move_file(source: str, dest: str) -> None:
    """
    Moves a file to the provided destination

    Arguments:
    source    - the path to the source file to copy
    dest      - the destination path of the copy
    """
    shutil.move(source, dest)


def get_temp_filepath() -> str:
    """
    Generates a temporary file path.

    Returns:
    A boolean, True if the file is of type text.
    """
    tmpfilename = None
    while tmpfilename is None:
        random_tmp_path = str(Path(tempfile.gettempdir(),
                                   os.urandom(24).hex()))
        if not os.path.isfile(random_tmp_path):
            tmpfilename = random_tmp_path
    return tmpfilename


def is_text_file(filename: str) -> bool:
    """
    Determines if a file is textual (that can be
    nicely viewed in a text editor) or belonging
    to other types.

    Arguments:
    filename        - the file name/path to check

    Returns:
    A boolean, True if the file is of type text.
    """
    txt_extensions = ("", ".conf", ".ini", ".txt",
                      ".md", ".rst", ".ascii", ".org", ".tex")

    file_ext = os.path.splitext(filename)[1]

    return file_ext in txt_extensions


def get_filename_parts_wo_prefix(
        filename: str,
        prefix_to_remove: str) -> List[str]:
    """
    Get filename parts without the provided prefix.
    E.g., if the filename is "/path/to/data/dir1/file2.txt"
    and the prefix to remove is "/path/to/data" then the
    returned will be a tuple containing ("dir1","file2.txt")

    Arguments:
    filename          - a string or path provided by pathlib
    prefix_to_remove  - a string or path provided by pathlib that
                        will be removed from the filename

    Returns:
    The provided filename without the provided prefix
    """
    filename_str = str(filename)
    prefix_str = str(prefix_to_remove)
    return tuple(filename_str.replace(prefix_str, '')
                 .replace("/", " ")
                 .replace("\\", " ")
                 .strip().split())


def grep_in_files(
        filelist: str,
        regex: str,
        case_insensitive: bool = False
) -> List[str]:
    """
    Grep recursively through a file list by trying to match
    a regex with the content of all the files.
    This is equivalent to:
    grep -nr 'regex' file1 file2 ...

    Arguments:
    filelist     - the file list where to match the regex
    regex        - the regex to match

    Returns
    A list of tuples containing (filepath, line number, matched string)
    """
    if case_insensitive:
        pattern = re.compile(regex, re.IGNORECASE)
    else:
        pattern = re.compile(regex)

    matches = list()
    for fname in filelist:
        try:
            with open(fname) as handle:
                for i, line in enumerate(handle):
                    match = pattern.search(line)
                    linenumber = i + 1
                    if match:
                        matches.append((fname, linenumber, line.strip()))
                        # !!!TODO: This can be of inspiration for later result show
                        # print("%s:%s: %s" % (filepath, lineno,
                        #     line.strip().replace(mo.group(), "\033[92m%s\033[0m"%
                        #         mo.group())))
        except UnicodeDecodeError:
            # In this case the file is binary,
            # so we don't search through binary files
            continue
    return matches


def grep_in_files_uniq(
        filelist: str,
        regex: str,
        case_insensitive=False
) -> List[str]:
    """
    Grep recursively through a list of files by trying to match
    a regex with the content of all the found files.
    Note that it will return only the set of filenames matched without
    the content.
    This is equivalent to:
    grep -lnr 'regex' file1 file2 ...

    Arguments:
    filelist     - the file list where to match the regex
    regex        - the regex to match

    Returns
    A list of file paths matching the regex.
    """
    if case_insensitive:
        pattern = re.compile(regex, re.IGNORECASE)
    else:
        pattern = re.compile(regex)

    matches = list()
    for fname in filelist:
        try:
            with open(fname) as handle:
                for line in handle:
                    match = pattern.search(line)
                    if match:
                        matches.append(fname)
        except UnicodeDecodeError:
            # In this case the file is binary,
            # so we don't search through binary files
            continue
    return list(set(matches))


def get_last_modified_time(fullfilename):
    try:
        return datetime.utcfromtimestamp(os.path.getmtime(fullfilename)).strftime('%Y-%m-%d %H:%M:%S')
    except OSError:
        return None
