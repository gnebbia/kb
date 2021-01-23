# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
plugin enabler module

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

def loadModules(function, parser, subparsers, COMMANDS,config,cmd):
    res = {}
    import kb
    import os
    from pathlib import Path
    
    libdir = os.path.dirname(kb.__file__)
    # check subfolders
    lst = os.listdir(str(Path(libdir, "plugins")))
    dir = []
    for d in lst:
        s = os.path.abspath(str(Path(libdir, "plugins"))) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
    # load the modules
    for plugin in dir:
        disabled = os.path.isfile(str(Path("kb", "plugins", plugin, ".disabled")))
        if (not disabled or cmd == 'plugins'): # if this is a "plugins" command - load ALL plugins irrespective of enabled/disabled
            res[plugin] = __import__(str(Path("kb", "plugins", plugin, "plugin_main")).replace(os.path.sep, '.'), fromlist=["*"])
            if (function == 'parser'):
                res[plugin].register_plugin(parser, subparsers,config)
            if (function == 'commands'):
                res[plugin].register_command(COMMANDS,'','')
    return res
    
def load_plugin_data(which: str, toml_data_file):
    import os
    from pathlib import Path
    import toml
    try:
        toml_data = toml.load(toml_data_file)

        if (which == 'metadata'):
            PLUGIN_METADATA={
                'PLUGIN_NAME':toml_data['config']['name'],
                'PLUGIN_VERSION':toml_data['config']['version'],
                'PLUGIN_GUID':toml_data['config']['guid'],
                'PLUGIN_SOURCE':toml_data['metadata']['source'],
                'PLUGIN_LONG_NAME':toml_data['config']['help'],
                'PLUGIN_AUTHOR':toml_data['metadata']['author'],
                'PLUGIN_CONTACT':toml_data['metadata']['contact']
            }
            return PLUGIN_METADATA
        if (which == 'config'):
            PLUGIN_CONFIG={
                'PLUGIN_NAME':toml_data['config']['name'],
                'PLUGIN_VERSION':toml_data['config']['version'],
                'PLUGIN_GUID':toml_data['config']['guid'],
                'PLUGIN_HELP':toml_data['config']['help']
            }
            return PLUGIN_CONFIG
    except toml.TomlDecodeError:
        print("Error: The plugin config data is not in the toml format")
    except FileNotFoundError:
        print("Error: The plugin config data is not in the toml format")
        return('')


def metadata(args, config, TOML_DATA_FILE,status,list_type):
    PLUGIN_METADATA=load_plugin_data('metadata',TOML_DATA_FILE)
    print_metadata(args, PLUGIN_METADATA, config,status,list_type)
    return PLUGIN_METADATA


def register_command(COMMANDS:dict,TOML_DATA_FILE,fn):
    PLUGIN_CONFIG=load_plugin_data('config',TOML_DATA_FILE)
    if (PLUGIN_CONFIG.get('PLUGIN_NAME','') !=''):
        COMMANDS[PLUGIN_CONFIG.get('PLUGIN_NAME')] = fn 
    return COMMANDS


def print_metadata(args, PLUGIN_METADATA, config,status,list_type):
    from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
    if (status == True):
        status_text = 'Enabled'
    else:
        status_text = 'Disabled'

    verbose = args.get('verbose',False)
    line1 = 'Plugin Name : ' + PLUGIN_METADATA['PLUGIN_NAME'] 
    line2 = 'Description : ' + PLUGIN_METADATA['PLUGIN_LONG_NAME']
    line3 = 'Author      : ' + PLUGIN_METADATA['PLUGIN_AUTHOR']
    line4 = 'Contact     : ' + PLUGIN_METADATA['PLUGIN_CONTACT']
    line5 = 'Version     : ' + PLUGIN_METADATA['PLUGIN_VERSION']
    line6 = 'Identifier  : ' + PLUGIN_METADATA['PLUGIN_GUID']
    line7 = 'Source      : ' + PLUGIN_METADATA['PLUGIN_SOURCE'] 
    line8 = 'Status      : ' + status_text 
    
    if (args.get('no_color',True) == True):
        line1 = BOLD + line1 + RESET
        line2 = BOLD + line2 + RESET
        line3 = BOLD + line3 + RESET
        line4 = BOLD + line4 + RESET
        line5 = BOLD + line5 + RESET
        line6 = BOLD + line6 + RESET
        line7 = BOLD + line7 + RESET
        line8 = BOLD + line8 + RESET

    print(line1)
    print(line2)
    if verbose:
        print(line3) 
        print(line4)
        print(line5)
        print(line6)
        print(line7)
        if (status != ''):
            print(line8)
    print()
    
    return None

def get_modules():
    import os
    import re
    import sys
    
    modules = [m.__name__[:-12] for m in sys.modules.values() if (re.search(r"plugin_main$", m.__name__) and ('plugins.plugin_main' not in m.__name__))]
    mods = []
    for _module in modules:
        mod = os.path.basename(_module.replace(".",os.path.sep))
        mods.append(mod)
    return mods

def get_plugin_status(plugin_name:str):
    import os
    from pathlib import Path
    mods_intermediate_root = str(Path(os.path.dirname(__file__),"plugins",plugin_name))    
    module_path = (str(Path(os.path.dirname(mods_intermediate_root) + os.path.sep + plugin_name)))
    return os.path.exists(str(Path(module_path, ".disabled")))
    

def get_plugin_info(filename):
    
    import os
    from pathlib import Path
    import toml
    
    # Read config.toml file to retrieve commands
    try:
        toml_data = toml.load(str(Path(os.path.dirname(filename), "config.toml")))
    except toml.TomlDecodeError:
        print("Error: The plugin config data is not in the toml format")
    except FileNotFoundError:
        return('')
    return toml_data

def get_plugin_commands(filename):
    
    import os
    from pathlib import Path
    import toml

    # Read config.toml file to retrieve commands
    try:
        toml_data = toml.load(str(Path(os.path.dirname(filename), "config.toml")))
    except toml.TomlDecodeError:
        print("Error: The plugin config data is not in the toml format")
    except FileNotFoundError:
        return('')
    commands = toml_data['commands']
    # formulate the list of new plugin commands with their respective functions
    # read from the config file.
    cmds = []
    for command in commands:
        cmd = [command['command'] , command['function']]
        cmds.append(cmd)
    return cmds