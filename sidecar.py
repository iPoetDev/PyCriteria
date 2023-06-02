#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN001, I001
# noqa: W293 blank line contains whitespace
# - Without global file level rule, using # noqa: is not possible
"""Module: Sidecar: App strings values for click commands, and Utilities.

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


"""
import dataclasses
import tracemalloc
import warnings
# Standard Imports
from typing import Literal

# 3rd Paty Imports
import click
import rich
from rich import inspect, print as rprint  # type: ignore

# 0.3 Local Imports


# VauleTypes: Literals
ActionType = Literal["default", "error", "ignore", "always", "module", "once"]


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
    FORWARDING: bool = True
    DISPLAYING: bool = True
    HIDING: bool = False
    SQUEEZE: bool = True
    SINGLE: bool = True
    TRACING: bool = True
    NOTRACING: bool = False,
    SEARCHFOCUS: str = "index"
    sep: str = ":: "
    shown: bool = True
    case: bool = False
    
    @dataclasses.dataclass
    class Display:
        """Display Values."""
        STANDALONE: str = 'show'
        SIDEBYSIDE: str = 'compare'
        TOLAYOUT: bool = True
        TOTERMINAL: bool = False
    
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
            """Views Options: Selects: String Settings.".
            
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
        ADD: str = "add"
        UPDATE: str = "update"
        DELETE: str = "delete"
        INSERT: str = "insert"
        APPEND: str = "append"
        CLEAR: str = "clear"
        
        @dataclasses.dataclass
        class Note:
            """Note command and option strings settings."""
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
            TOGGLE: str = 'toggle'
            SELECT: str = 'select'
            
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
    errfg: str = "white"
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
