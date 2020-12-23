# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for stats command module

:Copyright: © 2020, alshapton.
:License: GPLv3 (see /LICENSE).
"""

import os
from typing import List
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET
from kb.entities.artifact import Artifact


def generate_stats_header(
        stats: str,
        color: bool = True):
    """
    Generates kb stats results header.

    Arguments:
    stats           - a Dictionary string of statistics
    color           - a boolean, True if color is enabled

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    header = "{kb_version}{api_version}     {last_date}    {categories}   {tags}   {artifacts}    {templates}".format(
        kb_version="Versions:  KB/".rjust(9),
        api_version="API".ljust(7),
        last_date="Last updated".rjust(13),
        categories="Categories".ljust(7),
        tags="Tags".ljust(4),
        artifacts="Artifacts".ljust(7),
        templates="Templates".ljust(7))

    summary = "{kb_version} / {api_version} {last_date} {categories} {tags} {artifacts} {templates}".format(
        kb_version=stats["Versions"]["kb"].ljust(7),
        api_version=stats["Versions"]["kbAPI"].rjust(7),
        last_date=stats["lastUpdate"].rjust(22),
        categories=str(stats["CurrentStatistics"]["Categories"]["Total"]).rjust(7),
        tags=str(stats["CurrentStatistics"]["Tags"]["Total"]).rjust(9),
        artifacts=str(stats["CurrentStatistics"]["Artifacts"]["Total"]).rjust(10),
        templates=str(stats["CurrentStatistics"]["Templates"]["Total"]).rjust(10))
    
    current = "{current}".format(
        current='Current KB: "' + stats["CurrentKB"]["Name"] + '" - ' + stats["CurrentKB"]["Description"])

    if color:
        header = UND + BOLD + header + RESET
        summary = BOLD + summary + RESET
        current = BOLD + current + RESET
        
    print(header)
    print(summary)
    print()
    print(current)


def generate_sizes(
        stats: str,
        color: bool = True):
    """
    Generates kb stats output for the component sizes.

    Arguments:
    stats           - a Dictionary string of statistics
    color           - a boolean, True if color is enabled

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    header = "{size_header} {database}  {artifacts}  {templates}   {total}".format(
        size_header="Size (bytes)".rjust(9),
        database="Database".ljust(7),
        artifacts="Artifacts".ljust(7),
        templates="Templates".ljust(7),
        total="Total".ljust(7))

    summary = "{size_header} {database}  {artifacts}  {templates}   {total}".format(
        size_header="           ",
        database=str(stats["CurrentStatistics"]["Sizes"]["Database"]).rjust(7),
        artifacts=str(stats["CurrentStatistics"]["Sizes"]["Artifacts"]).rjust(7),
        templates=str(stats["CurrentStatistics"]["Sizes"]["Templates"]).rjust(7),
        total=str(stats["CurrentStatistics"]["Sizes"]["Total"]).rjust(11))

    if color:
        header = UND + BOLD + header + RESET
        summary = BOLD + summary + RESET

    print(header)
    print(summary)
    
    
def generate_lists(
        stats: str,
        color: bool = True):
    """
    Generates kb stats lists for the tags, categories and templates.

    Arguments:
    stats           - a Dictionary string of statistics
    color           - a boolean, True if color is enabled

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    header = "{categories}           {tags}                {templates}".format(
        categories="Categories".ljust(9),
        tags="Tags".ljust(7),
        templates="Templates".ljust(7))

    if color:
        header = UND + BOLD + header + RESET

    print(header)

    # Get totals of categories, tags and templates
    categories_count = stats["CurrentStatistics"]["Categories"]["Total"]
    tags_count = stats["CurrentStatistics"]["Tags"]["Total"]
    templates_count = stats["CurrentStatistics"]["Templates"]["Total"]

    # Get the categories, tags and templates
    categories = stats["CurrentStatistics"]["Categories"]["Current"]
    tags = stats["CurrentStatistics"]["Tags"]["Current"]
    templates = stats["CurrentStatistics"]["Templates"]["Current"]

    # Find the maximum number of categories/tags/templates
    top = sorted([categories_count, tags_count, templates_count], reverse=True)
    max_number = top[0]
    max_number = int(max_number)

    # Cycle through the categories, tags and templates
    for i in range(max_number):
        try:
            cat = categories[i]
        except:
            cat = ""
        
        try:
            tag = tags[i]
        except:
            tag = ""
        
        try:
            temp = templates[i]
        except:
            temp = ""
        row = "{cat}            {tg}                {temp}".format(
            cat=cat.ljust(9),
            tg=tag.ljust(7),
            temp=temp.ljust(7))

        # Print and reset
        print(row)
        cat = ''
        tg = ''
        temp = ''


def generate_def_config(
        stats: str,
        color: bool = True):
    """
    Generates kb stats output to show the initial default config

    Arguments:
    stats           - a Dictionary string of statistics
    color           - a boolean, True if color is enabled

    Returns:
    Nothing - the screen printout is produced by this module
    """
    
    header = "{def_config}".format(
        def_config="Default Config".ljust(53))

    misc = "{db_schema} {db_schemav}       {editor}  {editorv}".format(
        db_schema="Database Schema    Version",
        db_schemav=str(stats["DEFAULT_CONFIG"]["DB_SCHEMA_VERSION"]),
        editor="Editor",
        editorv=stats["DEFAULT_CONFIG"]["EDITOR"])

    deftmp = "{deftmp} '{deftmpv}' ".format(
        deftmp="Default template  ",
        deftmpv=os.path.basename(str(stats["DEFAULT_CONFIG"]["PATH_KB_DEFAULT_TEMPLATE"])))
    
    # Default Config paths:
    home = "{home}         {homev}".format(
        home="KB Home",
        homev=str(stats["DEFAULT_CONFIG"]["PATH_KB"]))
    config = "{config}       {configv}".format(
        config="KB Config",
        configv=str(stats["DEFAULT_CONFIG"]["PATH_KB_CONFIG"]))
    data = "{data}         {datav}".format(
        data="KB Home",
        datav=str(stats["DEFAULT_CONFIG"]["PATH_KB_DATA"]))
    db = "{db}     {dbv}".format(
        db="KB Database",
        dbv=str(stats["DEFAULT_CONFIG"]["PATH_KB_DB"]))
    hist = "{hist}      {histv}".format(
        hist="KB History",
        histv=str(stats["DEFAULT_CONFIG"]["PATH_KB_HIST"]))
    tmp = "{tmp}    {tmpv}".format(
        tmp="KB Templates",
        tmpv=str(stats["DEFAULT_CONFIG"]["PATH_KB_TEMPLATES"]))

    defcats = "{defcats}".format(
        defcats="Default Categories").ljust(53)

    if color:
        header = UND + BOLD + header + RESET
        misc = BOLD + misc + RESET
        deftmp = BOLD + deftmp + RESET
        home = BOLD + home + RESET
        config = BOLD + config + RESET
        data = BOLD + data + RESET
        db = BOLD + db + RESET
        hist = BOLD + hist + RESET
        tmp = BOLD + tmp + RESET
        defcats = UND + BOLD + defcats + RESET

    print(header)
    print(misc)
    print(deftmp)
    print()
    print(home)
    print(config)
    print(data)
    print(db)
    print(hist)
    print(tmp)
    print()
    print(defcats)

    initial_categories = stats["DEFAULT_CONFIG"]["INITIAL_CATEGORIES"]
    for i in initial_categories:
        category = "{category}".format(category=i)    
        if color:
            category = BOLD + category + RESET
        print(category)
