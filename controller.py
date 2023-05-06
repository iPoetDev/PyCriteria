#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Terminal/Console App."""
import typing
import warnings

import gspread  # type: ignore

from rich import pretty as rpretty  # type: ignore; type: ignore
from rich import print as rprint  # type: ignore; type: ignore
from rich.console import Console  # type: ignore; type: ignore; type: ignore
from rich.console import ConsoleDimensions  # type: ignore; type: ignore; type: ignore
from rich.console import ConsoleOptions  # type: ignore; type: ignore; type: ignore
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

class Controller:
    """Controller for the work/effort of loading the data, fetching it, tranforming it."""
    
    @staticmethod
    def load_criteria() -> list[str]:
        """Loads the criteria from the sheet."""
        # 2.1: Connect to the sheet
        # -> Move to Instance once the data is
        # loaded is tested and working on heroku
        creds: gspread.Client = connector.connect_to_remote(
                configuration.CRED_FILE)
        # rich.print(creds)
        # 2.2: Read the data from the sheet
        # -> Move to Instance once the data is loaded, working on heroku
        spread: gspread.Spreadsheet = \
            connector.get_source(creds,
                                 configuration.SHEET_NAME)
        # rich.print(spread)
        # 2.3: Return the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on
        # heroku
        tabs: gspread.Worksheet = \
            connector.open_sheet(spread, configuration.TAB_NAME)
        # rich.print(tabs)
        # 2.4 Fetch the Data and a.1 Return/Print it,
        # 2.4 a2 Return it and load it into a dataclass
        # 2.4 b1: transform it into a datamodel reference
        return connector.fetch_data(tabs)
    
    @staticmethod
    def load_wsheet() -> gspread.Worksheet:
        """Loads a worksheet.
        :return: gspread.Worksheet: The current worksheet to extract the data.
        """
        # 2.1: Connect to the sheet
        # -> Move to Instance once the data is loaded is tested and working on heroku
        creds: gspread.Client = \
            connector.connect_to_remote(configuration.CRED_FILE)
        # rich.print(creds)
        # 2.2: Read the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on heroku
        spread: gspread.Spreadsheet = \
            connector.get_source(creds,
                                 configuration.SHEET_NAME)
        # rich.print(spread)
        # 2.3: Return the data from the sheet
        # -> Move to Instance once the data is loaded is tested and working on
        # heroku
        return connector.open_sheet(spread, configuration.TAB_NAME)
    
    @staticmethod
    def load_data() -> list[str]:
        """Loads the data."""
        # 2.1: Connect to the sheet
        # 2.2: Read the data from the sheet
        # 2.3: Return the data from the sheet
        wsheet: gspread.Worksheet = Controller.load_wsheet()
        return transformer.get_data(wsheet, "H2:010")


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
    Display.display_data(data)
    Display.display_table(data,
                          mainconsole,
                          maintable)
    # 0.3: Upload the data


if __name__ == '__main__':
    warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    main()
