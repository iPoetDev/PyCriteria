#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN101, I001, ARG002, PLR0913, ANN001, ANN102
"""Module: Controller for the Terminal App.

Usage:
-------------------------
- Controller: Controller for the Terminal App.
- DataController: Data Controller for the Terminal App.
- ColumnSchema: Column Schema DataViews
- Headers: Views by Headers selection: READING, LOADING, VIEWS, DISPLAY
- RICHStyler: Rich.Style Defintions class and methods for the app terminal.
              Used on each Record
- Webconsole: Console class and methods for WEB versions of the app.
- Inner: Inner Terminal layouts, arrangement.Deprecate?  # noqa
- Record: Record class for displying individual record detials.
- Editor: C(R)UD Operations, and Editor Controller/Model:

Linting:
-------------------------
- pylint: disable=trailing-whitespace
- ruff: noqa:
      F841:     unused-variable
                Local variable {name} is assigned to but never used
      ARG002:   unused-method-argument
                Unused method argument: {name}
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

:class: Controller: Controller for the Terminal App.
:class: ColumnSchema: Column Schema DataViews
:class: Headers: Views by Headers selection: READING, LOADING, VIEWS, DISPLAY
:class: RICHStyler: Rich.Style Defintions class and methods for the app.
:class: WebConsole: Console class and methods for WEB versions of the app.
:class: Inner: Inner Terminal layouts, arrangement.Deprecate?  # noqa
:class: Display: Shared Mixed resposnibility with CriteriaApp, and Record
        Refactor candidates.
        Evoling design artefact
:class: Record: Individual Records, and Records Display/Controller/Model:
:class: Editor: C(R)UD Operations, and Editor Controller/Model:

Global Variables:,
-------------------------
:var: connector: connections.GoogleConnector = connections.GoogleConnector()
:var: configuration: settings.Settings = settings.Settings()
:var: console: Console = Console()
:var: stylde: Style = RICHStyleR()

"""

# 0.1 Standard Library Imports
import datetime
import typing
from typing import NoReturn, Type, Literal

#
# 0.2.1 Third Party Modules: Compleete
import click
import gspread  # type: ignore
import gspread_dataframe  # type: ignore
import pandas as pd  # type: ignore
import rich
#
# 0.2.2 Third Party Modules: Individual, Aliases
from gspread_dataframe import (set_with_dataframe as set_remote,
                               get_as_dataframe as get_gsdf,  # type: ignore
                               )
from rich import print as rprint, box  # type: ignore
from rich.console import (Console, ConsoleDimensions,
                          ConsoleOptions, )  # type: ignore
from rich.layout import Layout  # type: ignore
from rich.panel import Panel  # type: ignore
from rich.style import Style  # type: ignore
from rich.table import Table  # type: ignore

#
# 0.3 Local imports
import connections
import settings
from modelview import ColumnSchema, Headers

#
# 1.1: Global/Custom Variables
connector: connections.GoogleConnector = connections.GoogleConnector()
configuration: settings.Settings = settings.Settings()
console: Console = Console()


# 2. Read the data from the sheet by the controller

class Controller:
    """Controller.

    Methods:
    -------
    :method: load_wsheet: Loads the worksheet.
    :method: load_data: Loads the worksheet.
    """
    
    @staticmethod
    def load_wsheet() -> gspread.Worksheet:
        """Loads a worksheet.

        :return: gspread.Worksheet:
            The current worksheet to extract the data.
        """
        # 1.1: Connect to the sheet
        # -> Move to Instance once the data is loaded
        # is tested and working on heroku
        creds: gspread.Client = \
            connector.connect_to_remote(
                configuration.CRED_FILE)
        # 1.2: Read the data from the sheet
        # -> Move to Instance once the data is
        # loaded is tested and working on heroku
        spread: gspread.Spreadsheet = \
            connector.get_source(creds,
                                 configuration.SHEET_NAME)
        # 1.3: Return the data from the sheet
        # -> Move to Instance once the data is
        # loaded is tested and working on
        # heroku
        return connector.open_sheet(spread, configuration.TAB_NAME)
    
    @staticmethod
    def delete(creds: gspread.Client) -> None:
        """Deletes/Close the client.
        
        :param creds: gspread.Client:
        :return: None
        """
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


class DataController:
    """DataController."""
    
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
        self.gsdframe = get_gsdf(self.wsheet,
                                 parse_dates=True, header=1)
    
    # https://www.w3schools.com/python/pandas/pandas_dataframes.asp
    
    # Use gspread_dataframe.set_with_dataframe(worksheet, dataframe,
    # row=1, col=1, include_index=False, include_column_header=True,
    # resize=False, allow_formulas=True, string_escaping='default')
    # Sets the values of a given DataFrame, anchoring its upper-left
    # corner at (row, col).
    # (Default is row 1, column 1.)
    # https://gspread-dataframe.readthedocs.io/en/latest/
    
    @classmethod
    def load_dataframe_wsheet(cls, wsheet: gspread.Worksheet) \
        -> pd.DataFrame | None:  # noqa ANN102
        """Loads the worksheet into a dataframe.

        :param wsheet: gspread.Worksheet: The worksheet to load
        :return: pd.DataFrame | None: The dataframe or None
        """
        if wsheet.get_all_records():
            dataframe: pd.DataFrame = \
                pd.DataFrame(wsheet.get_all_records())
            return dataframe
        
        rprint("No data loaded from Google Sheets.")
        return None
    
    @classmethod
    def send_dataframe_wsheet(cls, dataframe: pd.DataFrame,
                              sheet: gspread.Worksheet) -> None:  # noqa ANN102
        """Sends the dataframe to the worksheet.

        :param dataframe: pd.DataFrame: The dataframe to send
        :param sheet: gspread.Worksheet: The worksheet to send to
        :return: None
        """
        if sheet.get_all_records() and dataframe.empty is False:
            set_remote(worksheet=sheet, dataframe=dataframe)


class RICHStyler:
    """Rich Styler for Rich.console Style."""
    style = Style()
    
    def __init__(self) -> None:
        """Initialises the TUI Styler."""
        self.style = Style()
    
    @staticmethod
    def panel(grey: int, tostring: bool = True) -> Style | str:
        """Returns the Style for the property.
        
        :param grey: int: The grey level
          https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param tostring: bool: Whether to return a string or Style
        """
        emp: str = "bold"
        co: str = "white"
        bg: str = f"grey{grey}"
        styled: str = f'{emp} {co} on {bg}'
        return styled if tostring else RICHStyler.style.parse(styled)
    
    @staticmethod
    def label() -> Style:
        """Style the text.
        
        :return: Style: The style
        """
        emp: str = "bold"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def property() -> Style:
        """Returns the Style for the property.
        
        :return: Style: The style
        """
        emp: str = "bold"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def value() -> Style:
        """Returns the Style for the property.
        
        :return: Style: The style
        """
        emp: str = "italic"
        co: str = "dark_turquoise"
        bg: str = "black"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def modified() -> Style:
        """Returns the Style for the property.
        
        :return: Style: The style
        """
        emp: str = "italic"
        co: str = "deep_pink3"
        bg: str = "black"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def heading() -> Style:
        """Returns the Style for the property.
        
        :return: Style: The style
        """
        emp: str = "bold italic underline2"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def border(stylestr: bool = True) -> Style | str:
        """Returns the Style for the property.
        
        :param stylestr: bool: Whether to return a string or Style
        :return: Style | str: The style or style string
        """
        emp: str = "bold"
        bg: str = "grey93"
        styled: str = f'{emp} {bg}'
        return styled if stylestr else RICHStyler.style.parse(styled)


styld = RICHStyler


class WebConsole:
    """Web Console."""
    
    console: Console
    options: ConsoleOptions
    table: Table
    terminal: Layout
    
    def __init__(self, width: int, height: int) -> None:
        """Initialises the web console."""
        self.console = self.console_configure()
        self.options = self.console_options(width, height)
        self.table = Table()
        self.terminal = Layout()
    
    @staticmethod
    def console_options(width: int = configuration.Console.WIDTH,
                        height: int = configuration.Console.HEIGHT) \
        -> ConsoleOptions:  # noqa # Pep8 E125
        """Configures the console.
        
        :param width: int: The width of the console
        :param height: int: The height of the console
        :return: ConsoleOptions
        """
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
        """Configures the console.
        
        :return: Console
        """
        _off: bool = False
        _on: bool = True
        _style: rich.style.StyleType = ""
        _tabs: int = 4
        _console: Console = Console(soft_wrap=_on,
                                    style=_style,
                                    tab_size=_tabs,
                                    markup=_on)
        return _console
    
    @staticmethod  #
    def page_data(dataset: list[str]) -> None | NoReturn:
        """Displays the data.
        
        :param dataset: list[str]: The dataset to display.
        :return: None | NoReturn:
        """
        with console.pager(styles=True):
            rprint(dataset)
    
    @staticmethod
    def configure_table(headers: typing.Optional[list[str]]) \
        -> rich.table.Table:  # noqa # Pep8 E125
        """Configures Rich Console table.
        
        :param headers: list[str]: The headers for the table.
        :return: rich.table.Table
        """
        consoletable: rich.table.Table = Table()
        
        def configure_columns(headings: list[str]) -> None:
            """Configures the headers."""
            if isinstance(headings, list):
                for header in headings:
                    # Check if the header is the predefined headers by values
                    consoletable.add_column(header)
            
            else:
                click.echo("No Headers. Text only", err=True)
        
        configure_columns(headings=headers)
        return consoletable
    
    @staticmethod
    def set_datatable(dataframe: pd.DataFrame | pd.Series) -> rich.table.Table:
        """Sets the table per dataframe.
        
        :param dataframe: Pandas DataFrame or Series object.
        :return: rich.table.Table
        """
        if isinstance(dataframe, pd.DataFrame):
            headers: list[str] = dataframe.columns.tolist()
        elif isinstance(dataframe, pd.Series):
            headers: list[str] = dataframe.index.tolist()
        else:
            raise ValueError("Bad Parameter: Pandas DataFrame"
                             " or Series object.")
        
        consoletable: Table = WebConsole.configure_table(headers=headers)
        return consoletable


