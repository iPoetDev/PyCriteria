#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: Controller for the Terminal App."""
import typing

from typing import Optional
import warnings

import gspread  # type: ignore

from rich import pretty as rpretty
from rich import print as rprint
from rich.console import Console
from rich.console import ConsoleDimensions
from rich.console import ConsoleOptions
from rich.prompt import Prompt  # type: ignore
import rich.style  # type: ignore
from rich.table import Table  # type: ignore

# 0.3 Local imports
import connections

from datatransform import DataTransform
import settings

connector: connections.GoogleConnector = connections.GoogleConnector()
configuration: settings.Settings = settings.Settings()
tablesettings: settings.TableSettings = settings.TableSettings()
console: rich.console.Console = Console()
transformer: DataTransform = DataTransform()


# 2. Read the data from the sheet by the controller

# plylint: disable=line-too-long
class Controller:
    """Controller for the effort of loading the data, fetching it, managing it.
    
    Links the connector to the app:
    
    CRUD engine + filter, find/search, show/hide
    ---------------------------------------------
    A: READ/FETCH: Loads the data from the sheet to the:
     - DataModel - NYI
     - App - WIP
     - Display - WIP
    B: CREATE: Inserts new data into the sheet: per item, per row, not per batch
    C: UPDATE: Updates data in the sheet: per item, per row, not per batch
       (matching cells, yet)
    D: DELETE: Deletes data from the sheet: per item, per row, not per batch
    E: READ/FILTER: Filters the data: per row, column
       --> Affirmative: "Given me a subset to ETL"
    F: READ/EXCLUDE: Hides the data: per row, column
       --> Non-Affirmative: "Hide what I do not want to see"
    G: SORT: Not doing sorting, thought, APIs have refernece to it.
    
    Controller is the hub of app tasks/actions; whereas:
    -----------------------------------------------
    1. The App handles TUI command logic (Typer) and bundles controller logic
       into one entry point.
    2. The WebConsole handles the console display/logics.
    3. The DataTransformer handles any Extract, Transform,
       Load (ETL) logic (load_* tasks are shared with controller)
    4. The DataModel handles the in memory data structure and
       data logics (maybe move Topics, Entry to DataModel)
    5. The Display handles the TUI output display rendering logics
       using the console.
    6. The Connector handles the connection to the remote data source
       (Google Sheets).
    7. The Settings handle the configurations of the app/local packages for
       strings, etc.
    

    Methods:
    -------
    :method: refresh: Refreshed entired connection, sheet, worksheet, and data.
    :method: load_data: Loads the worksheet.
    :method: load_data: Loads the data from the sheet.
    :method: insert_newrow: Inserts a new row into the worksheet.
    :method: insert_newitem: Inserts a new item into the worksheet.
    :method: update_row: Updates a row in the worksheet.
    :method: update_item: Updates an item in the worksheet.
    :method: update_items: Updates matching item in the worksheet.
    :method: delete_row: Deletes a row in the worksheet.
    :method: delete_item: Deletes an item in the worksheet.
    :method: filter_rows: Filters the worksheet by row(s).
    :method: filter_columns: Filters the worksheet by column(s).
    :method: hide_rows: Hides the worksheet by row(s) --> Display Class?
    :method: hide_columns: Hides the worksheet by column(s) --> Display Class?
    """
    
    # 1. Loading Actions/Methods: Bulk: Connecting, Worhsheet, Entire Dataset
    @staticmethod
    def refresh() -> list[str]:
        """Refreshed google sheet connection, returns the refreshed data."""
        # 1.1: Connect to the sheet
        # -> Move to Instance once the data is
        # loaded is tested and working on heroku
        creds: gspread.Client = connector.connect_to_remote(
                configuration.CRED_FILE)
        # rich.print(creds)
        # 1.2: Read the data from the sheet
        # -> Move to Instance once the data is loaded, working on heroku
        spread: gspread.Spreadsheet = \
            connector.get_source(creds,
                                 configuration.SHEET_NAME)
        # rich.print(spread)
        # 1.3: Return the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on
        # heroku
        tabs: gspread.Worksheet = \
            connector.open_sheet(spread, configuration.TAB_NAME)
        # rich.print(tabs)
        # 1.4 Fetch the Data and a.1 Return/Print it,
        # 1.5 Return it and load it into a dataclass
        # 1.6 transform it into a datamodel reference
        return connector.fetch_data(tabs)
    
    @staticmethod
    def load_wsheet() -> gspread.Worksheet:
        """Loads a worksheet.
        :return: gspread.Worksheet: The current worksheet to extract the data.
        """
        # 1.1: Connect to the sheet
        # -> Move to Instance once the data is loaded is tested and working on heroku
        creds: gspread.Client = \
            connector.connect_to_remote(configuration.CRED_FILE)
        # rich.print(creds)
        # 1.2: Read the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on heroku
        spread: gspread.Spreadsheet = \
            connector.get_source(creds,
                                 configuration.SHEET_NAME)
        # rich.print(spread)
        # 1.3: Return the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on
        # heroku
        return connector.open_sheet(spread, configuration.TAB_NAME)
    
    @staticmethod
    def load_data() -> list[str]:
        """Loads the data."""
        # 1.1: Connect to the sheet
        # 1.2: Read the data from the sheet
        # 1.3: Return the data from the sheet
        wsheet: gspread.Worksheet = Controller.load_wsheet()
        return transformer.get_data(wsheet, "H2:010")
    
    # Loading a set of cells/cells items/a cell items from a range/row
    # plylint: disable=line-too-long
    # 2. FINDING: Search Actions/Methods: Individual item, all matching items, row but not batch
    # https://docs.gspread.org/en/v5.4.0/user-guide.html#finding-a-cell # plylint: disable=line-too-long
    # A1 Notation: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet.acell #
    # plylint: disable=line-too-long,C0301
    # Row:Column: int: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet.cell
    # plylint: disable=line-too-long,C0301
    # Find 1st: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet.find #
    # plylint: disable=line-too-long,C0301
    # Find all: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet.findall #
    # plylint: disable=line-too-long,C0301
    
    # 3. CREATE: Insert Actions/Methods: Individual items, row but not batch insert
    # https://docs.gspread.org/en/v5.4.0/user-guide.html#getting-all-values-from-a-row-or-a-column
    # https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet.append_row
    
    @staticmethod  # Development Order: CREATE3.2
    def insert_newrow(rowdata: list[str] = None,
                      position: int = 1,
                      lastrow: bool = False,
                      editheader: bool = False,
                      defaultvalue: str = ""):
        """App Command: Inserts a new row into the sheet."""
        # 3.1: Connect to the sheet/loads data ☑️
        # 3.2: Find a row position, and cell position. 👔🚧
        # 3.3: Reload new dataset from the sheet with new item highlighted 👔
    
    # https://docs.gspread.org/en/v5.4.0/user-guide.html#getting-a-cell-value
    @staticmethod  # Development Order: CREATE3.3
    def insert_item(itemdata: str, position: int = 1,
                    cell_reference: Optional[str] = None,
                    editheader: bool = False):
        """App Command: Inserts an item into the sheet."""
        # 3.1: Connect to the sheet/loads data ☑️
        # 3.2: Find a row position, and cell position.👔🚧
        # 3.3: Appends data the cell at end:
        # 3.3:  either clearing and appending to cell contents 🚧
        # 3.3:  by overwrighting within new Cell Object 🚧
        # 3.5: Confirmed user with intermediate display (not commit/saved) 👔🚧
        # 3.6: Sends data to the sheet 🚧
        # 3.7: Reloads new dataset from the sheet, with new item displayed/highlighted 👔🚧
    
    # 4. DELETE: Remove Actions/Methods: Individual items, row but not batch delete/clear
    # Note: https://developers.google.com/sheets/api/guides/values
    # Note: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values
    # Note: Batch Clear: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet
    # Note: Delete Rows: https://docs.gspread.org/en/v5.4.0/api/models/worksheet.html#gspread.worksheet.Worksheet
    
    @staticmethod
    def delete_row(position: int = 1,
                   lastrow: bool = False,
                   valuesonly: bool = True,
                   editheader: bool = False):
        """App Command: Delete a row into the sheet."""
        # 4.1: Connect to the sheet/loads data ☑️
        # 4.2: Removes/Clears the end row, i.e. 👔🚧
        # 4.2: i.e. undo last append 🎬🔲
        # 4.2: i.e. undo last insert 🎬🔲
        # 4.2: i.e. removeś last row (last row id) 🎬🔲
        # 4.3: Confirmed user with intermediate display (not commit/saved) 👔🚧
        # 4.4: Sends data to the sheet 🚧🔲
        # 4.5: Refreshes new dataset from the sheet, new API call, 🎬 🔲
        # 4.6:   with new item displayed/highlighted 👔🚧
    
    @staticmethod
    def delete_item(itemdata: str,
                    position: int = 1,
                    editheader: bool = False,
                    defaultvalue: str = ""):
        """App Command: Delete a row into the sheet."""
        # 4.1: Connect to the sheet/loads data ☑️
        # 4.2: Finds the first item in a row by a row id, and column id: RC1:RC2 or A1 Notation 👔🚧
        # 4.2: Stores the item coordinates/Ai Notation to a ... 🎬🔲
        # 4.3: Deletes an item in a row by a row id, and column id: RC1:RC2 or A1 Notation 🎬🔲
        # 4.4: Confirmed user with intermediate display (not commit/saved) 👔🚧
        # 4.2: Deletes an item in a row by a row id, and column id: RC1:RC2 or A1 Notation 🎬🔲
        # 4.3: Reloads/refreshed new dataset from the sheet, refreshes the data 👔🚧
    
    # 5. UPDATE: Modify Actions/Methods: Individual items, row but not batch update
    # https://docs.gspread.org/en/v5.4.0/user-guide.html#updating-cells
    @staticmethod
    def update_item(itemdata: str,
                    position: int = 1,
                    coordinate: Optional[str] = None,
                    namerange: Optional[str] = None,
                    editheader: bool = False,
                    defaultvalue: str = ""):
        """App Command: Update an item into the sheet."""
        # 5.1: Connect to the sheet/loads data
        # 5.2: Finds the first item in a row by a row id, and column id: RC1:RC2 or A1 Notation
        # 5.3: Stored the items coordinates/Ai Notation to a datamodel
        # 5.4: Displays item and item context (row data, position, column)
        # 5.5: Updates an item in a row by stored coordinate
        # 5.6: Confirms to user with intermediate display (not commit/saved)
        # 5.7: Sends data to the sheet on confirmation.
        # 5.8: Reloads/refreshed new dataset from the sheet, refreshes the data
        # 5.9: Displays the newly refreshed data, highlighted
    
    # Batch Update: or Matching all Cells verses a query string
    @staticmethod
    def update_items(itemdata: str,
                     searching: str,
                     coordinate: Optional[str] = None,
                     namerange: Optional[str] = None,
                     editheader: bool = False):
        """App Command: Update an item into the sheet."""
        # 5.1: Connect to the sheet/loads data
        # 5.2: Finds the first item in a row by a row id, and column id: RC1:RC2 or A1 Notation
        # 5.3: Stored the items coordinates/Ai Notation to a datamodel
        # 5.4: Displays item and item context (row data, position, column)
        # 5.5: Updates an item in a row by stored coordinate
        # 5.6: Confirms to user with intermediate display (not commit/saved)
        # 5.7: Sends data to the sheet on confirmation.
        # 5.8: Reloads/refreshed new dataset from the sheet, refreshes the data
        # 5.9: Displays the newly refreshed data, highlighted
    
    @staticmethod
    def update_row(rowdata: list[str] = None,
                   position: int = 1,
                   coordinate: Optional[str] = None,
                   namerange: Optional[str] = None,
                   editheader: bool = False):
        """App Command: Update a row into the sheet."""
        # 5.1: Connect to the sheet/loads data
        # 5.2: Updates a row by id - Required
        # 5.2: Updates a row by id and, optionally, a coordinate
        # 5.2: Updates a row by id and, optionally, a named range
        # 5.3: If by id, Returns the items coordinates/Ai Notation to a datamodel/locally
        # 5.3: If by id: updates the entire rowdata
        # 5.4: If by coordinate: updates the row with rowdata (whole or subset)
        # 5.5: If by nameranged: updates the row with rowdata (whole or subset)
        # 5.6: Confirms to user with intermediate display (not commit/saved)
        # 5.7: Reloads/refreshed new dataset from the sheet, refreshes the data
        # 5.9: Displays the newly refreshed data, highlighted (User Feedback)
    
    # 6. FILTER: Reduction of DataSet: by row, column, cell, value, range, etc.
    # https://docs.gspread.org/en/v5.4.0/user-guide.html#filtering
    
    @staticmethod
    def filter_rows(dataset: list[str] = None,
                    selection: str = None,
                    wrapping: Optional[str] = None,
                    showheaders: bool = True,
                    removefilter: bool = False):
        """App Command: Filter a row or contigious rows from the sheet."""
    
    @staticmethod
    def filter_columns(dataset: list[str] = None,
                       selection: str = None,
                       wrapping: str = None,
                       showheader: bool = True,
                       removefilter: bool = False):
        """App Command: Filter a column or contigious rows from the sheet."""
    
    @staticmethod
    def hide_rows(dataset: list[str] = None,
                  selection: str = None,
                  showheaders: bool = True,
                  unhide: bool = False):
        """App Command: Filter a row or contigious rows from the sheet."""
        # Maybe better in Display Class
    
    @staticmethod
    def hide_columns(dataset: list[str] = None,
                     selection: str = None,
                     showheaders: bool = True,
                     unhide: bool = False):
        """App Command: Show/Hide a column or contigious columns from the display/dataset."""
        # Maybe better in Display Class


