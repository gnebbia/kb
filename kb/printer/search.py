# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for search command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import List
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_search_header(
        search_result: List[Artifact],
        color: bool = True
) -> str:
    """
    Generates kb query search results header.

    Arguments:
    search_result   - the list of Artifacts for generating
                      an adapted header
    color           - a boolean, True if color is enabled

    Returns:
    A string representing the header for the list of artifacts
    """

    if not search_result:
        return

    min_length = 20
    len_id = max(len(str(len(search_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in search_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in search_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in search_result]), min_length)

    header = "   [ {id} ]  {title} {category} {tags}".format(
        id="ID".rjust(len_id),
        title="Title".ljust(len_title),
        category="Category".ljust(len_categ),
        tags="Tags".ljust(len_tags))

    if color:
        return UND + BOLD + header + RESET
    return header


def generate_search_header_verbose(
        search_result: List[Artifact],
        color: bool = True
) -> str:
    """
    Generates kb query search results header in verbose mode.

    Arguments:
    search_result   - the list of Artifacts for generating
                      an adapted header
    color           - a boolean, True if color is enabled

    Returns:
    A string representing the header for the list of artifacts
    """
    if not search_result:
        return

    min_length = 20
    sec_min_length = 10
    len_id = max(len(str(len(search_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in search_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in search_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in search_result]), min_length)
    len_author = max(max(
        [len(art.author) if art.author else 0 for art in search_result]), sec_min_length)
    len_status = max(max(
        [len(art.status) if art.status else 0 for art in search_result]), sec_min_length)

    header = "   [ {id} ]  {title} {category} {tags} {author} {status}".format(
        id="ID".rjust(len_id),
        title="Title".ljust(len_title),
        category="Category".ljust(len_categ),
        tags="Tags".ljust(len_tags),
        author="Author".ljust(len_author),
        status="Status".ljust(len_status))

    if color:
        return UND + BOLD + header + RESET
    return header


def print_search_result(
        search_result: List[Artifact],
        color: bool = True
) -> None:
    """
    Print kb query search results

    Arguments:
    search_result   - the list of Artifacts to print
                      in the form of search result
    color           - a boolean, True if color is enabled
    """
    if not search_result:
        return

    print(generate_search_header(search_result, color=color))
    print()

    min_length = 20
    len_id = max(len(str(len(search_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in search_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in search_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in search_result]), min_length)

    # Print results
    for view_id, artifact in enumerate(search_result):
        tags = artifact.tags if artifact.tags else ""

        result_line = " - [ {id} ]  {title} {category} {tags}".format(
            id=str(view_id).rjust(len_id),
            title=artifact.title.ljust(len_title),
            category=artifact.category.ljust(len_categ),
            tags=tags.ljust(len_tags))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)


def print_search_result_verbose(
        search_result: List[Artifact],
        color: bool = True
) -> None:
    """
    Print kb query search results in verbose mode.

    Arguments:
    search_result   - the list of Artifacts to print
                      in the form of search result
    color           - a boolean, True if color is enabled
    """
    if not search_result:
        return

    print(generate_search_header_verbose(search_result, color=color))
    print()

    min_length = 20
    sec_min_length = 10
    len_id = max(len(str(len(search_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in search_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in search_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in search_result]), min_length)
    len_author = max(max(
        [len(art.author) if art.author else 0 for art in search_result]), sec_min_length)
    len_status = max(max(
        [len(art.status) if art.status else 0 for art in search_result]), sec_min_length)

    # Print results
    for view_id, artifact in enumerate(search_result):
        tags = artifact.tags if artifact.tags else ""
        author = artifact.author if artifact.author else ""
        status = artifact.status if artifact.status else ""

        result_line = "   [ {id} ]  {title} {category} {tags} {author} {status}".format(
            id=str(view_id).rjust(len_id),
            title=artifact.title.ljust(len_title),
            category=artifact.category.ljust(len_categ),
            tags=tags.ljust(len_tags),
            author=author.ljust(len_author),
            status=status.ljust(len_status))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)