class Display:
    """Displays the data."""
    ColumnResultType: Type[tuple] = tuple[str, str, pd.DataFrame]
    ItemSelectType: Type[tuple] = tuple[str, str, pd.DataFrame]
    LineNoSelectType: Type[tuple] = tuple[int, pd.DataFrame]
    ColumnSelectType: Type[tuple] = tuple[str, pd.DataFrame]
    SearchColumnQueryType: Type[tuple] = tuple[str, str, pd.DataFrame]
    
    ViewType: str = \
        typing.Literal["table", "column", "list", "frame", "pager",
        "tablepage", "columnpage", "listpage", "framepage"]  # noqa
    
    @staticmethod
    def display_data(dataframe: pd.DataFrame,
                     consoleholder,  # noqa: ANN001
                     consoletable: Table,
                     title: str = "PyCriteria") -> None:  # noqa: ANN001
        """Display Data: Wrapper for Any Display.
        
        :param dataframe: Pandas DataFrame
        :param consoleholder: Rich Console
        :param consoletable: Rich Console Table
        :param title: Title of the table
        :return: None | NoReturn:
        """
        # consoleholder.set_table(consoleholder, dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=consoleholder,
                              consoletable=consoletable,
                              headerview=Headers.HeadersChoices,
                              title=title)
    
    @staticmethod
    def display_frame(dataframe: pd.DataFrame,
                      consoleholder: Console,
                      consoletable: Table,
                      headerview: list[str] | str,
                      title: str = "PyCriteria") -> None | NoReturn:
        """Displays the data in a table.
        
        :param dataframe: Pandas DataFrame
        :param consoleholder: Rich Console
        :param consoletable: Rich Console Table
        :param headerview: List of headers
        :param title: Title of the table
        :return: None | NoReturn:
        """
        headers: list = headerview if \
            isinstance(headerview, list) else [headerview]
        consoletable.title = title
        
        filteredcolumns: pd.DataFrame = \
            dataframe.loc[:, dataframe.columns.isin(values=headers)]  # noqa
        # for column in headerview:
        for _index, row in filteredcolumns.iterrows():
            consoletable.add_row(*[str(row[column])
                                   for column in headers])
        consoleholder.print(consoletable)
    
    # The following is an AI Refactor from orginal authored code
    # https://www.perplexity.ai/search/c8250a15-6f8c-4180-b277-349f9ccf83c8?s=c
    @staticmethod
    def display_subframe(dataframe: pd.DataFrame,
                         consoleholder: Console | WebConsole,
                         consoletable: Table,
                         headerview: Headers | list[str] | str,
                         viewfilter: Headers.ViewFilter = "Criteria") \
        -> None | NoReturn:  # noqa # Pep8 E125
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
        for _index, row in filteredcolumns.iterrows():
            consoletable.add_row(*[str(row[column])
                                   for column in headers])
        consoleholder.print(consoletable)


class Results:
    """Results.

    Critical for all index and search results for rows.

    :meth: getrowframe: Get a row from a dataframe
     by an index or a search term.
    """
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def search(frame: pd.DataFrame,
               searchterm: str,
               exact: bool = False) -> pd.DataFrame | None:
        """Search across all columns for the searches team.

        :param frame: pd.DataFrame - Dataframe to search
        :param searchterm: str - Search term
        :param exact: bool - Exact match
        :return: pd.DataFrame - Search result
        """
        # Search by text
        if searchterm is None or isinstance(searchterm, str):
            return None
        # Search across all columns for the searches text/str value
        mask = frame.apply(lambda column: column.astype(str).
                           str.contains(searchterm))
        #
        return frame.loc[mask.all(axis=1)] if exact \
            else frame.loc[mask.any(axis=1)]
    
    @staticmethod
    def index(frame: pd.DataFrame,
              index: int,
              zero: bool = True) \
        -> pd.DataFrame | pd.Series | None:  # noqa # Pep8 E125
        """Get the row from the dataframe by index.

        :param frame: pd.DataFrame - Dataframe to search
        :param index: int - Index to search
        :param zero: bool - Zero based index
        :return: pd.DataFrame | pd.Series | None - Expect a result or None
        """
        if isinstance(index, int) and index is not None:
            return frame.iloc[index] if zero else frame.loc[index - 1]
        return None
    
    @staticmethod
    def rows(frame: pd.DataFrame,
             index: int = None,
             zero: bool = True,
             squeeze: bool = False) \
        -> pd.DataFrame | pd.Series | None:  # noqa # Pep8 E125
        """Get the rows from the dataframe.

        Parameters
        ----------
        frame: pd.DataFrame: Data to searches by rows
            The dataframe to searches.
        index: int: optional
            The index to searches for, by default None
        zero: bool: optional
            Whether to searches for a zero indexed dataset, by default True
        squeeze: bool: optional
            Whether to squeeze the dataframe result into a pd.Series,
            By default False

        return pd.DataFrame | None: - Expect a result or None
        """
        result: pd.DataFrame | pd.Series | None
        if index:
            result = Results.index(frame=frame, index=index, zero=zero)  # noqa
        else:
            click.echo("Please provide an index "
                       "identifier for a team")
            return None
        
        if squeeze and isinstance(result, pd.DataFrame) and len(result) == 1:
            result = result.squeeze()
        
        return result
    
    @staticmethod
    def getrowdata(data: pd.DataFrame,
                   ix: int,
                   single: bool = False,
                   debug: bool = False) \
        -> pd.Series | pd.DataFrame | None:  # noqa # Pep8 E125
        """Get a row from a dataframe by index or searches term.

        :param data: pd.DataFrame - Dataframe
        :param ix: int - Index
        :param single: bool - Single row
        :param debug: bool - Debug
        :return: pd.Series | pd.DataFrame | None - Row or rows
        """
        if ix:
            result = Results.rows(frame=data, index=ix,
                                  squeeze=single)
        else:
            click.echo(f"No Data for row: {ix}")
            return None
        
        # To check whether the result is a Series or DataFrame,
        # Use the type() function instead of isinstance(),
        # which author prefers.
        # https://www.perplexity.ai/search/a9842b96-f78d-4a83-a65f-de26448dc2f7?s=c
        if type(result) in [pd.Series, pd.DataFrame]:
            return result
        
        click.secho("GetRowData(): Found something: undefined")
        if debug is True:
            rich.inspect(result)
        return None


