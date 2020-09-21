# -*- encoding: utf-8 -*-
# kb v0.1.2
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb styler module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).

This is a gateway for the styler module used to styled text
"""
import colored


def set_bg(color: str) -> str:
    """
    Set background color.

    Arguments:
    color       - the color string to set, that
                  can be either a word (e.g., "green")
                  or an hex code (e.g., "#00AB00")
    Returns:
    A string representing the code to set the background color
    """
    return colored.bg(color)


def set_fg(color: str) -> str:
    """
    Set foreground color.

    Arguments:
    color       - the color string to set, that
                  can be either a word (e.g., "green")
                  or an hex code (e.g., "#00AB00")
    Returns:
    A string representing the code to set the foreground color
    """
    return colored.fg(color)


def set_style(style: str) -> str:
    """
    Set a specific text style

    Arguments:
    style       - a string representing the desired
                  style, examples:
                  "bold"
                  "underline"
    Returns:
    A string representing the code to set the desired style
    """
    return colored.attr(style)


def reset() -> str:
    """
    Reset applied style.

    Returns:
    A string representing the code to reset the style and colors to default
    """
    return colored.attr('reset')
