#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN101, I001, ARG002
"""Module: Controller for the Terminal App."""
import dataclasses
# 0.1 Standard Library Imports
import typing
import warnings
from typing import NoReturn, Type

import click
# 0.2 Third Party Modules: Compleete
import gspread  # type: ignore
import gspread_dataframe  # type: ignore
import pandas as pd  # type: ignore
import rich.style  # type: ignore
# 0.2 Third Party Modules: Individual
from click import echo  # type: ignore
from gspread_dataframe import get_as_dataframe as get_gsdf  # type: ignore
from rich import pretty as rpretty, print as rprint  # type: ignore
from rich.console import Console, ConsoleDimensions, ConsoleOptions  # type: ignore
from rich.prompt import Prompt  # type: ignore
from rich.table import Table  # type: ignore

# 0.3 Local imports
import connections
import settings
from datatransform import DataTransform
from sidecar import ProgramUtils

utils: ProgramUtils = ProgramUtils()
connector: connections.GoogleConnector = connections.GoogleConnector()
configuration: settings.Settings = settings.Settings()

tablesettings: settings.TableSettings = settings.TableSettings()
console: rich.console.Console = Console()
transformer: DataTransform = DataTransform()  # deprecate: remov datatransform.py


# 2. Read the data from the sheet by the controller
# plylint: disable=line-too-long
class Controller:
    """Controller.

    Methods:
    -------
    :method: refresh: Refreshed entired connection, sheet, worksheet, and data.
    :method: load_wsheet: Loads the worksheet.
    :method: load_data: Loads the worksheet.
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
    def fetch_data() -> list[str]:
        """Loads the data.
        
        Deprecated: Use load_dataf instead.
        """
        # 1.1: Connect to the sheet
        # 1.2: Read the data from the sheet
        # 1.3: Return the data from the sheet
        wsheet: gspread.Worksheet = Controller.load_wsheet()
        return transformer.get_data(wsheet, "H2:010")
    
    @staticmethod
    def delete(creds: gspread.Client) -> None:
        """Deletes/Cloes the client."""
        # https://www.perplexity.ai/search/ac897d0d-bd38-4ebd-9a12-1e90fc172977?s=c
        if not isinstance(creds, gspread.Client):
            raise ValueError("Invalid: "
                             "'creds' is not a authorised Client")
        
        if creds.session is not None:
            try:
                creds.session.close()
            except Exception as e:
                click.echo(f"Error closing session: {e}", err=True)
            finally:
                creds.session = None
        
        try:
            del creds
        except Exception as e:
            click.echo(f"Error deleting client: {e}", err=True)


@dataclasses.dataclass(frozen=True)
class ColumnSchema:
    """Column Names: simple Dataschema for the Datamodel.
    
    Usage:
    To reduce string repetition, as per datamodel, and simplify reuse.
    Done by centralising string values into one class/instance, for config.
    
    Future:
    Additionally, this class could be (future feature) used to
    dynamically generate/CRUD any changed in the Google sheet
    without negatively impacting the codebase and raising KeyErrors.
    
    

    Attributes:
    ----------
    property: Row: str
    property: Position: str
    property: Tier: str
    property: Prefix: str
    property: Depth: str
    property: DoD: str
    property: Performance: str
    property: Group: str
    property: Topic: str
    property: Reference: str
    property: Criteria: str
    property: Progress: str
    property: Flag: str
    property: Notes: str
    ------
    """
    Row: str = "RowID"
    Position: str = "Position"
    Tier: str = "Tier"
    Prefix: str = "TierPrefix"
    Depth: str = "TierDepth"
    DoD: str = "DoD"
    Performance: str = "Performance"
    Group: str = "CriteriaGroup"
    Topic: str = "Topic"
    Reference: str = "CriteriaRef"
    Criteria: str = "Criteria"
    Progress: str = "Progress"
    Flag: str = "ToDoFlag"
    Notes: str = "Notes"
    Related: str = "LinkedRef"


class Headers:
    """Headers.

    Attributes:
    ----------
    property: Criteria: list[Column]
    property: Project: list[Column]
    property: MetaData: list[Column]
    property: References: list[Column].
    
    Where Column is an Enum of the column names or a subset.
    """
    c: ColumnSchema = ColumnSchema()
    CriteriaView: list[str] = [c.Row, c.Position, c.Topic,
                               c.Reference, c.Criteria, c.Notes]
    ProjectView: list[str] = ["RowID", "Position", "Tier", "DoD", "CriteriaRef", "Progress", "ToDoFlag"]
    ToDoAllView: list[str] = ["RowID", "Position", "Performance", "DoD", "Criteria", "Progress", "Notes"]
    ToDoSimpleView: list[str] = ["Position", "Criteria", "Progress", "Notes"]
    ToDoDoDView: list[str] = ["Position", "DoD", "Criteria", "Progress"]
    ToDoGradeView: list[str] = ["Position", "Criteria", "Performance", "DoD"]
    ToDoReviewView: list[str] = ["CriteriaRef", "Criteria", "Performance", "Progress"]
    NotesView: list[str] = ["Position", "Criter", "Notes"]
    ReferenceView: list[str] = ["Position", "CriteriaRef", "LinkedRef"]
    ViewFilter: list[str] = ["Criteria", "Project", "ToDo", "References"]
    ToDoChoices: list[str] = ["All", "Simple", "DoD", "Grade", "Review"]
    
    def __init__(self, labels: ColumnSchema) -> None:
        """Headers."""
        self.c = labels


class DataController:
    """DataController for the effort of loading the data, fetching it, managing it.

    Links the connector to the app's command:

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
    :method: load_dataf: Loads the dataframe from the sheet.
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
    
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    ###
    
    dataframe: pd.DataFrame
    wsheet: gspread.Worksheet
    gsdframe: gspread_dataframe
    
    def __init__(self, wsheet: gspread.Worksheet) -> None:
        """Initialies the DataController."""
        # Load the data into a panda dataframe
        self.wsheet = wsheet
        self.dataframe = pd.DataFrame(wsheet.get_all_records())
        self.gsdframe = get_gsdf(self.wsheet, parse_dates=True, header=1)
    
    # https://www.w3schools.com/python/pandas/pandas_dataframes.asp
    
    # Use gspread_dataframe.set_with_dataframe(worksheet, dataframe,
    # row=1, col=1, include_index=False, include_column_header=True,
    # resize=False, allow_formulas=True, string_escaping='default')
    # Sets the values of a given DataFrame, anchoring its upper-left
    # corner at (row, col).
    # (Default is row 1, column 1.)
    # https://gspread-dataframe.readthedocs.io/en/latest/
    
    def load_dataframe_wsheet(self, wsheet: gspread.Worksheet) -> pd.DataFrame | None:
        """Loads the worksheet into a dataframe.

        :param wsheet: gspread.Worksheet: The worksheet to load
        :return: pd.DataFrame | None: The dataframe or None
        """
        if wsheet.get_all_records():
            dataframe: pd.DataFrame = pd.DataFrame(wsheet.get_all_records())
            self.dataframe = dataframe
            return dataframe
        
        rprint("No data loaded from Google Sheets.")
        return None
    
    def load_dataf(self, wsheet: gspread.Worksheet,
                   filterr: str,
                   dimensions=None) -> pd.DataFrame:  # noqa: ANN001
        """Load the data into a panda dataframe.

        :param wsheet: gspread.Worksheet: The worksheet to load the data from
        :param filterr: str: The filter to apply to the data
        :param dimensions: list[str]: The dimensions to load
        """
        if filter and dimensions:
            self.dataframe = self.dataframe.loc[filterr, dimensions]
        elif filterr:
            self.dataframe = self.dataframe.loc[filterr]
        elif dimensions:
            self.dataframe = self.dataframe.loc[:, dimensions]
        else:
            self.dataframe = pd.DataFrame(wsheet.get_all_records())
        
        return self.dataframe
    
    def find_rows(self, query: str) -> pd.DataFrame:
        """Find Rows by a query.

        :param query: str: The query to search for
        :return: pd.DataFrame
        """
        return self.dataframe.query(query)
    
    def filter_rows(self, position: int) -> pd.Series:
        """Filter rows in the dataframe."""
        return self.dataframe.iloc[position]
    
    def filter_columns(self, columns: str) -> pd.DataFrame:
        """Filter columns in the dataframe."""
        self.dataframe = self.dataframe.loc[:, columns]
        return self.dataframe
    
    def add_item(self, position: int, item: str) -> pd.Series:
        """Add an item to the dataframe."""
        self.dataframe.iloc[position] = item
        return self.dataframe.iloc[position]
    
    def add_row(self, position: int, values: list | dict) -> pd.Series:
        """Add a row to the dataframe at the specified position."""
        self.dataframe.loc[position] = values
        return self.dataframe.loc[position]
    
    def update_item(self, position: int, item: str) -> pd.Series:
        """Update an item in the dataframe."""
        self.dataframe.iloc[position] = item
        return self.dataframe.iloc[position]
    
    def update_row(self, position: int, values: list | dict) -> pd.Series | None:
        """Update a row in the dataframe."""
        for index, row in self.dataframe.iterrows():
            if all(row == values):
                continue
            
            self.dataframe.iloc[index] = values
            return self.dataframe.iloc[index]
        
        return None
    
    def update_tarow(self, position: int, values: dict) -> pd.Series | None:
        """Update a row in the dataframe."""
        row = pd.Series(values)
        if all(self.dataframe.iloc[position] == row):
            return None
        self.dataframe.iloc[position] = row
        return self.dataframe.iloc[position]
    
    def delete_item(self, position: int, item: str) -> pd.Series:
        """Delete an item in the dataframe."""
        self.dataframe.iloc[position] = ""
        return self.dataframe.iloc[position]
    
    def delete_row(self, position: int, values: list | dict) -> pd.DataFrame | None:
        """Delete a row in the dataframe."""
        for index, row in self.dataframe.iterrows():
            if all(row == values):
                self.dataframe = self.dataframe.drop(index)
                return self.dataframe
        return None


