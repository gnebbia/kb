    # -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb plugins printed output module

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.plugin import print_metadata, load_plugin_data

def print_list(args, config, results):
    res = results['plugins']
    for plugin in res:
        toml_data_file = plugin['info']
        X = load_plugin_data('metadata',toml_data_file)
        print_metadata(args,X,config,plugin['status'],results['list_type'])
    return 0



