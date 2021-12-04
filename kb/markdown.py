# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb markdown viewer module

:Copyright: © 2021, gnc, pliski.
:License: GPLv3 (see /LICENSE).
"""
from typing import Dict

from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel


def md_print(string: str, markers: Dict[str, str]):
    """
    Print an artifact parsing it as a markdown document.

    Arguments:
    string  - the message to be printed
    markers  - the configuration options for the markdown lexer

    Returns:
      nothing
    """

    # defaults
    style = "solarized-dark"
    justify = "full"
    hyperlinks = False
    usepager = False
    pager_color = False
    padding_vertical = 0
    padding_horizontal = 0

    # template override
    if "STYLE" in markers:
        style = markers["STYLE"]

    if "JUSTIFY" in markers:
        justify = markers["JUSTIFY"]

    if "HYPERLINKS" in markers:
        hyperlinks = markers["HYPERLINKS"]

    if "PAGER" in markers:
        usepager = markers["PAGER"]

    if "PADDING_VERTICAL" in markers:
        padding_vertical = markers["PADDING_VERTICAL"]

    if "PADDING_HORIZONTAL" in markers:
        padding_horizontal = markers["PADDING_HORIZONTAL"]

    # This assume that you have a color capable pager as default.
    # Ex. `export PAGER="less -r"`
    if "PAGER_COLOR" in markers:
        pager_color = markers["PAGER_COLOR"]

    # print
    console = Console()
    text = Markdown(string, style, justify=justify, hyperlinks=hyperlinks)

    pan = Panel(text)
    out = Padding(pan, (padding_vertical, padding_horizontal))

    if usepager:
        with console.pager(styles=pager_color):
            console.print(out)
    else:
        console.print(out)

    # console.print(locals())
