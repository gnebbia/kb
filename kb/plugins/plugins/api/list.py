# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager (list plugins api)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""
def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path
    from kb.plugin import metadata as print_metadata, get_modules

    list_type = str(args.get("status","all"))

    # Get a list of installed plugins
    plugins = get_modules()

    # Cycle through the available plugins and display their metadata
    for plugin in plugins:
        toml_data_file=(str(Path(os.path.dirname(str(Path(os.path.dirname(__file__)))), plugin,'config.toml')))
    
        # Check to see if this module should be included in the list
        disabled = get_plugin_status(plugin)
        if ((list_type == 'all' ) or
            (list_type == 'enabled' and not disabled ) or
            (list_type == 'disabled' and disabled )):
            print_metadata(args, config, toml_data_file,not disabled,list_type)
            print()
    return None