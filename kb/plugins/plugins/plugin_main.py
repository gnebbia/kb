# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Plugin extension manager

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import argparse
import os
from pathlib import Path
import re
from typing import Dict

import kb.initializer as initializer
from kb.cl_parser import parse_args
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET

list_of_plugins = {}

PLUGIN_CONFIG = {}
PLUGIN_METADATA = {}

TOML_DATA_FILE = str(Path(os.path.dirname(__file__), "config.toml"))


def register_plugin(parser:argparse, subparsers, config):
    
    # Create parsers
    plugins_parser = subparsers.add_parser(
        'plugins', help='Manage plugins')  
    plugins_subparsers = plugins_parser.add_subparsers(help='Commands to manage plugins', dest="plugins_command")
    plugins_subparsers.required = True
    
    _plugins_parser_metadata = plugins_subparsers.add_parser('metadata', help='Show this plugin\'s metadata')
    _plugins_parser_metadata.add_argument(
        "-v", "--verbose",
        help="Show ALL plugin information",
        action='store_true',
        dest='verbose',
        default=False)
    _plugins_parser_metadata.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)

    _plugins_parser_list = plugins_subparsers.add_parser('list', help='Show the installed plugins')
    _plugins_parser_list.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    _plugins_parser_list.add_argument(
        "-s",'--status',
        default='all',
        choices=['enabled', 'disabled', 'all'],
        help='list enabled, disabled, or all (default: %(default)s)')
    _plugins_parser_list.add_argument(
        "-v", "--verbose",
        help="Show ALL plugin information",
        action='store_true',
        dest='verbose',
        default=False)

    _plugins_parser_disable = plugins_subparsers.add_parser('disable', help='Disable an installed plugins')
    _plugins_parser_disable.add_argument(
        "name",
        help="Name of plugin to disable",
        type=str,
        nargs="*")
    
    _plugins_parser_disable.add_argument(
        "-v", "--verbose",
        help="Be verbose in response",
        action='store_true',
        dest='verbose',
        default=False)
    
    _plugins_parser_enable = plugins_subparsers.add_parser('enable', help='Enable an installed plugins')
    _plugins_parser_enable.add_argument(
        "name",
        help="Name of plugin to enable",
        type=str,
        nargs="*")
    
    _plugins_parser_enable.add_argument(
        "-v", "--verbose",
        help="Be verbose in response",
        action='store_true',
        dest='verbose',
        default=False)

    return subparsers

# DO NOT EDIT THESE FUNCTIONS
def register_command(COMMANDS:dict,TOML_DATA_FILE,fn):
    import kb.plugin as utils
    return utils.register_command(COMMANDS,str(Path(os.path.dirname(__file__), "config.toml")),entry) 

def metadata(args, config):
    from kb.plugin import metadata as print_metadata
    return print_metadata(args, config, TOML_DATA_FILE,'','')
# DO NOT EDIT THE ABOVE FUNCTIONS

def get_modules():
    import sys

    modules = [m.__name__[:-12] for m in sys.modules.values() if (re.search(r"plugin_main$", m.__name__) and ('plugins.plugin_main' not in m.__name__))]
    mods=[]
    for _module in modules:
        mod = os.path.basename(_module.replace(".",os.path.sep))
        mods.append(mod)
    return mods


def disable_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path
    
    mods=get_modules()

    mods_intermediate_root = str(Path(os.path.dirname(__file__)))    
    for plugin in args['name']:
        if plugin not in mods:
            print('Plugin ' + plugin + ' is not installed.')
            continue

        module_path = (str(Path(os.path.dirname(mods_intermediate_root) + os.path.sep + plugin)))

        # Check to see the status of this module
        disabled_path = str(Path(module_path, ".disabled"))
        disabled = os.path.exists(str(Path(module_path, ".disabled")))

        if disabled:
            print('Plugin ' + plugin + ' is already disabled.')
            continue

        if not disabled:
            Path(disabled_path).touch()
            print('Plugin ' + plugin + ' has been disabled.')

    return None

def enable_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path
    
    mods=get_modules()

    mods_intermediate_root = str(Path(os.path.dirname(__file__)))    
    for plugin in args['name']:
        if plugin not in mods:
            print('Plugin ' + plugin + ' is not installed.')
            continue

        module_path = (str(Path(os.path.dirname(mods_intermediate_root) + os.path.sep + plugin)))

        # Check to see the status of this module
        disabled_path = str(Path(module_path, ".disabled"))
        disabled = os.path.exists(str(Path(module_path, ".disabled")))
        if not disabled:
            print('Plugin ' + plugin + ' is already enabled.')
            continue

        if disabled:
            # enable plugin here
            Path(disabled_path).unlink(missing_ok=True)
            print('Plugin ' + plugin + ' has been enabled.')
            
    return None

def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path

    from kb.plugin import metadata as print_metadata

    list_type = str(args["status"])
    modules = [m.__name__[:-12] for m in sys.modules.values() if (re.search(r"plugin_main$", m.__name__) and ('plugins.plugin_main' not in m.__name__))]
    for _module in modules:
        args['output'] = False
        mod = os.path.basename(_module.replace(".",os.path.sep))
        mods_intermediate_root = str(Path(os.path.dirname(__file__)))
        module_path=(str(Path(os.path.dirname(mods_intermediate_root)+ os.path.sep + mod)))
        toml_data_file = str(Path(module_path, "config.toml"))
        
        # Check to see if this module should be included in the list
        disabled = os.path.isfile(str(Path(module_path, ".disabled")))
        if ((list_type == 'all' ) or
            (list_type == 'enabled' and disabled == False) or
            (list_type == 'disabled' and disabled == True)):
            print_metadata(args, config, toml_data_file,not disabled,list_type)
            print()
    return None


def entry(args: Dict[str, str], config: Dict[str, str]):   
    
    # Check initialization
    initializer.init(config)

    cmd = args['plugins_command'] 
    CMDS = {
        'metadata': metadata, # DO NOT REMOVE
        'list': list_plugins,
        'disable': disable_plugins,
        'enable': enable_plugins         
    }                          
    CMDS[cmd](args, config)
   

