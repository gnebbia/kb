# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Example plugin

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import argparse
from typing import Dict


def register_plugin(parser:argparse, subparsers, config):
    from kb.plugin import get_plugin_info
    
    # DO NOT EDIT THIS PART OF THE FUNCTION
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

# ==========================================#
# YOU WILL NEEED TO EDIT THE FILE FROM HERE #
# ==========================================#

    # ADD YOUR PARSER CODE HERE:
    """
    Below: you should :
    * Create parsers with the name " _parser_<command_name> "
    * Use the "argparse"-style of syntax for construction to built parsers (see https://docs.python.org/3/library/argparse.html)

    """
    # User-supplied commands
    _parser_lastchanged = globals()[PS].add_parser('lastchanged', help='Show the last changed information for an artifact')
    _parser_lastchanged.add_argument(
        "id",
        help="article ID",
        )
    _parser_lastchanged.add_argument(
        "-v", "--verbose",
        help="Show ALL document information",
        action='store_true',
        dest='verbose',
        default=False)   
    _parser_lastchanged.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True)
    _parser_lastchanged.add_argument(
        "-d", "--dateformat",
        help="Format date/time in Arrow format",
        nargs='?',
        dest='dateformat',
        default='')
    _parser_lastchanged.add_argument(
        "-t", "--timesince",
        help="Show time since last change",
        action='store_true',
        dest='timesince',
        default='')
    _parser_lastchanged.add_argument(
        "-g", "--granularity",
        help="Indicate granularity of time since last change",
        nargs='*',
        dest='granularity',
        default='')

    return subparsers


# START OF USER FUNCTIONS

"""
You will need to:
 * Create Functions here for each of the commands you define
   (there are always 2 arguments - args & config)
 * Import the corresponding function to carry out the commnd from the "commands" module
 * You will need to return a "results" object (content is user-definable)
""" 

def show_lastchange(args: Dict[str, str], config: Dict[str, str]): 
    from kb.plugins.example.commands.lastchanged import last_changed
    results = last_changed(args,config)
    return results

# END OF USER FUNCTIONS




# =======================================#
# DO NOT EDIT ANY FURTHER IN THIS FILE ! #
# =======================================#


def register_command(COMMANDS:dict,_None,fn):
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !
    import os
    from pathlib import Path
    import kb.plugin as utils
    return utils.register_command(COMMANDS,str(Path(os.path.dirname(__file__), "config.toml")),entry) 


def metadata(args, config):
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !
    import os
    from pathlib import Path
    from kb.plugin import metadata as print_metadata
    return print_metadata(args, config, str(Path(os.path.dirname(__file__), "config.toml")),'','')


def entry(args: Dict[str, str], config: Dict[str, str]):   
    # DO NOT EDIT THIS FUNCTION IN ANY WAY !
    import kb.initializer as initializer
    from kb.plugin import get_plugin_commands,get_plugin_info

    # Get this plugin's location
    filename = __file__

    # Check initialization
    initializer.init(config)
    
    # Initialize empty list of commands for this plugin to populate
    icmds = {}

    # Retrieve list of commands for this plugin
    plugin_commands = get_plugin_commands(filename)
    
    # Assemble the list of commands for this plugin
    # and append to the mandatory metadata command
    for icmd in plugin_commands:
        comm = {icmd[0] : globals()[icmd[1]]}
        icmds.update(comm)

    # Retrieve the parser entry point for this plugin
    plugin_entry = get_plugin_info(filename)['parser']['entry']

    cmd = args[plugin_entry] 
    CMDS = {
        'metadata': metadata 
    }        
    # Combine mandatory commands with user-supplied commands                  
    CMDS.update(icmds) 
    CMDS[cmd](args, config)
   

