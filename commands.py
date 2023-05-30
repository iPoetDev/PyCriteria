#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, D415
"""Module: Command and Command Strings, Values.

Usage:
-------------------------
- Commands: Click.Command Strings and Command completions, AutoCompleter

Linting:
-------------------------
- pylint: disable=trailing-whitespace
- ruff: noqa:
      F841:     unused-variable
                Local variable {name} is assigned to but never used
      D415:     ends-in-punctuation
                First line should end with a period, question mark,
                or exclamation point
      ANN101:   missing-type-self
                Missing type annotation for {name} in method
- noqa: W293

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
:imports: dataclasses

3rd Paty Imports
:imports: prompt_toolkit.completion
   :depreaction: Possibly deprecated by use of click_repl, due to use
                 of completion from prompt_toolkit.

:class: Commands: Command Strings and Command completions, AutoCompleter
"""

# 0.1 Standard Library Imports
import dataclasses

# 0.2. 3rd Party Imports
from prompt_toolkit.completion import NestedCompleter, WordCompleter


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