class Display:
    """Displays the data."""
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def configure_output():
        """Configures the output."""
        pass
    
    @staticmethod
    def display_data(dataset: list[str], switch: int = 0):
        """Displays the data."""
        separator: str = "||"
        carriage: str = "\n"
        flush: typing.List[bool] = [False, True]
        rprint(dataset, sep=separator, end=carriage, flush=flush[switch])
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def display_sheet():
        """Displays the sheet."""
        pass
    
    @staticmethod
    def display_pretty(dataset: list[str], switch: int = 0):
        """Displays the data."""
        rpretty.install()
        separator: str = "||"
        carriage: str = "\n"
        flush: typing.List[bool] = [False, True]
        rprint(dataset, sep=separator, end=carriage, flush=flush[switch])
    
    #
    @staticmethod
    def display_table(dataset: list[str],
                      consoleholder: Console,
                      consoletable: Table,
                      title: str = "PyCriteria"):
        """Displays the data in a table."""
        # https://improveandrepeat.com/2022/07/python-friday-132-rich-tables-for-your-terminal-apps/
        # 1 Set Table
        consoletable.title = title
        # 2 Transform Data to Table
        for row in dataset:
            consoletable.add_row(*row)
        # 3 Print Table
        consoleholder.print(consoletable)


class WebConsole:
    """Web Console."""
    
    console: Console
    options: ConsoleOptions
    table: Table
    
    def __init__(self, width: int, height: int) -> None:
        """Initializes the web console."""
        self.console = self.console_configure()
        self.options = self.console_options(width, height)
        self.table = self.configure_table()
    
    @staticmethod
    def console_options(width: int = 80, height: int = 24) -> ConsoleOptions:
        """Configures the console."""
        max_width: int = width
        max_height: int = height
        windowsize: ConsoleDimensions = ConsoleDimensions(
                width=max_width, height=max_height)
        nolegacy: bool = False
        is_terminal: bool = True
        encoding: str = "utf-8"
        options: ConsoleOptions = ConsoleOptions(
                size=windowsize,
                legacy_windows=nolegacy,
                min_width=max_width,
                max_width=max_width,
                max_height=max_height,
                encoding=encoding,
                is_terminal=is_terminal)
        return options
    
    @staticmethod
    def console_configure() -> Console:
        """Configures the console."""
        _off: bool = False
        _on: bool = True
        _style: rich.style.StyleType = ""
        _tabs: int = 4
        _console: Console = Console(soft_wrap=_on,
                                    style=_style,
                                    tab_size=_tabs,
                                    markup=_on)
        return _console
    
    @staticmethod
    def layout_configure():
        """Configures the Rich layout.
        
        Sets a bounding box for the console.
        """
    
    @staticmethod  #
    def page_data(dataset: list[str]):
        """Displays the data."""
        with console.pager(styles=True):
            rprint(dataset)
    
    @staticmethod
    def configure_table(headings: int = 1) -> rich.table.Table:
        """Configures Rich Console table."""
        wsheet: gspread.Worksheet = Controller.load_wsheet()
        consoletable: rich.table.Table = Table()
        selectheaders: dict[str, str] = tablesettings.CRITERIA_FILTER
        headersrange: str = tablesettings.HEADERS_RANGE
        _headers: list[str] = wsheet.row_values(headings)
        
        def configure_columns(_headers: list[str]):
            """Configures the headers."""
            for _header in _headers:
                # Check if the header is the predefined headers by values
                if _header in selectheaders.values():
                    # Use list comprehension to get the key from the value: reverse lookup
                    key = list(selectheaders.keys())[list(selectheaders.values()).index(_header)]
                    # Use the key to get the value from the dictionary
                    if key in headersrange:
                        consoletable.add_column(selectheaders[key])
        
        configure_columns(_headers)
        return consoletable


