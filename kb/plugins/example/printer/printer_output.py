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


def print_last_changed(args, results):

    from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
    import arrow
    dateformat = args['dateformat']
    last_updated = results['last_updated']
    timesince = ''
    granularity = ''
    if (args['granularity'] != ''):
        granularity = args['granularity']
    print(args)
    if (args['timesince']!=''):
        intermediate = arrow.get(results['last_updated'] ,'YYYY-MM-DD HH:mm:ss')
        if (granularity != ''):
            timesince = intermediate.humanize(granularity=granularity)
        else:
            timesince = intermediate.humanize()
    if (dateformat != ''):
        intermediate = arrow.get(results['last_updated'] ,'YYYY-MM-DD HH:mm:ss')
        last_updated = intermediate.format(dateformat)
    
    if (not args['no_color']):
        BEF=''
        AFT=''
    else:
        BEF = BOLD 
        AFT = RESET
    if (not args['verbose']):
        print(BEF + last_updated + AFT)
    else:
        print(BEF + "Artifact ID       : " + str(results['artifact'].id) + AFT)
        print(BEF + "Title             : " + results['artifact'].title + AFT)
        print(BEF + "Category          : " + results['artifact'].category + AFT)
        print(BEF + "Tags              : " + results['artifact'].tags + AFT)
        print(BEF + "Location          : " + results['document'] + AFT)
        print(BEF + "Last Updated      : " + last_updated + AFT)
        print(BEF + "Time since update : " + timesince + AFT)
        
    return None



