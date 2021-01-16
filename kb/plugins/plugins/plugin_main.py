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
import re
from typing import Dict
import kb.initializer as initializer
from kb.cl_parser import parse_args
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.plugins.plugins.printer.plugins import metadata as print_metadata

__version__ = '0.0.0'

list_of_plugins = {}

PLUGIN_CONFIG={
    'PLUGIN_NAME':'plugins',
    'PLUGIN_VERSION':__version__,
    'PLUGIN_HELP':'Plugin Manager for kb',
}
PLUGIN_METADATA={
    'PLUGIN_NAME':PLUGIN_CONFIG['PLUGIN_NAME'],
    'PLUGIN_VERSION':PLUGIN_CONFIG['PLUGIN_VERSION'],
    'PLUGIN_LONG_NAME':'Plugin Manager for kb',
    'PLUGIN_AUTHOR':'Andrew Shapton',
    'PLUGIN_CONTACT':'alshapton@gmail.com'
    }

regex = r"plugin_main$"

def register_plugin(parser:argparse, subparsers):
    
    plugins_parser = subparsers.add_parser(
        'plugins', help='Manage plugins')  
    plugins_subparsers = plugins_parser.add_subparsers(help='Commands to manage plugins', dest="plugins_command")
    plugins_subparsers.required = True
    
    _plugins_parser_metadata = plugins_subparsers.add_parser('metadata', help='Show this plugin\'s metadata')

    _plugins_parser_list = plugins_subparsers.add_parser('list', help='Show the installed plugins')
    _plugins_parser_list.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    _plugins_parser_list.add_argument(
        "-v", "--verbose",
        help="Show ALL plugin information",
        action='store_true',
        dest='verbose',
        default=False)
    return subparsers

def register_command(COMMANDS:dict):
    if (PLUGIN_CONFIG.get('PLUGIN_NAME','') !=''):
        COMMANDS[PLUGIN_CONFIG.get('PLUGIN_NAME')] = plugins 
    return COMMANDS

def metadata(args, config):
    print_metadata(args, PLUGIN_METADATA, config)
    return(PLUGIN_METADATA)


def list_plugins(args: Dict[str, str], config: Dict[str, str]): 
    import sys
    from pathlib import Path
    
    modules = [m.__name__[:-12] for m in sys.modules.values() if (re.search(regex, m.__name__) and ('plugins.plugin_main' not in m.__name__))]
    
    for module in modules:
        plugin_main_full = module + '.plugin_main'
        this_plugin_main = __import__(str(Path(plugin_main_full)), fromlist = ["*"])
        args['output'] = False
        _M = this_plugin_main.metadata(args, config)
        list_of_plugins[_M['PLUGIN_NAME']]=(_M)
        print_metadata(args, _M, config)
        print()
    return None


def plugins(args: Dict[str, str], config: Dict[str, str]):   # Change this function name to be the plugin name and retain the structure #
    
    # Check initialization
    initializer.init(config)

    cmd = args['plugins_command'] 
    CMDS = {
        'metadata': metadata,
        'list': list_plugins         
    }                          
    CMDS[cmd](args, config)
   

