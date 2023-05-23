#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN001, I001
# noqa: W293 blank line contains whitespace
# - Without global file level rule, using # noqa: is not possible
"""Module: Sidecar: App strings values for click commands, and Utilities

Usage:
-------------------------
- AppValues.app centralises all strings for app levels settings.
- ProgramUtilities is a light collection of developer tools, app functions.

Linting:
-------------------------
- pylint: disable=trailing-whitespace
- ruff: noqa:
      I001:     unsorted-imports
                Import block is unsorted or unformatted
      ANN001: 	missing-type-function-argument
                Missing type annotation for function argument {name}

Critieria:
LO2.2: Clearly separate and identify code written for the application and
       the code from external sources (e.g. libraries or tutorials)
LO2.2.3: Clearly separate code from external sources
LO2.2.4: Clearly identify code from external sources
LO6: Use library software for building a graphical user interface,
or command-line interface, or web application, or mathematical software
LO6.1 Implement the use of external Python libraries
LO6.1.1 Implement the use of external Python libraries
      where appropriate to provide the functionality that the project requires.
-------------------------
Standard Libraries
:imports: dataclasses, typing, tracemalloc, warnings,

3rd Paty Imports
:imports: click, rich, inspect, Prompt

Custom Authored Libraries
:imports: apptypes.ActionType

:class: AppValues: Static Class App Strings for each
:class: ActionType:
:class: ProgramUtilities:
"""
# Standard Imports
import dataclasses
import tracemalloc
import warnings

# 3rd Paty Imports
import click
import rich
from rich import inspect, print as rprint  # type: ignore
from rich.prompt import Prompt  # type: ignore

# 0.3 Local Imports
from apptypes import ActionType


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
    class Run:
        """Start."""
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
        refresh: str = "refresh"
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
    """Program Utilities.

    :property: ActionType:
        Literal["default", "error", "ignore", "always", "module", "once"]
    :method: start_memory: Start memory tracing.
    :method: stop_memory: Stop memory tracing.
    :method: printmemtrace: Print memory trace.
    :method: inspectcmd: Inspect a command's context.
    :method: inspectcontent: Inspect a command's content.
    :method: warn: Warn the user about a command's action.
    """
    
    ActionType: list = ActionType  # noqa
    
    @staticmethod
    def startmemory() -> None:
        """Start memory tracing."""
        tracemalloc.start()
    
    @staticmethod
    def stopmemory() -> None:
        """Stop memory tracing."""
        tracemalloc.stop()
    
    @staticmethod
    def printmemtrace(obj: object) -> None:
        """Print memory usage."""
        # inspect(inspect)
        trace = \
            tracemalloc.get_object_traceback(obj)  # noqa
        rich.print(f"Memory: {trace}")
        rich.inspect(trace, all=True)
        click.echo(f"Memory: {trace}", err=True)
    
    @staticmethod
    def inspectcmd(func) -> None:
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
    def inspectcontext(ctx) -> None:
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
    def warn(action: ActionType = "ignore") -> None:
        """Configured Python Interpreter warnings.

        Added: typing.Literal[str] : Invalid Type

        Parameters:
        ====================
        :param action: Literal["default", "error", "ignore",
                                "always", "module", "once"]:
                    "ignore" to ignore warnings,
                    "default" to show warnings
                    "error" to turn matching warnings into exceptions
                    "always" to always print matching warnings
                    "module" to print the first occurrence of matching warnings
                             for each module where the warning is issued
                    "once" to print only the first occurrence
                           of matching warnings, regardless of location
        """
        trace: str = \
            "Enable tracemalloc to get the object allocation traceback"  # noqa
        warnings.filterwarnings(action, message=".*deprecated.*",
                                category=DeprecationWarning)
        warnings.filterwarnings(action, category=ResourceWarning)
        warnings.filterwarnings(action, message=trace)
