# -*- encoding: utf-8 -*-
# kb v0.1.7
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
Command Line Parsing Module for kb

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import sys
import argparse
import shtab
from kb import __version__
from typing import Sequence

commands_descriptions = {
    'add': 'Add an artifact',
    'edit': 'Edit an artifact content',
    'list': 'Search for artifacts',
    'view': 'View artifacts',
    'grep': 'Grep through kb artifacts',
    'update': 'Update artifact properties',
    'delete': 'Delete artifacts',
    'template': {
        '.': 'Manage templates for artifacts',
        'add': 'Add a template from a file',
        'edit': 'Edit a template',
        'list': 'List all templates',
        'new': 'Create a template from starting from an example',
        'delete': 'Delete an existing template',
        'apply': 'Apply a template to an entire set of artifacts'
    },
    'import': 'Import a knowledge base',
    'export': 'Export the knowledge base',
    'erase': 'Erase the entire kb knowledge base',
    'sync': 'Synchronize the knowledge base with a remote git repository',
    'help': 'Show help of a particular command'
}


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

    shtab.add_argument_to(parser, ["--print-completion"])

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__))

    subparsers = parser.add_subparsers(help='commands', dest="command")
    subparsers.required = True

    # Main Commands
    add_parser = subparsers.add_parser(
        'add',
        description=commands_descriptions['add'],
        help=commands_descriptions['add'])
    edit_parser = subparsers.add_parser(
        'edit',
        description=commands_descriptions['edit'],
        help=commands_descriptions['edit'])
    list_parser = subparsers.add_parser(
        'list',
        description=commands_descriptions['list'],
        help=commands_descriptions['list'])
    view_parser = subparsers.add_parser(
        'view',
        description=commands_descriptions['view'],
        help=commands_descriptions['view'])
    grep_parser = subparsers.add_parser(
        'grep',
        description=commands_descriptions['grep'],
        help=commands_descriptions['grep'])
    update_parser = subparsers.add_parser(
        'update',
        description=commands_descriptions['update'],
        help=commands_descriptions['update'])
    delete_parser = subparsers.add_parser(
        'delete',
        description=commands_descriptions['delete'],
        help=commands_descriptions['delete'])
    template_parser = subparsers.add_parser(
        'template',
        description=commands_descriptions['template']['.'],
        help=commands_descriptions['template']['.'])
    import_parser = subparsers.add_parser(
        'import',
        description=commands_descriptions['import'],
        help=commands_descriptions['import'])
    export_parser = subparsers.add_parser(
        'export',
        description=commands_descriptions['export'],
        help=commands_descriptions['export'])
    erase_parser = subparsers.add_parser(
        'erase',
        description=commands_descriptions['erase'],
        help=commands_descriptions['erase'])
    sync_parser = subparsers.add_parser(
        'sync',
        description=commands_descriptions['sync'],
        help=commands_descriptions['sync'])
    help_parser = subparsers.add_parser(
        'help',
        description=commands_descriptions['help'],
        help=commands_descriptions['help'])

    # add parser
    add_parser.add_argument(
        "file",
        help="Path of the file to add to kb as artifact",
        type=str,
        nargs="*",
        choices=shtab.Required.FILE
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
        help="Tags to associate to the artifact in the form \"tag1;tag2;...;tagN\"",
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
        help="Tags associates to the artifact to search in the form \"tag1;tag2;...;tagN\"",
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
        "-f", "--full-identifier",
        help="Print results in full-identifier mode",
        action='store_true',
        dest='full_identifier',
        default=False,
    )
    list_parser.add_argument(
        "-n", "--no-color",
        help="Enabled no-color mode",
        action='store_true',
        dest='no_color',
        default=False,
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
        help="Tags associates to the artifact to search in the form \"tag1;tag2;...;tagN\"",
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
    delete_parser.add_argument(
        "-f", "--force",
        help="Force removal without asking for confirmation prompt",
        action='store_true',
        default=False,
    )

    # template parser
    template_subparsers = template_parser.add_subparsers(
        help='template commands', dest="template_command")
    template_subparsers.required = True

    # template subcommands
    add_template_parser = template_subparsers.add_parser(
        'add',
        description=commands_descriptions['template']['add'],
        help=commands_descriptions['template']['add'])
    edit_template_parser = template_subparsers.add_parser(
        'edit',
        description=commands_descriptions['template']['edit'],
        help=commands_descriptions['template']['edit'])
    list_template_parser = template_subparsers.add_parser(
        'list',
        description=commands_descriptions['template']['list'],
        help=commands_descriptions['template']['list'])
    new_template_parser = template_subparsers.add_parser(
        'new',
        description=commands_descriptions['template']['new'],
        help=commands_descriptions['template']['new'])
    delete_template_parser = template_subparsers.add_parser(
        'delete',
        description=commands_descriptions['template']['delete'],
        help=commands_descriptions['template']['delete'])
    apply_template_parser = template_subparsers.add_parser(
        'apply',
        description=commands_descriptions['template']['apply'],
        help=commands_descriptions['template']['apply'])

    add_template_parser.add_argument(
        "file",
        help="The template file to add to kb",
        type=str,
        choices=shtab.Required.FILE
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
        choices=shtab.Required.FILE
    )

    # export parser
    export_parser.add_argument(
        "-f", "--file",
        help="Name of the exported archive",
        type=str,
        nargs="?",
        choices=shtab.Required.FILE
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

    # sync parser
    sync_parser.add_argument(
        'operation',
        help="""Use \"init\" to initialize the remote repo,
                Use \"push\" to git push (write local -> remote) the knowledge base,
                Use \"pull\" to git pull (retrieve remote -> local) the remote kb,
                Use \"info\" to show information about the repository
             """,
        choices=['init', 'push', 'pull', 'info'])

    help_parser.add_argument(
        'cmd',
        help='Name of command to get help for',
        nargs='?'
    )

    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

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
