# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for template command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import List
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_template_search_header(
        color: bool = True
) -> str:
    """
    Generates kb query template results header.

    Arguments:
    color           - a boolean, True if color is enabled

    Returns:
    A string representing the header for the list of templates
    """
    header = "Templates"

    if color:
        return UND + BOLD + header + RESET
    return header


def print_template_search_result(
        template_search_result: List[str],
        color: bool = True
) -> None:
    """
    Print kb template search results.

    Arguments:
    template_search_result  - the list of templates
    color                   - a boolean, True if color is enabled
    """

    print(generate_template_search_header(color=color))
    print()

    len_template_name = max([len(template)
                            for template in template_search_result])

    # Print template search results
    for view_id, template in enumerate(template_search_result):
        result_line = " - {template}".format(
            template=template.ljust(len_template_name))

        if color and (view_id % 2 == 0):
            print(ALT_BGROUND + result_line + RESET)
        else:
            print(result_line)
