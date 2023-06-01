#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN101, I001, ARG002
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
from click import echo  # type: ignore
from gspread_dataframe import get_as_dataframe as get_gsdf  # type: ignore
from rich import pretty as rpretty, print as rprint, box  # type: ignore
from rich.columns import Columns as Column  # type: ignore
from rich.console import (Console, ConsoleDimensions,
                          ConsoleOptions, )  # type: ignore
from rich.layout import Layout  # type: ignore
from rich.panel import Panel  # type: ignore
from rich.prompt import Prompt  # type: ignore
from rich.style import Style  # type: ignore
from rich.table import Table, Column  # type: ignore
from rich.text import Text  # type: ignore
from rich.theme import Theme  # type: ignore

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
        """Deletes/Close the client."""
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
    """DataController"""
    
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
    
    def load_dataframe_wsheet(self, wsheet: gspread.Worksheet) \
            -> pd.DataFrame | None:
        """Loads the worksheet into a dataframe.

        :param wsheet: gspread.Worksheet: The worksheet to load
        :return: pd.DataFrame | None: The dataframe or None
        """
        if wsheet.get_all_records():
            dataframe: pd.DataFrame = \
                pd.DataFrame(wsheet.get_all_records())
            self.dataframe = dataframe
            return dataframe
        
        rprint("No data loaded from Google Sheets.")
        return None


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
        """Style the text."""
        emp: str = "bold"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def property() -> Style:
        """Returns the Style for the property."""
        emp: str = "bold"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def value() -> Style:
        """Returns the Style for the property."""
        emp: str = "italic"
        co: str = "dark_turquoise"
        bg: str = "black"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def modified() -> Style:
        """Returns the Style for the property."""
        emp: str = "italic"
        co: str = "deep_pink3"
        bg: str = "black"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def heading() -> Style:
        """Returns the Style for the property."""
        emp: str = "bold italic underline2"
        co: str = "purple4"
        bg: str = "grey93"
        styled: str = f'{emp} {co} on {bg}'
        return RICHStyler.style.parse(styled)
    
    @staticmethod
    def border(stylestr: bool = True) -> Style | str:
        """Returns the Style for the property."""
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
            -> ConsoleOptions:
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
    
    @staticmethod  #
    def page_data(dataset: list[str]) -> None | NoReturn:
        """Displays the data."""
        with console.pager(styles=True):
            rprint(dataset)
    
    @staticmethod
    def configure_table(
            headers: typing.Optional[list[str]]) -> rich.table.Table:
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
    def set_datatable(dataframe: pd.DataFrame | pd.Series) -> rich.table.Table:
        """Sets the table per dataframe."""
        if isinstance(dataframe, pd.DataFrame):
            headers: list[str] = dataframe.columns.tolist()
        elif isinstance(dataframe, pd.Series):
            headers: list[str] = dataframe.index.tolist()
        else:
            raise ValueError("Bad Parameter: Pandas DataFrame"
                             " or Series object.")
        
        consoletable: Table = WebConsole.configure_table(headers=headers)
        return consoletable