class Topics:
    """Topics."""
    currenttopic: list[str]
    datatransformr: DataTransform
    
    def __init__(self):
        """Init."""
        self.currenttopic: list[str] = []
        self.datatransformr: DataTransform = DataTransform()
    
    @classmethod
    def load_uniques(cls, columnname: str) -> list[str]:
        """Loads the unqiue topics of a column."""
        _worksheet: gspread.Worksheet = Controller.load_wsheet()
        _heading: str = columnname
        currenttopics: list[str] = transformer.column_uniques(_worksheet, _heading)
        return currenttopics
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def add_topic():
        """Adds a topic."""
        pass
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def remove_topic():
        """Removes a topic."""
        pass


class Entry:
    """Entry: Prompt, Input, Confirm."""
    
    reference: str
    criteria: str
    note: str
    todo: str
    topics: list[str]
    todo_state: typing.Tuple[str, str] = ("unchecked", "checked")
    categories = Topics()
    
    def __init__(self):
        """Init."""
        self.reference: str = ""
        self.criteria: str = ""
        self.note: str = ""
        self.todo: str = ""
        self.topics: list[str] = Topics.load_uniques("CriteriaTopics")
    
    @staticmethod
    def prompt_addreferenece() -> str:
        """Prompts the user to add a reference.
        Prints a guidance message on how to format the input.
        Takes only a string input for the reference (type: str].
        :returns: str: User input for the reference
        Test elsewhere for the format of the input.
        """
        prompttext: str = \
            ("A criteria reference has a format of x.x.x. \n"
             + "Example: Uses multi-level list notations. \n"
             + "1.2.0 is a reference to the second criteria of the first topic.\n"
             + "Where 1 is the top item, 2 is the sub item, and 0 is the sub.sub item.\n")
        rprint(prompttext, flush=True)
        return Prompt.ask("Enter a x.x.x reference for the item?")
    
    @staticmethod
    def prompt_addcriteria():
        """Prompts the user."""
        return Prompt.ask("Enter a criteria text to this item?")
    
    @staticmethod
    def prompt_addnote() -> str:
        """Prompts the user."""
        return Prompt.ask("Enter a note for this item?")
    
    @staticmethod
    def prompt_selecttopic(topicslist: list[str], is_choices: bool = True):
        """Prompts the user to update."""
        prompttext: str = "\\\\n".join([f"{i}. {topic}"
                                        for i, topic
                                        in enumerate(topicslist, 1)])
        rprint(prompttext, flush=True)
        rprint("Enter the name, not the number", flush=True)
        return Prompt.ask("Choose a new topic for the critera?",
                          choices=topicslist,
                          default=topicslist[
                              0], show_choices=is_choices)
    
    @staticmethod
    def prompt_checktodo(state: typing.Tuple[str, str] = todo_state) -> str:
        """Prompts the user to toggle the todo."""
        _state: list[str] = [state[0].lower(), state[1].lower()]
        return Prompt.ask("Choose to check, or not the todo item?",
                          choices=_state, default=_state[0])


def main():
    """Main."""
    # Initilse WebConsole
    webconsole: WebConsole = WebConsole(width=80, height=20)
    mainconsole: Console = webconsole.console
    maintable: Table = webconsole.table
    # 0.1: Load the data
    data: list[str] = Controller.load_data()
    # 0.2: Display the data
    Display.display_table(data,
                          mainconsole,
                          maintable)
    # 0.3: Upload the data


if __name__ == '__main__':
    warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    main()