class Record:
    """A Record is a row of data to be displayed in console, by views.

    :property: view: The view of the record, default is table.
    :property: index: The index of the record, default is 0.
    :property: z: The z index of the record, default is 0.
    :property: length: The length of the record, default is 1.
    :property: headers: The headers of the record, default is None.
    :property: values pd.DataFrame:
                The values of the record, default is None - Default: []
    :property: series: The series of the record, default is None.
    :property: sourceframe: The sourceframe of the record, default is None.
    :property: size: The size of the record
    :property: recordid: The recordid of the record.
    :property: positionid: The positionid of the record.
    :property: recordid: The recordid of the record.
    :property: todo: The todo of the record.
    :property: grade: The grade of the record.
    :property: status: The status of the record.
    :property: topics: The topics of the record.
    :property: criteria: The criteria of the record.
    :property: type: The type of the record.
    :property: prefix: The prefix of the record.
    :property: linked: The linked of the record, default is None.
    :property: reference: The reference of the record.
    :property: group: The group of the record.
    :property: notes: The notes of the record, default is None.
    """
    
    view: str = "table"
    index: int = 0
    z: int = 0
    length: int = 1
    headers: list[str] | None = []
    values: list[str] | None = []
    series: pd.Series | None = None
    sourceframe: pd.DataFrame | None = None
    size: int = 0
    recordid = 0
    positionid: int = int(recordid) + 1
    recordid: str
    todo: str
    grade: str
    status: str
    topics: str
    criteria: str
    type: str
    prefix: str
    linked: str | None = ''
    reference: str
    group: str
    notes: str | None = ''
    lastcommand: str = ''
    editedmode: str = ''
    lastmodified: str | None = ''
    
    def __init__(self,
                 labels: list[str] | None = None,
                 display: str = "table",
                 series: pd.Series | None = None,
                 source: pd.DataFrame | None = None) -> None:
        """A Record is a row of data in a table.

        Usage:
        - A single row of data / record.
          Many record instances equals many rows of data, for display only
        - For printing individual records to the console, when < 5 per view.
        - For greater than 5 records, use a DataFrame and a full table view.
        - Display is the view, default is table, else: column, page, panel.
        - Labels, for views, as a filtered list of DataFrame's headers.

        Parameters:
        --------------------
        :param labels: list[str]: The row headers, i.e. columns, data.
        :param display: str: The view of the record, default is table.
        :param series: pd.Series | None: The series of data, if any.
        :param source: pd.DataFrame | None: The source of the data, if any.
        """
        self.view: str = display
        self.values: list[str]
        self.index: int
        self.length: int
        self.headers: list[str] | list[pd.Index] | None = labels
        self.series: pd.Series | None = series
        self.sourceframe: pd.DataFrame | None = source
        # Checks/loads Source, Dataframe, per instance
        if isinstance(series, pd.Series):
            self.loadsingle(single=series)
            self.loadrecord(single=series)
        elif isinstance(source, pd.DataFrame):
            self.loadsingle(single=source)
    
    @property
    def editmode(self) -> str:
        """The editedmode of the record.
        
        :return: str | None: The editedmode of the record.
        """
        return self.editedmode
    
    @editmode.setter
    def editmode(self, value: str) -> None:
        """The editedmode of the record.

        :param value: str: The editedmode of the record.
        :return: str | None: The editedmode of the record.
        """
        self.editedmode = value
    
    @property
    def modified(self) -> str | None:
        """The lastmodified of the record.
 
        :return: str | None: The lastmodified of the record.
        """
        return self.lastmodified
    
    @modified.setter
    def modified(self, value: str) -> None:
        """The lastmodified of the record.

        :param value: str: The lastmodified of the record.
        :return: str | None: The lastmodified of the record.
        """
        self.lastmodified = value
    
    @property
    def command(self) -> str:
        """The lastcommand of the record.

        :return: str | None: The lastcommand of the record.
        """
        return self.lastcommand
    
    @command.setter
    def command(self, value: str) -> None:
        """The lastcommand of the record.

        :param value: str: The lastcommand of the record.
        :return: str | None: The lastcommand of the record.
        """
        self.lastcommand = value
    
    @staticmethod
    def cmdnote(value: str) -> str | None:
        """The lastcommand of the record.

        :param value: str: The lastcommand of the record.
        :return: str | None: The lastcommand of the record.
        """
        commands = {
            'insert': 'This note is now added',
            'append': 'This note is now updated',
            'clear': 'This note is now deleted',
            'select': 'The progress status is now reported'
            }
        return commands.get(value, None)
    
    def modedisplay(self) -> str | None:
        """The Displaying Editing Command of the record."""
        commands = {
            'insert': 'Editing Tasks: Edit > Note: Adding',
            'append': 'Editing Tasks: Edit > Note: Updating',
            'clear': 'Editing Tasks: Edit > Note: Deleting',
            'add': 'Editing Mode: Edit > Note: Adding',
            'update': 'Editing Mode: Edit > Note: Updating',
            'delete': 'Editing Mode: Edit > Note: Deleting',
            'select': 'Editing Mode: Edit > Progress',
            'toggle': 'Editing Mode: Edit > Progress',
            'locate': 'Finding Mode: Locate > Record'
            }
        return commands.get(self.editmode, None)
    
    def loadsingle(self, single: pd.DataFrame | pd.Series) -> None:
        """Loads the source of the record, if any."""
        if isinstance(single, pd.DataFrame):
            if Record.checksingle(single):
                self.series = pd.Series(
                    data=single.values[Record.z],
                    index=single.columns)
                self.values = single.values[Record.z].tolist()
                self.headers = single.columns.tolist()
                self.sourceframe = single
                self.length = len(self.values)
                self.index = single.index[Record.z]
        elif isinstance(single, pd.Series) and Record.checksingle(single):
            self.series: pd.Series = single
            self.values = single.tolist()
            self.headers: list[pd.Index] = single.axes
            self.sourceframe: pd.DataFrame = \
                single.to_frame(name=single.name)  # noqa
            self.length = single.size
            self.index = single.index[Record.z]
            self.size = single.size
    
    def loadrecord(self, single: pd.Series) -> None:
        """Sets individial record properties."""
        if Record.checksingle(single):
            self.recordid: int = single.Position
            self.type: str = single.Tier
            self.prefix: str = single.TierPrefix
            self.grade: str = single.Performance
            self.status: str = single.DoD
            self.todo: str = single.Progress
            self.group: str = single.CriteriaGroup
            self.topics: str = single.CriteriaTopic
            self.reference: str = single.CriteriaRef
            self.criteria: str = single.Criteria
            self.linked: str = single.LinkedRef
            self.notes: str = single.Notes
    
    @staticmethod
    def checksingle(single: pd.DataFrame | pd.Series, debug: bool = False) -> bool:
        """Checks the source of the record, if any."""
        if isinstance(single, pd.DataFrame):
            if single.ndim == Record.length and single.empty is False:
                if debug is True:
                    rich.inspect(single)
                return True
            
            click.echo(message="The DataFrame must be a single row.",
                       err=True)
            return False
        
        if isinstance(single, pd.Series) and single.empty is False:
            if debug is True:
                rich.inspect(single)
            return True
        click.echo(message="The Series must be a single row.",
                   err=True)
        return False
    
    def card(self,
             consolecard: Console,
             source: pd.Series | None = None,
             sendtoterminal: bool = False) -> Table | None:
        """Either Displays the record as a terminal card, or forwards"""
        
        def config() -> Table:
            """Displays the record as a Inner card.
            
            :return: Table: The record as a card.
            """
            g: Table = Table.grid(expand=True)
            g.add_column(header="Property",
                         min_width=15,
                         ratio=1,
                         vertical='top')  # noqa
            g.add_column(header="Value",
                         min_width=50,
                         justify="right",
                         ratio=2,
                         vertical='top')  # noqa
            return g
        
        def display(table: Table, data: pd.Series | None = None) \
            -> Table | None:  # noqa # Pep8 E125
            """Populates the card from instance or a from external source."""
            series = data if isinstance(data, pd.Series) \
                else self.series
            if series is not None:
                for label, value in series.items():
                    table.add_row(str(label), str(value))
                return table
            return None
        
        card: Table = display(table=config(), data=source)
        
        return Record.switch(card,
                             printer=consolecard,
                             switch=sendtoterminal)
    
    @staticmethod
    def panel(consolepane: Console,
              renderable,
              fits: bool = False,
              card: tuple[int, int] = (0, 0),
              align: typing.Literal["left", "center", "right"] = "left",
              outline: rich.box = box.SIMPLE, sendtolayout: bool = False,
              debug: bool = False) \
        -> Panel | None:  # noqa ANN001
        """Frames the renderable as a panel."""
        
        def config(dimensions: tuple[int, int],
                   styler: str,
                   safe: bool = False) -> Panel:
            """Frames the renderable as a panel."""
            width, height = dimensions
            if width == 0 and height == 0:
                p: Panel = Panel(renderable=renderable,
                                 expand=fits,
                                 box=outline,
                                 style=styler,
                                 safe_box=safe,
                                 border_style=styld.border(),
                                 title_align=align,
                                 highlight=True)
                return p
            
            p: Panel = Panel(renderable=renderable,
                             expand=fits,
                             width=width,
                             height=height,
                             style=styler,
                             box=outline,
                             safe_box=safe,
                             border_style=styld.border(),
                             title_align=align,
                             highlight=True)
            return p
        
        panel: Panel = config(dimensions=card,
                              styler=styld.panel(grey=23),
                              safe=True)
        
        if debug is True:
            rich.inspect(panel)
        
        # Switches the flow: returns | print| to stdout
        return Record.switch(panel,
                             printer=consolepane,
                             switch=sendtolayout)
    
    def display(self, consoledisplay: Console,
                sizing: tuple[int, int] = None,
                record=None, sendtolayout: bool = False) \
        -> Panel | None:  # noqa ANN001
        """Displays the record as a table, card."""
        # Checks the external record, self record
        if record is not None:
            card: Table | None = record.card(consolecard=consoledisplay)
        else:
            card: Table | None = self.card(consolecard=consoledisplay)
        # Exluced Printed card deets
        if card is None:
            click.echo(message="__")
            return None
        # Get a panel
        panel: Panel | None = \
            self.panel(consolepane=consoledisplay,
                       renderable=card,
                       card=sizing)  # noqa
        # Switches the flow: returns | print| to stdout
        return Record.switch(panel,
                             printer=consoledisplay,
                             switch=sendtolayout)
    
    def boxed(self, table, style: int = 1) -> Table:  # noqa
        """Sets the table box style.
        
        :param table: The table to be boxed.
        :param style: The style of the box.
        :return: The boxed table.
        """
        styles = {
            1: box.SIMPLE,
            2: box.ROUNDED,
            3: box.HEAVY_HEAD,
            4: box.SIMPLE_HEAD,
            5: box.HORIZONTALS,
            6: box.SQUARE
            }
        
        table.box = styles.get(style, box.SIMPLE)
        
        return table
    
    def header(self,
               consolehead: Console,
               sendtolayout: bool = False,
               gridfit: bool = False,
               valign: str = "top",
               debug: bool = False) -> Table | None:
        """Displays the header of the record."""
        
        def config(fit: bool, vertical: str) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            g.show_header = True
            g.add_column(header="Record",
                         min_width=35,
                         ratio=2,
                         vertical=vertical)  # noqa
            g.add_column(header="-",
                         min_width=15,
                         ratio=1,
                         vertical=vertical)  # noqa
            g.add_column(header="Grading",
                         min_width=35,
                         ratio=2,
                         vertical=vertical)  # noqa
            return g
        
        def head(table: Table) -> Table:
            """Display the subtable for Index/Identifiers."""
            h: Table = table
            h.title = 'Assignment Details'
            
            rowid: str = 'Record Name:  ' + f'{self.series.name}'
            grade: str = 'Grade:  ' + f'{self.grade}'
            position: str = 'Position ID:  ' + f'{self.recordid}'
            outcome: str = 'Outcome:  ' + f'{self.status}: {self.todo}'
            
            h.add_row(rowid, "", grade)
            h.add_section()
            h.add_row(position, "", outcome)
            return h
        
        header: Table = head(table=config(fit=gridfit, vertical=valign))
        
        if debug is True:
            rich.inspect(header)
        
        return Record.switch(header,
                             printer=consolehead,
                             switch=sendtolayout)
    
    def editable(self,
                 consoleedit: Console | None = None,
                 expand: bool = False,
                 sendtolayout: bool = False,
                 title: str = 'Current Data',
                 debug: bool = False) -> Table | None:  # noqa
        """Displays the record: Use it for Current | Modified Records."""
        webconsole: Console = consoleedit  # noqa
        
        def config(fit: bool) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            g.pad_edge = True
            g.add_column(header="Current",
                         min_width=50,
                         ratio=1,
                         vertical='top')  # noqa
            return g
        
        def currentdata(table: Table, t: str) -> Table:
            """Display the subtable for Index/Identifiers."""
            currenttable: Table = table
            if currenttable.title is None and t is not None:
                currenttable.title = t
            todo_label: str = 'To Do:'
            todo_value = f'{self.todo} \n'
            criteria_label: str = 'Criteira: ' + f'{self.topics}'
            criteria_value = f'{self.criteria} \n\n'
            currenttable.add_section()
            notes_label: str = 'Notes: '
            notes_value = 'Add a note' \
                if self.notes is None else f'{self.notes} \n'
            # Build rows
            currenttable.add_row(todo_label,
                                 style=styld.label())
            currenttable.add_row(todo_value,
                                 style=styld.value())
            currenttable.add_row(criteria_label,
                                 style=styld.label())
            currenttable.add_row(criteria_value,
                                 style=styld.value())  # noqa
            currenttable.add_row(notes_label,
                                 style=styld.label())
            currenttable.add_row(notes_value,
                                 style=styld.value())
            return currenttable
        
        currentdatapane: Table = \
            currentdata(table=config(fit=expand), t=title)  # noqa
        
        if debug is True:
            rich.inspect(currentdatapane)
        
        return Record.switch(currentdatapane,
                             printer=consoleedit,
                             switch=sendtolayout)
    
    def footer(self,
               consolefoot: Console,
               sendtolayout: bool = False,
               expand: bool = True,
               valign: str = 'top',
               debug: bool = False) -> Table | None:
        """Displays footer as a card/record."""
        
        # Config Table/Grid for Footer
        def config(fit: bool, vertical: str) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            
            g.add_column(header="More",
                         min_width=33,
                         ratio=1,
                         vertical=vertical)  # noqa
            g.add_column(header="Linked",
                         min_width=33,
                         ratio=1,
                         vertical=vertical)  # noqa
            g.add_column(header="Categories",
                         min_width=33,
                         ratio=1,
                         vertical=vertical)  # noqa
            return g
        
        def metapane(table: Table) -> Table:
            """Display the subtable for Index/Identifiers."""
            meta: Table = table
            meta.title = 'Project Data'
            meta.add_section()
            tier_label: str = 'Tier: '
            progress_label: str = 'Progress: '
            topics_label: str = 'Topics: '
            tier_value = f'{self.type}.{self.prefix}.{self.reference}'
            meta.add_row(f'{tier_label}  {tier_value})',
                         f'{progress_label}:  {self.linked}',
                         f'{topics_label}:  {self.topics}')
            meta.add_section()
            now: datetime = datetime.datetime.now()
            dt_string: str = now.strftime("%d/%m/%Y %H:%M")  # %S
            meta.add_row(f'Viewed: {dt_string}',
                         f'{topics_label}:  {self.topics}', ' ')
            return meta
        
        footer: Table = metapane(table=config(fit=expand, vertical=valign))
        
        if debug is True:
            rich.inspect(footer)
        
        return Record.switch(footer,
                             printer=consolefoot,
                             switch=sendtolayout)
    
    @staticmethod
    def setcolumn(table: Table,
                  heading: str = '',
                  hstyle: str = None,
                  footing: str = '',
                  fstyle: str = None,
                  styler: str | Style = None,
                  minw: int = 35,
                  maxw: int = 50,
                  width: int = 50,
                  wraps: bool = False,
                  proportion: int = 1) -> Table:  # noqa ANN001
        """Configured the Rich Column for the webconsole, side x side."""
        table.add_column(header=heading,
                         footer=footing,
                         header_style=hstyle,
                         footer_style=fstyle,
                         style=styler,
                         min_width=minw,
                         max_width=maxw,
                         width=width,
                         overflow='fold',
                         ratio=proportion,
                         justify='default',
                         vertical='top',  # noqa
                         no_wrap=wraps)
        return table
    
    def footnote(self) -> str:
        """Renders the footnote for the record."""
        return f'{self.cmdnote(self.editmode)} at: {self.modified}'
    
    def comparegrid(self,
                    container: Table,
                    left: Table,
                    right: Table,
                    fit: bool = False,
                    sendtolayout: bool = False,
                    debug: bool = False) -> Table | None:
        """Display the header grid table."""
        main: Table = container
        main.grid(expand=fit)
        main.width = 100
        main.title = f'{self.command}: {self.type}.' \
                     f'{self.prefix}.{self.reference}'
        main.show_footer = True
        main = Record.setcolumn(table=main,
                                heading="Existing",
                                footing='-----------------')
        main = Record.setcolumn(table=main,
                                heading="Modified",
                                footing=f'{self.footnote()}')
        main.add_row(left, right)
        
        if debug is True:
            rich.inspect(main)
        
        return Record.switch(main,
                             printer=container,
                             switch=sendtolayout)
    
    @staticmethod
    def switch(renderable,
               printer: Console | Table,
               switch: bool = False) -> Table | None:  # noqa ANN001
        """Switches between console print or redirecting to a layout."""
        # ""App.values.Display.TOLAYOUT = True"", (author notes, not unused code).
        # Then send renderable to next Rich Renderable handler.
        # Does not print to console.
        if switch is True:
            return renderable
        
        # If ""App.values.Display.TOTERMINAL = False"",
        # (author notes, not unused code).
        # Then print to terminal console
        if isinstance(printer, Console):
            printer.print(renderable)
        elif isinstance(printer, Table):
            c = Console()
            c.print(renderable)
        # Output to StdOut
        return None