class Inner:
    """Displays inner terminal layout."""
    
    layout: Layout = None
    current: Layout = None
    modified: Layout = None
    header: Layout = None
    editor: Layout = None
    
    def __init__(self) -> None:
        """Initialises the inner terminal layout."""
        self.layout = Layout()
        self.arrange()
        self.edit()
    
    def arrange(self) -> None:
        """Configures the terminal."""
        self.header = Layout(name="header", ratio=2)
        self.editor = Layout(name="editor", ratio=3)
        self.layout.split_column(self.header, self.editor)
    
    def edit(self, width: int = 40, part: int = 1) -> None:
        """Configures the terminal."""
        self.current = Layout(name="current",
                              size=part,
                              minimum_size=width)  # noqa
        self.modified = Layout(name="modified",
                               ratio=part,
                               minimum_size=width)  # noqa
        
        self.layout.split_row(self.current, self.modified)
    
    def toggle(self,
               headershow: bool = True,
               editorshow: bool = True) -> None:
        """Toggles Layouts."""
        
        self.layout["header"].visible = headershow
        self.layout["editor"].visible = editorshow
    
    def updates(self,
                renderable,
                target:
                Literal["header", "editor", "current", "modified", "footer"]) \
            -> None:  # noqa
        """Updates the layout."""
        self.layout[target].update(renderable)
    
    def refresh(self, consoleholder: Console,
                target:
                Literal["header", "editor", "current", "modified", "footer"]) -> None:  # noqa
        """Refreshes the layout."""
        if consoleholder is None:
            consoleholder = Console()
            self.layout.refresh(consoleholder, layout_name=target)
        elif isinstance(consoleholder, Console):
            self.layout.refresh(consoleholder, layout_name=target)
    
    def laidout(self, consoleholder: Console, output: bool = True) \
            -> Layout | None:
        """Returns the layout."""
        if not output:
            return self.layout
        
        click.echo(f"Pane is: {self.layout['current'].name}")
        consoleholder.print(self.layout)
        return None


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
        """Display Data: Wrapper for Any Display."""
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
        """Displays the data in a table."""
        headers: list = headerview if isinstance(headerview, list) else [headerview]
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
            -> None | NoReturn:
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

    :meth: getrowframe: Get a row from a dataframe by an index or a search term.
    """
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def search(frame: pd.DataFrame,
               searchterm: str,
               exact: bool = False) -> pd.DataFrame | None:
        """Search across all columns for the searches team

        :param frame: pd.DataFrame - Dataframe to search
        :param searchterm: str - Search term
        :param exact: bool - Exact match
        :return: pd.DataFrame - Search result """
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
            -> pd.DataFrame | pd.Series | None:
        """Get the row from the dataframe by index.
        
        :param frame: pd.DataFrame - Dataframe to search
        :param index: int - Index to search
        :param zero: bool - Zero based index
        :return: pd.DataFrame | pd.Series | None - Expect a result or None
        """
        if isinstance(index, int) and index is not None:
            return frame.iloc[index] if zero else frame.loc[index - 1]
    
    @staticmethod
    def rows(frame: pd.DataFrame,
             index: int = None,
             zero: bool = True,
             squeeze: bool = False,
             debug: bool = False) \
            -> pd.DataFrame | pd.Series | None:
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
        debug: bool: optional debug flag, by default False

        return pd.DataFrame | None: - Expect a result or None
        """
        result: pd.DataFrame | pd.Series | None
        if index:
            result = Results.index(frame=frame, index=index, zero=zero)  # noqa
        else:
            click.echo("Please provide an index identifier for a team")
            return None
        
        if squeeze and isinstance(result, pd.DataFrame) and len(result) == 1:
            result = result.squeeze()
        
        return result
    
    @staticmethod
    def getrowdata(data: pd.DataFrame,
                   ix: int,
                   single: bool = False,
                   debug: bool = True) \
            -> pd.Series | pd.DataFrame | None:
        """Get a row from a dataframe by index or searches term.

        :param data: pd.DataFrame - Dataframe
        :param ix: int - Index
        :param single: bool - Single row
        :param debug: bool - Debug
        :return: pd.Series | pd.DataFrame | None - Row or rows
        """
        if ix:
            result = Results.rows(frame=data, index=ix,
                                  squeeze=True,
                                  debug=debug)
        else:
            click.echo(f"No Data for row: {ix}")
            return None
        
        if isinstance(result, pd.Series):
            if debug is True:
                click.secho(f"GetRowData(): Series:"
                            f" Found a Series's record\n")
                rich.inspect(result)
            return result
        elif isinstance(result, pd.DataFrame):
            if debug is True:
                click.secho("GetRowData() Dataframe: "
                            "Found a set of records")
                rich.inspect(result)
            return result
        else:
            click.secho("GetRowData(): Found something: undefined")
            if debug:
                rich.inspect(result)
            return None


