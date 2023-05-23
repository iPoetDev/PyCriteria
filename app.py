#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, ANN001, D415, RET505, I001,
"""Module: PyCriteria Command/REPL Terminal app.

Usage: Commands and REPL
-------------------------
- Multi-line level nested commands structure.
    - Run - Core/BASE command AND ANCHORED command.
        - Load              - TOP INTENT, nested under Run
            - Views         - SUB COMMAND, nested under Load
                              Switches between sub-views of the data
            - ToDo          - SUB COMMAND, nested under Load
                              Switches between sub-views of the todo tasks
        - Find              - TOP INTENT, nested under Run
            - Locate        - SUB COMMAND, nested under Find
                              Locate a record by ID (row)
                              Future by column value, or row search term
        - Edit              - TOP INTENT, nested under Run
                              Core activity/action of the app for user
            - AddNote       - SUB COMMAND, nested under Edit
            - UpdateNote    - SUB COMMAND, nested under Edit
            - DeleteNote    - SUB COMMAND, nested under Edit
            - TooggleTodo   - SUB COMMAND, nested under Edit
        - Exit - TOP INTENT, nested under Run

If Time, merge the Note commands into one command,
   and use a flag/choice to switch action

Linting:
-------------------------
- pylint: disable=trailing-whitespace
- ruff: noqa:
      I001	    unsorted-imports
                Import block is un-sorted or un-formatted
      F841:     unused-variable
                Local variable {name} is assigned to but never used
      ANN101	missing-type-self
                Missing type annotation for {name} in method
      ANN101:   missing-type-self
                Missing type annotation for {name} in method
      RET505	superfluous-else-return
                Unnecessary {branch} after return statement
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
:imports: typing.Literal

3rd Paty Imports
:imports: rich
:imports: rich.panel
:imports: rich.table
:imports: click
:imports: click_repl
:imports: pandas

Local Imports
:imports: commands
:imports: controller
:imports: sidecar


Classes
-------------------------
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
:var: Commands: Commands.py - Commands values
:var: Actions: Controller.py - Controller / Hub logic
:var: AppValues: sidecar.py - AppValues
:var: DataControl: Controller.py - DataController for DataModel, shared, alias
:var: Columns: Controller.py - DataModel schema
:var: Head: Controller.py - Header Views for Views filters
:var: Display: Controller.py - Duplicate effort with CriteriaApp, and Record
:var: Webconsole: Controller.py - WebConsole for WEB versions of the app.
:var: utils: sidecar.py - ProgramUtils, miscellaneous functions
:var: view: app.py - Simialr to Head, but for the app.py commands choices.
                    Possible Duplicate
:var: window: app.py - Window class for Terminal Layouts, Panels, Cards.
:var: App: app.py - Key DataConrtooler/Controller.py
:var: Guard: app.py - Validation of inputs, and guards conditions/tests.

"""
# 1. Std Lib
from typing import Literal

import click  # type: ignore
# 2. 3rd Party
import rich
import rich.panel
from click_repl import register_repl  # type: ignore
from pandas import pandas as pd, DataFrame, Series  # type: ignore
from rich import pretty, print as rprint  # type: ignore
from rich.panel import Panel  # type: ignore
from rich.table import Table  # type: ignore

# 3. Local: Note the controller * intentionally imports all from the module
from commands import Commands
from controller import (Controller, DataController, ColumnSchema, Headers,
                        Display, WebConsole, configuration, gspread,
                        Record, Inner, Editor, )
from sidecar import AppValues, ProgramUtils

# Note: Move third-party import `gspread` into a type-checking block

# Global Modules/Objects
# 1.1 Commands.py
Commands: Commands = Commands()
# 1.2 Controller.py
Actions: Controller = Controller()
AppValues: AppValues = AppValues()
DataControl: DataController = DataController(Actions.load_wsheet())
Columns: ColumnSchema = ColumnSchema()
Head: Headers = Headers(labels=Columns)
Display: Display = Display()
Webconsole: WebConsole = WebConsole(configuration.Console.WIDTH,
                                    configuration.Console.HEIGHT)
Webconsole.terminal = Inner()
# 1.3 Sidecar.py
utils: ProgramUtils = ProgramUtils()
pretty.install()


class View:
    """View.
    
    :property: View.Load
    :property: View.Todo
    """
    
    Load: list[str] = ["Load", "Begins", "Project", "Criteria",
                       "ToDo", "Reference", "Refresh"]
    Todo: list[str] = ["ToDo", "All", "Simple", "Done", "Grade", "Review"]
    
    def __init__(self):
        """Initialize."""
        pass


view: View = View()