class WebConsole:
    """Web Console."""
    
    console: Console
    options: ConsoleOptions
    table: Table
    
    def __init__(self, width: int, height: int) -> None:
        """Initialises the web console."""
        self.console = self.console_configure()
        self.options = self.console_options(width, height)
        self.table = Table()
    
    @staticmethod
    def console_options(width: int = configuration.Console.WIDTH,
                        height: int = configuration.Console.HEIGHT) -> ConsoleOptions:
        """Configures the console."""
        max_width: int = width
        max_height: int = height
        windowsize: ConsoleDimensions = ConsoleDimensions(
                width=max_width, height=max_height)
        nolegacy: bool = False
        is_terminal: bool = True
        encoding: str = configuration.ENCODE
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
    def layout_configure() -> None:
        """Configures the Rich layout.

        Sets a bounding box for the console.
        """
    
    @staticmethod  #
    def page_data(dataset: list[str]) -> None | NoReturn:
        """Displays the data."""
        with console.pager(styles=True):
            rprint(dataset)
    
    @staticmethod
    def configure_table(headers: typing.Optional[list[str]]) -> rich.table.Table:
        """Configures Rich Console table."""
        consoletable: rich.table.Table = Table()
        
        def configure_columns(headings: list[str]) -> None:
            """Configures the headers."""
            if isinstance(headings, list):
                for header in headings:
                    # Check if the header is the predefined headers by values
                    consoletable.add_column(header)
            
            else:
                # raise TypeError("The headers must be a list of strings.")
                click.echo("No Headers. Text only", err=True)
        
        configure_columns(headings=headers)
        return consoletable
    
    @staticmethod
    def set_datatable(dataframe: pd.DataFrame) -> rich.table.Table:
        """Sets the table per dataframe."""
        headers: list[str] = dataframe.columns.tolist()
        consoletable: Table = WebConsole.configure_table(headers=headers)
        return consoletable


