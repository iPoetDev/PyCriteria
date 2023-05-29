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
import pandas as pd
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
    shown: bool = True
    case: bool = False
    
    @dataclasses.dataclass
    class Run:
        """Base Anchor: String Settings."""
        cmd: str = "run"
        name: str = "PyCriteria"
        welcome: str = f"Welcome to!{name}"
        confirm: str = "Start PyCriteria?"
    
    @dataclasses.dataclass
    class Load:
        """Load Intent: String Settings."""
        cmd: str = "load"
        help: str = ("Available Actions: Todo, Views\n"
                     "Parent Menu: Load -> Sub commands: todo, views")
    
    class Todo:
        """Todo Action: String Setting."""
        cmd: str = "todo"
        intro: str = "Todo Settings."
        help: str = "Load todo list: Select views to Display."
        quik: str = "Todo Settings."
        
        class Selects:
            """Todo Options: Selects: String Settings.
            
            Click's options parameters: must match the function parameters label
            """
            opt: str = "-s"
            param: str = "selects"
            default: str = "All"
            show: bool = True
            help: str = "Choose a option: All, Simple, Notes, Done, Grade, Review"
            prompt: str = "Selects ToDo Views: :"
    
    @dataclasses.dataclass
    class Views:
        """Views: Action: String Settings."""
        cmd: str = "views"
        help: str = "Load views. Select bulk data to view to Display."
        
        class Selects:
            """Views Options: Selects: String Settings."
            
            Click's options parameters: must match the function parameters label
            """
            opt: str = "-s"
            option: str = "selects"
            default: str = "Overview"
            show: bool = True
            help: str = "Choose a option: Overview, Project, Criteria, " \
                        "Todos, Reference"
            prompt: str = "Choose a assignment view: "
    
    @dataclasses.dataclass
    class Find:
        """Find Settings."""
        cmd: str = "find"
        help: str = "Available Actions: Locate by row index"
        
        # Common Options for Locate, and Edit commands
        @dataclasses.dataclass
        class Index:
            """Find Options: Index: String Settings.
            
            Click's options parameters: must match the function parameters label
            """
            opt: str = "-i"
            param: str = "index"
            min: int = 1
            clamp: bool = True
            help: str = 'BY ROW: ☑️ Select: 1 to ',
        
        class Axis:
            """Find Options: Axis: String Settings.
            
            Axis for Search Focuses/Dimensions:
            Click's options parameters: must match the function parameters label
            """
            opt: str = "-a"
            param: str = "axis"
            Choices: str = ["index"]
            default: str = "index"
            case: bool = False
            help: str = '🔎 Search focus. Currently: by row\'s index',
            prompt: str = "🔎 Select search focus on: index",
            required: bool = True
        
        @dataclasses.dataclass
        class Locate:
            """Find Commands: Locate | String Settings."""
            cmd: str = "locate"
            help: str = "🔎 Search focus. Currently: by row\'s index"
    
    @dataclasses.dataclass
    class Edit:
        """Add Settings."""
        cmd: str = "edit"
        help: str = "Edit Mode: Available Actions: Note, Todo"
        opthelp: str = 'Select the edit mood: add, update, delete'
        
        @dataclasses.dataclass
        class Note:
            """Note command and option strings settings"""
            cmd: str = "note"
            help: str = 'Add | Update | Delete a note to record'
            prompt: str = "The Note: Leave blank to delete."
            required: bool = True
            
            class Mode:
                """Edit mode options strings settings."""
                opt: str = "-m"
                param: str = "mode"
                case: bool = False
                help: str = "Select the edit mood: add, update, delete"
                prompt: str = "Choose: add, update, delete: "
                required: bool = True
        
        class ToDo:
            """Select (filterr) Settings."""
            cmd: str = "progress"
            indexhelp: str = "BY ROW: ☑️ Select: 1 to "
            Statuses: list = ["ToDo", "WIP", "Done", "Missed"]
            
            @dataclasses.dataclass
            class Status:
                """Status Settings."""
                opt: str = "-s"
                param: str = "status"
                default: str = "ToDo"
                case: bool = False
                help: str = "Select the status: complete, incomplete"
                prompt: str = "Update project status: Todo, WIP, Done, Missed: "
                required: bool = True
        
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


class Checks:
    """Checks.

    :meth: isnot_context
    :meth: has_dataframe
    :meth: isnot_querytype
    :meth: is_querycomplete
    :meth: compare_frames
    :meth: santitise
    """
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def isnot_context(ctx: click.Context) -> bool:
        """Tests dataframe context.

        :param ctx: click.Context - Click context
        :return: bool - True if not context
        """
        return not (ctx and isinstance(ctx, click.Context))
    
    @staticmethod
    def has_dataframe(ctx: click.Context) -> bool:
        """Tests dataframe context.

        Hinted by Sourcery
        - Lift code into else after jump in control flow,
        - Replace if statement with if expression,
        - Swap if/else branches of if expression to remove negation

        Refactored from: Perplexity
        www.perplexity.ai/searches/a2f9c214-11e8-4f7d-bf67-72bfe08126de?s=c

        :param ctx: click.Context - Click context
        :return: bool - True if it has a dataframe
        """
        return isinstance(ctx, pd.DataFrame) if True else False
    
    @staticmethod
    def isnot_querytype(header: str,
                        query: str) -> bool:
        """Tests Search Query.

        :header: str - Header
        :query: str - Query
        :return: bool - True if not query
        """
        return not isinstance(header, str) or not isinstance(query, str)
    
    @staticmethod
    def is_querycomplete(header: str,
                         query: str) -> bool:
        """Tests for Empty Serach.

        :header: str - Header
        :query: str - Query
        :return: bool - True if header or query is not empty
        """
        return header is not None or query is not None
    
    @staticmethod
    def compare_frames(olddata: pd.DataFrame,
                       newdata: pd.DataFrame) -> bool:
        """Compare dataframes.

        :param olddata: pd.DataFrame - Old dataframe
        :param newdata: pd.DataFrame - New dataframe
        :return: bool - True if no changes
        """
        diff = olddata.compare(newdata,
                               keep_shape=True,
                               keep_equal=True)
        if not diff.empty:
            click.echo(message="Updated refreshed/rehydrated data")
            rprint(diff, flush=True)
            return False
        
        click.echo(message="No changes in refreshed/rehydrated data")
        return True
    
    @staticmethod
    def santitise(s: str) -> str | None:
        """Sanitise strings.

        :param s: str - String to sanitised
        :return: str | None - Sanitised string or None
        """
        empty: str = ''
        if s != empty and isinstance(s, str):
            return s.strip() if s else None
        click.echo(message="Searching by index only. No keywords.")
        return None


class CliStyles:
    """App Styles."""
    infofg: str = "white"
    infobg: str = "green"
    infobold: bool = True
    invalidfg: bool = "yellow"
    invalidbg: str = "white"
    invalidbold: bool = True
    warnfg: str = "white"
    warnbg: str = "yellow"
    warnbold: bool = True
    warnblk: bool = True
    warnunder: bool = True
    warnrev: bool = True
    errfg: str = "whit"
    errbg: str = "red"
    errbold: bool = True
    errblk: bool = True
    errrev: bool = True
    reset: bool = True
    resetno: bool = False
    toerror: bool = True


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