class Window:
    """Window: Arrange Terminal Layouts, Panels, Cards.
    
    Methods:
    --------------------------------------------
    :method: Window.sendto
    :method: Window.showrecord
    :method: Window.printpane
    :method: Window.printpanels
    :method: Window.showedited
    :method: Window.showmodified
    
    """
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def sendto(value, switch: bool) -> Record | None:
        """Switch Record for dual-return statements.
        
        :param value: Record - Individual Record to display
        :param switch: bool - Switch to send to the Editor or not.
        """
        if switch:
            return value
        else:
            return None
    
    @staticmethod
    def showrecord(data: pd.Series | pd.DataFrame,
                   sendtoeditor: bool = False,
                   debug: bool = False) -> Record | None:
        """Display Record.
        
        :param data: pd.Series | pd.DataFrame - Individual Record to display
        :param sendtoeditor: bool - Switch to send to the Editor or not.
        :param debug: bool - Switch to debug mode or not.
        :return: Record | None - Individual Record to display or None
        """
        if data.empty is False:
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop.
            individual = Record(series=data, source=data)
            
            if debug:
                rprint("Debug Mode: Show Record")
                rich.inspect(individual)
            
            if individual.card(consolecard=Webconsole.console) is not None:
                window.printpanels(record=individual)
            else:
                click.echo("Displaying Simple Card")
                individual.card(consolecard=Webconsole.console)
            
            return Window.sendto(individual, sendtoeditor)
    
    @staticmethod
    def printpane(panel: str, printer: rich.Console) -> None:
        """Print Pane.
        
        :param panel: str - Panel to print
        :param printer: rich.Console - Console to print to
        :return: None
        """
        if panel == 'bannerfull':
            pane = Panel(
                    "======================="
                    "================="
                    "Displaying Updated Card"
                    "========================"
                    "=================")
            printer.print(pane)
    
    @staticmethod
    def printpanels(record) -> None:
        """Print Panels.
        
        :param record: Record - Individual Record to display
        :return: None
        """
        if record is not None:
            window.printpane(panel='bannerfull',
                             printer=Webconsole.console)
            # Switch to Rich/Terminal display
            header = record.header(
                    consolehead=Webconsole.console,
                    sendtolayout=True,
                    gridfit=True)
            current = record.editable(
                    consoleedit=Webconsole.console,
                    sendtolayout=True)
            footer = record.footer(
                    consolefoot=Webconsole.console, sendtolayout=True)
            # Print: the Panel as a Group of Renderables
            record.panel(consolepane=Webconsole.console,
                         renderable=header,
                         fits=True,
                         sendtolayout=False)
            record.panel(consolepane=Webconsole.console,
                         renderable=current,
                         sendtolayout=False)
            record.panel(consolepane=Webconsole.console,
                         renderable=footer,
                         fits=True,
                         sendtolayout=False)
    
    @staticmethod
    def showedited(editeddata: pd.Series | pd.DataFrame,
                   sendtoeditor: bool = False,
                   debug: bool = False) -> Record | None:
        """Display Edited Record.
        
        :param editeddata: pd.Series | pd.DataFrame
                - Individual Record to display
        :param sendtoeditor: bool - Switch to send to the Editor or not.
        :param debug: bool - Switch to debug mode or not.
        :return: Record | None - Individual Record to display or None
        """
        if debug:
            rprint(editeddata)
        elif editeddata.empty is False:
            individual = Record(source=editeddata)
            if individual.card(consolecard=Webconsole.console) is not None:
                window.printpanels(record=individual)
            else:
                individual.card(consolecard=Webconsole.console)
            
            if sendtoeditor:
                return individual
            else:
                return None
    
    @staticmethod
    def showmodified(editeddata: pd.Series,
                     editor: Editor,
                     commandtype: Literal['insert', 'append', 'clear'],
                     dataview: Literal['show', 'compare'] = 'show',
                     debug=False) -> None:
        """Display Modified Record.
        
        :param editeddata: pd.Series - Individual Record to display
        :param editor: Editor - Editor to use
        :param commandtype: Literal['insert', 'append', 'clear']
                - Command type to use
        :param dataview: Literal['show', 'compare'] - Data view to use
        :param debug: bool - Switch to debug mode or not.
        :return: None
        """
        # Display single records
        if Record.checksingle(editeddata):
            if editor.ismodified and editor.lasteditmode == commandtype:
                if debug:
                    click.echo(message="==========Displaying: "
                                       "Changes=========\n")
                # 1. Display the Edited record
                if dataview == 'show':
                    window.showedited(editeddata=editeddata, debug=debug)
                elif dataview == 'compare':
                    window.comparedata(editeddata=editeddata,
                                       editor=editor,
                                       debug=False)  # noqa
                #  [DEBUG]
                if debug:
                    click.echo(message="=== [DEBUG] Saving: "
                                       "changes made [DEBUG]==\n")
                    click.echo(f" Modified: {editor.lastmodified} ")
            else:
                click.echo(message="No changes made. See above.")
            #
            if debug:
                click.echo(message=f"=====================================")
            # Switch confirmation on a command's type
            if commandtype == 'insert':
                click.echo(message=f"🆕 A new note is now added 🆕 at:"
                                   + editor.lastmodified)
            elif commandtype == 'append':
                click.echo(message="A note is updated at:"
                                   + editor.lastmodified)
            elif commandtype == 'clear':
                click.echo(message="A record's is now deleted at:"
                                   + editor.lastmodified)
            click.echo(message=f"Exiting: Command completed")
            return None
        else:
            click.echo(message="No changes made. Bulk edits not supported.")
            return None
    
    @staticmethod
    def comparedata(editeddata: pd.Series,
                    editor: Editor,
                    debug=False) -> None:
        """Compare Old and New side by side.
        
        :param editeddata: pd.Series - Individual Record to display
        :param editor: Editor - Editor to use
        :param debug: bool - Switch to debug mode or not.
        :return: None
        """
        shown: bool = True
        if debug:
            rprint(editeddata)
            rich.inspect(editeddata)
        elif editeddata.empty is False and editor.ismodified:
            oldrecord: Record = editor.record
            newrecord: Record = Record(series=editor.newresultseries)
            # 1. Display the Edited recor
            left = oldrecord.editable(
                    consoleedit=Webconsole.console,
                    sendtolayout=shown,
                    title="Original Record")
            right = newrecord.editable(
                    consoleedit=Webconsole.console,
                    sendtolayout=shown,
                    title="Updated Record")
            # Compare Old with New, else just show the new
            if left is not None or right is not None:
                window.printpane(panel="bannerfull",
                                 printer=Webconsole.console)
                header = newrecord.header(
                        consolehead=Webconsole.console,
                        sendtolayout=shown,
                        gridfit=True)
                sidebyside = newrecord.comparegrid(
                        container=Webconsole.table,
                        left=left,
                        right=right,
                        sendtolayout=shown,
                        fit=True)
                footer = newrecord.footer(
                        consolefoot=Webconsole.console,
                        expand=False)
                
                newrecord.panel(consolepane=Webconsole.console,
                                renderable=header,
                                fits=True,
                                sendtolayout=False)  # noqa
                newrecord.panel(consolepane=Webconsole.console,
                                renderable=sidebyside,
                                fits=True,
                                sendtolayout=False)  # noqa
                newrecord.panel(consolepane=Webconsole.console,
                                renderable=footer,
                                fits=True,
                                sendtolayout=False)  # noqa
            else:
                window.showedited(editeddata=editeddata, debug=debug)


