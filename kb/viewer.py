# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb viewer module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import re
from typing import Dict
from kb.styler import set_fg, reset

def colorize_string(string, color):
    """
    This function applies the provided color to the specified string

    Arguments:
    msg   - The message to be colored
    color - The name of the color (or hex code), e.g., "red" or "#C0C0C0"

    Returns:
    A colored message
    """
    return set_fg(color) + string + reset()


def colorize_string_on_match(string, regex, color):
    """
    This function take a string and substitute it using regex and match
    with configured colors.

    Arguments:
    string   - A string
    regex    - A regex that will be matched against the string
    color    - The string name of color or hex, like "red" or "#C0C0C0"

    Returns:
    A colored string when regex matches
    """
    # re.search(r"%(.*?)%", str)
    try:
        new_msg = re.search(rf"{regex}", string).group(1)
    except BaseException:
        new_msg = string
    return re.sub(regex, colorize_string(new_msg, color), string)


def mark_row(row, markers=None):
    """
    This function take a string, recognize markers using regex and returns
    the row formatted if needed.

    Arguments:
    row     - The message
    markers - an object containing configured marks in the form:


    Returns:
    A new formatted message
    """
    is_marked = False
    for mark in markers:
        regex = rf'{(markers[mark][0])}'
        color_match = markers[mark][1]

        if re.search(regex, row) is not None:
            res = colorize_string_on_match(row, regex, color_match)
            is_marked = True
            return res

    if not is_marked:
        return row


def colorize_output(data, markers):
    """
    A function that takes an input list of strings, for example they
    can be taken from a file or any other source, processes them
    and returns a list of formatted colored strings ready to be
    visualized

    Arguments:
    data    - A list of strings.
    markers - an object contains configured marks

    Returns:
    A new formatted list
    """
    if markers is None:
        return data
    colorized_output = list()
    for row in data:
        colorized_output.append(mark_row(row, markers))
    return colorized_output


def view(filepath: str, markers: Dict[str, str], color: bool = True) -> None:
    """
    Visualize the specified file with applied markers
    if color is True.

    Arguments:
    filepath        - the file to visualize on stdout
    markers         - the markers dictionary to apply
    color           - a boolean, if True color is enabled
    """
    content = ""
    with open(filepath) as fname:
        content = fname.read()

    # Print on screen with proper markers
    lines = content.splitlines()
    if color:
        colored_lines = colorize_output(lines, markers)
        for line in colored_lines:
            print(line)
    else:
        for line in lines:
            print(line)
