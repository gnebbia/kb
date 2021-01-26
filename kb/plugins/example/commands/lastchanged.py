# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin command to get the last changed date/time of a document

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""
from typing import Dict
from kb.plugins.example.actions.lastchanged import last_changed as lastchanged
from kb.plugins.example.printer.printer_output import print_last_changed

def last_changed(args: Dict[str, str], config: Dict[str, str]): 
    print(args)
    results = lastchanged(args,config)
    print_last_changed(args,results)
    return results