window: Window = Window()


class CriteriaApp:
    """PyCriteria Terminal App.
    
    :property: values: AppValues - App Values
    
    Methods:
    :method: get_data - get the remote data, alias for DataController
    :method: display_data -
    :method: update_appdata -
    :method: display_view -
    :method: display_todo -
    :method: query_data -
    :method: search_data -
    :method: search_rows -
    :method: rows -
    :method: index -
    :method: value
    :method: get_results
    """
    
    values: AppValues
    
    def __init__(self, values: AppValues):
        """Initialize."""
        self.values = values
    
    @staticmethod
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs.
        
        :param context: click.Context - Click context
        :return: None
        """
        root: str = "BASE: Run"
        click.echo(message="Navigation: CLI: > Run > ... "
                           "[Intent] > [Action]\n")
        if context.info_name is not None:
            crumb: str = context.info_name
        else:
            crumb: str = root
        
        text: str = ('Navigation: CLI: > Run > ... > Load'
                     + f'> {crumb.title()}*\n *: '
                     + f'You are here: {crumb.title()}\n'
                     + 'To go up one or two level, enter, each time:  ..  \n'
                     + 'To Exit: ctrl + d  \n')
        click.echo(
                message=text)
    
    @staticmethod
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context.
        
        :return: pd.DataFrame - Dataframe
        """
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    @staticmethod
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe.
        
        :param dataframe: pd.DataFrame - Dataframe to display
        :return: None
        """
        WebConsole.table = Webconsole.set_datatable(dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=Webconsole.console,
                              consoletable=Webconsole.table,
                              headerview=Head.OverviewViews)
    
    @staticmethod
    def update_appdata(context, dataframe: pd.DataFrame) -> None:
        """Update the app data.
        
        :param context: click.Context - Click context
        :param dataframe: pd.DataFrame - Dataframe to update
        """
        context.obj = dataframe
        DataControl.dataframe = dataframe
    
    @staticmethod
    def display_view(dataframe: pd.DataFrame,
                     viewer: list[str] = None,
                     label: str = 'Overview') -> None:
        """Display the dataframe.
        
        :param dataframe: pd.DataFrame - Dataframe to display
        :param viewer: list[str] - List of views to display
        :param label: str - Label to display
        :return: None
        """
        if view is None:
            headers: list[str] = Head.OverviewViews
        else:
            headers: list[str] = viewer
        
        Webconsole.table = Webconsole.configure_table(headers=headers)
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=headers,
                                 viewfilter=label)
        click.echo(message='Your data is refreshed/rehydrated')
    
    @staticmethod
    def display_todo(dataframe: pd.DataFrame, viewoption: str = 'All') -> None:
        """Display the dataframe by view option.
        
        :param dataframe: pd.DataFrame - Dataframe to display
        :param viewoption: str - View option
        :return: None
        """
        
        def select_view(viewss: str) -> list[str]:
            """Select the view."""
            if viewss.lower() == 'All'.lower():
                headers: list[str] = Head.ToDoAllView
            elif viewss.lower() == 'Simple'.lower():
                headers: list[str] = Head.ToDoDoDView
            elif viewss.lower() == 'Done'.lower():
                headers: list[str] = Head.ToDoGradeView
            elif viewss.lower() == 'Grade'.lower():
                headers: list[str] = Head.ToDoReviewView
            elif viewss.lower() == 'Review'.lower():
                headers: list[str] = Head.ToDoGradeView
            else:
                headers: list[str] = Head.ProjectView
            return headers
        
        Webconsole.table = Webconsole.configure_table(
                headers=select_view(viewoption))
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=select_view(viewoption),
                                 viewfilter='ToDo')
    
    @staticmethod
    def query_data(dataframe: pd.DataFrame,
                   querystring: str,
                   case: bool = False) -> pd.DataFrame:
        """Query the dataframe.
        
        :param dataframe: pd.DataFrame - Dataframe to query
        :param querystring: str - Query string
        :param case: bool - Case sensitive
        :return: pd.DataFrame - Query result
        """
        subsetframe: pd.DataFrame = \
            dataframe.apply(lambda x: x.astype(str).str.contains(querystring,
                                                                 case=case))
        return subsetframe
    
    @staticmethod
    def search_data(frame: pd.DataFrame,
                    label: str,
                    searchstr: str,  # noqa
                    case: bool = False, echos: bool = False) \
            -> pd.DataFrame:  # noqa
        """Search the dataframe.
        
        :param frame: pd.DataFrame - Dataframe to search
        :param label: str - Label to search
        :param searchstr: str - Search string
        :param case: bool - Case sensitive
        :param echos: bool - Echo the result
        :return: pd.DataFrame - Search result
        """
        searchresult: pd.DataFrame = \
            frame[frame[label].astype(str).str.contains(searchstr,
                                                        case=case)]
        
        if echos:
            click.echo(
                    message=f'The rows with "{searches}" in column\'s'
                            f' "{label}" are:\n {searchresult}')
        
        return searchresult
    
    @staticmethod
    def search_rows(frame: pd.DataFrame,
                    searchterm: str,
                    exact: bool = False) \
            -> pd.DataFrame | None:
        """Search across all columns for the searches team
        
        :param frame: pd.DataFrame - Dataframe to search
        :param searchterm: str - Search term
        :param exact: bool - Exact match
        :return: pd.DataFrame - Search result
    
        """
        if searchterm is None or isinstance(searchterm, str):
            return None
        # Search across all columns for the searches text/str value
        mask = frame.apply(lambda column: column.astype(str).
                           str.contains(searchterm))
        #
        if exact:
            return frame.loc[mask.all(axis=1)]
        
        return frame.loc[mask.any(axis=1)]
    
    @staticmethod
    def rows(frame: pd.DataFrame,
             index: int = None,
             searchterm: str = None,
             strict: bool = False,
             zero: bool = True, debug: bool = False) \
            -> pd.DataFrame | pd.Series | None:
        """Get the rows from the dataframe.
        
        Parameters
        ----------
        frame: pd.DataFrame: Data to searches by rows
            The dataframe to searches.
        index: int: optional
            The index to searches for, by default None
        searchterm: str: optional
            The searches term to searches for, by default None
        strict: bool: optional
            Whether to searches for
            - a non-exact (any) match, by default False, so any can match
            - exact (all), by True, so all muct match
        zero: bool: optional
            Whether to searches for a zero indexed dataset, by default True
        debug: bool: optional debug flag, by default False
        
        return pd.DataFrame | None: - Expect a result or None
        """
        result: pd.DataFrame | pd.Series | None
        if index:
            result = App.index(frame=frame, index=index, zero=zero)  # noqa
        elif searchterm:
            # Search across all columns for the position value
            result = App.search_rows(frame=frame,
                                     searchterm=searchterm,
                                     exact=strict)
            if result.empty is not False:
                if debug:
                    click.echo(f"Found: {result}")
            else:
                click.echo(f"Could not find {search}")
        else:
            click.echo("Please provide either "
                       "an index or searches term")
            return None
        
        return result
    
    @staticmethod
    def index(frame: pd.DataFrame,
              index: int = None,
              zero: bool = True, debug: bool = False) \
            -> pd.DataFrame | pd.Series | None:
        """Get the index from the dataframe.
        
        :param frame: pd.DataFrame - Dataframe to search
        :param index: int - Index to search
        :param zero: bool - Zero index
        :param debug: bool - Debug flag
        :return: pd.DataFrame - Index result
        """
        if zero and index is not None:
            result = frame.iloc[index - 1] \
                if index >= 0 else frame.iloc[index]
            if debug:
                click.echo(f"Found: {result} "
                           f"for zero index {index - 1}")
            return result
        elif not zero and index is not None:
            result = frame.iloc[index] \
                if index > 0 else frame.iloc[index]
            if debug:
                click.echo(f"Found: {result} "
                           f"for standard index {index}")
            return result
        else:
            click.echo(f"Could not find index {index}")
            return None
    
    @staticmethod
    def value(frame: pd.DataFrame | pd.Series,
              row: int = None,
              column: int | str = None,
              direct: bool = False) -> str | None:
        """Get the value from the dataframe.
        
        :param frame: pd.DataFrame - Dataframe to search
        :param row: int - Row to search
        :param column: int - Column to search
        :param direct: bool - Direct search
        :return: str - Value result
        """
        if row is None or column is None:
            click.echo(message="Plese try again: "
                               f"One of {row}, {column} is blank")
            return None
        
        try:
            if not direct and isinstance(row, int) and isinstance(column, int):
                if row >= 0 or column >= 0:
                    result: str = frame.iat[row, column]
                    return result
                else:
                    raise IndexError
            elif direct and isinstance(row, int) and isinstance(column, int):
                if row >= 0 or column >= 0:
                    result: str = frame.iloc[row, column]
                    return result
                else:
                    raise IndexError
        except IndexError:
            click.echo("No value found.")
            return None
    
    @staticmethod
    def get_results(sourceframe: pd.DataFrame,
                    filterframe: pd.DataFrame,
                    exact: bool = False,
                    axes=1) -> pd.DataFrame | None:
        """Get the results from the query.
        
        :param sourceframe: pd.DataFrame - Source dataframe
        :param filterframe: pd.DataFrame - Filter dataframe
        :param exact: bool - Exact match
        :param axes: int - Axis to search
        :return: pd.DataFrame - Result dataframe
        """
        if not exact:
            resultframe: pd.DataFrame | None = \
                sourceframe.where(filterframe).dropna(how='any') \
                    .dropna(how='any', axis=axes)  # noqa
        elif exact:
            resultframe: pd.DataFrame | None = \
                sourceframe.where(filterframe).dropna(how='all') \
                    .dropna(how='all', axis=axes)  # noqa
        else:
            click.echo("Could not find results.")
            return None
        #
        return resultframe if not None else filterframe


App: CriteriaApp = CriteriaApp(values=AppValues)


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
        else:
            click.echo(message="Searching by index only. No keywords.")
            return None


Guard: Checks = Checks()


class Results:
    """Results.
    
    Critical for all index and search results for rows.
    
    :meth: getrowframe: Get a row from a dataframe by an index or a search term.
    """
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def getrowframe(data: pd.DataFrame,
                    ix: int, st: str, debug: bool = False) \
            -> pd.Series | pd.DataFrame | None:
        """Get a row from a dataframe by index or searches term.
        
        :param data: pd.DataFrame - Dataframe
        :param ix: int - Index
        :param st: str - Search term - Not yet implemented, critical to design
        :param debug: bool - Debug
        :return: pd.Series | pd.DataFrame | None - Row or rows
        """
        if ix and not st:
            result = App.rows(frame=data, index=ix)
        elif ix and st:
            result = App.rows(frame=data, index=ix, searchterm=st)
        elif not ix and st:
            result = App.rows(frame=data, searchterm=st)
        else:
            click.echo(f"No Data for row: {ix}")
            return None
        
        if isinstance(result, pd.Series):
            if debug:
                click.echo(f"GetRowFrame(): Found a record\n")
                rich.inspect(result)
            return result
        elif isinstance(result, pd.DataFrame):
            if debug:
                click.echo("GetRowFrame(): Found a set of records")
                rich.inspect(result)
            return result
        else:
            click.echo(f"GetRowFrame(): Found something: undefined")
            if debug:
                rich.inspect(result)
            return None


@click.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx: click.Context) -> None:  # noqa
    """Level: Run. Type: about to learn to use this CLI.
    
    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """


# 1. Load Data: Have the user load the data:
# A) The app pulls the remote Google connection;
# B) Loads Intent intentionally allows the user to load the data.
@run.group(name=AppValues.Load.cmd)
@click.pass_context
def load(ctx: click.Context) -> None:  # noqa
    """Load data from the current context, intentionally.
    
    a) Get the dataframe from remote
    b) Check context for dataframe if is/is not present
    c) Display dataframe accoridngly
    
    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """


@load.command("todo", help="Load todo list. Select views to Display.")
@click.pass_context
@click.option('-d', '--Display',
              type=str,
              default='All',
              show_default=True,
              help="Choose a Display: from All, Simple, Done, Grade, Review")
@click.option('-s', '--selects',
              type=click.Choice(choices=Head.ToDoChoices),
              default='All',
              show_default=True,
              help="Choose a option: from All, Simple, Done, Grade, Review")
def todo(ctx, display: str, selects: str) -> None:
    """Load todos, and Display different filters/views.
    
    :param ctx: click.Context
    :param display: str: Views options by text input
    :param selects: str: Views options to select by choice
    :return: None: Produces stdout --help text
    """
    dataframe: pd.DataFrame = App.get_data()
    
    def viewopt(inputs: str, choice: str) -> str:
        """Choose a view input source to Display."""
        if inputs == choice:
            return choice
        elif inputs is not None:
            return inputs
        elif choice is not None:
            return choice
        else:
            return choice
    
    # Display
    try:
        App.display_todo(dataframe=dataframe,
                         viewoption=viewopt(inputs=display, choice=selects))
    except TypeError:
        App.display_todo(dataframe=dataframe)
        rprint(f"You entered the wrong option: "
               f"{display.lower()}\n"
               f"Please try again@ All, Simple, Done, Grade or Review")  # noqa
    
    finally:
        App.update_appdata(context=ctx, dataframe=dataframe)


load.add_command(todo)


@load.command("views", help="Load views. Select bluk data to view to Display.")
@click.option('-d', '--Display',
              type=click.Choice(choices=view.Load),
              default='All', show_default=True)
@click.pass_context
def views(ctx, display) -> None:
    """Load Reference/Index.
    
    :param ctx: click.Context
    :param display: str: Views options by choice options inpyt
    :return: None: Produces stdout --help text
    """
    dataframe: pd.DataFrame = App.get_data()
    if display == 'All':
        App.display_view(dataframe=dataframe,
                         viewer=Head.OverviewViews,
                         label="Overview")  # noqa
    elif display == 'Project':
        App.display_view(dataframe=dataframe,
                         viewer=Head.ProjectView,
                         label="Project")
    elif display == 'Criteria':
        App.display_view(dataframe=dataframe,
                         viewer=Head.CriteriaView,
                         label="Criteria")
    elif display == 'ToDo':
        App.display_view(dataframe=dataframe,
                         viewer=Head.ReferenceView,
                         label="Todos")
    elif display == 'Reference':
        App.display_view(dataframe=dataframe,
                         viewer=Head.ReferenceView,
                         label="Reference/Index")
    else:
        rich.print(f"No dataloaded for: {display}")
    
    App.update_appdata(context=ctx, dataframe=dataframe)


# 2. Find
@run.group(AppValues.Find.cmd)
@click.pass_context
def find(ctx: click.Context) -> None:  # noqa
    """Find: Find item, row(s), column(s).
    
    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """


@find.command(name="locate", help="🔎 Locate row(s), via index only. "
                                  "Soon: by column, row.")
@click.option('-s', '--searches', 'searche', type=str,
              help='SEARCH TERM:✋ Leave blank if known location/row, '
                   'i.e. index\n'
                   '✋ SKIP: Hit Enter. Default:  , a blank string',
              prompt='✋ SKIP: Hit Enter. Default:  , a blank string: ',
              default='')
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help='BY ROW: ☑️ MUST: Know the line/row\'s index\'s id \n'
                   f'Select between 1 and {len(DataControl.dataframe)}: ',
              prompt='BY ROW: ☑️ MUST: Select between 1 and '
                     f'{len(DataControl.dataframe)}: ')
@click.option('-a', '--axis',
              type=click.Choice(['index'],
                                case_sensitive=False),
              help='🔎 How to search in/by. Default: by row\'s index',
              default='index',
              prompt="🔎 Select by, to focus on: index",
              required=True)
@click.pass_context
def locate(ctx: click.Context, index: int, searche: str,
           axis: str = Literal['index', 'column', 'row']) -> None:
    """Locate: a row: by index or searches term via index, column or row.
    
    :param ctx: click.Context
    :param index: int: The index of the row to locate
    :param searche: str: The search term to locate.
    :param axis: str: The axis to search in.
            Default: index
    :return: None: Display as stdout or stderr
    """
    # Debugging Flags
    debugON: bool = True  # noqa
    debugOFF: bool = False  # noqa
    # Get the dataframe
    dataframe: pd.DataFrame = App.get_data()
    # If the axis is index, -a, --axis, then search the index
    if axis.lower() == 'index':
        # Get the result source
        resultframe = \
            Results.getrowframe(data=dataframe,
                                ix=index,
                                st=Guard.santitise(searche))
        # Check if the result is a single record
        if Record.checksingle(resultframe):
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop. # noqa
            
            # Shows a result
            window.showrecord(data=resultframe,
                              debug=debugON)
        # If the result is not a single record, then display a message
        else:
            click.echo(message="The result is not a single record")
    # Additional Axes: by column, by row are not implemented yet.
    else:
        click.echo(message="Command did not run. Axes not implemented", err=True)
    # Update appdata data
    App.update_appdata(context=ctx, dataframe=dataframe)


run.add_command(locate)


# CRUD: Create, Read, Update, Delete.
# New (Add) | Create, Add commands -> None: by item, by row
@run.group("edit🎬", help="🎬 Edit: Enter editing mode. 🎬")
@click.pass_context
def edit(ctx: click.Context) -> None:  # noqa: ANN101
    """Editing mode: enter editing for notes, todos, etc.
    
    :param ctx: click.Context
    :return: None: Display as stdout --help or when subcommands is called
    """
    click.echo(message="Entering editing mode for notes, todos, etc.")
    click.echo(message="Steps: \n  1. Find a record: \n"
                       "  2. Enter it's index id:\n"
                       "  3. Edit by: adding, updating, deleting, \n"
                       "  4. Save changes, \n  5. Exits automatically.")
    click.echo(message="Prompts & Confirms used for a step by step process.")
    App.update_appdata(context=ctx, dataframe=App.get_data())
    click.echo(message="Working data is now ... rehydrated.")


@edit.command("addnote🆕", help="🆕 Add a note to a row of the record. 🆕 ")
@click.pass_context
@click.option('-s', '--searches', 'searche', type=str,
              help='Leave blank if known location/row, i.e. index',
              prompt="To use this option, enter a search term: ",
              default='')
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help='Optionally leave blank when searching '
                   'by a string, i.e. searches\n'
                   f'Select between 1 and {len(DataControl.dataframe)}: ',
              prompt=f'Select between 1 and {len(DataControl.dataframe)}: ')
@click.option('-n', '--note', 'note', type=str,
              help='Add 1st note to the record',
              prompt="Add a note to the record",
              required=True)
@click.option('-a', '--axis',
              type=click.Choice(['index', 'column', 'row'],
                                case_sensitive=False),
              help='🔎 How to search in/by. Default: by row\'s index',
              default='index',
              prompt="Select by, to focus on: index",
              required=True)
def addsinglenote(ctx: click.Context, index: int, searche: str, note: str,
                  axis: str = Literal['index']) -> None:  # noqa: ANN101
    """ADDING a new note to a record

    A: Find by a location/coordinate:
    1) Index only searches by index
    2) Searches term - Not implemented, User hits enter to skip
    3) Index and Search Term - Not implemented, skips the search term on input.
    - Uses Results.getrowframe
    B: Check if it is a single result, i.e. a pd.Series,
    C: Create a new record for local display and editing
    D: Editor modifies the record by ADDING a new note by index
    E: Display the modified record, either alone, or side by side.
    with the original record.
    F: Update the local app data.
    
    Parameters:
    -----------
    :param ctx: click.Context
    :param index: int: The index of the row to add a note to
    :param searche: str: The search term to find the row to add a note to
    :param note: str: The note to add to the row
    :param axis: str: The axis to search by, default: index
    :return: None: Display as stdout, or with --help
    """
    # Debugging Flags
    debugON = True  # noqa
    debugOFF = False  # noqa
    # Rehydrtate dataframe from remote
    dataframe: pd.DataFrame = App.get_data()
    # Search by index (-i, --index option, default/only choice)
    if axis.lower() == 'index' and searche == '':
        click.echo(message="🆕 Adding .... a new note to a record 🆕")
        # - Get the record
        resultframe = Results.getrowframe(data=dataframe,
                                          ix=index,
                                          st=Guard.santitise(searche))
        # - Check if it is a single record
        if Record.checksingle(resultframe) and note is not None:
            # - Display the found result and - send to the editor
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=True,
                                  debug=debugOFF)  # noqa
            # - Send the result to the editor
            if editing is not None:
                editor = Editor(currentrecord=editing,
                                sourceframe=resultframe)
                # - Add the note to the record
                if index is not None:
                    editor.addingnotes(notes=note,
                                       location=index,
                                       debug=debugOFF)
                # Else, exit (No changes made, as no location to update)
                else:
                    click.echo(message=f"No changes made")
                    click.echo(message=f"Exiting: editing mode. No Note Added")
                # - Display the modified record
                click.echo(message=f"=====================================")
                click.echo(message=f"Loading: edited record")
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='insert',
                                    dataview='compare',
                                    debug=debugOFF)
                # - Update the local app data
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            # Else, exit
            else:
                click.echo(message=f"Exiting: editing mode: Adding a Note")
    # Features Flag: Text Searches Branch. Future to implement.
    else:
        click.echo(message="Text searches is not yet implemented\n"
                           "Use searches with no input\n"
                           "Try again, using -i/--index and a number value"
                           "and axes: index")


@edit.command("updatenote🔂", help="🔂 Append a note in "
                                  "current record's note 🔂")
@click.pass_context
@click.option('-s', '--searches', 'searche', type=str,
              help='SEARCH TERM:✋ Leave blank if known location/row, '
                   'i.e. index\n'
                   '✋ SKIP: Hit Enter. Default:  , a blank string',
              prompt='✋ SKIP: Hit Enter. Default:  , a blank string: ',
              default='')
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help='BY ROW: ☑️ MUST: Know the line/row\'s index\'s id \n'
                   f'Select between 1 and {len(DataControl.dataframe)}: ',
              prompt=f'BY ROW: ☑️ MUST: Select between 1 and '
                     f'{len(DataControl.dataframe)}: ')
@click.option('-n', '--note', 'note', type=str,
              help='NOTE: 📝 Updates the note on record',
              prompt="NOTE: 📝 Updates the note on record",
              required=True)
@click.option('-a', '--axis',
              type=click.Choice(['index'],
                                case_sensitive=False),
              help='🔎 How to search in/by. Default: by row\'s index',
              default='index',
              prompt="🔎 Select by, to focus on: index",
              required=True)
def updateanote(ctx: click.Context, index: int, searche: str, note: str,
                axis: str = Literal['index']) -> None:  # noqa: ANN101
    """UPDATING to a NOTE
    
    A: Find by a location/coordinate:
    1) Index only searches by index
    2) Searches term - Not implemented, User hits enter to skip
    3) Index and Search Term - Not implemented, skips the search term on input.
    - Uses Results.getrowframe
    B: Check if it is a single result, i.e. a pd.Series,
    C: Create a new record for local display and editing
    D: Editor modifies the record by UPDATING a new note by index
    E: Display the modified record, either alone, or side by side.
    with the original record.
    F: Update the local app data.
    
    Parameters:
    -----------
    :param ctx: click.Context
    :param index: int: The index of the row to add a note to
    :param searche: str: The search term to find the row to add a note to
    :param note: str: The note to add to the row
    :param axis: str: The axis to search by, default: index
    :return: None: Display as stdout, or with --help

    Append by a location/coordinate.
    """
    debugON = True  # noqa
    debugOFF = False  # noqa
    # Fetch the dataframe
    dataframe: pd.DataFrame = App.get_data()
    # Search by index (-i, --index option, default/only choice)
    if axis.lower() == 'index':
        # Fetch the data by index
        click.echo(f"🗑🔂 Updating a Note, in {index}...🔂")
        resultframe = Results.getrowframe(data=dataframe,
                                          ix=index,
                                          st=Guard.santitise(searche))
        # Check if it is a single record
        if Record.checksingle(resultframe) and note is not None:
            # Display the found record and - send to the editor
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=True,
                                  debug=debugOFF)  # noqa
            # Send the result to the editor
            if editing is not None:
                editor = Editor(currentrecord=editing,
                                sourceframe=resultframe)
                # Update the note by index
                if index is not None:
                    editor.updatingnotes(notes=note,
                                         location=index,
                                         debug=debugOFF)
                # Else, exit (No changes made, as no location to update)
                else:
                    click.echo(message=f"No changes made")
                    click.echo(message=f"Exiting: editing mode. "
                                       f"No Note Updated")
                # Display Record with Modified Data
                click.echo(message=f"Loading: edited record")
                # Display the modified record
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='append',
                                    dataview='compare',
                                    debug=debugOFF)
                # Update the local app data
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            else:
                # Else, exit (No changes made, as no record to edit)
                click.echo(message=f"Exiting: editing mode")
    # Features Flag: Text Searches Branch. Future to implement.
    else:
        click.echo(message="Text searches is not yet implemented\n"
                           "Use searches with no input\n"
                           "Try again, using -i/--index and a number value"
                           "and axes: index")


@edit.command("deletenote🗑️", help="🗑️Clears the note(s) from a record's "
                                   "line/row🗑️")
@click.pass_context
@click.option('-s', '--searches', 'searche', type=str,
              help='SEARCH TERM:✋ Leave blank if known location/row, '
                   'i.e. index\n'
                   '✋ SKIP: Hit Enter. Default:  , a blank string',
              prompt="SEARCH TERM: SKIP: ⬇️ Hit enter, to continue: ",
              default='')
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help='BY ROW: ☑️ MUST: Know the line/row\'s index\'s id \n'
                   f'Select between 1 and {len(DataControl.dataframe)}: ',
              prompt=f'BY ROW: ☑️ Select between 1 and '
                     f'{len(DataControl.dataframe)}: ',
              required=True)
@click.option('-n', '--note', 'note', type=str,
              help='NOTE: ⭕ Clears the note. Hit Enter. Default:'
                   '  , a blank string',
              prompt="NOTE: ⭕ ⬇️ Hit enter, to continue: ",
              confirmation_prompt="This will delete the note, "
                                  "⬇️ hit enter, no input:",
              default='',
              show_default=True)
@click.option('-a', '--axis',
              type=click.Choice(['index'],
                                case_sensitive=False),
              help='🔎 How to search in/by. Default: by row\'s index',
              default='index',
              prompt="⬇️ Hit enter, to continue: index",
              required=True,
              show_default=True)
def deleteanote(ctx: click.Context, index: int, searche: str, note: str,
                axis: str = Literal['index']) -> None:  # noqa: ANN101
    """DELETE a note from a record
    
    A: Find by a location/coordinate:
    1) Index only searches by index
    2) Searches term - Not implemented, User hits enter to skip
    3) Index and Search Term - Not implemented, skips the search term on input.
    - Uses Results.getrowframe
    B: Check if it is a single result, i.e. a pd.Series,
    C: Create a new record for local display and editing
    D: Editor modifies the record by ADDING a new note by index
    E: Display the modified record, either alone, or side by side.
    with the original record.
    F: Update the local app data.
    
    Parameters:
    -----------
    :param ctx: click.Context
    :param index: int: The index of the row to add a note to
    :param searche: str: The search term to find the row to add a note to
    :param note: str: The note to add to the row
    :param axis: str: The axis to search by, default: index
    :return: None: Display as stdout, or with --help
    """
    # Debugging Flags
    debugON = True  # noqa
    debugOFF = False  # noqa
    # Rehydrtate dataframe from remote
    dataframe: pd.DataFrame = App.get_data()
    # Search by index (-i, --index option, default/only choice)
    if axis.lower() == 'index' and searche == '':
        click.echo(f"🗑️ Deleting a Note, in {index}...🗑️")
        # - Get the record
        resultframe = Results.getrowframe(data=dataframe,
                                          ix=index,
                                          st=Guard.santitise(searche))
        # - Check if it is a single record
        if Record.checksingle(resultframe) and note is not None:
            # - Display the found result and - send to the editor
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=True)  # noqa
            # - Send the result to the editor
            if editing is not None:
                editor = Editor(currentrecord=editing,
                                sourceframe=resultframe)  # noqa
                # - Add the note to the record
                if index is not None:
                    editor.deletingnotes(notes=note, location=index)
                # Else, exit (No changes made, as no location to update)
                else:
                    click.echo(message=f"No changes made")
                    click.echo(message=f"Exiting: editing mode. "
                                       f"No Note Deleted")
                # - Display the modified record
                click.echo(message=f"=====================================")
                click.echo(message=f"Loading: edited record")
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='clear',
                                    dataview='compare',
                                    debug=debugOFF)
                # - Update the local app data
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            # Else, exit
            else:
                click.echo(message=f"Exiting: editing mode: no deletes made")
    # Features Flag: Text Searches Branch. Future to implement.
    else:
        click.echo(message="Text searches is not yet implemented\n"
                           "Use searches with no input\n"
                           "Try again, using -i/--index and a number value"
                           "and axes: index")


# Click Command repl is run from this function
# See https://www.perplexity.ai/search/085c28b9-d6e8-4ea2-8234-783d7f1a054c?s=c
register_repl(run)

if __name__ == "__main__":
    utils.warn()
    # Opening Introduction
    click.echo(
            message="PyCriteria: A simple CLI for managing"
                    " Code Institute's criteria\n"
                    "==================================="
                    "==============================\n"
                    "\n"
                    "GETTING STARTED\n"
                    "Type --help to get started\n"
                    "Hold ctrl + d to exit \n"
                    "Hold ctrl + c to abort \n"
                    "Tab completion is available\n"
                    "\n"
                    "======================================"
                    "===========================\n"
                    "\n"
                    "CLI COMMANDS / REPL\n"
                    "1: BASE: run (app.py). INFO only.\n"
                    "2: INTENT: (load, find, add, update, "
                    "delete). INFO only.\n"
                    
                    "3: ACTION: per INTENT the actionable "
                    "sub-commands with options\n"
                    "4: OPTIONS: per ACTION the options "
                    "to perform the action\n"
                    "NB: Each command can have multiple options\n"
                    "\n"
                    "========================================"
                    "=========================\n"
                    "\n"
                    "CLI DATA: REMOTE & LOCAL\n"
                    "DATA: The data remotely pulled from "
                    "Google Sheets (the remote).\n"
                    "NB: Each command rehydrates/refreshes "
                    "local data from the remote.\n"
                    "  - This rehydration pattern is more"
                    " expensive per command.\n"
                    "  - It does ensure most recent data "
                    "is pulled from the remote.\n"
                    "  - An app local copy is stored globally,"
                    " and updated per command.\n"
                    "  - A scoped copy is used per command "
                    "as active data.\n"
                    "\n"
                    "========================================="
                    "========================\n"
                    "\n"
                    "CLI ENVIRONMENT & MAKING MISTAKES\n"
                    "This CLI runs within its own sub "
                    "shell/enviornment/REPL.\n"
                    " - 🚧 As such it is tollerant to user "
                    "input and user errors. 🚧\n"
                    " - There will be commands input errors,"
                    " as with any cli app.\n"
                    " - These types of errors are part of "
                    "the cli environment/repl.\n"
                    " - Just try the command again, and "
                    "enter in the correct input.\n"
                    "\n"
                    "======================================"
                    "===========================\n"
                    "\n"
                    "CLI COMMANDS & OPTIONS\n"
                    "CLI uses multi-level command structure, "
                    "similar to 'aws cli'.\n"
                    " - This means that you can type a ACTION "
                    "command and EITHER: \n"
                    " a) then hit enter to enter a prompts "
                    "sequence, to enter values.\n"
                    " OR \n"
                    " b) at a ACTION enter using -o or "
                    "--option then a value/input\n"
                    "    - e.g. '-o' with single hyphen "
                    "is same as '--option'.\n"
                    " NB: 'o' or 'option' is for illustrative "
                    "purposes only\n"
                    "\n"
                    "========================================"
                    "=========================\n"
                    "QUICK START\n"
                    "\n"
                    "Get started by typing: either --help or "
                    "load, find, edit"
                    "\n"
                    "Use 'tab' when typing in command's first"
                    " letters for autocomplete\n"
                    "\n"
                    "Then press 'space' to show the "
                    "subcommands sub-menus\n")  # noqa
    run()