WebConsoleType: Type[WebConsole] = WebConsole


class Display:
    """Displays the data."""
    ColumnResultType: Type[tuple] = tuple[str, str, pd.DataFrame]
    ItemSelectType: Type[tuple] = tuple[str, str, pd.DataFrame]
    LineNoSelectType: Type[tuple] = tuple[int, pd.DataFrame]
    ColumnSelectType: Type[tuple] = tuple[str, pd.DataFrame]
    SearchColumnQueryType: Type[tuple] = tuple[str, str, pd.DataFrame]
    
    ViewType: str = \
        typing.Literal["table", "column", "list", "frame", "pager",
        "tablepage", "columnpage", "listpage", "framepage"]
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def configure_output():
        """Configures the output."""
        pass
    
    @staticmethod
    def display_datalist(dataset: list[str], switch: int = 0) -> None:
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
    def display_pretty(dataset: list[str], switch: int = 0) -> None:
        """Displays the data."""
        rpretty.install()
        separator: str = "||"
        carriage: str = "\n"
        flush: typing.List[bool] = [False, True]
        rprint(dataset, sep=separator, end=carriage, flush=flush[switch])
    
    @staticmethod
    def display_data(dataframe: pd.DataFrame,
                     consoleholder,  # noqa: ANN001
                     consoletable: Table,
                     title: str = "PyCriteria") -> None:  # noqa: ANN001
        """Display Data: Wrapper for Any display."""
        # consoleholder.set_table(consoleholder, dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=consoleholder,
                              consoletable=consoletable,
                              title=title)
    
    @staticmethod
    def display_views(dataframe: pd.DataFrame,
                      consoleholder,  # noqa: ANN001
                      view: ViewType = "table",
                      title: str = "PyCriteria") -> None:
        """Display Data: Wrapper for Any display."""
        pass
    
    @staticmethod
    def display_table(dataset: list[str],
                      consoleholder: Console,
                      consoletable: Table,
                      title: str = "PyCriteria") -> None | NoReturn:
        """Displays the data in a table."""
        # https://improveandrepeat.com/2022/07/python-friday-132-rich-tables-for-your-terminal-apps/
        # 1 Set Table
        consoletable.title = title
        # 2 Transform Data to Table
        for row in dataset:
            consoletable.add_row(*row)
        # 3 Print Table
        consoleholder.print(consoletable)
        return None
    
    @staticmethod
    def display_frame(dataframe: pd.DataFrame,
                      consoleholder: Console,
                      consoletable: Table,
                      title: str = "PyCriteria") -> None | NoReturn:
        """Displays the data in a table."""
        consoletable.title = title
        
        for column in dataframe.columns:
            # Create the table header headers
            consoletable.add_column(header=column)
        for _index, row in dataframe.iterrows():
            # For each column, in dataframe's columns
            # Retrieve the string value of the row by column refernece
            # Then add the row to the table
            consoletable.add_row(*[str(row[column]) for column in dataframe.columns])
        
        consoleholder.print(consoletable)
    
    # The following is an AI Refactor from orginal authored code
    # https://www.perplexity.ai/search/c8250a15-6f8c-4180-b277-349f9ccf83c8?s=c
    @staticmethod
    def display_subframe(dataframe: pd.DataFrame,
                         consoleholder: Console | WebConsole,
                         consoletable: Table,
                         headerview: Headers | list[str] | str,
                         viewfilter: Headers.ViewFilter = "Criteria") -> None | NoReturn:
        """Displays the data in a table."""
        # AI refactor put in place these guard conditions for the headerview
        if isinstance(headerview, Headers):
            headers: list = getattr(headerview, viewfilter)
        elif isinstance(headerview, list):
            headers: list = headerview
        else:
            headers: list = [headerview]
        
        filteredcolumns: pd.DataFrame = \
            dataframe.loc[:, dataframe.columns.isin(values=headers)]
        # for column in headerview:
        # consoletable.add_column(header=column)
        for _index, row in filteredcolumns.iterrows():
            consoletable.add_row(*[str(row[column])
                                   for column in headers])
        consoleholder.print(consoletable)
    
    @staticmethod
    def display_search(output: tuple,
                       consoleholder: Console,
                       consoletable: Table,
                       title: str = "PyCriteria") -> None | NoReturn:
        """Displays the search accoridng to an output's result-set.
        
        A ResultSet is a type of tuple that varies in length and component types.
        A resultset is used to carry the parameters of a search along
            with the results of that search from
             a) the command's stdin
             b) to the cli's stdout or stderr.
        The ResultSet is a tuple of the following types:
            i) SearchColumnResultType: tuple[str, str, pd.DataFrame]
                i.e. header, query, dataframe
            ii) ItemSelectType: tuple[str, str, pd.DataFrame]
        Parameters:
        --------------------
        :param output: tuple: The output of the search
        :param consoleholder: Console: The console to print to
        :param consoletable: Table: The table to print to
        :param title: str: The title of the table
        """
        if ValidationQuerySetType.querysetcolumntype(output):
            # If the output is a tuple of item selection
            # Display the item selection
            # Prints out the item's coordinates
            headers, query, dataframe = output
            Display.display_frame(dataframe=dataframe,
                                  consoleholder=consoleholder,
                                  consoletable=consoletable,
                                  title=title)
            echo(message=(f"You searched for: Query: {query}"
                          + f"Against this Header: {headers}")),
    
    @staticmethod
    def display_selection(output: tuple,
                          consoleholder,  # noqa: ANN001
                          consoletable: Table,
                          title: str = "PyCriteria") -> None | NoReturn:  # noqa: ANN001
        """Displays the selection accoridng to an output's result-set.
        
        A ResultSet is a type of tuple that varies in length and component types.
        A resultset is used to carry the parameters of a selection along
            with the results of that selection from
             a) the command's stdin
             b) to the cli's stdout or stderr.
        The ResultSet is a tuple of the following types:
        1. ItemSelectType: tuple[str, str, pd.DataFrame]
        2. LineNoSelectType: tuple[int, pd.DataFrame]
        3. ColumnResultType: tuple[str, str, pd.DataFrame]
        
        Parameters:
        --------------------
        :param output: tuple: The output of the selection
        :param consoleholder: Any: The console to print to
        :param consoletable: Table: The table to print to
        :param title: str: The title of the table
        

        Returns:
        --------------------
        :return: None | NoReturn: This displays to the stdout/stderr
        """
        # Uses the return Data Structure types, i.e, of outputto determine the display set
        
        if ValidateResultSetTypes.selectitemtype(output):
            # If the output is a tuple of item selection
            # Display the item selection
            # Prints out the item's coordinates
            headers, linenumber, dataframe = output
            consoleholder.set_table(dataframe=dataframe)
            Display.display_frame(dataframe=dataframe,
                                  consoleholder=consoleholder,
                                  consoletable=consoletable,
                                  title=title)
            echo((f"Selected Reference: Line Number: {linenumber}\n"
                  + f"Selected Column: Header: {headers}"))
        elif ValidateResultSetTypes.selectrowtype(output):
            # If the output is a tuple of row selection
            # Display the row in a table.
            # Print the row selected
            linenumber, dataframe = output
            consoleholder.set_table(dataframe=dataframe)
            Display.display_frame(dataframe, consoleholder, consoletable, title)
            rprint(f"Selected Row: Line Number: {linenumber}")
        elif ValidateResultSetTypes.selectcolumntype(output):
            # If the output is a tuple of column selection
            # Display the column in a table.
            # Print the column selected
            header, dataframe = output
            consoleholder.set_table(dataframe=dataframe)
            Display.display_frame(dataframe, consoleholder, consoletable, title)
            echo(f"Selected Column\'s: Header: {header}")
        else:
            # If the output is not of the above types
            # Display an exception message, raise no error (yet_
            echo(message=('The parameter out is not '
                          + f'the correct resultset type: {output}'), err=True)


