# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Example plugin template

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import argparse
import os
from pathlib import Path

from typing import Dict
from kb.cl_parser import parse_args

import kb.initializer as initializer
import kb.plugin as utils
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET

from .commands.newcommand import newcommand

__version__ = '0.0.1'

TOML_DATA_FILE = str(Path(os.path.dirname(__file__), "config.toml"))

PLUGIN_CONFIG = {}
PLUGIN_METADATA = {}

"""
Brief instructions:

Pre-requisites
--------------
You'll need a local install of the latest kb software (0.1.6 or above) to allow your plugin to reside within the 
tree in the correct location. 'pip -e install kb-manager' will do this.

Folder structure
----------------
Ensure that your plugin folder structure is as follows:

plugin1
├── __init__.py
├── actions
│   ├── __init__.py
│   └── newcommand.py
├── commands
│   ├── __init__.py
│   └── newcommand.py
├── plugin_main.py
└── printer
    ├── __init__.py
    └── plugin1.py

As you see, the example 'plugin1' is simply a folder WITHIN the plugins folder.
It MUST have a blank __init__.py
It MUST have a 'plugin_main.py' similar to this.
You MUST have a 'commands' folder which will house the code for the CLI entry to your plugin
You MUST have an 'actions' folder which will house the code for the core functionality of your plugin
You MUST have an 'api' folder which will house the entry point for the API call to your function.

Take note of the standard names, and instructions within each sample Python program to understand what
    should be placed where
    
ALL content for each plugin MUST be kept within the folder.

Coding
------
Ensure that __version__ to the correct version in semver notation (above)
Modify PLUGIN_CONFIG keys to your plugin specification
        
        PLUGIN_NAME     - Name of the plugin - should be a UNIQUE single word (please check if anyone else has chosen this name first)
        PLUGIN_LONG_NAME- Longer description of the plugin
        PLUGIN_GUID     - An unique identifier (get one from https://guidgenerator.com - simply press the "Generate somoe GUIDs!" button with defaults)
        PLUGIN_HELP     - Small message explaining what the plugin does

Modify ONLY these PLUGIN_METADATA keys to your plugin specification

        PLUGIN_AUTHOR    - Name of the authors
        PLUGIN_CONTACT   - eMail address of the author
        PLUGIN_SOURCE    - Address of publicly available source code
        PLUGIN_LONG_NAME - Description of the plugin

Do NOT modify or delete the following functions:
    register_command
    metadata

Modify the register_plugin function as detailed therein, but do NOT delete it.

Complete other minor modifications as detailed throughout the code.

Add functionality as shown........
"""


def register_plugin(parser:argparse, subparsers,config):
    '''
    Changes required for your plugin:
    * Change instances of plugin1_parser to <your_plugin_name>_parser
    * Change all quoted references to "plugin1" to "<your_plugin_name>"
    * Change instances of plugin1_subparsers to <your_plugin_name>_subparsers
    * Change instances of plugin1_parser_metadata to <your_plugin_name>_parser_metadata
    * Amend all 'help' messages to reflect your plugin's functionality
    * Ensure that you do not remove references in the parsers to the core required functionality

    '''
    plugin1_parser = subparsers.add_parser(
        'plugin2', help='Example plugin')  
    plugin1_subparsers = plugin1_parser.add_subparsers(dest="plugin2_command") # See below (1)
    plugin1_subparsers.required = True
    
    plugin1_parser.add_argument(
        "--version",
        action="version",
        version="Plugin: {} - {}".format(PLUGIN_CONFIG.get('PLUGIN_NAME',''),__version__))

    
    _plugin1_parser_metadata = plugin1_subparsers.add_parser('metadata', help='Show this plugin\'s metadata')
    _plugin1_parser_metadata.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    _plugin1_parser_metadata.add_argument(
        "-s", "--silent",
        help="Produce no output",
        action='store_false',
        dest='output',
        default=True)
    _plugin1_parser_metadata.add_argument(
        "-v", "--verbose",
        help="Display full metadata",
        action='store_true',
        dest='verbose',
        default=False)

    _plugin1_parser_newcommand = plugin1_subparsers.add_parser('newcommand', help='An example new coommand')
      
    '''
    # Example structure for a new command - add as many of these as you need - following the naming structures 
    # as described above
    _<your_plugin_name>_<your_new_command> = <your_plugin_name>_subparsers.add_parser('<your_new_command>', help='A new Command')
    _<your_plugin_name>_parser_<your_new_command>.add_argument(
        "<your_new_command_abbreviation>", "<your_new_command>",
        help="Command Help",
        action='store_false',
        dest='xxxx',
        default=True)
        # Change these as per Python's parser features (https://docs.python.org/3/library/argparse.html)
    '''
    return subparsers


def register_command(COMMANDS:dict,TOML_DATA_FILE,fn):
        return utils.register_command(COMMANDS,str(Path(os.path.dirname(__file__), "config.toml")),entry)


def metadata(args, config):
    from kb.plugin import metadata as print_metadata
    return print_metadata(args, config, TOML_DATA_FILE,'','')


def entry(args: Dict[str, str], config: Dict[str, str]):   # Change this function name to be the plugin name and retain the structure #
    
    # Check initialization
    initializer.init(config)

    cmd=args['plugin2_command'] # Change this to be <your_plugin_name>_command (also - see above (1) - change that too)
    CMDS = {
        'metadata': metadata,
        'newcommand': newcommand         
    }     
    CMDS[cmd](args, config)
   