class Editor:
    """The Editor is a CRUD Controller for editing records.
    
    :property record: The record to edit.
    :property oldresultseries: The original record as a Pandas Series.
    :property newresultseries: The modified record as a Pandas Series.
    :property oldresultframe: The original record as a Pandas DataFrame.
    :property newresultframe: The modified record as a Pandas DataFrame.
    :property sourceframe: The source DataFrame for the record.
    :property ismodified: True if the record has been modified.
    :property lastmodified: The last modified date/time.
    :property modified: The modified record as a Record object.
    :property lasteditmode: The last edit mode.
    :property ADDMODE: The add mode.
    :property UPDATEMODE: The update mode.
    :property DELETEMODE: The delete mode.
    :property SELECTMODE: The select mode.
    :property INSERTEDIT: The insert edit.
    :property APPENDEDIT: The append edit.
    :property REPLACEEDIT: The replace edit.
    :property CLEAREDIT: The clear edit.
    :property SELECTEDIT: The select edit.
    :property lastcommand: The last command.
    :property editmode: The current edit mode.
    :property command: The current command.
    """
    
    record: Record = None
    oldresultseries: pd.Series | None = None
    newsresultseries: pd.Series | None = None
    oldresultframe: pd.DataFrame | None = None
    newresultframe: pd.DataFrame | None = None
    sourceframe: pd.DataFrame | None = None
    ismodified: bool = False
    lastmodified: str | None = None
    modified: Record | None = None
    lasteditmode: str
    ADDMODE: str = 'add'
    UPDATEMODE: str = 'update'
    DELETEMODE: str = 'delete'
    SELECTMODE: str = 'select'
    INSERTEDIT: str = 'insert'
    APPENDEDIT: str = 'append'
    REPLACEEDIT: str = 'replace'
    CLEAREDIT: str = 'clear'
    SELECTEDIT: str = 'select'
    lastcommand: str | None = None
    
    def __init__(self,
                 currentrecord: Record = None,
                 sourceframe: pd.DataFrame | None = None,
                 debug: bool = False) -> None:
        """The Editor is CRUD Controller for editing records.
        
        :param currentrecord: The record to edit.
        :param sourceframe: The source frame to edit.
        :param debug: Debug mode.
        :return: None
        """
        if currentrecord is not None:
            self.record = currentrecord
            if debug is True:
                rich.inspect(currentrecord)
        else:
            click.echo(message="No editing possible", err=True)
        
        if debug is True:
            rich.inspect(sourceframe)
        self.sourceframe = sourceframe
        
        # Assign Properties
        self.oldresultseries = self.record.series
        self.oldresultframe = self.record.sourceframe
        self.newresultseries = None
        self.newresultframe = None
        self.ismodified = False
        self.lastmodified = None
        self.modified = None
        self.lasteditmode: str = ''
    
    @property
    def command(self) -> str:
        """Return the last command."""
        return self.lastcommand
    
    @command.setter
    def command(self, value: str) -> None:
        """Set the last command."""
        self.lastcommand = value
    
    def editnote(self,
                 edits: str,
                 index: int,
                 notepad: str,
                 debug: bool = False) -> None:
        """Hub switch between editing modes, and actions for Notes.

        :param edits: The edit mode.
        :param index: The index of the note.
        :param notepad: The notes.
        :param debug: Debug flag.
        :return: None
        """
        # Example of improved efficiency, over the orginal if statements
        notemethods: dict = {
            self.ADDMODE: self.addingnotes,
            self.UPDATEMODE: self.updatingnotes,
            self.DELETEMODE: self.deletingnotes
            }
        
        method = notemethods.get(edits, None)
        if method is not None:
            method(notes=notepad, location=index, debug=debug)
            self.editmode = edits
        else:
            click.echo(message="Exiting Editing Mode. Bad Edit Mode.")
    
    @property
    def editmode(self) -> str:
        """Return the last edit mode."""
        return self.lasteditmode
    
    @editmode.setter
    def editmode(self, value: str) -> None:
        """Set the last edit mode."""
        self.lasteditmode = value
    
    def editprogress(self,
                     edits: str,
                     index: int,
                     choicepad: str,
                     debug: bool = False) -> None:
        """Hub switch between editing modes, and actions for ToDos.

        And similar status/values choice fields/column

        :param edits: The edit mode.
        :param index: The index of the note.
        :param choicepad: The notes.
        :param debug: Debug flag.
        :return: None
        """
        # Example of improved efficiency, over the orginal if statements
        selectmethods: dict = {self.SELECTMODE: self.togglestatus}
        toggle = selectmethods.get(edits, None)
        if toggle is not None:
            self.togglestatus(status=choicepad, location=index, debug=debug)
            self.editmode = self.SELECTMODE
        else:
            click.echo(message="Exiting Editing Mode. Bad Edit Mode.")
    
    # =======================NOTES===============================
    # Methods
    # 1) Actions:
    #   a) AddingNotes()
    #   b) UpdatingNotes()
    #   c) DeletingNotes()
    # 2) Hub: Common to all actions:
    #   a) modifynotes()
    # 3) Tasks: Given these are descrtuctive tasks:
    #   a) appendnotes(): Linked within UpdatingNotes()
    #   b) deletenotes(): Linked within DeletingNotes()
    def addingnotes(self, notes: str,
                    location: int | None = None,
                    debug: bool = False) -> None:
        """Adding Notes to the Record/Series for the add note command.
        
        The Editor is a CUD controller for modifing record values.
        The column is well known: ColumnSchema.Notes
        The index is inputted by the user.
        The value is the note's text inputted by the user.

        Similar: updatingnotes(), deletingnotes()

        Parameters
        ----------
        :param notes: The notes to be added to the record.
        :param location: The location of the notes to be added to the record.
        :param debug: The debug flag for the function.
        :return: None
        """
        # Guard conditions, 2nd layer of santisation,
        if notes is not None and isinstance(notes, str):
            # PROMPT USE, as an exmaple, for user by PerplexityAI
            # copy old result series to a new result series with added notes
            # copy old result frame into a new result frame with added notes
            # find the location in the source frame of the new series
            # update the same index by either editing the note by column/id
            # so a series column must match the source frame column
            # and a series index must match the source frame index
            # and the location row, column of the sourceframe be updated
            # with the new note
            # and then a copy of the sourceframe be either
            # a) returned
            # b) using click.prompt() to ask if the user wants to save the
            #    sourceframe and
            #    using click.confirm() to ask if the
            #    user wants commit to the remote
            #    commit function is to be defined,
            #    as it is destructive/overwrites
            # THEN:
            # Then I take the AI generated code and
            #    refactor it into several functions for reuse and development.
            # 1: Add guard clauses: _isempty() and _hascontent()
            # 2: Add a hub function to modify the notes with a 'editmode' flag
            # 3: Use multiple confirm prompts to confirm the user's intent
            # 4: By branching on the user's intent:
            #    - add notes becomes insert note if the target was empty.
            #    - add notes becomes append note if the target was not empty.
            #    - so does not force the user to retype the same note
            #      on a new command in CLI app => UserFlow
            # THIS IS HOW I use the AI start an idea, but I drive the solution.
            # As the design pattern is formed, then it is adapted for similar.
            # -----------------------------------------------------------------
            # Update the record's series with the new notes
            # Copy current records into local series
            editingseries = self.record.series.copy()
            self.editmode = ''  # Clears out the last edit mode, before use
            # Check if the target location data (series) is empty for Notes
            if self._isempty(editingseries, ColumnSchema.Notes):
                # Perplexity AI was used to build out this function,
                # https://www.perplexity.ai/search/a8d503cb-8aec-489a-8cf5-7f3e5b573cb7?s=c
                # Set the edit mode explicitly to insert
                self.editmode = self.INSERTEDIT
                # User confirmation to add the note, step by step
                if click.confirm("Please confirm to "
                                 f"add/{self.editmode} your note"):
                    # Send to hub modifier function for all Notes editing
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes,
                                     editmode=self.INSERTEDIT,
                                     location=location)
                # Allow user to modify their note, if change of mind
                elif click.confirm(
                    text="Do you want to modify your new note? \n"
                         + f"Your latest note is {notes}. \n"):
                    newnotes = click.prompt("Please enter changes: ")
                    # Guard for input and then send to hub modifier function
                    if isinstance(newnotes, str):
                        self.modifynotes(editingseries,
                                         record=self.record,
                                         notes=str(newnotes),
                                         editmode=self.INSERTEDIT,
                                         location=location,
                                         debug=debug)
                    # Graceful user exit for wrong type of input.
                    else:
                        click.echo(message="Please enter a string",
                                   err=True)
                # If user does not want to add/amend the note, then exit
                else:
                    click.echo("Exiting editing mode")
                    return
            # Check if the target location data (series) is not empty for Notes
            elif click.confirm(
                text="You are adding a note to an exitsing note. \n"
                     + "Do you want to continue?"):
                # Set the edit mode explicitly to append and append.
                # Not much different from insert, but the user is aware.
                self.modifynotes(editingseries,
                                 record=self.record,
                                 notes=notes,
                                 editmode=self.APPENDEDIT,
                                 location=location,
                                 debug=debug)
                click.echo("Note appended, not created")
            else:
                # User does not want to add a note to an existing note
                click.echo("Exit editing mode")
                return
    
    def updatingnotes(self, notes: str,
                      location: int | None = None,
                      debug: bool = False) -> None:
        """Updating Notes to the Record/Series for the update note command.
        
        The Editor is a CUD controller for modifing record values.
        The column is well known: ColumnSchema.Notes
        The index is inputted by the user.
        The value is the note's text inputted by the user.
        
        Similar: updatingnotes(), deletingnotes()
        
        Parameters
        ----------
        :param notes: The notes to be added to the record.
        :param location: The location of the notes to be added to the record.
        :param debug: The debug flag for the function.
        :return: None
        """
        # See addingnotes() for the PerplexityAI use case as co-Pilot.
        # Guard conditions, 2nd layer of santisation,
        if notes is not None and isinstance(notes, str):
            # Copy the current record's series into a local series
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode
            # , before use.
            # Check if the target location data (series) ha content for Notes
            if self._hascontent(editingseries, ColumnSchema.Notes):
                # Set the edit mode explicitly to append.
                self.editmode = self.APPENDEDIT  # noqa
                # User confirmation to append the note, step by step
                if click.confirm("Please confirm to"
                                 f" {self.editmode} your note"):
                    # Send to hub modifier function for all Notes editing
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes.strip(),
                                     editmode=self.APPENDEDIT,
                                     location=location,
                                     debug=debug)
                # Allow user to modify their note, if change of mind
                elif click.confirm(
                    text="Do you want to modify your current note? \n"
                         + f"Your latest note is {notes}. \n"):
                    newnotes = click.prompt("Please enter changes: ")
                    # Guard for input and then send to hub modifier function
                    if isinstance(newnotes, str):
                        self.modifynotes(editingseries,
                                         record=self.record,
                                         notes=str(newnotes.strip()),
                                         editmode=self.APPENDEDIT,
                                         location=location,
                                         debug=debug)
                    # Graceful user exit for wrong type of input.
                    else:
                        click.echo(message="No Edit Made for  "
                                           f"Update {self.editmode}",
                                   err=True)
                # If user does not want to add/amend the note, then exit
                else:
                    click.echo("Exiting editing mode:"
                               f" Update {self.editmode}")
                    return
    
    def deletingnotes(self,
                      notes: str,
                      location: int | None = None,
                      debug: bool = False) -> None:
        """Deleting Notes to the Record/Series for the delete note command.
        
        The Editor is a CUD controller for modifing record values.
        The column is well known: ColumnSchema.Notes
        The index is inputted by the user.
        The value is the note's text inputted by the user.

        Similar: updatingnotes(), addingnotes()

        Parameters
        ----------
        :param notes: The notes to be added to the record.
        :param location: The location of the notes to be added to the record.
        :param debug: The debug flag for the function.
        :return: None
        """
        # See addingnotes() for the PerplexityAI use case as co-Pilot.
        # Guard conditions, 2nd layer of santisation,
        if notes is not None and isinstance(notes, str):
            # Backup User's input into current record
            # Create a transitory single data series from record
            editingseries = self.record.series.copy()
            self.editmode = ''  # Clears out the last edit mode, before use
            # Check if the series has notes
            if self._hascontent(editingseries, ColumnSchema.Notes):
                # Set the edit mode explicitly to clear.
                self.editmode = self.CLEAREDIT  # noqa
                # Confirm if the user wants to proceed.
                # It is a CLI and not a GUI, and thus keywboard driven.
                # The user clear all the notes and
                # then decide to delete or not.
                if click.confirm("Please confirm to clear your note?"):
                    # Call the hub (CUD) function with editmode='clear' flag.
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes,
                                     editmode=self.CLEAREDIT,
                                     location=location,
                                     debug=debug)
                # If user does not want to clear all the notes, then exit
                else:
                    click.echo(f"Exiting editing mode: "
                               f"Delete: {self.editmode}")
                    return
    
    # Check if the editing series needs to be type annotated or left magic
    def modifynotes(self,
                    editingseries: pd.Series,
                    record: Record,
                    notes: str,
                    editmode: str = Literal["insert", "append", "clear"],
                    location: int | None = None, debug=False) -> None:  # noqa
        """Hub Function for editing notes: Note to the designed pattern.

        Changes the notes, refeshes of the datasets, and commits.

        Notes to the Record/Series for the add note command

        The Editor is a CUD controller for modifing record values.
        The column is well known: ColumnSchema.Notes
        The index is inputted by the user.
        The value is the note's text inputted by the user.

        Similar: updatingnotes(), deletingnotes()

        Parameters
        ----------
        :param editingseries: pandas.Series: The series to be edited.
        :param record: Record: The record to be edited.
        :param notes: The notes to be added to the record.
        :param editmode: Literal["insert", "append", "clear"]: Possible values.
                The mode of editing the notes.
        :param location: int: | None:
                The location of the notes to be added to the record.
        :return: None
        """
        # EditMode is Insert: then add / overwrite / create at the location
        if isinstance(editmode, str) and isinstance(editingseries, pd.Series):
            if editmode == self.INSERTEDIT:
                self.lasteditmode = self.INSERTEDIT
                # Insert the notes - add / overwrite / create
                editingseries[ColumnSchema.Notes] = notes
                click.echo("Note inserted")
            # EditMode is Append: then append the notes the Notes column
            elif editmode == self.APPENDEDIT:
                self.lasteditmode = self.APPENDEDIT
                # Append the notes - by target location (Notes)
                editingseries[ColumnSchema.Notes] = \
                    self.appendnotes(series=editingseries,
                                     column=ColumnSchema.Notes,
                                     value=notes)
                click.echo("Note inserted")
            # EditMode is Clear: then clear the notes the Notes column
            elif editmode == self.CLEAREDIT:
                self.lasteditmode = self.CLEAREDIT
                editingseries[ColumnSchema.Notes] = \
                    self.deletenotes(series=editingseries,
                                     column=ColumnSchema.Notes)
                click.echo("Note cleared")
            
            # Current and Modified datasets diverge here
            # Create a new updated series & dataframe with the new data
            updatedframe = self.insert(
                record=record,
                value=editingseries[ColumnSchema.Notes],
                column=ColumnSchema.Notes,
                index=location,
                debug=debug)
            self.newresultseries = editingseries
            self.newresultframe = updatedframe
            # Debug flows
            if debug is True:
                if isinstance(self.newresultseries, pd.Series) and \
                    self.newresultseries.empty is False:  # noqa # Pep8 E125
                    click.echo("Modified Series")
                
                if isinstance(self.newresultframe, pd.DataFrame) and \
                    self.newresultframe.empty is False:  # noqa # Pep8 E125
                    click.echo("Modified DataFrame")
            # Check if the new result is NOT empty and set Update flags
            if self.newresultframe.empty is False:
                self.ismodified = True
                self.lastmodified = self.timestamp()
                click.echo("Modified at " + self.lastmodified)
                self.modified = Record(
                    series=editingseries,
                    source=self.newresultframe)
                # Debug flows
                if debug is True:
                    rich.inspect(self.modified)
                # sets the last edit mode for the record
                self.lasteditmode = editmode
            # To be implemented
            if click.confirm("Do you want to save "
                             "the updated DataFrame?"):
                self.save(self.newresultframe,
                          series=self.newresultseries,
                          index=location,
                          action='s3',
                          debug=False)  # noqa
            else:
                click.echo("Exit editing mode")
                return
        
        click.echo(message="Exit editing mode: Modifing Notes "
                           + self.lasteditmode)
    
    # Modifying Tasks
    def appendnotes(self, series: pd.Series, column: str, value: str) -> str:
        """Appends notes to the existing notes; builds with a timestamp..

        Parameters
        ----------
        :param series: pandas.Series: The series to be edited.
        :param value: str: The notes to be added to the record.
        :param column: str: The name of the column to be edited.
        :return: str
        """
        currentnotes = f"{series[column]}\n\n"
        label = f"New Note: {self.timestamp()}\n"
        newnote = f"{label}{value}\n"
        return f"{currentnotes}{newnote}"
    
    @staticmethod
    def deletenotes(series: pd.Series,
                    column: str,
                    nodestroy: bool = False) -> str:
        """Deletes complete/all notes from the existing record/row
        
        if flag: nodestroy/destroy.

        Parameters
        ----------
        :param series: pandas.Series: The series to be edited.
        :param column: str: The name of the column to be edited.
        :param nodestroy: bool: The flag to delete or not to delete.
               A mechanism to handle destructive actions and safely delete.
               Potentially flagged by user from a CLI command option.
        :return: str
        """
        
        def _removelabel(clear: str) -> str:
            """Removes the label from the notes."""
            if series[column] == 'Add a note'.strip():
                series[column] = clear
            return series[column]
        
        def _haslabel() -> bool:
            """Checks if the notes have a label."""
            return bool(series[column].startswith("Add a note"))
        
        def _emptydelete(clear: str = '') -> bool:
            """Checks if the notes are empty."""
            if nodestroy is False and not _haslabel():
                # Returning True if the notes are empty
                return series[column] == clear
            
            if nodestroy is True and _haslabel():
                # Returning True if the notes cleared and now are empty
                series[column] = _removelabel(clear)
                return series[column] == clear
            
            if nodestroy is True:
                return series[column] == clear
            
            return False
        
        # Check if the notes are empty
        if _emptydelete(series[column]):
            click.echo(message="No notes to delete")
            return series[column]
        # Check if the notes are not empty and nodestroy is False
        if nodestroy is False:
            click.echo(message="Existing notes present. No change")
            return series[column]
        
        # Return the cleared notes
        click.echo(message="Cleared")
        return ''
    
    # =======================TODO===============================
    # Methods
    # 1) Actions:
    #   a) ToggleStatus()
    # 2) Hub: Common to all actions:
    #   a) modifyprogress()
    # 3) Tasks: Given these are descrtuctive tasks:
    #   a) appendnotes(): Linked within UpdatingNotes()
    #   b) deletenotes(): Linked within DeletingNotes()
    def togglestatus(self,
                     status: str = Literal['todo', 'wip', 'done', 'missed'],
                     location: int | None = None,
                     debug: bool = False) -> None:
        """Toggle the status of the record."""
        shown: bool = True
        notso: bool = False
        validstatus: list[str] = ['ToDo', 'WIP', 'Done', 'Missed']
        
        def reprompt() -> str | None:
            """Re-prompt the user to enter a valid status."""
            tryagain = click.prompt(text="Enter a valid status:",
                                    default="todo",
                                    type=click.Choice(choices=validstatus),
                                    prompt_suffix=" Again: ",
                                    show_choices=shown,
                                    show_default=shown,
                                    err=notso)
            
            return tryagain.lower() if isinstance(tryagain, str) \
                else click.secho(
                message="Exiting Editing Mode. "
                        "Invalid input",
                fg="bright_yellow", bold=True)
        
        # Inner function to check the status against the allowed values
        def _checkstatus(state: str, debg: bool = False) -> str | None:
            valid = {'todo', 'wip', 'done', 'missed'}
            if state.lower() in valid:
                if debg is True:
                    click.secho(message=f"Valid status: {state.lower()}",
                                fg="bright_green", bold=True)
                return state.lower()
            
            click.echo("Invalid status. Try again.")
            return None
        
        # Check if the status is valid
        if _checkstatus(state=status, debg=debug) is not None:
            editingseries = self.record.series.copy()
            self.editmode = ''  # Clears out the last edit mode, before use
            # Check if the datasource values are valid, allowed.
            if self._hasstatus(editingseries, ColumnSchema.Progress):
                self.editmode = self.SELECTEDIT
                if click.confirm(text="Please confirm to"
                                      f" {self.editmode} "
                                      "your ToDo progress status"):
                    self.modifyprogress(editingseries,
                                        record=self.record,
                                        status=_checkstatus(status),
                                        editmode=self.editmode,
                                        location=location,
                                        debug=debug)
                elif click.confirm(
                    text="Do you want to modify progress status? \n"):  # noqa # Pep8 E125
                    newprogress = reprompt()
                    if isinstance(newprogress, str) \
                        and newprogress is not None:  # noqa # Pep8 E125
                        self.modifyprogress(
                            editingseries,
                            record=self.record,
                            status=_checkstatus(newprogress),
                            editmode=self.editmode,
                            location=location,
                            debug=debug)
                    else:
                        click.echo(message="No Edit Made for"
                                           f"  {self.editmode}"
                                           " of progress status",
                                   err=True)
                else:
                    click.echo("Exiting editing mode:"
                               f" Status: {self.editmode} for Progress")
                    return
        else:
            return
    
    @staticmethod
    def updatingdod(progress: str, series: pd.Series) -> pd.Series | None:
        """Update the DoD based on the progress.

        The Progress status field controlls the progression of
        the Defintion of Done Fields via a matrix of truthy states

        :param progress: str: The progress status to be updated.
               Relies on outer scope access.
               for the editingseries variable.
        :param series: pd.Series: The series to be updated.
        :return: None
        """
        # Use of PerplexityAI to reformulate updatedod for efficiency
        # Also based on ruff checks . => controller.py:2057:22:
        # SIM114 Combine `if` branches using logical `or` operator
        # https://www.perplexity.ai/search/8cdbda60-51fe-46cb-b205-f39386c9fff0?s=c
        # Using dicts over multiple if statements for efficiency
        
        click.echo("Current Item' Project Status :"
                   f" {series[ColumnSchema.Progress]}")
        # Statically State machine for updating the DoD reporting:
        reporting = {
            'todo': 'Planned',
            'wip': 'In Progress',
            'done': 'Completed',
            'missed': 'Unfinished'
            }
        
        new_dod = reporting.get(progress.lower(), None)
        if new_dod is None:
            click.secho(message="Progress and Project reporting not updated")
            return None
        
        if series[ColumnSchema.DoD] == 'Unfinished' \
            and new_dod == 'Unfinished':  # noqa # Pep8 E125
            return series
        
        series[ColumnSchema.DoD] = new_dod
        click.secho(message="Progress & Definition of Done reporting updated")
        return series
    
    # Refactor: controller.py:1976:9: PLR0915 Too many statements (51 > 50)
    # Check if the editing series needs to be type annotated or left magic
    def modifyprogress(self,
                       editingseries: pd.Series,
                       record: Record,
                       status: str,
                       editmode: str = Literal["select"],
                       location: int | None = None,
                       debug: bool = False) \
        -> None:  # noqa
        """Hub Function for editing progress status.

        Changes the progress, refeshes of the datasets, and commits.

        NB to the Record/Series for the progress field

        The Editor is a CUD controller for modifing record values.
        The column is well known: ColumnSchema.Progress
        The index is inputted by the user.
        The value is the progress's choice selection as selected by the user.


        Parameters
        ----------
        :param editingseries: pandas.Series: The series to be edited.
        :param record: Record: The record to be edited.
        :param status: The status to be added to the record.
        :param editmode: Literal["select"]: Possible values.
                The mode of editing the notes.
        :param location: int: | None:
                The location of the notes to be added to the record.
        :param debug: bool: The flag to debug.

        Inner Methods
        :method: _updatedod: Update the DoD based on the progress
                 The Progress status field controlls the progression of
                 the Defintion of Done Fields via a matrix of truthy states
                 per phase of a project.
        :method: _frameupdate: Update the record dataframe
                 with multipe columns.
                 As per _updatedod, the DoD column is updated,
                 as the Progress is updated.
        

        Returns:
        ----------
        :return: None
        """
        self.editmode = str(editmode).lower()
        
        def _updatedod(progress):
            """Update the DoD based on the progress.
            
            The Progress status field controlls the progression of
            the Defintion of Done Fields via a matrix of truthy states

            :param progress: str: The progress status to be updated.
                   Relies on outer scope access.
                   for the editingseries variable.
            :return: None
            """
            # Use of PerplexityAI to reformulate updatedod for efficiency
            # Also based on ruff checks . => controller.py:2057:22:
            # SIM114 Combine `if` branches using logical `or` operator
            # https://www.perplexity.ai/search/8cdbda60-51fe-46cb-b205-f39386c9fff0?s=c
            # Using dicts over multiple if statements for efficiency
            click.echo("Current Item' Project Status :"
                       f" {editingseries[ColumnSchema.Progress]}")
            # Statically State machine for updating the DoD reporting:
            reporting = {
                'todo': 'Planned',
                'wip': 'In Progress',
                'done': 'Completed',
                'missed': 'Unfinished'
                }
            
            click.echo("Current Item' Project Status :"
                       f" {editingseries[ColumnSchema.Progress]}")
            dod = editingseries[ColumnSchema.DoD]
            newdod: str | None = reporting.get(progress.lower(), None)
            if newdod is None:
                click.secho(message="Progress and Project "
                                    "reporting not updated")
                return
            if dod == 'Planned' and newdod == 'Unfinished':
                pass
            elif dod == 'In Progress' and newdod == 'Unfinished':
                editingseries[ColumnSchema.DoD] = 'Unfinished'
            elif dod == 'Unfinished' and newdod == 'Unfinished':
                pass
            else:
                editingseries[ColumnSchema.DoD] = newdod
            click.echo("Progress updated")
        
        def _frameupdate() -> pd.DataFrame:
            """Update the frame with the new data.

            Updating the DataFrame with linked column of DoD & Progress

            :return: pd.DataFrame: The updated dataframe
            """
            # Create a new updated series & dataframe with the new data
            updated = self.insert(
                record=record,
                value=editingseries[ColumnSchema.Progress],
                column=ColumnSchema.Progress,
                index=location, debug=debug)
            # Overwrite initial assignment with new dataframe
            updated = self.insert(
                record=record,
                value=editingseries[ColumnSchema.DoD],
                updatedata=updated,
                isupdate=True,
                column=ColumnSchema.DoD,
                index=location, debug=debug)
            return updated
        
        def _selectstatus(mode: str,
                          series: pd.Series,
                          column: str,
                          value: str) -> pd.Series:
            if mode.lower() == "select" and series[column] != value:
                series[column] = value.upper()
                if column == ColumnSchema.Progress:
                    # Modify the DoD Column based on the
                    # progress status/state
                    _updatedod(progress=value)
                    click.echo(message="Progress & Definition"
                                       " of Done updated")
            return series
        
        # Current and Modified datasets diverge here
        # Create a new updated series & dataframe with the new data
        if isinstance(editingseries, pd.Series) and \
            editingseries.empty is False:  # noqa # Pep8 E125
            # Update the series with the new data
            self.newresultseries = _selectstatus(mode=editmode,
                                                 series=editingseries,
                                                 column=ColumnSchema.Progress,
                                                 value=status)
            # Above for inner function for the update frame flow
            # for multiple columns/fields values modifications.
            self.newresultframe = _frameupdate()
            
            # Debug flows
            if debug is True:
                if isinstance(self.newresultseries, pd.Series) and \
                    self.newresultseries.empty is False:  # noqa # Pep8 E125
                    click.echo("Modified Series")
                
                if isinstance(self.newresultframe, pd.DataFrame) and \
                    self.newresultframe.empty is False:  # noqa # Pep8 E125
                    click.echo("Modified DataFrame")
            # Check if the new result is NOT empty and set Update flags
            if self.newresultframe.empty is False:
                self.ismodified = True
                self.lastmodified = self.timestamp()
                click.echo("Modified Frame at " + self.lastmodified)
                self.modified = Record(
                    series=editingseries,
                    source=self.newresultframe)
                # Debug flows
                if debug is True:
                    rich.inspect(self.modified)
                # sets the last edit mode for the record
                self.lasteditmode = editmode
            
            # To be implemented
            if click.confirm("Do you want to save "
                             "the updated DataFrame?"):
                # Save the updated DataFrame to the remote source. NOT WORKING
                self.save(self.newresultframe,
                          series=self.newresultseries,
                          index=location,
                          action='s3',
                          debug=True)
            else:
                click.echo("Exit editing mode")
                return
        
        click.secho(message="No record found at location: " + str(location))
    
    # Editor's Record Actions
    # https://docs.gspread.org/en/v5.7.1/user-guide.html#using-gspread-with-pandas
    # I used this method to save the updated DataFrame to the remote source
    
    def save(self,
             saved: pd.DataFrame,
             series: pd.Series,
             index: int,
             action: str,
             debug: bool = False) -> None:
        """Saves the dataframe and commits it to the remote source.

        :param saved: pd.DataFrame: The updated DataFrame to be saved.
        :param series: pd.Series: The updated Series to be saved.
        :param index: int: The index of the record to be saved.
        :param action: str: The action to be taken on the record.
        :param debug: bool: The debug flag to be used: Default: False
        :return: None
        """
        # 1. Prompt the user to save the updated DataFrame
        if click.confirm("Are you ready to commit changes?"):
            sheet: gspread.Worksheet = Controller.load_wsheet()
            # 2. Check for Validation Client and Worksheet ID presence
            if sheet.client is not None and \
                isinstance(sheet.client, gspread.Client) and \
                sheet.id is not None and sheet.get_all_records():  # noqa
                
                # 3. Convert sheet to a target DataFrame
                target: pd.DataFrame = \
                    DataController.load_dataframe_wsheet(sheet)
                # 4. SAVE ATTEMPT 1: INTEGRATE a single record into the target
                integratedframe: pd.DataFrame = self.integrate(
                    single=saved,
                    source=target,
                    index=index)
                saving = integratedframe.astype(str)
                # 4. SAVE ATTEMPT 1b: switch based on TEST Saving mode
                # s1 = Use integratedframe &
                # Tried gspread_dataframe & set_with_dataframe => set_remote
                # This is not commment out code, it is an annotation
                if action == 's1' and debug is False:
                    set_remote(worksheet=sheet,
                               dataframe=saving,
                               allow_formulas=False)
                # 5. SAVE ATTEMPT 2: Commit the updated DataFrame to remote
                # Use the integratedframe as a overwrit: sheet.update
                # Using https://docs.gspread.org/en/latest/user-guide.html#using-gspread-with-pandas  # noqa # E501 #
                # -# Pep8
                
                # 6. SAVE ATTEMPT 3: Inject the updated series into the remote
                # source, via the series row and index parameters.
                # BY matching on the Position column, primary key
                elif action == 's3' and debug is True:
                    self.injection(series=series,
                                   sheet=sheet,
                                   row=index,
                                   debug=debug)
        else:
            click.echo("Exit editing mode. "
                       "No Changed saved to remote")
            return
    
    # This code was adapted from the PerplexityAI as a generated code
    # https://www.perplexity.ai/search/33fb1a34-54aa-49d4-84aa-45b5d846eba8?s=c
    @staticmethod
    def injection(series: pd.Series,
                  sheet: gspread.Worksheet,
                  row: int,
                  debug: bool = False) -> None:
        """Injects the updated series into the remote source, via the row.

        :param series: The updated series to inject into the remote source.
        :param sheet: The remote source to inject the updated series into.
        :param row: The row to inject the updated series into.
        :param debug: The debug flag to enable/disable debug mode.
        :return: None
        """
        records = sheet.get_all_records()
        
        row_id = None
        for record in records:
            if record['Position'] == series['Position']:
                row_id = int(record[row])
                break
        rich.inspect(row_id)
        # Update the row with the values from the series
        if row_id is not None:
            values = [series[key]
                      for key in series]
            
            if debug is True:
                rich.inspect(values)
            
            if debug is False:
                sheet.update(str(row_id), values)
    
    @staticmethod
    def integrate(single: pd.DataFrame,
                  source: pd.DataFrame,
                  index: int,
                  reset: bool = True,
                  debug: bool = False) -> pd.DataFrame:
        """Merges the source and target DataFrames."""
        # merge the single-row DataFrame into
        # the source DataFrame at the same index
        # https://www.perplexity.ai/search/2a256f73-47dc-4117-bbab-87e4c0a7cbe1?s=c
        # drop any NaN values from the single-row DataFrame
        single = single.dropna()
        
        if debug is True:
            rich.inspect(single)
        
        return pd.concat([source.iloc[:index],
                          single,
                          source.iloc[index:]]).reset_index(drop=reset)
    
    @staticmethod
    def convertto(lt):
        """Converts the list of lists to a list of strings without nan vals."""
        return [[str(element) for element in sublist
                 if str(element) != 'nan'] for sublist in lt]
    
    @staticmethod
    def insert(record: Record,
               value: str,
               updatedata: pd.DataFrame | None = None,
               isupdate: bool = False,
               column: str | None = None,
               index: int | None = None,
               debug: bool = False) -> pd.DataFrame:
        """Inserts by column, using the Record name or index for rows.

        The Editor is a console utility for editing records.

        :param record: The record to be updated
        :param value: The value to be inserted
        :param updatedata: The DataFrame to be updated
        :param isupdate: The update gate flag to indicate
                if the same DataFrame is to be updated again,
                Different column's value for same row's index.
        :param column: The column to be updated
        :param index: The index to be updated
        :param debug: The flag to indicate if debug is enabled

        :method: _update: Update the DataFrame: Private:
        :method: _atindexcolumn: Update the frame's location
        with the new value.

        :return: pd.DataFrame: The updated DataFrame
        """
        
        # https://www.perplexity.ai/search/1ae6c535-37ae-4721-bbc8-38aa37cae119?s=c # noqa
        # Use for debuging IndexError: iloc cannot enlarge its target object
        # Not used for developing the pattern below.
        def _update(framedata: pd.DataFrame,
                    vlue: str,
                    ix: int,
                    col: str) -> pd.DataFrame | None:
            """Update the data at the index and column."""
            
            def _atindexcolumn(data, isz: bool, debg: bool) -> None:  # noqa ANN01 ANN202
                """Update the data at the index and column.

                :param data: The DataFrame to be updated
                :param isz: The flag to indicate if the index is zero
                :param debg: The flag to indicate if debug is enabled
                :return: None

                """
                data.at[ix, col] = vlue
                if isz and debg is True:
                    click.secho(
                        message=f"_IXxCol: Note Updated at row: {ix} "
                                "by zero index for "
                                f"{record.series.name}",
                        err=True)
                    rich.inspect(data.at[ix, col])
                elif not isz and debg is True:
                    click.secho(
                        message="_IXxCol: Note Updated at nonzero'd"
                                f" row: {ix} "
                                f"by {record.series.name} only",
                        err=True)
                    rich.inspect(data.at[ix, col])
            
            # Use the internal DF pointer if the index is not given
            if ix is None and col is not None:
                framedata.at[record.series.name, col] = vlue
            # Use the index of the row if the column is given
            elif isinstance(ix, int) and col is not None:
                if isinstance(record.series.name, int):
                    if index - 1 == record.series.name:
                        _atindexcolumn(data=framedata, debg=debug, isz=True)
                    elif ix != record.series.name:
                        _atindexcolumn(data=framedata, debg=debug, isz=False)
                    elif ix:
                        _atindexcolumn(data=framedata, debg=debug, isz=False)
                        if debug is True:
                            click.secho(message=f"Row's Index {ix} identified")
                    else:
                        if debug is True:
                            click.secho(message="Row not identified", err=True)
                        click.echo("On Update: No changes made")
                else:
                    _atindexcolumn(data=framedata, debg=debug, isz=False)
            else:
                click.echo("Nothing inserted")
        
        # For first column update and assignment of the updated DataFrame
        if updatedata is None and isupdate is False:
            updatedframe = record.sourceframe.copy()
            _update(framedata=updatedframe, vlue=value, ix=index, col=column)
            return updatedframe
        
        # For subsequent column updates and reuse of the same updated DataFrame
        if updatedata is not None and isupdate is True:
            updatedframe = updatedata.copy()
            _update(framedata=updatedframe, vlue=value, ix=index, col=column)
            return updatedframe
        
        # If neither, return the original DataFrame, with no changes
        click.secho("Nothing changed", fg="bright_yellow", err=True)
        return record.sourceframe
    
    @staticmethod
    def clear(record: Record, column: str | None = None,
              index: int | None = None,
              cleared: bool = True) -> pd.DataFrame:
        """Clears by column, using the Record."""
        _noned = None
        updatedframe = record.sourceframe.copy()
        if click.confirm(text="Do you want to clear the notes?. \n"
                              "Importantly clears all notes"):
            value = '' if cleared else _noned
            if index is None and column is not None:
                updatedframe.loc[record.series.name, column] = value
            elif isinstance(index, int) and column is not None:
                if isinstance(record.series.name, int):
                    if index == record.series.name:
                        updatedframe.iloc[index, column] = value
                    else:
                        updatedframe.iloc[index - 1, column] = value
                else:
                    click.echo(message="Series.name is not an int", err=True)
                    updatedframe.iloc[index, column] = value
            else:
                click.echo("Nothing inserted")
        else:
            click.echo("Nothing cleared")
            click.echo("Exiting editing mode")
        
        # Note: If no changes were made, then a copy of original is returned
        return updatedframe
    
    # Editor Utilities
    @staticmethod
    def _isempty(series: pd.Series, column: str) -> bool:
        return not series[column] or series[column] is None
    
    @staticmethod
    def _hascontent(series: pd.Series, column: str) -> bool:
        """Checks if the datasource status is empty.

        Another form of data validation is to
         - check for presence content in the remote, i.e. has content.

        :param series: pd.Series: The series to check
        :param column: str: The column to check
        :return: bool: True if the value is valid, False.
        """
        return bool(series[column]) or series[column] is not None
    
    @staticmethod
    def _hasstatus(series: pd.Series, column: str) -> bool:
        """Checks if the datasource status is valid.

        Another form of data validation is to check the value in the remote.

        :param series: pd.Series: The series to check
        :param column: str: The column to check
        :return: bool: True if the value is valid,
         False otherwise witb message.
        """
        if series[column].lower() in {'todo', 'wip', 'done', 'missed'}:
            return True
        
        click.secho(message="Datasource Status: "
                            f"{series[column]} is invalid"
                            "Check the datasource for accepted values", )
        return False
    
    @staticmethod
    def timestamp(tostring: bool = True,
                  stamp: Literal['date', 'time', 'full', 'precise'] = 'full') \
        -> str | None:  # noqa
        """Returns a timestamp
        
        :param tostring: bool: True if the timestamp is to be returned as a
            string, False otherwise
        :param stamp: Literal['date', 'time', 'full', 'precise']: The format
            of the timestamp to be returned
        :return: str | None: The timestamp as a string, or None
        """
        if tostring:
            fmat: str = "%Y-%m-%d %H:%M:%S.%f"
            if stamp == 'date':
                fmat = "%Y-%m-%d"
            elif stamp == 'time':
                fmat = "%H:%M:%S"
            elif stamp == 'full':
                fmat = "%Y-%m-%d %H:%M:%S"
            elif stamp == 'precise':
                fmat = "%Y-%m-%d %H:%M:%S.%f"
            return datetime.datetime.now().strftime(fmat)
        return None

# End of Controller Module
# Ruff Checked controller.py:1989:9: PLR0915 Too many statements (52 > 50)
# Pep6CI Checked, MyPy Checked, - All Passing
# Timestamp: 2022-06-02T18:00, copywrite (c) 2022-2025, Charles J Fowler
