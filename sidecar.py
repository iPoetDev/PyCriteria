#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: PyCriteria Terminal App."""
import dataclasses
import tracemalloc
import typing
import warnings

import click
import rich
from rich import inspect


@dataclasses.dataclass
class AppValues:
    """App Values."""
    app: str = "TUI"
    name: str = "PyCriteria"
    author: str = "iPoetDev"
    version: str = "0.1.1"
    lastmodified: str = "2023-05-07"
    copyright: str = "(c) 2023, 2024, 2025. All rights reserved."
    epilogue: str = f"{name}. Version: {version}. " \
                    f"Updated: {lastmodified} " \
                    f"{copyright}. @{author}."
    richpanel: bool = True
    deprecated: bool = False
    OFF: bool = False
    ON: bool = True
    sep: str = ":: "
    
    @dataclasses.dataclass
    class Start:
        """Start"""
        cmd: str = "start"
        name: str = "PyCriteria"
        welcome: str = f"Welcome to!{name}"
        confirm: str = "Start PyCriteria?"
    
    @dataclasses.dataclass
    class Run:
        """Start"""
        cmd: str = "run"
        name: str = "PyCriteria"
        welcome: str = f"Welcome to!{name}"
        confirm: str = "Start PyCriteria?"
    
    @dataclasses.dataclass
    class Load:
        """Load Settings.
        :property: intro:str: typer panel/intro.
        :property: help:str: typer help.
        :property: quik:str: typer short_help.
        """
        cmd: str = "load"
        projects: str = "projects"
        criterias: str = "criteria"
        references: str = "reference"
        intro: str = "Load Settings."
        help: str = "Load Settings."
        quik: str = "Load Settings."
    
    @dataclasses.dataclass
    class Views:
        """Choose a View."""
        cmd: str = "views"
        allname: str = "showall"
        list: str = "list"
        table: str = "table"
        columns: str = "columns"
        intro: str = "Select which view: List, Table, Columns."
        help: str = "Load Settings."
        quik: str = "Load Settings."
    
    @dataclasses.dataclass
    class Find:
        """Find Settings."""
        cmd: str = "find"
        items: str = "items"
        rows: str = "rows"
        columns: str = "columns"
        intro: str = "Find an items. By single item, rows, columns."
        help: str = "Find Settings."
        quik: str = "Find Settings."
    
    @dataclasses.dataclass
    class Select:
        """Add Settings."""
        cmd: str = "select"
        items: str = "items"
        rows: str = "rows"
        columns: str = "columns"
        intro: str = "Select to filter items. By single item, rows, columns"
        help: str = "Select Settings."
        quik: str = "Select Settings."
    
    @dataclasses.dataclass
    class Add:
        """Add Settings."""
        cmd: str = "add"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Add a new record: by cell or a single row."
        help: str = "Add Settings."
        quik: str = "Add Settings."
    
    @dataclasses.dataclass
    class Update:
        """Select (filterr) Settings."""
        cmd: str = "update"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Update an existing record: by cell or a single row."
        help: str = "Update Settings."
        quik: str = "Update Settings."
    
    @dataclasses.dataclass
    class Delete:
        """Select (filterr) Settings."""
        cmd: str = "delete"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Delete an existing record: by cell/item or a single row."
        help: str = "Delete Settings."
        quik: str = "Delete Settings."
    
    @dataclasses.dataclass
    class Close:
        """Close Settings."""
        cmd: str = "close"
        intro: str = "Close the remote connection."
        help: str = "Close Settings."
        quik: str = "Close Settings."
    
    @dataclasses.dataclass
    class Exit:
        """Exit Settings."""
        cmd: str = "exit"
        intro: str = "Exit the terminal (and close the connection)."
        help: str = "Exit Settings."
        quik: str = "Exit Settings."


class ProgramUtils:
    """Program Utilities

    :property: ActionType: Literal["default", "error", "ignore", "always", "module", "once"]
    :method: inspect_cmd: Inspect a command's context.
    :method: warn: Warn the user about a command's action.
    """
    
    ActionType: str = typing.Literal["default", "error", "ignore", "always", "module", "once"]
    
    @staticmethod
    def inspectcmd(func):
        """Inspect a command's context."""
        command: click.Command = click.Command(name=func.__name__)
        context: click.Context = click.Context(command)
        c2 = command.context_class
        if context is None:
            rich.print("Command: not found a current context.")
            inspect(command)
        
        if c2:
            rich.inspect("2nd Context:")
            inspect(c2)
        
        rich.print(f"Command: {context.info_name}")
        inspect(context.parent)
        inspect(context)
        inspect(context.command)
        inspect(context.invoked_subcommand)
        inspect(context.args)
        inspect(context.obj)
    
    @staticmethod
    def inspectcontext(ctx):
        """Inspect a command's context."""
        context: click.Context = ctx
        if context is None:
            rich.print("Command: not found a current context.")
        
        rich.print(f"Command: {context.info_name}")
        inspect(context.parent)
        inspect(context)
        inspect(context.command)
        inspect(context.invoked_subcommand)
        inspect(context.args)
        inspect(context.obj)
    
    @staticmethod
    def warn(show: bool = True, action: ActionType = "ignore"):
        """Configured Python Interpreter warnings.

        Added: typing.Literal[str] : Invalid Type
        Fixme: 'Literal' may be parameterized with literal ints, byte and unicode
                strings, bools, Enum values, None, other literal types, or type
                aliases to other literal types

        Parameters:
        ====================
        :param show: bool:
                    True to hide warnings, False to show warnings
        :param action: Literal["default", "error", "ignore", "always", "module", "once"]:
                    "ignore" to ignore warnings,
                    "default" to show warnings
                    "error" to turn matching warnings into exceptions
                    "always" to always print matching warnings
                    "module" to print the first occurrence of matching warnings
                             for each module where the warning is issued
                    "once" to print only the first occurrence of matching warnings,
                           regardless of location
        """
        tracemalloc.start()
        if show:
            warnings.filterwarnings(action, message=".*deprecated.*", category=DeprecationWarning)
            warnings.filterwarnings(action, category=ResourceWarning)
