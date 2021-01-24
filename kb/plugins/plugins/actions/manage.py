# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager (manage plugins action)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""


from typing import Dict

def manage_plugins(args: Dict[str, str], config: Dict[str, str],filename): 
    import os
    import sys
    from pathlib import Path
    from kb.plugin import get_modules, get_plugin_status, get_plugin_info

    # Retrieve plugin entry command
    plugin_entry = get_plugin_info(filename)['parser']['entry']

    results = []
    # Get a list of modules
    mods = get_modules()

    mods_intermediate_root = str(Path(os.path.dirname(filename)))    
    for plugin in args['name']:

        if plugin not in mods:
            results.append('Plugin ' + plugin + ' is not installed.')
            continue

        # Check to see the status of this module
        disabled = get_plugin_status(plugin)

        if (args[plugin_entry] == 'disable'):

            if disabled:
                results.append('Plugin ' + plugin + ' is already disabled.')
                continue

            if not disabled:
                module_path = (str(Path(os.path.dirname(mods_intermediate_root) + os.path.sep + plugin)))
                disabled_path = str(Path(module_path, ".disabled"))
                Path(disabled_path).touch()
                results.append('Plugin ' + plugin + ' has been disabled.')               
        
        if (args[plugin_entry] == 'enable'):
            if not disabled:
                results.append('Plugin ' + plugin + ' is already enabled.')
                continue

            if disabled:
                # enable plugin here
                module_path = (str(Path(os.path.dirname(mods_intermediate_root), plugin)))
                disabled_path = str(Path(module_path, ".disabled"))
                Path(disabled_path).unlink(missing_ok=True)
                results.append('Plugin ' + plugin + ' has been enabled.')   

    return results