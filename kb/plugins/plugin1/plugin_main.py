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
from typing import Dict
import kb.initializer as initializer
from kb.cl_parser import parse_args
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.plugins.plugins.printer.plugins import metadata as print_metadata

__version__ = '0.0.1'

"""
Brief instructions:

Pre-requisites
--------------
You'll need a local install of the latest kb software (0.1.6 or above) to allow your plugin to reside within the 
tree in the correct location. 'pip -e install kb-manager' will do this.

Folder structure
----------------
Ensure that your plugin folder structure is as follows:

plugins
├── __init__.py
└── plugin1
    ├── __init__.py
    └── plugin_main.py

As you see, the example 'plugin1' is simply a folder WITHIN the plugins folder.
It MUST have a blank __init__.py
It MUST have a 'plugin_main.py' similar to this.
You can if you wish add oother python files within this folder and/or create a folder structure WITHIN. 
ALL content for each plugin MUST be kept within the folder.

Coding
------
Ensure that __version__ to the correct version in semver notation (above)
Modify PLUGIN_CONFIG keys to your plugin specification
        
        PLUGIN_NAME     - Name of the plugin - should be a UNIQUE single word (please check if anyone else has chosen this name first)
        PLUGIN_LONG_NAME- Longer description of the plugin
        PLUGIN_HELP     - Small message explaining what the plugin does

Modify ONLY these PLUGIN_METADATA keys to your plugin specification

        PLUGIN_AUTHOR    - Name of the authors
        PLUGIN_CONTACT   - eMail address of the author
        PLUGIN_LONG_NAME - Description of the plugin

Do NOT modify or delete the following functions:
    register_command
    metadata

Modify the register_plugin function as detailed therein, but do NOT delete it.

Complete other minoor modifications as detailed throughout the code.

Add functionality as shown........
"""


PLUGIN_CONFIG={
    'PLUGIN_NAME':'plugin1',
    'PLUGIN_VERSION':__version__,
    'PLUGIN_HELP':'A new command',
}
PLUGIN_METADATA={
    'PLUGIN_NAME':PLUGIN_CONFIG['PLUGIN_NAME'],
    'PLUGIN_VERSION':PLUGIN_CONFIG['PLUGIN_VERSION'],
    'PLUGIN_LONG_NAME':'A skeleton plugin to illustrate how to write a kb plugin',
    'PLUGIN_AUTHOR':'Andrew Shapton',
    'PLUGIN_CONTACT':'alshapton@gmail.com'
    }

def register_plugin(parser:argparse, subparsers):
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
        'plugin1', help='Example plugin')  
    plugin1_subparsers = plugin1_parser.add_subparsers(help='Plugin 1 commands', dest="plugin1_command") # See below (1)
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

def register_command(COMMANDS:dict):
    # DO NOT MODIFY THIS FUNCTION, except where indicated #
    if (PLUGIN_CONFIG.get('PLUGIN_NAME','') !=''):
        COMMANDS[PLUGIN_CONFIG.get('PLUGIN_NAME')] = plugin1 # This HAS to be the plugin name #
    return COMMANDS

def metadata(args, config):
    # DO NOT MODIFY THIS FUNCTION #
    if (args.get('output',False) == True):
        print_metadata(args, PLUGIN_METADATA, config)
    return(PLUGIN_METADATA)

# Add/modify this to include your new plugin's functionality
def newcommand(args: Dict[str, str], config: Dict[str, str]): 
    print('New command')
    return None

def plugin1(args: Dict[str, str], config: Dict[str, str]):   # Change this function name to be the plugin name and retain the structure #
    
    # Check initialization
    initializer.init(config)

    cmd=args['plugin1_command'] # Change this to be <your_plugin_name>_command (also - see above (1) - change that too)
    CMDS = {
        'metadata': metadata,
        'newcommand': newcommand         
    }                           # Add any new commands in here together with their respective functions
    CMDS[cmd](args, config)
   

