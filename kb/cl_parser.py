# -*- encoding: utf-8 -*-
# kb v0.1.5
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Command Line Parsing Module for kb

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import argparse
import sys
from typing import Sequence

from kb import __version__
from kb.config import DEFAULT_CONFIG,DEFAULT_KNOWLEDGEBASE


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    """
    This function parses the arguments which have been passed from the command
    line, these can be easily retrieved for example by using "sys.argv[1:]".
    It returns an argparse Namespace object.

    Arguments:
    args -- the list of arguments passed from the command line as the sys.argv
            format

    Returns:
    An argparse Namespace object with the provided arguments, which
    can be used in a simpler format.
    """
    parser = argparse.ArgumentParser(prog='kb',
                                     description='A knowledge base organizer')
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__))

   

    subparsers = parser.add_subparsers(help='commands', dest="command")
    subparsers.required = True

    
    # Main Commands
    add_parser = subparsers.add_parser(
        'add', help='Add an artifact')
    base_parser = subparsers.add_parser(
        'base', help='Manage knowledge bases')    
    delete_parser = subparsers.add_parser(
        'delete', help='Delete artifacts')
    edit_parser = subparsers.add_parser(
        'edit', help='Edit an artifact content')    
    erase_parser = subparsers.add_parser(
        'erase', help='Erase the entire kb knowledgebase')
    export_parser = subparsers.add_parser(
        'export', help='Export the knowledge base')
    grep_parser = subparsers.add_parser(
        'grep', help='Grep through kb artifacts')
    help_parser = subparsers.add_parser(
        'help', help='Show help of a particular command')
    import_parser = subparsers.add_parser(
        'import', help='Import a knowledge base')
    list_parser = subparsers.add_parser(
        'list', help='Search for artifacts')
    stats_parser = subparsers.add_parser(
        'stats', help='Show stats for the knowledgebase')
    template_parser = subparsers.add_parser(
        'template', help='Manage templates for artifacts')
    update_parser = subparsers.add_parser(
        'update', help='Update artifact properties')
    view_parser = subparsers.add_parser(
        'view', help='View artifacts')

    # add parser
    add_parser.add_argument(
        "file",
        help="Path of the file to add to kb as artifact",
        type=str,
        nargs="*",
    )
    add_parser.add_argument(
        "-t", "--title",
        help="Title of the added artifact",
        type=str,
    )
    add_parser.add_argument(
        "-c", "--category",
        help="Category associated to the artifact",
        default="default",
        type=str,
    )
    add_parser.add_argument(
        "-g", "--tags",
        help="""
        Tags to associate to the artifact in the form \"tag1;tag2;...;tagN\"
        """,
        type=str,
    )
    add_parser.add_argument(
        "-a", "--author",
        help="Author of the artifact",
        type=str,
    )
    add_parser.add_argument(
        "-s", "--status",
        help="Status of the artifact",
        type=str,
    )
    add_parser.add_argument(
        "--template",
        help="Template to apply to the artifact",
        type=str,
    )
    add_parser.add_argument(
        "-b", "--body",
        help="Body of the artifact",
        type=str,
    )


    # base parser
    base_subparsers = base_parser.add_subparsers(help='base commands', dest="base_command")
    base_subparsers.required = True


    # base subcommands
    current_base_parser = base_subparsers.add_parser('current', help='Show the currently active knowledge base')
    delete_base_parser = base_subparsers.add_parser('delete', help='Delete a knowledge base')
    list_base_parser = base_subparsers.add_parser('list', help='Show available knowledge bases')
    new_base_parser = base_subparsers.add_parser('new', help='Creeate a new knowledge base')
    switch_base_parser = base_subparsers.add_parser('switch', help='Switch to a named knowledge base')
    rename_base_parser = base_subparsers.add_parser('rename', help='Rename the current knowledge base')

    rename_base_parser.add_argument(
        help="Name of the original knowledge base",
        action='store',
        dest='old',
        metavar='<old>',
        default='',
    )

    rename_base_parser.add_argument(
        help="Name of the new knowledge base",
        action='store',
        dest='new',
        metavar='<new>',        
        default='',
    )

    rename_base_parser.add_argument(
        "-d","--description",
        help="Description of the renamed knowledge base",
        action='store',
        dest='description',
        metavar='<description>',
        default='',
    )

    new_base_parser.add_argument(
        help="Name of the new knowledge base",
        action='store',
        dest='name',
        default='new',
    )

    delete_base_parser.add_argument(
        help="Knowledge base to delete",
        action='store',
        dest='name',
        default='',
    )
    
    new_base_parser.add_argument(
        "-d","--description",
        help="Description of the new knowledge base",
        action='store',
        dest='description',
        default='',
    )

    switch_base_parser.add_argument(
        help="knowledge base to switch to",
        action='store',
        dest='kb',
        default=DEFAULT_KNOWLEDGEBASE,
    )
  
    list_base_parser.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True,
    )

    current_base_parser.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True,
    )

    # delete parser
    delete_parser.add_argument(
        "-i", "--id",
        help="ID of the artifact",
        type=str,
        nargs='*',
    )
    delete_parser.add_argument(
        "-t", "--title",
        help="Title of the artifact to remove",
        default=None,
        type=str,
    )
    delete_parser.add_argument(
        "-c", "--category",
        help="Category associated to the artifact to remove",
        default=None,
        type=str,
    )

    # edit parser
    edit_parser.add_argument(
        "nameid",
        help="Title or ID of the artifact to edit",
        type=str,
        nargs="?",
    )
    edit_parser.add_argument(
        "-i", "--id",
        help="ID of the artifact to edit",
        type=str,
    )
    edit_parser.add_argument(
        "-t", "--title",
        help="Title to update",
        default=None,
        type=str,
    )
    edit_parser.add_argument(
        "-c", "--category",
        help="Category to update",
        default=None,
        type=str,
    )
    edit_parser.add_argument(
        "-g", "--tags",
        help="Tags to update in the form \"tag1;tag2;...;tagN\"",
        default=None,
        type=str,
    )
    edit_parser.add_argument(
        "-a", "--author",
        help="Author to update",
        default=None,
        type=str,
    )
    edit_parser.add_argument(
        "-s", "--status",
        help="Status to update",
        default=None,
        type=str,
    )

    # grep parser
    grep_parser.add_argument(
        "regex",
        help="Filter search results by specified regex",
        type=str,
    )
    grep_parser.add_argument(
        "-c", "--category",
        help="Filter search results by specified category",
        default=None,
        type=str,
    )
    grep_parser.add_argument(
        "-g", "--tags",
        help="""
        Tags associates to the artifact to search in the form \"tag1;tag2;...;tagN\"
        """,
        default=None,
        type=str,
    )
    grep_parser.add_argument(
        "-a", "--author",
        help="Filter search results by specified author",
        default=None,
        type=str,
    )
    grep_parser.add_argument(
        "-s", "--status",
        help="Filter search results by specified status",
        default=None,
        type=str,
    )
    grep_parser.add_argument(
        "-m", "--show-matches",
        help="Show text matching the regex within the artifact ",
        action='store_true',
        dest='matches',
        default=False,
    )
    grep_parser.add_argument(
        "-i", "--case-insensitive",
        help="Perform grep using a case insensitive regex",
        action='store_true',
        dest='case_insensitive',
        default=False,
    )
    grep_parser.add_argument(
        "-v", "--verbose",
        help="Show additional information for the provided results",
        action='store_true',
        dest='verbose',
        default=False,
    )
    grep_parser.add_argument(
        "-n", "--no-color",
        help="Enabled no-color mode",
        action='store_true',
        dest='no_color',
        default=False,
    )

    # list parser
    list_parser.add_argument(
        "query",
        help="Filter search results by specified title",
        default="",
        nargs="?",
        type=str,
    )
    list_parser.add_argument(
        "-c", "--category",
        help="Filter search results by specified category",
        default=None,
        type=str,
    )
    list_parser.add_argument(
        "-g", "--tags",
        help="""
        Tags associates to the artifact to search in the form \"tag1;tag2;...;tagN\"
        """,
        default=None,
        type=str,
    )
    list_parser.add_argument(
        "-a", "--author",
        help="Filter search results by specified author",
        default=None,
        type=str,
    )
    list_parser.add_argument(
        "-s", "--status",
        help="Filter search results by specified status",
        default=None,
        type=str,
    )
    list_parser.add_argument(
        "-v", "--verbose",
        help="Show additional information for the provided results",
        action='store_true',
        dest='verbose',
        default=False,
    )
    list_parser.add_argument(
        "-n", "--no-color",
        help="Enabled no-color mode",
        action='store_true',
        dest='no_color',
        default=False,
    )
    list_parser.add_argument(
        "-C", "--allcategories",
        help="List the current categories",
        action='store_true',
        dest='all_categories',
        default=False,
    )
    list_parser.add_argument(
        "-G", "--alltags",
        help="List the current tags",
        action='store_true',
        dest='all_tags',
        default=False,
    )

    # stats parser
    stats_parser.add_argument(
        "-v", "--verbose", 
        help='Show stats in a verbose mode',
        action='store_true',
        dest='stats_verbose',
        default=False)

    stats_parser.add_argument(
        "-n", "--no-color",
        help="Enable no-color mode",
        action='store_false',
        dest='no_color',
        default=True,
    )

    # update parser
    update_parser.add_argument(
        "-i", "--id",
        help="ID of the artifact to update",
        type=str,
    )
    update_parser.add_argument(
        "-t", "--title",
        help="Title to update",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "-c", "--category",
        help="Category to update",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "-g", "--tags",
        help="Tags to update in the form \"tag1;tag2;...;tagN\"",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "-a", "--author",
        help="Author to update",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "-s", "--status",
        help="Status to update",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "--template",
        help="Template to update",
        default=None,
        type=str,
    )
    update_parser.add_argument(
        "-e", "--edit-content",
        help="Edit content of the artifact with an editor",
        action="store_true",
        dest="edit_content",
    )
    update_parser.add_argument(
        "-b", "--body",
        help="Update the body of the artifact (erases the current content)",
        type=str,
    )

    # view parser
    view_parser.add_argument(
        "nameid",
        help="Title or ID of the artifact to view",
        type=str,
        nargs="?",
    )
    view_parser.add_argument(
        "-i", "--id",
        help="ID of the artifact to visualize",
        type=str,
    )
    view_parser.add_argument(
        "-t", "--title",
        help="Title of the artifact to visualize",
        type=str,
    )
    view_parser.add_argument(
        "-c", "--category",
        help="Category associated to the artifact to visualize",
        type=str,
    )
    view_parser.add_argument(
        "-e", "--open-editor",
        help="Open the file in a text editor (read-only mode)",
        action='store_true',
        dest='editor',
        default=False,
    )
    view_parser.add_argument(
        "-n", "--no-color",
        help="Enabled no-color mode",
        action='store_true',
        dest='no_color',
        default=False,
    )

    # template parser
    template_subparsers = template_parser.add_subparsers(help='template commands', dest="template_command")
    template_subparsers.required = True

    # template subcommands
    add_template_parser = template_subparsers.add_parser(
        'add', help='Add a template from a file')
    edit_template_parser = template_subparsers.add_parser(
        'edit', help='Edit a template')
    list_template_parser = template_subparsers.add_parser(
        'list', help='List all templates')
    new_template_parser = template_subparsers.add_parser(
        'new', help='Create a template from starting from an example')
    delete_template_parser = template_subparsers.add_parser(
        'delete', help='Delete an existing template')
    apply_template_parser = template_subparsers.add_parser(
        'apply', help='Apply a template to an entire set of artifacts')

    add_template_parser.add_argument(
        "file",
        help="The template file to add to kb",
        type=str,
    )
    add_template_parser.add_argument(
        "-t", "--title",
        help="The title to assign to the template added from a file to kb",
        type=str,
    )
    edit_template_parser.add_argument(
        "template",
        help="The name of the template to edit",
        type=str,
    )
    list_template_parser.add_argument(
        "query",
        help="The name (or part of it) of the template to search for",
        type=str,
        nargs='?',
    )
    list_template_parser.add_argument(
        "-n", "--no-color",
        help="Enabled no-color mode",
        action='store_true',
        dest='no_color',
        default=False,
    )
    delete_template_parser.add_argument(
        "template",
        help="The name of the template to delete",
        type=str,
    )
    new_template_parser.add_argument(
        "template",
        help="The name of the template to create",
        type=str,
    )

    apply_template_parser.add_argument(
        "template",
        help="The name of the template to apply to the filtered artifacts",
        type=str,
    )

    apply_template_parser.add_argument(
        "-t", "--title",
        help="Title of the artifacts on which template is applied",
        type=str,
    )
    apply_template_parser.add_argument(
        "-c", "--category",
        help="Category of the artifacts on which template is applied",
        default=None,
        type=str,
    )
    apply_template_parser.add_argument(
        "-g", "--tags",
        help="""
        Tags associates to the artifacts in the form \"tag1;tag2;...;tagN\" where template is applied
        """,
        default=None,
        type=str,
    )
    apply_template_parser.add_argument(
        "-a", "--author",
        help="Author of the artifacts on which template is applied",
        default=None,
        type=str,
    )
    apply_template_parser.add_argument(
        "-s", "--status",
        help="Status of the artifacts on which template is applied",
        default=None,
        type=str,
    )
    apply_template_parser.add_argument(
        "-m", "--extended-match",
        help="""
        Perform application query not on a strict match,
        for example:
        `kb template apply --category cheat -m`
        will match all artifacts containing in their category \"cheat\",
        hence \"cheatsheet\", \"mycheats\",\"cheatsheets\" and so on"
        """,
        action='store_true',
        dest='extended_match',
        default=False,
    )

    # import parser
    import_parser.add_argument(
        "file",
        help="Archive to import as knowledge base",
        type=str,
    )

    # export parser
    export_parser.add_argument(
        "-f", "--file",
        help="Name of the exported archive",
        type=str,
        nargs="?"
    )
    export_parser.add_argument(
        "-d",
        "--only-data",
        help="Export only notes files organized as directories (one for each category)",
        action='store_true',
        dest='only_data',
        default=False,
    )

    # erase parser
    erase_parser.add_argument(
        "--db",
        help="Only remove kb database",
        action='store_true',
        dest='db',
        default=False,
    )

    help_parser.add_argument(
        'cmd',
        help='Name of command to get help for',
        nargs='?'
    )

    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    try:                                                                    # Attempt to load
        from kb.plugin import loadModules                                   # functionality for plugin architecture
        loadModules('parser', parser, subparsers, '',DEFAULT_CONFIG,'')     # Load any plugins that are available
    except ModuleNotFoundError:                                             # If the plugin mod. isn't installed, 
        pass                                                                #  then ignore error

    parsed_args = parser.parse_args()
    if parsed_args.command == 'help':
        if not parsed_args.cmd:
            parser.print_help(sys.stderr)
        else:
            try:
                subparsers.choices[parsed_args.cmd].print_help()
            except KeyError:
                print(f'Unknown command name `{parsed_args.cmd}`')
                print(
                    f"Valid commands are: {', '.join(subparsers.choices.keys())}"
                )
        sys.exit(1)
    return parsed_args
