# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager (list plugins action)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""


from typing import Dict

def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import os
    import sys
    from pathlib import Path
    from kb.plugin import metadata as print_metadata, get_modules
    from kb.plugin import get_plugin_status

    list_type = str(args.get("status","all"))

    # Get a list of installed plugins
    plugins = get_modules()

    # Set up empty list of plugins
    list_of_plugins = []

    # Cycle through the available plugins and display their metadata
    for plugin in plugins:

        interim_root = (str((os.path.dirname(str((os.path.dirname(__file__)))))))

        root = str(Path(os.path.dirname(interim_root)))
        toml_data_file = (str(Path(root, plugin, 'config.toml')))
        print(plugin, "     -    ", toml_data_file)

        # Check to see if this module should be included in the list
        disabled = get_plugin_status(plugin)
        if ((list_type == 'all' ) or
            (list_type == 'enabled' and not disabled ) or
            (list_type == 'disabled' and disabled )):
            plugin = {'info': toml_data_file, 'status':not disabled}
            list_of_plugins.append(plugin)
    return {'plugins': list_of_plugins,'list_type':list_type}