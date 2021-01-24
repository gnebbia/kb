# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager (manage plugins command)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""
from typing import Dict
from kb.plugins.plugins.actions.manage import manage_plugins as manage_as_plugins
from kb.plugins.plugins.printer.printer_output import print_managed_list

def manage_plugins(args: Dict[str, str], config: Dict[str, str], filename): 
    results = manage_as_plugins(args,config, filename)
    print_managed_list(args, config,results)
    return None