class ValidateResultSetTypes:
    """Validates the resultset types. From CRUD + Find/Select Ops.
    
    :method: selectitemtype: Checks the item resultset types.
    :method: selectrowtype: Checks the row resultset types.
    :method: selectcolumntype: Checks the column's resultset types.
    """
    
    @staticmethod
    def selectitemtype(typecheck: tuple) -> bool:
        """Checks the item types.
        
        ItemSelectTypes: Tuple[str, int, pd.DataFrame]
        Format: (header, linenumber, dataframe).
        """
        if (isinstance(typecheck, tuple) and
                typing.get_args(typing.get_type_hints(Display)['ItemSelectType']) ==
                (str, int, pd.DataFrame)):
            echo("Output is not of type Display.ItemSelectType")
            return False
        
        echo("Output is of type Display.ItemSelectType")
        return True
    
    @staticmethod
    def selectrowtype(typecheck: tuple) -> bool:
        """Checks the item types.
        
        RowSelectTypes: Tuple[int, pd.DataFrame]
        Format: (linenumber, dataframe).
        """
        if not (isinstance(typecheck, tuple) and
                typing.get_args(typing.get_type_hints(Display)['RowSelectType']) ==
                (int, pd.DataFrame)):
            
            echo("Output is not of type Display.ItemSelectType")
            return False
        
        echo("Output is of type Display.ItemSelectType")
        return True
    
    @staticmethod
    def selectcolumntype(typecheck: tuple) -> bool:
        """Checks the item types.
        
        ColumnSelectType: Tuple[str, pd.DataFrame].
        """
        if (isinstance(typecheck, tuple) and
                typing.get_args(typing.get_type_hints(Display)['ColumnSelectType']) ==
                (str, pd.DataFrame)):
            
            echo("Output is not of type Display.ColumnSelectType")
            return False
        
        echo("Output is of type Display.ColumnSelectType")
        return True


