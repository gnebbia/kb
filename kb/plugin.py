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

def loadModules(function, parser, subparsers, COMMANDS):
    res = {}
    import os
    from pathlib import Path
    # check subfolders
    lst = os.listdir(str(Path(os.getcwd(),"kb","plugins")))
    dir = []
    for d in lst:
        s = os.path.abspath(str(Path(os.getcwd(),"kb","plugins"))) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
    # load the modules
    for plugin in dir: 
        res[plugin] = __import__(str(Path("kb","plugins",plugin,"plugin_main")).replace('/','.'), fromlist = ["*"])
        if (function=='parser'):
            res[plugin].register_plugin(parser,subparsers)
        if (function=='commands'):
            res[plugin].register_command(COMMANDS)
    return res