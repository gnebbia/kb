# -*- encoding: utf-8 -*-
# kb v0.1.3
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


def colorize_row(row, markers=None):
    """
    This function takes a string and a dictionary of markers
    (where key is regex and value is color) and
    the transforms the passed string (row) with colors.

    Arguments:
    row     - the string
    markers - a dictionary having as key strings
              representing the purpose of the formatting
              and having as values a list where
              the first element is a regex and the second
              element is the color value.
              Example:
              markers = { 
                    "TITLE":    ["^#.*", "blue"]
                    "WARNINGS": ["^!.*", "yellow"]
              }

    Returns:
    A new message colored following the rules within the markers
    dictionary
    """
    colored_row = row
    for mark in markers:
        regex = re.compile(rf'{(markers[mark][0])}')
        color = markers[mark][1]
        
        match = regex.search(row)

        if match:
            colored_row = re.sub(regex, rf'{colorize_string(match.group(0), color)}', rf'{row}')
            row = colored_row

    return colored_row


def colorize_output(data, markers):
    """
    This function takes an input a list of strings, for example they
    can be taken from a file or any other source, processes them
    and returns a list of formatted colored strings ready to be
    visualized.

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
        colorized_output.append(colorize_row(row, markers))
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
