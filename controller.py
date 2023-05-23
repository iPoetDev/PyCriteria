#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN101, I001, ARG002
"""Module: Controller for the Terminal App."""

# 0.1 Standard Library Imports
import dataclasses
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
from rich.columns import Columns  # type: ignore
from rich.console import Console, ConsoleDimensions, ConsoleOptions, RenderableType  # type: ignore
from rich.layout import Layout  # type: ignore
from rich.panel import Panel  # type: ignore
from rich.prompt import Prompt  # type: ignore
from rich.style import Style  # type: ignore
from rich.table import Table  # type: ignore
from rich.text import Text  # type: ignore
from rich.theme import Theme  # type: ignore

#
# 0.3 Local imports
import connections
import settings

#
# 1.1: Global/Custom Variables
connector: connections.GoogleConnector = connections.GoogleConnector()
configuration: settings.Settings = settings.Settings()
tablesettings: settings.TableSettings = settings.TableSettings()
console: Console = Console()


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
    Topic: str = "CriteriaTopic"
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
    OverviewViews: list[str] = [c.Position, c.Group, c.Performance,
                                c.Topic, c.Criteria, c.Progress]
    CriteriaView: list[str] = [c.Row, c.Position, c.Topic,
                               c.Reference, c.Criteria, c.Notes]
    ProjectView: list[str] = [c.Position, c.Tier, c.DoD, c.Reference,
                              c.Progress, c.Flag]
    ToDoAllView: list[str] = [c.Position, c.Performance, c.DoD, c.Criteria,
                              c.Progress, c.Notes]
    ToDoSimpleView: list[str] = [c.Position, c.Criteria, c.Progress, c.Notes]
    ToDoDoDView: list[str] = [c.Position, c.DoD, c.Criteria, c.Progress]
    ToDoGradeView: list[str] = [c.Position, c.Criteria, c.Performance, c.DoD]
    ToDoReviewView: list[str] = [c.Reference, c.Criteria, c.Performance, c.Progress]
    NotesView: list[str] = [c.Position, c.Criteria, c.Notes]
    ReferenceView: list[str] = [c.Position, c.Reference, c.Related]
    ViewFilter: list[str] = ["Overview", "Criteria", "Project", "ToDo", "References"]
    ToDoChoices: list[str] = ["All", "Simple", "DoD", "Grade", "Review"]
    HeadersChoices: list[str] = ["Position", "Tier", "Performance",
                                 "Criteria", "Progress", "Notes"]
    
    def __init__(self, labels: ColumnSchema) -> None:
        """Headers."""
        self.c = labels


