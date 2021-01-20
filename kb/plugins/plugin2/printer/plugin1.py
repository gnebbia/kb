    # -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb example plugin print output module (prints metadata)

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET

def metadata(args, PLUGIN_METADATA, config):
    verbose = args.get('verbose',False)

    line1 = 'Plugin Name : ' + PLUGIN_METADATA['PLUGIN_NAME'] + '-' + PLUGIN_METADATA['PLUGIN_LONG_NAME']
    line2 = 'Author      : ' + PLUGIN_METADATA['PLUGIN_AUTHOR'] + ' ' + PLUGIN_METADATA['PLUGIN_CONTACT']
    line3 = 'Version     : ' + PLUGIN_METADATA['PLUGIN_VERSION'] 
    line4 = 'Identifier  : ' + PLUGIN_METADATA['PLUGIN_GUID']
    line5 = 'Source      : ' + PLUGIN_METADATA['PLUGIN_SOURCE'] 

    if (args['no_color'] == True):
        line1 = BOLD + line1 + RESET
        line2 = BOLD + line2 + RESET
        line3 = BOLD + line3 + RESET
        line4 = BOLD + line4 + RESET
        line5 = BOLD + line5 + RESET

    print(line1)
    if verbose:
        print(line2)
        print(line3) 
        print(line4) 
        print(line5) 
    
    return(PLUGIN_METADATA)