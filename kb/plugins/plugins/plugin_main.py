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

from kb.cl_parser import parse_args
import kb.initializer as initializer
from kb.plugin import get_plugin_status, get_plugin_commands, get_plugin_info
from .printer.printer_output import print_list


PLUGIN_CONFIG = {}
PLUGIN_METADATA = {}

TOML_DATA_FILE = str(Path(os.path.dirname(__file__), "config.toml"))

def register_plugin(parser:argparse, subparsers, config):
    # Get overall content for registratioon of plugin
    info = get_plugin_info(__file__)
    # Get main parser information
    prsr = info['parser']
    P = prsr['prefix'] + "_parser"
    PS = prsr['prefix'] + '_subparsers'
    # Create parsers
    globals()[P] = subparsers.add_parser(prsr['prefix'], help=prsr['help'])  
    globals()[PS] = globals()[P].add_subparsers(help=prsr['detail'], dest=prsr['entry'])
    globals()[PS].required = True
    
    # Create subparsers
    # Create MANDATORY metadata parser - this NEVER changes
    _parser_metadata = globals()[PS].add_parser('metadata', help='Show this plugin\'s metadata')
    _parser_metadata.add_argument(
        "-v", "--verbose",
        help="Show ALL plugin information",
        action='store_true',
        dest='verbose',
        default=False)
    _parser_metadata.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    # End of MANDATORY metadata parser

    # User-supplied commands
    _parser_list = globals()[PS].add_parser('list', help='Show information about plugins')
    _parser_list.add_argument(
        "-v", "--verbose",
        help="Show ALL plugin information",
        action='store_true',
        dest='verbose',
        default=False)
    _parser_list.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    _parser_list.add_argument(
        '-s','--status',
        choices = ['enabled', 'disabled', 'all'],
        help = 'list enabled, disabled, or all (default)',
        default = 'all')

    _plugins_parser_disable = globals()[PS].add_parser('disable', help='Disable an installed plugin')
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
    
    _plugins_parser_enable = globals()[PS].add_parser('enable', help='Enable an installed plugins')
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


def manage_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path
    from kb.plugin import get_modules

    # Retrieve plugin entry command
    plugin_entry = get_plugin_info(__file__)['parser']['entry']

    results = []
    # Get a list of modules
    mods = get_modules()

    mods_intermediate_root = str(Path(os.path.dirname(__file__)))    
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

    print_list(args,config,results)
    return results

def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    from kb.plugins.plugins.commands.list import list_plugins as get_list_of_plugins
    get_list_of_plugins(args,config)
    return None


def register_command(COMMANDS:dict,TOML_DATA_FILE,fn):
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !
    import kb.plugin as utils
    return utils.register_command(COMMANDS,str(Path(os.path.dirname(__file__), "config.toml")),entry) 


def metadata(args, config):
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !
    from kb.plugin import metadata as print_metadata
    return print_metadata(args, config, TOML_DATA_FILE,'','')


def entry(args: Dict[str, str], config: Dict[str, str]):   
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !

    # Check initialization
    initializer.init(config)

    # Initialize empty list of commands for this plugin to populate
    icmds = {}

    # Retrieve list of commands for this plugin
    plugin_commands = get_plugin_commands(__file__)
    # Retrieve the parser entry point for this plugin
    plugin_entry = get_plugin_info(__file__)['parser']['entry']
    
    # Assemble the list of commands for this plugin
    # and append to the mandatory metadata command
    for icmd in plugin_commands:
        comm = {icmd[0] : globals()[icmd[1]]}
        icmds.update(comm)

    cmd = args[plugin_entry] 
    CMDS = {
        'metadata': metadata 
    }        
    # Combine mandatory commands with user-supplied commands                  
    CMDS.update(icmds) 
    CMDS[cmd](args, config)
   

