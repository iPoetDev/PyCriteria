#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, D415
"""Module: PyCriteria Terminal App."""

import dataclasses

import click

from pandas import pandas as pd
from rich import print as rprint

import prompt_toolkit

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import WordCompleter


class DataFrameContext:
    """DataFrame Context."""
    
    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Initialize."""
        self.dataframe: pd.DataFrame = dataframe


pass_dataframe_context = click.make_pass_decorator(
        DataFrameContext, ensure=True)


@click.group(name="start")
def start() -> None:
    """Main. Starts a local CLI REPL."""
    click.echo(message="PyCriteria Terminal App.")
    session: prompt_toolkit.PromptSession = \
        prompt_toolkit.PromptSession(completer=Commands.nest_auto)
    
    while True:
        try:
            text = session.prompt('PyCriteria >  ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            click.echo('You entered:', text)
    click.echo('GoodBye!')


@dataclasses.dataclass(frozen=True)
class Commands:
    """Class: Command Completer for Terminal App."""
    base_run: str = "run"  # done, empty, help
    base_about: str = "about"  # done
    ########################
    intent_load: str = "load"  # done, empty, help
    load_refresh: str = "refresh"  # function, writen
    load_list: str = "list"
    load_frame: str = "frame"
    load_table: str = "table"
    load_cols: str = "column"
    load_card: str = "card"
    intent_find: str = "find"
    search_row: str = "searches row"
    search_column: str = "searches column"
    intent_select: str = "select"
    select_item: str = "one row"
    select_row: str = "one row"
    select_column: str = "one column"
    ########################
    intent_add: str = "add"  # Add Intents: 3 sub commands
    add_row: str = "add row"  # A new row appended
    new_row: str = "new row"  # A new row appended
    insert_row: str = "insert row"  # Insert at a posotion
    intent_update: str = "update"
    update_row: str = "u-row"
    intent_delete: str = "delete"
    intent_commit: str = "commit"
    commit_push: str = "push"
    commit_sync: str = "sync"
    delete_row: str = "d-row"
    intent_exit: str = "exit"
    
    def __init__(self):
        """Initialize."""
        pass
    
    cmd_auto: WordCompleter = \
        WordCompleter([base_run,
                       intent_load,
                       load_refresh, load_list, load_frame,
                       load_table, load_cols, load_card,
                       intent_find, search_row, search_column,
                       intent_select, select_row, select_column,
                       intent_add, add_row,
                       intent_update, update_row,
                       intent_delete, delete_row,
                       intent_commit, commit_push, commit_sync,
                       intent_exit], ignore_case=True)
    
    nest_auto: NestedCompleter = \
        NestedCompleter.from_nested_dict({
                base_run: {intent_load: {
                        load_refresh: None,
                        load_list: None,
                        load_frame: None,
                        load_card: None},
                        intent_find: {
                                search_row: None, search_column: None},
                        intent_select: {
                                select_item: None,
                                select_row: None,
                                select_column: None},
                        intent_add: {
                                add_row: None},
                        intent_update: {
                                update_row: None},
                        intent_delete: {
                                delete_row: None},
                        intent_commit: {
                                commit_push: None,
                                commit_sync: None},
                        intent_exit: None,
                        },
                base_about: None,
                })


@dataclasses.dataclass(frozen=True)
class AboutUsage:
    """About Usage."""
    
    @staticmethod
    def describe_usage():
        """About: Describe Usage."""
        aws: str = ("     Example: AWS CLI Commands Pattern\n"
                    + "        `aws <service> <action>`\n"
                    + "         L1    L2       L3\n\n")
        i0: str = "OVERVIEW: RUN || 2: INTENTS || 3: ACTIONS/TASKS\n"
        i1: str = ("1: Level 1 command: Lists the user's options by showing help.\n"
                   + "1: Name: RUN e.g run: {empty}, lists help\n")
        i2: str = ("2: Level 2 command: Lists the next level command.\n"
                   + "2: Name: INTENTS "
                   + "e.g run: {empty}, lists 2nd level commands and help.\n"
                   + "2: e.g load: {empty}, lists 2nd level commands and help.\n")
        i3: str = ("3: Level 3 command: Lists the next level command.\n"
                   + "3: Name: ACTIONS/TASKS "
                   + "e.g run: {empty}, lists 3rd level commands and help.\n"
                   + "2: e.g load: {empty}, lists 2nd level commands and help.\n")
        
        rprint(aws)
        rprint(i0 + i1 + i2 + i3)
    
    @staticmethod
    def example_usage():
        """About: Usage Example."""
        e: str = ("USAGE EXAMPLES\n"
                  + "$ python app.py                   "
                  + "to view the CORE\n"
                  + "$ python app.py COMMAND           "
                  + "to view the INTENTS\n"
                  + "$ python app.py COMMAND COMMAND   "
                  + "to view the ACTIONS/TASKS\n")
        rprint(e)
    
    @staticmethod
    def loadmodel_usage():
        """Usage Model."""
        i1: str = ("LOADING DATA\n"
                   + "$ python app.py load............to view Loading Commands: "
                   + "projects, criterias, references.\n"
                   + "$ python app.py load criteria...to view criterias data.\n"
                   + "$ python app.py load project....to view project meta data.\n"
                   + "$ python app.py load reference..to view reference data.\n")
        rprint(i1)
    
    @staticmethod
    def findmodel_usage():
        """Usage Model."""
        i1: str = ("FINDING DATA, LOCATING\n"
                   + "$ python app.py find............to view Finding Commands: "
                   + "items, rows, columns.\n"
                   + "$ python app.py find items...to view items data.\n"
                   + "$ python app.py find rows...to view rows data.\n"
                   + "$ python app.py find columns...to view column data.\n")
        rprint(i1)
    
    @staticmethod
    def selectmodel_usage():
        """Usage Model."""
        i1: str = ("SELECTING DATA, FILTERING DATA\n"
                   + "$ python app.py select............to view Selecting Commands: "
                   + "items, rows, columns.\n"
                   + "$ python app.py select items...to view items data.\n"
                   + "$ python app.py select rows...to view rows data.\n"
                   + "$ python app.py select columns...to view column data.\n")
        rprint(i1)
    
    @staticmethod
    def addmodel_usage():
        """Usage Model."""
        i1: str = ("ADDING DATA\n"
                   + "$ python app.py add............to view Adding Commands: "
                   + "items, rows.\n"
                   + "$ python app.py add items...to view items data.\n"
                   + "$ python app.py add rows...to view rows data.\n")
        rprint(i1)
    
    @staticmethod
    def updatemodel_usage():
        """Usage Model."""
        i1: str = ("UPDATING DATA\n"
                   + "$ python app.py update............to view Updating Commands: "
                   + "items, rows.\n"
                   + "$ python app.py update items...to view items data.\n"
                   + "$ python app.py update rows...to view rows data.\n")
        rprint(i1)
    
    @staticmethod
    def deletemodel_usage():
        """Usage Model."""
        i1: str = ("DELETING DATA\n"
                   + "$ python app.py delete............to view Deleting Commands: "
                   + "items, rows.\n"
                   + "$ python app.py delete items...to view items data.\n"
                   + "$ python app.py delete rows...to view rows data.\n")
        rprint(i1)