class DataController:
    """DataController for the effort of loading the data, fetching it, managing it.

    Links the connector to the app's command:

    CRUD engine + filter, find/searches, show/hide
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
    2. The WebConsole handles the console Display/logics.
    3. The DataTransformer handles any Extract, Transform,
    Load (ETL) logic (load_* tasks are shared with controller)
    4. The DataModel handles the in memory data structure and
    data logics (maybe move Topics, Entry to DataModel)
    5. The Display handles the TUI output Display rendering logics
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

        :param query: str: The query to use as a search
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
    
    def update_row(self, values: list | dict) -> pd.Series | None:
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
    
    def delete_item(self, position: int) -> pd.Series:
        """Delete an item in the dataframe."""
        self.dataframe.iloc[position] = ""
        return self.dataframe.iloc[position]
    
    def delete_row(self, values: list | dict) -> pd.DataFrame | None:
        """Delete a row in the dataframe."""
        for index, row in self.dataframe.iterrows():
            if all(row == values):
                self.dataframe = self.dataframe.drop(index)
                return self.dataframe
        return None
    
    @staticmethod
    def max(dataframe: pd.DataFrame) -> str:
        """Return the maximum value in a row."""
        return str(len(dataframe))


class RICHStyler:
    """Rich Styler for Rich.console Style."""
    style = Style()
    
    def __init__(self) -> None:
        """Initialises the TUI Styler."""
        self.style = Style()
        pass
    
    @staticmethod
    def panel(grey: int, tostring: bool = True) -> Style | str:
        """Returns the Style for the property.
        
        :param grey: int: The grey level
          https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param tostring: bool: Whether to return a string or Style
        """
        emp: str = "bold"
        co: str = "white"
        bg: str = f"grey{str(grey)}"
        styled: str = f'{emp} {co} on {bg}'
        if tostring:
            return styled
        else:
            return RICHStyler.style.parse(styled)
    
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
        if stylestr:
            return styled
        else:
            return RICHStyler.style.parse(styled)


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
    def set_datatable(dataframe: pd.DataFrame | pd.Series) -> rich.table.Table:
        """Sets the table per dataframe."""
        if isinstance(dataframe, pd.DataFrame):
            headers: list[str] = dataframe.columns.tolist()
        elif isinstance(dataframe, pd.Series):
            headers: list[str] = dataframe.index.tolist()
        else:
            raise ValueError("Bad Parameter: Pandas DataFrame or Series object.")
        
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
        
        if headershow:
            self.layout["header"].visible = True
        else:
            self.layout["header"].visible = False
        
        if editorshow:
            self.layout["editor"].visible = True
        else:
            self.layout["editor"].visible = False
    
    def updates(self,
                renderable,
                target: Literal["header", "editor", "current", "modified", "footer"]) -> None:
        """Updates the layout."""
        self.layout[target].update(renderable)
    
    def refresh(self, consoleholder: Console,
                target: Literal["header", "editor", "current", "modified", "footer"]) -> None:
        """Refreshes the layout."""
        if consoleholder is None:
            consoleholder = Console()
            self.layout.refresh(consoleholder, layout_name=target)
        elif isinstance(consoleholder, Console):
            self.layout.refresh(consoleholder, layout_name=target)
        elif isinstance(consoleholder, Console) and target is not None:
            self.layout.refresh(consoleholder, layout_name=target)
    
    def laidout(self, consoleholder: Console, output: bool = True) -> Layout | None:
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
        """Display Data: Wrapper for Any Display."""
        # consoleholder.set_table(consoleholder, dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=consoleholder,
                              consoletable=consoletable,
                              headerview=Headers.HeadersChoices,
                              title=title)
    
    @staticmethod
    def display_views(dataframe: pd.DataFrame,
                      consoleholder,  # noqa: ANN001
                      view: ViewType = "table",
                      title: str = "PyCriteria") -> None:
        """Display Data: Wrapper for Any Display."""
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
                      headerview: list[str] | str,
                      title: str = "PyCriteria") -> None | NoReturn:
        """Displays the data in a table."""
        if isinstance(headerview, list):
            headers: list = headerview
        else:
            headers: list = [headerview]
        
        consoletable.title = title
        
        filteredcolumns: pd.DataFrame = \
            dataframe.loc[:, dataframe.columns.isin(values=headers)]
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
        for _index, row in filteredcolumns.iterrows():
            consoletable.add_row(*[str(row[column])
                                   for column in headers])
        consoleholder.print(consoletable)
    
    @staticmethod
    def display_search(output: tuple,
                       consoleholder: Console,
                       consoletable: Table,
                       title: str = "PyCriteria") -> None | NoReturn:
        """Displays the searches accoridng to an output's result-set.
        
        A ResultSet is a type of tuple that varies in length and component types.
        A resultset is used to carry the parameters of a searches along
            with the results of that searches from
             a) the command's stdin
             b) to the cli's stdout or stderr.
        The ResultSet is a tuple of the following types:
            i) SearchColumnResultType: tuple[str, str, pd.DataFrame]
                i.e. header, query, dataframe
            ii) ItemSelectType: tuple[str, str, pd.DataFrame]
        Parameters:
        --------------------
        :param output: tuple: The output of the searches
        :param consoleholder: Console: The console to print to
        :param consoletable: Table: The table to print to
        :param title: str: The title of the table
        """
        
        headers, query, dataframe = output
        Display.display_frame(dataframe=dataframe,
                              consoleholder=consoleholder,
                              consoletable=consoletable,
                              headerview=Headers.HeadersChoices,
                              title=title)
        echo(message=(f"You searched for: Query: {query}"
                      + f"Against this Header: {headers}")),
    
    @staticmethod
    def display_selection(output: tuple,
                          consoleholder,  # noqa: ANN001
                          consoletable: Table,
                          title: str = "PyCriteria") -> None | NoReturn:  # noqa: ANN001
        """Displays the selection accoridng to an output's result-set.
        
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
        # Uses the return Data Structure types, i.e, of outputto determine the Display set
        
        pass


