# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for grep command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import List
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_grep_header(
        grep_result: List[Artifact],
        hits_list: List[int],
        color: bool = True
) -> None:
    """
    Generates kb grep results header.

    Arguments:
    grep_result     - the list of Artifacts for generating
                      an adapted header
    hits_list       - a list ordered as the artifacts
                      representing the number of grep
                      matches for that artifact
    color           - a boolean, True if color is enabled

    Returns:
    A string representing the header for the list of artifacts
    """
    if not grep_result:
        return

    min_length = 20
    len_id = max(len(str(len(grep_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in grep_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in grep_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in grep_result]), min_length)

    len_hits = max(len(str(max(hits_list))), 4)

    header = "   [ {id} ]  {title} {category} {hits} {tags}".format(
        id="ID".rjust(len_id),
        title="Title".ljust(len_title),
        category="Category".ljust(len_categ),
        hits="Hits".ljust(len_hits),
        tags="Tags".ljust(len_tags))

    if color:
        return UND + BOLD + header + RESET
    return header


def generate_grep_header_verbose(
        grep_result: List[Artifact],
        hits_list: List[int],
        color: bool = True
) -> None:
    """
    Generates kb grep results header in verbose mode.

    Arguments:
    grep_result     - the list of Artifacts for generating
                      an adapted header
    hits_list       - a list ordered as the artifacts
                      representing the number of grep
                      matches for that artifact
    color           - a boolean, True if color is enabled

    Returns:
    A string representing the header for the list of artifacts
    """

    if not grep_result:
        return

    min_length = 20
    sec_min_length = 10
    len_id = max(len(str(len(grep_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in grep_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in grep_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in grep_result]), min_length)
    len_author = max(max(
        [len(art.author) if art.author else 0 for art in grep_result]), sec_min_length)
    len_status = max(max(
        [len(art.status) if art.status else 0 for art in grep_result]), sec_min_length)

    len_hits = max(len(str(max(hits_list))), 4)

    header = "   [ {id} ]  {title} {category} {hits} {tags} {author} {status}".format(
        id="ID".rjust(len_id),
        title="Title".ljust(len_title),
        category="Category".ljust(len_categ),
        hits="Hits".ljust(len_hits),
        tags="Tags".ljust(len_tags),
        author="Author".ljust(len_author),
        status="Status".ljust(len_status))

    if color:
        return UND + BOLD + header + RESET
    return header


def print_grep_result(
        grep_result: List[Artifact],
        hits_list: List[int],
        color: bool = True
) -> None:
    """
    Print kb query grep results.

    Arguments:
    grep_result     - the list of Artifacts to print
                      in the form of grep result
    hits_list       - a list ordered as the artifacts
                      representing the number of grep
                      matches for that artifact
    color           - a boolean, if True, color is enabled
    """
    if not grep_result:
        return

    print(generate_grep_header(grep_result, hits_list, color=color))
    print()

    min_length = 20

    len_id = max(len(str(len(grep_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in grep_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in grep_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in grep_result]), min_length)

    len_hits = max(len(str(max(hits_list))), 4)

    # Print results
    for view_id, artifact in enumerate(grep_result):
        tags = artifact.tags if artifact.tags else ""

        hits_id = view_id
        hits = str(hits_list[hits_id])

        result_line = "   [ {id} ]  {title} {category} {hits} {tags}".format(
            id=str(view_id).rjust(len_id),
            title=artifact.title.ljust(len_title),
            category=artifact.category.ljust(len_categ),
            hits=hits.ljust(len_hits),
            tags=tags.ljust(len_tags))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)


def print_grep_result_verbose(
        grep_result: List[Artifact],
        hits_list: List[int],
        color: bool = True
) -> None:
    """
    Print more verbose kb query grep results.

    Arguments:
    grep_result     - the list of Artifacts to print
                      sorted by number of hits
    hits_list       - a list ordered as the grep_result artifacts
                      (i.e., by number of hits) representing the number
                      of grep matches for that artifact
    color           - a boolean, if True, color is enabled
    """
    if not grep_result:
        return

    print(generate_grep_header(grep_result, hits_list, color=color))
    print()

    min_length = 20
    sec_min_length = 10

    len_id = max(len(str(len(grep_result) - 1)), 2)

    len_title = max(
        max([len(art.title) if art.title else 0 for art in grep_result]), min_length)
    len_categ = max(max(
        [len(art.category) if art.category else 0 for art in grep_result]), min_length)
    len_tags = max(
        max([len(art.tags) if art.tags else 0 for art in grep_result]), min_length)
    len_author = max(max(
        [len(art.author) if art.author else 0 for art in grep_result]), sec_min_length)
    len_status = max(max(
        [len(art.status) if art.status else 0 for art in grep_result]), sec_min_length)

    len_hits = max(len(str(max(hits_list))), 4)

    # Print results
    for view_id, artifact in enumerate(grep_result):
        tags = artifact.tags if artifact.tags else ""

        author = artifact.author if artifact.author else ""
        status = artifact.status if artifact.status else ""

        hits_id = view_id
        hits = str(hits_list[hits_id])

        result_line = "   [ {id} ]  {title} {category} {hits} {tags} {author} {status}".format(
            id=str(view_id).rjust(len_id),
            title=artifact.title.ljust(len_title),
            category=artifact.category.ljust(len_categ),
            hits=hits.ljust(len_hits),
            tags=tags.ljust(len_tags),
            author=author.ljust(len_author),
            status=status.ljust(len_status))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)

# This function still has to be implemented, this is just a placeholder
def print_grep_matches(grep_matches, hits_list, color=True):
    """
    Print text associated to grep matches.

    Arguments:
    grep_matches    - the list of Artifacts to print
                      in the form of grep matches
    color           - a boolean, if True, color is enabled
    """

    generate_grep_header

    num_results_digits = len(str(len(grep_matches) - 1))

    header = "{} {} {} {} {}".format(
        "Category".ljust(20),
        "Title".ljust(20),
        "Line".ljust(20),
        "Match".ljust(20))

    # Print header
    print(UND + BOLD + header + RESET)
    print()

    # Print results
    for view_id, artifact in enumerate(grep_matches):
        tags = artifact.tags if artifact.tags else ""

        status = artifact.status if artifact.status else ""
        author = artifact.author if artifact.author else ""
        hits_id = view_id
        hits = str(hits_list[hits_id])

        result_line = " - [ {} ] {} {} {} {} {} {}".format(
            str(view_id).rjust(num_results_digits),
            artifact.title.ljust(20),
            artifact.category.ljust(20),
            hits.ljust(6),
            tags.ljust(20),
            status.ljust(20),
            author.ljust(20))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)