class ValidationQuerySetType:
    """Validates the query types. From CRUD + Find/Select Ops."""
    
    @staticmethod
    def querysetitemtype(typecheck: tuple) -> bool:
        """Checks the item types."""
        pass
    
    @staticmethod
    def querysetcolumntype(typecheck: tuple) -> bool:
        """Checks the item types.
        
        ColumnQueryTypes: Tuple[str, pd.DataFrame].
        """
        if not (isinstance(typecheck, tuple) and
                typing.get_args(typing.get_type_hints(Display)['SearchColumnQueryType']) ==
                (str, str, pd.DataFrame)):
            rprint("Output is not of type Display.SearchColumnQueryType")
            return False
        
        rprint("Output is of type Display.SearchColumnQueryType")
        return True


class Entry:
    """Entry: Prompt, Input, Confirm."""
    
    reference: str
    criteria: str
    note: str
    todo: str
    topics: list[str]
    todo_state: typing.Tuple[str, str] = ("unchecked", "checked")
    
    def __init__(self):
        """Init."""
        self.reference: str = ""
        self.criteria: str = ""
        self.note: str = ""
        self.todo: str = ""
        # self.topics: list[str] = Topics.load_uniques("CriteriaTopics")
    
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
    def prompt_selecttopic(topicslist: list[str], is_choices: bool = True) -> str:
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


# def main():
#    """Main."""
#    # Initilse WebConsole
#    webconsole: WebConsole = WebConsole(width=configuration.Console.WIDTH,
#                                        height=configuration.Console.HEIGHT)
#    mainconsole: Console = webconsole.console
#    maintable: Table = webconsole.table
# 0.1: Load the data
#    data: list[str] = Controller.load_data()
# 0.2: Display the data
#    Display.display_table(data,
#                          mainconsole,
#                         maintable)
# 0.3: Upload the data

ActionType = typing.Literal["default", "error", "ignore", "always", "module", "once"]


def warn(hide: bool = True, action: ActionType = "ignore") -> None:
    """Configured Python Interpreter warnings.

    Added: typing.Literal[str] : Invalid Type
    Fixme: 'Literal' may be parameterised with literal ints, byte and unicode
            strings, bools, Enum values, None, other literal types, or type
            aliases to other literal types

    Parameters:
    ====================
    :param hide: bool:
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
    if hide:
        warnings.filterwarnings(action, message=".*deprecated.*", category=DeprecationWarning)
        warnings.filterwarnings(action, category=ResourceWarning)

# if __name__ == '__main__':
#     warn(hide=True, action="ignore")
#     main()
