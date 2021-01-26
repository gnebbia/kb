# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager (list plugins command)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""
from typing import Dict

def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    from kb.plugins.plugins.actions.list import list_plugins as get_list_of_plugins
    from kb.plugins.plugins.printer.printer_output import print_list

    results = get_list_of_plugins(args,config)
    print_list(args, config,results)
    return None