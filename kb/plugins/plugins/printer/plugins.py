    # -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb plugins printed output module

:Copyright: © 2021, alshapton.
:License: GPLv3 (see /LICENSE).
"""

from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET

def metadata(args, PLUGIN_METADATA, config):
    line1 = 'Plugin Name : ' + PLUGIN_METADATA['PLUGIN_NAME'] + '-' + PLUGIN_METADATA['PLUGIN_LONG_NAME']
    line2 = 'Author      : ' + PLUGIN_METADATA['PLUGIN_AUTHOR'] + ' ' + PLUGIN_METADATA['PLUGIN_CONTACT']
    line3 = 'Version     : ' + PLUGIN_METADATA['PLUGIN_VERSION'] 

    if (args['no_color'] == True):
        line1 = BOLD + line1 + RESET
        line2 = BOLD + line2 + RESET
        line3 = BOLD + line3 + RESET

    print(line1)
    print(line2)
    print(line3) 
    
    return(PLUGIN_METADATA)