class Record:
    """A Record is a row of data to be displayed in console, by views
    
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
        """The editedmode of the record."""
        return self.editedmode
    
    @editmode.setter
    def editmode(self, value: str) -> None:
        """The editedmode of the record."""
        self.editedmode = value
    
    @property
    def modified(self) -> str | None:
        """The lastmodified of the record."""
        return self.lastmodified
    
    @modified.setter
    def modified(self, value: str) -> None:
        """The lastmodified of the record."""
        self.lastmodified = value
    
    @property
    def command(self) -> str:
        """The lastcommand of the record."""
        return self.lastcommand
    
    @command.setter
    def command(self, value: str) -> None:
        """The lastcommand of the record."""
        self.lastcommand = value
    
    @staticmethod
    def cmdnote(value: str) -> str:
        """The lastcommand of the record."""
        if value == 'insert':
            return 'This note is now added'
        elif value == 'append':
            return 'This note is now updated'
        elif value == 'clear':
            return 'This note is now deleted'
        elif value == 'toggle':
            return 'The progress status is now reported'
    
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
        elif isinstance(single, pd.Series):
            if Record.checksingle(single):
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
    def checksingle(single: pd.DataFrame | pd.Series) -> bool:
        """Checks the source of the record, if any."""
        if isinstance(single, pd.DataFrame):
            if single.ndim == Record.length and single.empty is False:
                return True
            click.echo(message="The DataFrame must be a single row.",
                       err=True)
            return False
        
        if isinstance(single, pd.Series) and single.empty is False:
            return True
        click.echo(message="The Series must be a single row.",
                   err=True)
        return False
    
    def card(self, consolecard: Console,
             source: pd.Series | None = None,
             sendtolayout: bool = False) -> Table | None:
        """Displays the record as a cardinal."""
        
        def config() -> Table:
            """Displays the record as a cardinal."""
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
                -> Table | None:  # noqa
            """Populates the card from instance or a from external source"""
            if data is not None and isinstance(data, pd.Series):
                for label, value in data.items():
                    table.add_row(str(label), str(value))
                return table
            elif self.series is not None and \
                    isinstance(self.series, pd.Series):
                for label, value in self.series.items():
                    table.add_row(str(label), str(value))
                return table
        
        card: Table = display(table=config(), data=source)
        
        if sendtolayout:
            consolecard.print(card)
            return None
        else:
            return card
    
    @staticmethod
    def panel(consolepane: Console,
              renderable,
              fits: bool = False,
              card: tuple[int, int] = (0, 0),
              align: typing.Literal["left", "center", "right"] = "left",
              outline: rich.box = box.SIMPLE, sendtolayout: bool = False,
              debug: bool = False) \
            -> Panel | None:  # noqa
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
                record=None, sendtolayout: bool = False) -> Panel | None:
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
        """Sets the table box style."""
        if style == 1:
            table.box = box.SIMPLE
        elif style == 2:
            table.box = box.ROUNDED
        elif style == 3:
            table.box = box.HEAVY_HEAD
        elif style == 4:
            table.box = box.SIMPLE_HEAD
        elif style == 5:
            table.box = box.HORIZONTALS
        elif style == 6:
            table.box = box.SQUARE
        
        return table
    
    def header(self, consolehead: Console,
               sendtolayout: bool = False,
               gridfit: bool = False,
               subgrid: bool = False,
               debug: bool = False) -> Table | None:
        """Displays the header of the record"""
        
        def config(fit: bool = False,
                   sides: int = 1,
                   block: int = 0,
                   outline: int = 1) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            g.show_lines = True
            g.padding = (block, sides)
            g.add_column(header="Index",
                         # min_width=30,
                         # max_width=35,
                         ratio=2,
                         header_style=styld.heading(),
                         vertical='top')  # noqa
            g.add_column(header="Grade",
                         # min_width=30,
                         # max_width=35,
                         ratio=2,
                         header_style=styld.heading(),
                         vertical='top')  # noqa
            
            g = self.boxed(table=g, style=outline)
            return g
        
        def indexgrid(expan: bool, boxd: int = 1) -> Table:
            """Display the subtable for Index/Identifiers"""
            identtable: Table = config(fit=expan,
                                       sides=5,
                                       outline=boxd)
            rowid_label: str = 'Record Name:  '
            rowid_value: str = f'{self.series.name}'
            identtable.add_row(rowid_label,
                               rowid_value)
            pos_label: str = 'Position ID:  '
            pos_value: str = f'{self.recordid}'
            identtable.add_row(pos_label,
                               pos_value)
            return identtable
        
        def gradegrid(expan: bool, boxd: int = 1) -> Table:
            """Display the subtable for Grade/Performance"""
            gradetable: Table = config(fit=expan, sides=5, outline=boxd)
            grade_label: str = 'Grade:  '
            grade_value = f'{self.grade}'
            gradetable.add_row(grade_label, grade_value)
            outcome_label: str = 'Outcome:  '
            
            outcome_value = f'{self.type} | {self.prefix}:{self.reference}'
            gradetable.add_row(outcome_label, outcome_value)
            return gradetable
        
        def maingrid(table: Table,
                     left: Table,
                     right: Table,
                     boxd: int = 1,
                     sides: int = 1,
                     block: int = 0,
                     fit: bool = gridfit) -> Table:
            """ Display the header grid table"""
            m: Table = table
            m.grid(expand=fit)
            m.padding = (block, sides)
            m = self.boxed(table=m, style=boxd)
            m.add_row(left, "   ", right)
            return m
        
        indexpane: Table = indexgrid(expan=subgrid)
        gradepane: Table = gradegrid(expan=subgrid)
        mainpane: Table = maingrid(table=config(),
                                   left=indexpane,
                                   right=gradepane,
                                   sides=5,
                                   boxd=3,
                                   fit=gridfit)  # noqa
        
        if debug is True:
            rich.inspect(mainpane)
        
        return Record.switch(mainpane,
                             printer=consolehead,
                             switch=sendtolayout)
    
    def editable(self, consoleedit: Console | None = None,
                 expand: bool = False,
                 sendtolayout: bool = False,
                 title: str = 'Current Data',
                 debug: bool = False) -> Table | None:  # noqa
        """Displays the record: Use it for Current | Modified Records"""
        webconsole: Console = consoleedit  # noqa
        
        def config(fit: bool) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            g.add_column(header="Current",
                         min_width=30,
                         ratio=1,
                         vertical='top')  # noqa
            return g
        
        def currentdata(table: Table, t: str) -> Table:
            """Display the subtable for Index/Identifiers"""
            currenttable: Table = table
            if currenttable.title is None and t is not None:
                currenttable.title = t
            todo_label: str = 'To Do:'
            todo_value = f'{self.todo} \n'
            criteria_label: str = 'Criteira: '
            criteria_value = f'{self.criteria} \n\n'
            currenttable.add_section()
            notes_label: str = 'Notes: '
            notes_value = 'Add a note' if self.notes is None else f'{self.notes} \n'
            # Build rows
            currenttable.add_row(todo_label, style=styld.label())
            currenttable.add_row(todo_value, style=styld.value())
            currenttable.add_row(criteria_label, style=styld.label())
            currenttable.add_row(criteria_value, style=styld.value())  # noqa
            currenttable.add_row(notes_label, style=styld.label())
            currenttable.add_row(notes_value, style=styld.value())
            return currenttable
        
        currentdatapane: Table = \
            currentdata(table=config(fit=expand), t=title)  # noqa
        
        if debug is True:
            rich.inspect(currentdatapane)
        
        return Record.switch(currentdatapane,
                             printer=consoleedit,
                             switch=sendtolayout)
    
    def footer(self, consolefoot: Console,
               sendtolayout: bool = False,
               expand: bool = True,
               valign: str = 'top',
               debug: bool = False) -> Table | None:
        """Displays footer as a card/record"""
        
        # Config Table/Grid for Footer
        def config(fit: bool, vertical: str) -> Table:
            """Displays the record as a cardinal."""
            g: Table = Table.grid(expand=fit)
            g.add_column(header="More",
                         min_width=30,
                         ratio=1,
                         vertical=vertical)  # noqa
            g.add_column(header="Linked",
                         min_width=15,
                         ratio=1,
                         vertical=vertical)  # noqa
            g.add_column(header="Categories",
                         min_width=20,
                         ratio=1,
                         vertical=vertical)  # noqa
            return g
        
        def metapane(table: Table) -> Table:
            """Display the subtable for Index/Identifiers"""
            meta: Table = table
            meta.title = 'Project Data'
            meta.add_section()
            tier_label: str = 'Tier: '
            link_label: str = 'Linked: '
            topics_label: str = 'Topics: '
            tier_value = f'{self.type}.{self.prefix}.{self.reference}'
            meta.add_row(f'{tier_label}  {tier_value})',
                         f'{link_label}:  {self.linked}',
                         f'{topics_label}:  {self.topics}')
            meta.add_section()
            now: datetime = datetime.datetime.now()
            dt_string: str = now.strftime("%d/%m/%Y %H:%M")  # %S
            meta.add_row(f'Viewed: {dt_string}',
                         f'{topics_label}:  {self.topics}', ' ')
            return meta
        
        footer: Table = metapane(table=config(fit=expand, vertical=valign))  # noqa
        
        if debug is True:
            rich.inspect(footer)
        
        return Record.switch(footer,
                             printer=consolefoot,
                             switch=sendtolayout)
    
    @staticmethod
    def setcolumn(table: Table,
                  heading: str = '',
                  hstyle=None,
                  footing: str = '',
                  fstyle=None,
                  styler=None,
                  minw: int = 35,
                  maxw: int = 50,
                  width: int = 50,
                  full: bool = True,
                  wraps: bool = False,
                  proportion: int = 1) -> Table:
        """Configured the Rich Column for the webconsole, side x side"""
        table.add_column(header=heading,
                         footer=footing,
                         header_style=hstyle,
                         footer_style=fstyle,
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
        """Renders the footnote for the record"""
        return f'{self.cmdnote(self.editmode)} at: {self.modified}'
    
    def comparegrid(self,
                    container: Table,
                    left: Table,
                    right: Table,
                    fit: bool = False,
                    sendtolayout: bool = False,
                    debug: bool = False) -> Table | None:
        """ Display the header grid table"""
        main: Table = container
        main.grid(expand=fit)
        main.width = 100
        main.title = f'{self.command}: {self.type}.{self.prefix}.{self.reference}'
        main.show_footer = True
        main = Record.setcolumn(table=main,
                                heading="Existing",
                                footing=f'-----------------')
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
               switch: bool = False) -> Table | None:
        """Switches between console print or redirecting to a layout"""
        # App.values.Display.TOLAYOUT = True, (author notes, not unused code).
        # Then send renderable to next Rich Renderable handler.
        # Does not print to console.
        if switch is True:
            return renderable
        
        # If App.values.Display.TOTERMINAL = False,
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
    """The Editor is a console utility for editing records."""
    
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
    TOGGLEMODE: str = 'toggle'
    INSERTEDIT: str = 'insert'
    APPENDEDIT: str = 'append'
    REPLACEEDIT: str = 'replace'
    CLEAREDIT: str = 'clear'
    lastcommand: str | None = None
    
    def __init__(self,
                 currentrecord: Record = None,
                 sourceframe: pd.DataFrame | None = None,
                 debug=False) -> None:
        """The Editor is a console utility for editing records."""
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
        """Return the last command"""
        return self.lastcommand
    
    @command.setter
    def command(self, value: str) -> None:
        """Set the last command"""
        self.lastcommand = value
    
    def edit(self) -> None:
        """The Editor is a console utility for editing records."""
        pass
    
    def editnote(self,
                 edits,
                 index: int,
                 notepad,
                 debug: bool = False) -> None:
        """Hub switch between editing modes, and actions for Notes """
        #
        if edits == self.ADDMODE:
            self.addingnotes(notes=notepad,
                             location=index,
                             debug=debug)
        elif edits == self.UPDATEMODE:
            self.updatingnotes(notes=notepad,
                               location=index,
                               debug=debug)
        elif edits == self.DELETEMODE:
            self.deletingnotes(notes=notepad,
                               location=index,
                               debug=debug)
        else:
            click.echo(message="Exiting Editing Mode. Bad Edit Mode.")
    
    @property
    def editmode(self) -> str:
        """Return the last edit mode"""
        return self.lasteditmode
    
    @editmode.setter
    def editmode(self, value: str) -> None:
        """Set the last edit mode"""
        self.lasteditmode = value
    
    def editprogress(self, edits,
                     index: int,
                     choicepad,
                     debug: bool = False) -> None:
        """Hub switch between editing modes, and actions for ToDos
         
         And similar status/values choice fields/columns"""
        
        if edits == self.TOGGLEMODE:
            self.togglestatus(status=choicepad,
                              location=index,
                              debug=debug)
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
        """ Adding Notes to the Record/Series for the add note command
        
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
                # Perplexity AI was used to build out this function, based on below.
                # https://www.perplexity.ai/search/a8d503cb-8aec-489a-8cf5-7f3e5b573cb7?s=c
                # Set the edit mode explicitly to insert
                EDITMODE = self.INSERTEDIT  # noqa
                self.editmode = EDITMODE
                # User confirmation to add the note, step by step
                if click.confirm("Please confirm to "
                                 f"add/{EDITMODE} your note"):
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
                    return None
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
                return None
    
    def updatingnotes(self, notes: str,
                      location: int | None = None,
                      debug: bool = False) -> None:
        """Updating Notes to the Record/Series for the update note command
        
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
        :return: None"""
        # See addingnotes() for the PerplexityAI use case as co-Pilot.
        # Guard conditions, 2nd layer of santisation,
        if notes is not None and isinstance(notes, str):
            # Copy the current record's series into a local series
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode, before use
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
                    return None
    
    def deletingnotes(self,
                      notes: str,
                      location: int | None = None,
                      debug: bool = False) -> None:
        """Deleting Notes to the Record/Series for the delete note command
        
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
        :return: None"""
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
                # The user clear all the notes and then decide to delete or not.
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
                    return None
    
    def modifynotes(self, editingseries, record: Record,
                    notes: str,
                    editmode: str = Literal["insert", "append", "clear"],
                    location: int | None = None, debug=False) -> None:  # noqa
        """ Hub Function for editing notes: Note to the designed pattern
        
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
        :return: None"""
        # EditMode is Insert: then add / overwrite / create at the location
        if editmode == self.INSERTEDIT:
            self.lasteditmode = self.INSERTEDIT
            # Insert the notes - add / overwrite / create
            editingseries[ColumnSchema.Notes] = notes
            click.echo(f"Note inserted")
        # EditMode is Append: then append the notes the Notes column
        elif editmode == self.APPENDEDIT:
            self.lasteditmode = self.APPENDEDIT
            # Append the notes - by target location (Notes)
            editingseries[ColumnSchema.Notes] = \
                self.appendnotes(series=editingseries,
                                 column=ColumnSchema.Notes,
                                 value=notes)
            click.echo(f"Note inserted")
        # EditMode is Clear: then clear the notes the Notes column
        elif editmode == self.CLEAREDIT:
            self.lasteditmode = self.CLEAREDIT
            editingseries[ColumnSchema.Notes] = \
                self.deletenotes(series=editingseries,
                                 column=ColumnSchema.Notes)
            click.echo(f"Note cleared")
        
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
                    self.newresultseries.empty is False:
                click.echo("Modified Series")
            
            if isinstance(self.newresultframe, pd.DataFrame) and \
                    self.newresultframe.empty is False:
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
        if click.confirm("Do you want to save the updated DataFrame?"):
            # self.sourceframe = updatedframe
            # TODO: Implement the commit function to save
            # the updated DataFrame remotely
            # commit()
            click.echo("TODO: DataFrame saved")
        else:
            click.echo("Exit editing mode")
            return None
    
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
        """Deletes complete/all notes from the existing record/row if flag: nodestroy/destroy
        
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
            """Removes the label from the notes"""
            
            if series[column] == 'Add a note'.strip():
                series[column] = cleared
            return series[column]
        
        def _haslabel() -> bool:
            """Checks if the notes have a label"""
            return True if series[column].startswith('Add a note') else False
        
        def _emptydelete(clear: str = '') -> bool:
            """Checks if the notes are empty"""
            if nodestroy is False and _haslabel() is False:
                return True if series[column] == clear else False
            elif nodestroy is True and _haslabel() is True:
                series[column] = _removelabel(clear)
                return True if series[column] == clear else False
            elif nodestroy is True and _haslabel() is False:
                return True if series[column] == clear else False
            elif nodestroy is True and _haslabel() is True:
                series[column] = _removelabel(clear)
                return True if series[column] == clear else False
        
        _cleared = ''
        if _emptydelete(_cleared):
            click.echo(message="No notes to delete")
            return series[column]
        elif nodestroy is False:
            click.echo(message="Exitsing notes present. No change")
            return series[column]
        else:
            click.echo(message="Cleared")
            cleared = series[column] = _cleared
            return cleared
    
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
        """Toggle the status of the record"""
        shown: bool = True
        notso: bool = False
        validstatus: list[str] = ['ToDo', 'WIP', 'Done', 'Missed']
        
        def reprompt() -> str | None:
            """Re-prompt the user to enter a valid status"""
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
            else:
                click.echo("Invalid status. Try again.")
                return None
        
        # Check if the status is valid
        if _checkstatus(state=status, debg=debug) is not None:
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode, before use
            if self._hascontent(editingseries, ColumnSchema.Notes):
                EDITMODE = 'toogle'  # noqa
                if click.confirm(text="Please confirm to"
                                      f" {EDITMODE} your ToDo progress status"):
                    self.modifyprogress(editingseries,
                                        record=self.record,
                                        status=_checkstatus(status),
                                        editmode=EDITMODE,
                                        location=location,
                                        debug=debug)
                elif click.confirm(
                        text="Do you want to modify progress status? \n"):
                    newprogress = reprompt()
                    if isinstance(newprogress, str) and newprogress is not None:
                        self.modifyprogress(editingseries,
                                            record=self.record,
                                            status=_checkstatus(newprogress),
                                            editmode=EDITMODE,
                                            location=location,
                                            debug=debug)
                    else:
                        click.echo(message="No Edit Made for  "
                                           f"{EDITMODE} of progress status",
                                   err=True)
                else:
                    click.echo("Exiting editing mode:"
                               f" Update {EDITMODE}")
                    return None
        else:
            return None
    
    def modifyprogress(self, editingseries, record: Record,
                       status: str,
                       editmode: str = Literal["toggle"],
                       location: int | None = None, debug=False) \
            -> None:  # noqa
        """ Hub Function for editing notes: Note to the designed pattern

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
        :param editmode: Literal["toggle"]: Possible values.
                The mode of editing the notes.
        :param location: int: | None:
                The location of the notes to be added to the record.
        :param debug: bool: The flag to debug.

        Inner Methods
        :method: _updatedod: Update the DoD based on the progress
        :method: _frameupdate: Update the record dataframe with multipe columns.
        
        Returns:
        ----------
        :return: None """
        
        # EditMode is Toggle:
        #  then clear current and
        #  create/assign at the location
        #  i.e. an destructive overwrite of the progress
        
        def _updatedod(progress):
            """Update the DoD based on the progress"""
            # Did ask, and did not accepted/use, the Perplexity AI suggestion
            # It was a bit more advanced for my needs/comprehension.
            # https://www.perplexity.ai/search/86c9fb35-3b58-4b7b-83ed-78e1f5ede769?s=c
            click.echo("Current Item' Project Status :"
                       f" {editingseries[ColumnSchema.Progress]}")
            # Statically State machine for updating the DoD reporting:
            # Truthy only.
            if editingseries[ColumnSchema.Progress] == progress:
                click.echo("Progress updated")
                # Keep the same, is the default
                if editingseries[ColumnSchema.DoD] == 'Planned' and \
                        progress.lower() == 'todo':
                    editingseries[ColumnSchema.DoD] = 'Planned'
                # Update if item is overlooked
                if editingseries[ColumnSchema.DoD] == 'Planned' and \
                        progress.lower() == 'missed':
                    editingseries[ColumnSchema.DoD] = 'Unfinished'
                # Update if item is started, up DoD is not updated
                elif editingseries[ColumnSchema.DoD] == 'Planned' and \
                        progress.lower() == 'wip':
                    editingseries[ColumnSchema.DoD] = 'In Progress'
                # Update if item is done, up DoD is not updated
                elif editingseries[ColumnSchema.DoD] == 'In Progress' and \
                        progress.lower() == 'done':
                    editingseries[ColumnSchema.DoD] = 'Completed'
                # Update if item is not completed on time
                elif editingseries[ColumnSchema.DoD] == 'In Progress' and \
                        progress.lower() == 'missed':
                    editingseries[ColumnSchema.DoD] = 'Unfinished'
                # Update if item is not done, status is missed, DoD is refreshed
                elif editingseries[ColumnSchema.DoD] == 'Unfinished' and \
                        progress.lower() != 'done' \
                        and progress.lower() == 'missed':
                    editingseries[ColumnSchema.DoD] = 'Unfinished'
                else:
                    click.secho(
                            message="Progress and Project reporting not updated")
        
        def _frameupdate() -> pd.DataFrame:
            """Update the frame with the new data
            
            :return: pd.DataFrame: The updated dataframe"""
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
        
        if editmode.lower() == "toggle":
            # Insert the notes - add / overwrite / create
            editingseries[ColumnSchema.Progress] = ''
            
            if editingseries[ColumnSchema.Progress] == '':
                editingseries[ColumnSchema.Progress] = status
                
                if editingseries[ColumnSchema.Progress] == status:
                    # Modify the DoD Column based on the progress status/state
                    _updatedod(progress=status)
                    click.echo("Progress & Definition of Done updated")
        # Current and Modified datasets diverge here
        # Create a new updated series & dataframe with the new data
        self.newresultseries = editingseries
        # Above for inner function for the update frame flow
        # for multiple columns/fields values modifications.
        self.newresultframe = _frameupdate()
        # Debug flows
        if debug is True:
            if isinstance(self.newresultseries, pd.Series) and \
                    self.newresultseries.empty is False:
                click.echo("Modified Series")
            
            if isinstance(self.newresultframe, pd.DataFrame) and \
                    self.newresultframe.empty is False:
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
        if click.confirm("Do you want to save the updated DataFrame?"):
            # self.sourceframe = updatedframe
            # TODO: Implement the commit function to save
            # the updated DataFrame remotely
            # commit()
            click.echo("TODO: DataFrame saved")
        else:
            click.echo("Exit editing mode")
            return None
    
    # Editor's Record Actions
    def save(self, savedfranme: pd.DataFrame) -> None:
        """ Saves the dataframe and commits it to the remote source
        
        The Editor is a console utility for editing records."""
        # Prompt the user to save the updated DataFrame
        if click.confirm("Do you want to save the updated DataFrame?"):
            self.sourceframe = savedfranme
            # TODO: Implement the commit function to
            # save the updated DataFrame remotely
            # commit()
        else:
            click.echo("Exit editing mode")
            return None
    
    @staticmethod
    def insert(record: Record,
               value: str,
               updatedata: pd.DataFrame | None = None,
               isupdate: bool = False,
               column: str | None = None,
               index: int | None = None,
               debug: bool = False) -> pd.DataFrame:
        """ Inserts by column, using the Record.
        name or index for rows, if either is known or given.
        
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
        :method: _atindexcolumn: Update the frame's location with the new value.
        
        :return: pd.DataFrame: The updated DataFrame
        """
        
        # https://www.perplexity.ai/search/1ae6c535-37ae-4721-bbc8-38aa37cae119?s=c # noqa
        # Use for debuging IndexError: iloc cannot enlarge its target object
        # Not used for developing the pattern below.
        def _update(framedata: pd.DataFrame,
                    vlue: str,
                    ix: int,
                    col: str) -> pd.DataFrame | None:
            """Update the data at the index and column"""
            
            def _atindexcolumn(data, debg: bool, isz: bool):
                """Update the data at the index and column"""
                data.at[ix, col] = vlue
                if isz and debug is True:
                    click.secho(
                            message=f"_IXxCol: Note Updated at row: {ix} "
                                    "by zero index for "
                                    f"{record.series.name}",
                            err=True)
                    rich.inspect(data.at[ix, col])
                elif not isz and debug is True:
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
        elif updatedata is not None and isupdate is True:
            updatedframe = updatedata.copy()
            _update(framedata=updatedframe, vlue=value, ix=index, col=column)
            return updatedframe
        # For If neither, return the original DataFrame, with no changes
        else:
            click.secho("Nothing changed",
                        fg="bright_yellow",
                        err=True)
            return record.sourceframe
    
    @staticmethod
    def clear(record: Record, column: str | None = None,
              index: int | None = None,
              cleared: bool = True) -> pd.DataFrame:
        """ Clears by column, using the Record."""
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
        return series[column] == '' or series[column] is None
    
    @staticmethod
    def _hascontent(series: pd.Series, column: str) -> bool:
        return series[column] != '' or series[column] is not None
    
    @staticmethod
    def timestamp(tostring: bool = True,
                  stamp: Literal['date', 'time', 'full', 'precise'] = 'full') \
            -> str:
        """Returns a timestamp"""
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
# End of Controller Module
# Globals: connector, configuration, console
# Class: Controller, ColumnSchema, Headers, DataController,
#         Editor, WebConsole,
# Class: Inner, Display, Record, Editor
# Timestamp: 2022-05-21T16:30, copywrite (c) 2022-2025,
#       see {} for more details.