class Record:
    """A Record is a row of data to be displayed in console, by views"""
    
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
    rowid: str
    recordid: str
    todo: str
    flag: str
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
            self.rowid: str = single.RowID
            self.recordid: int = single.Position
            self.type: str = single.Tier
            self.prefix: str = single.TierPrefix
            self.grade: str = single.Performance
            self.status: str = single.DoD
            self.todo: str = single.Progress
            self.flag: str = single.ToDoFlag
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
            else:
                click.echo(message="The DataFrame must be a single row.",
                           err=True)
                return False
        
        if isinstance(single, pd.Series) and single.empty is False:
            return True
        else:
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
        
        def display(table: Table, data: pd.Series | None = None) -> Table | None:
            """Populates the card from instance or a from external source"""
            if data is not None and isinstance(data, pd.Series):
                for label, value in data.items():
                    table.add_row(str(label), str(value))
                return table
            elif self.series is not None and isinstance(self.series, pd.Series):
                for label, value in self.series.items():
                    table.add_row(str(label), str(value))
                return table
        
        card: Table = display(table=config(), data=source)
        
        if sendtolayout is True:
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
              outline: rich.box = box.SIMPLE, sendtolayout: bool = False) \
            -> Panel | None:  # noqa
        """Frames the renderable as a panel."""
        
        def config(dimensions: tuple[int, int], styler: str, safe: bool = False) -> Panel:
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
        
        # Switches the flow: returns | print| to stdout
        panel: Panel = config(dimensions=card,
                              styler=styld.panel(grey=23),
                              safe=True)
        
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
               subgrid: bool = False) -> Table | None:
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
            identtable.add_
            rowid_label: str = 'Record Name:  '
            rowid_value: str = f'{self.rowid} - {self.series.name}'
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
        
        return Record.switch(mainpane,
                             printer=consolehead,
                             switch=sendtolayout)
    
    def editable(self, consoleedit: Console | None = None,
                 expand: bool = False,
                 sendtolayout: bool = False,
                 title: str = 'Current Data') -> Table | None:
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
            if self.notes is None:
                notes_value = 'Add a note'
            else:
                notes_value = f'{self.notes} \n'
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
        return Record.switch(currentdatapane,
                             printer=consoleedit,
                             switch=sendtolayout)
    
    def footer(self, consolefoot: Console,
               sendtolayout: bool = False,
               expand: bool = True,
               valign: str = 'top') -> Table | None:
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
            meta.title = 'Footer: Project Data'
            meta.add_section()
            tier_label: str = 'Tier: '
            link_label: str = 'Linked: '
            tier_value = f'{self.type}.{self.prefix}.{self.reference}'
            meta.add_row(f'{tier_label} {tier_value})', f'{link_label} {self.linked}', '')
            meta.add_section()
            now: datetime = datetime.datetime.now()
            dt_string: str = now.strftime("%d/%m/%Y %H:%M")  # %S
            meta.add_row(f'Viewed: {dt_string}', '/', '/')
            return meta
        
        footer: Table = metapane(table=config(fit=expand, vertical=valign))  # noqa
        return Record.switch(footer,
                             printer=consolefoot,
                             switch=sendtolayout)
    
    @staticmethod
    def comparegrid(container: Table,
                    left: Table,
                    right: Table,
                    fit: bool = False,
                    sendtolayout: bool = False) -> Table | None:
        """ Display the header grid table"""
        main: Table = container
        main.grid(expand=fit)
        main.add_row(left, right)
        
        return Record.switch(main, printer=container, switch=sendtolayout)
    
    @staticmethod
    def switch(renderable, printer: Console | Table, switch: bool = False) -> Table | None:
        """Switches between console print or redirecting to a layout"""
        if switch is True:
            return renderable
        else:
            printer.print(renderable)
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
    lasteditmode: str = ''
    
    def __init__(self, currentrecord: Record = None,
                 sourceframe: pd.DataFrame | None = None) -> None:
        """The Editor is a console utility for editing records."""
        if currentrecord is not None:
            self.record = currentrecord
        else:
            click.echo(message="No editing possible", err=True)
        
        self.oldresultseries = self.record.series
        self.oldresultframe = self.record.sourceframe
        self.newresultseries = None
        self.newresultframe = None
        self.sourceframe = sourceframe
        self.ismodified = False
        self.lastmodified = None
        self.modified = None
        self.lasteditmode: str = ''
    
    def edit(self, consoleedit: Console) -> None:
        """The Editor is a console utility for editing records."""
        pass
    
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
        
        # Perplexity AI was used to build out this function, based on below.
        # https://www.perplexity.ai/search/a8d503cb-8aec-489a-8cf5-7f3e5b573cb7?s=c
        EDITMODE = 'insert'  # noqa
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
            #    using click.confirm() to ask if the user wants commit to the remote
            #    commit function is to be defined, as it is destructive/overwrites
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
            
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode, before use
            if self._isempty(editingseries, ColumnSchema.Notes):
                if click.confirm(f"Please confirm to add/{EDITMODE} your note"):
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes,
                                     editmode=EDITMODE,
                                     location=location)
                elif click.confirm(
                        text="Do you want to modify your new note? \n"
                             + f"Your latest note is {notes}. \n"):
                    newnotes = click.prompt("Please enter changes: ")
                    if isinstance(newnotes, str):
                        self.modifynotes(editingseries,
                                         record=self.record,
                                         notes=str(newnotes),
                                         editmode=EDITMODE,
                                         location=location,
                                         debug=debug)
                    else:
                        click.echo(message="Please enter a string",
                                   err=True)
                else:
                    click.echo("Exiting editing mode")
                    return None
            elif click.confirm(
                    text="You are adding a note to an exitsing note. \n"
                         + "Do you want to continue?"):
                self.modifynotes(editingseries,
                                 record=self.record,
                                 notes=notes,
                                 editmode='append',
                                 location=location,
                                 debug=debug)
                click.echo("Note appended, not created")
            else:
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
        EDITMODE = 'append'  # noqa
        # See addingnotes() for the PerplexityAI use case as co-Pilot.
        if notes is not None and isinstance(notes, str):
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode, before use
            if self._hascontent(editingseries, ColumnSchema.Notes):
                if click.confirm(f"Please confirm to {EDITMODE} your note"):
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes,
                                     editmode=EDITMODE,
                                     location=location,
                                     debug=debug)
                elif click.confirm(
                        text="Do you want to modify your new note? \n"
                             + f"Your latest note is {notes}. \n"):
                    newnotes = click.prompt("Please enter changes: ")
                    if isinstance(newnotes, str):
                        self.modifynotes(editingseries,
                                         record=self.record,
                                         notes=str(newnotes),
                                         editmode=EDITMODE,
                                         location=location,
                                         debug=debug)
                    else:
                        click.echo(message=f"No Edit Made for  Update {EDITMODE}",
                                   err=True)
                else:
                    click.echo(f"Exiting editing mode: Update {EDITMODE}")
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
        EDITMODE = 'clear'  # noqa
        if notes is not None and isinstance(notes, str):
            # Backup User's input into current record
            # Create a transitory single data series from record
            editingseries = self.record.series.copy()
            self.lasteditmode = ''  # Clears out the last edit mode, before use
            # Check if the series has notes
            if self._hascontent(editingseries, ColumnSchema.Notes):
                # Confirm if the user wants to proceed.
                # It is a CLI and not a GUI, and thus keywboard driven.
                if click.confirm("Please confirm to clear your note?"):
                    # Call the hub (CUD) function with editmode='clear' flag.
                    self.modifynotes(editingseries,
                                     record=self.record,
                                     notes=notes,
                                     editmode=EDITMODE,
                                     location=location,
                                     debug=debug)
                else:
                    click.echo(f"Exiting editing mode: Delete: {EDITMODE}")
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
        if editmode == "insert":
            # Insert the notes - add / overwrite / create
            editingseries[ColumnSchema.Notes] = notes
        elif editmode == "append":
            # Append the notes - add / overwrite / create
            editingseries[ColumnSchema.Notes] = \
                self.appendnotes(series=editingseries,
                                 column=ColumnSchema.Notes,
                                 value=notes)
        elif editmode == "clear":
            editingseries[ColumnSchema.Notes] = \
                self.deletenotes(series=editingseries,
                                 column=ColumnSchema.Notes,
                                 value=notes)
        
        updatedframe = self.insert(
                record=record,
                value=editingseries[ColumnSchema.Notes],
                column=ColumnSchema.Notes,
                index=location, debug=debug)
        self.newresultseries = editingseries
        self.newresultframe = updatedframe
        
        if debug is True:
            if isinstance(self.newresultseries, pd.Series) and \
                    self.newresultseries.empty is False:
                click.echo("Modified Series")
            
            if isinstance(self.newresultframe, pd.DataFrame) and \
                    self.newresultframe.empty is False:
                click.echo("Modified DataFrame")
        
        if self.newresultframe.empty is False:
            self.ismodified = True
            self.lastmodified = self.timestamp()
            click.echo("Modified Frame at " + self.lastmodified)
            self.modified = Record(
                    series=editingseries,
                    source=self.newresultframe)
            if debug is True:
                rich.inspect(self.modified)
            self.lasteditmode = editmode  # sets the last edit mode for the record
        
        if click.confirm("Do you want to save the updated DataFrame?"):
            # self.sourceframe = updatedframe
            # TODO: Implement the commit function to save the updated DataFrame remotely
            # commit()
            click.echo("TODO: DataFrame saved")
        else:
            click.echo("Exit editing mode")
            return None
    
    # Editor's Notes Actions: ColumnSchema.Notes
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
                    value: str,
                    nodestroy: bool = False) -> str:
        """Deletes notes from the existing notes if flag: nodestroy/destroy
        
        Parameters
        ----------
        :param series: pandas.Series: The series to be edited.
        :param value: str: The notes to be added to the record.
        :param column: str: The name of the column to be edited.
        :param nodestroy: bool: The flag to delete or not to delete.
               A mechanism to handle destructive actions and safely delete.
               Potentially flagged by user from a CLI command option.
        :return: str
        """
        _cleared = ''
        if nodestroy and series[column] is _cleared:
            click.echo(message="No notes to delete")
            return series[column]
        elif nodestroy and series[column] is not _cleared:
            click.echo(message="Exitsing notes present. No change")
            return series[column]
        elif not nodestroy and series[column] is not _cleared:
            click.echo(message="Cleared")
            cleared = series[column] = ''
            return cleared
        elif not nodestroy and series[column] is _cleared:
            click.echo(message="No notes to delete")
            return series[column]
        elif value not in series[column]:
            return series[column]
        else:
            click.echo(message="Replaced")
            return series[column].replace(value, '')
    
    # Editor's Record Actions
    def save(self, savedfranme: pd.DataFrame) -> None:
        """ Saves the dataframe and commits it to the remote source
        
        The Editor is a console utility for editing records."""
        # Prompt the user to save the updated DataFrame
        if click.confirm("Do you want to save the updated DataFrame?"):
            self.sourceframe = savedfranme
            # TODO: Implement the commit function to save the updated DataFrame remotely
            # commit()
        else:
            click.echo("Exit editing mode")
            return None
    
    @staticmethod
    def insert(record: Record, value: str,
               column: str | None = None,
               index: int | None = None,
               debug: bool = False) -> pd.DataFrame:
        """ Inserts by column, using the Record.
        name or index for rows, if either is known or given.
        
        The Editor is a console utility for editing records."""
        # https://www.perplexity.ai/search/1ae6c535-37ae-4721-bbc8-38aa37cae119?s=c
        # Use for debuging IndexError: iloc cannot enlarge its target object
        # Not used for developing the pattern below.
        updatedframe = record.sourceframe.copy()
        if index is None and column is not None:
            updatedframe.at[record.series.name, column] = value
        elif isinstance(index, int) and column is not None:
            if isinstance(record.series.name, int):
                if index - 1 == record.series.name:
                    updatedframe.at[index, column] = value
                    if debug:
                        click.echo(f"Note Updated at row: {index} "
                                   f"by zero index for {record.series.name}")
                        rich.inspect(updatedframe.at[index, column])
                elif index != record.series.name:
                    # Debuging
                    updatedframe.at[index, column] = value
                    if debug:
                        click.echo(f"Note Updated at row: by {index} only")
                        rich.inspect(updatedframe.at[index, column])
                if not debug:
                    click.echo(f"Note Updated at row: {index} "
                               f"for {record.series.name}")
            else:
                click.echo(message="Series.name is not an int", err=True)
                updatedframe.at[index, column] = value
        else:
            click.echo("Nothing inserted")
        
        # Note: If no changes were made, then a copy of original is returned
        return updatedframe
    
    @staticmethod
    def clear(record: Record, column: str | None = None,
              index: int | None = None,
              cleared: bool = True) -> pd.DataFrame:
        """ Clears by column, using the Record."""
        _empty = ''
        _noned = None
        if cleared:
            value = _empty
        else:
            value = _noned
        
        updatedframe = record.sourceframe.copy()
        if click.confirm(text="Do you want to clear the notes?. \n"
                              "Importantly clears all notes"):
            if index is None and column is not None:
                updatedframe.loc[record.series.name, column] = value
            elif isinstance(index, int) and column is not None:
                if isinstance(record.series.name, int):
                    if index == record.series.name:
                        updatedframe.iloc[index, column] = value
                    elif index != record.series.name:
                        updatedframe.iloc[index - 1, column] = value
                    else:
                        updatedframe.iloc[index, column] = value
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
        if series[column] == '' or \
                series[column] is None:
            return True
        
        return False
    
    @staticmethod
    def _hascontent(series: pd.Series, column: str) -> bool:
        if series[column] != '' or \
                series[column] is not None:
            return True
        
        return False
    
    @staticmethod
    def timestamp(tostring: bool = True,
                  stamp: Literal['date', 'time', 'full', 'precise'] = 'full') -> str:
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
# Globals: connector, configuration, tablesettings, console
# Class: Controller, ColumnSchema, Headers, DataController,  Editor, WebConsole,
# Class: Inner, Display, Record, Editor
# Timestamp: 2022-05-21T16:30, copywrite (c) 2022-2025, see {} for more details.
