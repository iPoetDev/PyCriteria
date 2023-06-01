#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, ANN001, D415, RET505, I001,
"""Module: PyCriteria Command/REPL Terminal app.

Usage: Commands and REPL
-------------------------
- Multi-line level nested commands structure.
    - Run - Core/BASE command AND ANCHORED command.
        - Clear             - SUB COMMAND, nested under Run: to clear REPL/screen.
        - Load              - TOP INTENT, nested under Run
            - Views         - SUB COMMAND, nested under Load
                              Switches between sub-views of the data
            - ToDo          - SUB COMMAND, nested under Load
                              Switches between sub-views of the ToDo tasks
        - Find              - TOP INTENT, nested under Run
            - Locate        - SUB COMMAND, nested under Find
                              Locate a record by ID (row)
                              Future by column value, or row search term
        - Edit              - TOP INTENT, nested under Run
                              Core activity/action of the app for user
            - Note          - SUB COMMAND, under Edit: Edits a note
                - Mode      - Option, nested with Note: to enter an edit mode
                              Bundles add, update and delete under one command
            - ToDo          - SUB COMMAND, under Edit: Edits a ToDo field
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
:var: Logs: Logging.py - Logging.py for app.py
:var: DataControl: Controller.py - DataController for DataModel, shared, alias
:var: Webconsole: Controller.py - WebConsole for WEB versions of the app.
:var: window: app.py - Window class for Terminal Layouts, Panels, Cards.
:var: App: app.py - Key DataConrtooler/Controller.py

"""
# 1. Std Lib
from typing import Literal

import click  # type: ignore
# 2. 3rd Party
from click_repl import register_repl  # type: ignore
from pandas import pandas as pd, DataFrame, Series  # type: ignore
from rich import inspect as inspector, pretty, print as rprint  # type: ignore
from rich.console import Console
from rich.panel import Panel  # type: ignore
from rich.table import Table  # type: ignore

# 3. Local: Note the controller * intentionally imports all from the module
from controller import (Controller as Actions, DataController,
                        Display, Results, WebConsole,
                        configuration, gspread, Record, Inner, Editor, )
from modelview import (Views, Head, )  # type: ignore
from sidecar import (AppValues as Val, ProgramUtils as utils,
                     CliStyles as styles, Checks as Guard, )

# Global Modules/Objects
# 1.1 controller.py
DataControl: DataController = DataController(Actions.load_wsheet())

Webconsole: WebConsole = WebConsole(configuration.Console.WIDTH,
                                    configuration.Console.HEIGHT)
Webconsole.terminal = Inner()
# 1.2 sidecar.py
pretty.install()


class Valid:
    """Command/Input Validation"""
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def index(ctx, param, value) -> int:  # noqa Parameters uses in callbacks
        """Check if value is in range."""
        # If None, Raise BadParameter
        if value is None:
            raise click.BadParameter('Try again, '
                                     'enter an (numerical) value.')
        # If not an integer, Raise BadParameter
        if not isinstance(value, int):
            raise click.BadParameter('Index must be an number.')
        # If not in range, Raise BadParameter, as Index starts at 1
        if value <= 0 or value > App.get_range:
            raise click.BadParameter('Index must be '
                                     f'between 0 and {App.get_range}.')
        return value
    
    @staticmethod
    def santitise(ctx, param, value) \
            -> str | None:  # noqa Contexts, Parameters uses in callbacks
        
        """Sanitise strings: by validating input - empty or not string.

        :param ctx: click.Context - Click Context
        :param param: click.Parameter - Click Parameter
        :param value: str - String to sanitised
        :return: str | None - Sanitised string or None
        """
        empty: str = ''
        # Check if value is empty or not a string
        if value == empty or not isinstance(value, str):
            click.secho(message="Exiting Editing Mode. "
                                "Must be a text or string. "
                                "Try again.",
                        fg=styles.invalidfg,
                        bold=styles.invalidbold)
            return None
        # Return trimmed value if not empty
        return value.strip() if value else empty
    
    @staticmethod
    def mode(ctx, param, value) \
            -> str | None:  # noqa Contexts, Parameters uses in callbacks
        """Check the mode."""
        if isinstance(value, str) and value.lower() is not None:
            # Enter Add Edit Mode: To insert, create, new inputs to a record.
            if value.lower() == 'add':
                click.secho(message="Adding to the record: .......",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Enter Update Edit Mode: To append, update, new inputs to existing.
            elif value.lower() == 'update':
                click.secho(message=f"Updating the record: .......",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Enter Delete Edit Mode: To clear, remove existing record's value.
            elif value.lower() == 'delete':
                click.secho(message=f"Deleting from the record: .......",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Exit Edit Mode: Automatically exit Editing Mode.
            else:
                click.secho(message="Exiting Editing Mode. "
                                    "Try again.",
                            fg=styles.invalidfg, bold=styles.invalidbold)
                return None
        else:
            click.secho(message="Exiting Editing Mode. Invalid entry.",
                        fg=styles.invalidfg, bold=styles.invalidbold)
            return None
    
    @staticmethod
    def correctaxis(ctx, param, value) \
            -> str | None:  # noqa Contexts, Parameters uses in callbacks
        """Check valid choice of axis.
        
        Dimensions: across rows or columns or by index; depends on the Pandas.
        """
        if isinstance(value, str) and value.lower() is not None:
            # Current feature: Implemented: DataFrames have these dimensions.
            if value.lower() == 'index':
                return value
            # Future feature: Not Implemented: DataFrames have these dimensions.
            elif value.lower() == 'row':
                return value
            # Future feature: Not Implemented: DataFrames have these dimensions.
            elif value.lower() == 'column':
                return value
            else:
                click.secho(message="Exiting Editing Mode. "
                                    "Wrong axis. "
                                    "Try again.",
                            fg=styles.invalidfg, bold=styles.invalidbold)
                return None
        # Exit Edit Mode: Automatically exit Editing Mode due to invalid entry.
        else:
            click.secho(message="Exiting Editing Mode. Invalid entry.",
                        fg=styles.invalidfg, bold=styles.invalidbold)
            return None
    
    @staticmethod
    def selectviews(ctx, param, value) \
            -> str | None:  # noqa Contexts, Parameters uses in callbacks
        """Check valid choice of view."""
        allview, projectview, criteriaview, todoview, referenceview = \
            Views.Load
        click.echo(f"\n")
        if isinstance(value, str) and value.lower() is not None:
            # Select All View: Display all records in the sheet.
            if value.lower() == allview.lower():
                click.secho(message="Displaying Assignment's Criteria"
                                    f" {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Project View: Display all records in the sheet.
            elif value.lower() == projectview.lower():
                click.secho(message="Displaying Assignment's "
                                    f" {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Criteria View: Display all records in the sheet.
            elif value.lower() == criteriaview.lower():
                click.secho(message="Displaying Assignment's "
                                    f" {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Todo View: Display all records in the sheet.
            elif value.lower() == todoview.lower():
                click.secho(message="Displaying Assignment's "
                                    f" {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Reference View: Display all records in the sheet.
            elif value.lower() == referenceview.lower():
                click.secho(message="Displaying Assignment's "
                                    f" {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Exit Edit Mode: Automatically exit Editing Mode.
            else:
                click.secho(message="Exiting Editing Mode. "
                                    "No View selected. "
                                    "Try again.",
                            fg=styles.invalidfg, bold=styles.invalidbold)
                return None
        # Exit Edit Mode: Automatically exit Editing Mode due to invalid entry.
        else:
            click.secho(message="Exiting Editing Mode. Invalid entry.",
                        fg=styles.invalidfg, bold=styles.invalidbold)
            return None
    
    @staticmethod
    def selecttodo(ctx, param, value) \
            -> str | None:  # noqa Contexts, Parameters uses in callbacks
        """Check Valid Todo Views."""
        allview, simpleview, notesview, dodview, gradeview, reviewview = \
            Views.Todo
        click.echo(f"\n")
        if isinstance(value, str) and value.lower() is not None:
            # Select All View: Display all records in the sheet.
            if value.lower() == allview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Simple View: Display a reduced view of records.
            elif value.lower() == simpleview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Notes View: Display a reduced view of records for notes.
            elif value.lower() == notesview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Definition of Done View: Display progression of records.
            elif value.lower() == dodview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Grades View: Display a grade focused view of records.
            elif value.lower() == gradeview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Select Review View: Display review of the records; a quick review.
            elif value.lower() == reviewview.lower():
                click.secho(message=f"Displaying Todo's {value} View: \n",
                            fg=styles.infofg, bold=styles.infobold)
                return value
            # Exit Edit Mode: Automatically exit Editing Mode.
            else:
                click.secho(message="Exiting Editing Mode. "
                                    "No View selected. Try again.",
                            fg=styles.invalidfg, bold=styles.invalidbold)
                return None
        # Exit Edit Mode: Automatically exit Editing Mode due to invalid entry.
        else:
            click.secho(message="Exiting Editing Mode. Invalid entry.",
                        fg=styles.invalidfg, bold=styles.invalidbold)
            return None
    
    @staticmethod
    def checktoggle(edits) -> str | None:
        """Check the mode."""
        if isinstance(edits, str):
            # Add
            if edits.lower() == 'toggle':
                return edits
            else:
                click.secho(message="Exiting Editing Mode. Invalid Mode. Try again.",
                            fg=styles.invalidfg, bold=styles.invalidbold)
        else:
            click.secho(message="Exiting Editing Mode. Try again.",
                        fg=styles.invalidfg, bold=styles.invalidbold)
            return None
    
    @staticmethod
    def checkstatus(state) -> str | None:
        """Check the status."""
        if isinstance(state, str):
            # Add
            if state.lower() == 'todo':
                click.echo(message=f"🆕 ToDo Status, {state} 🆕")
                return state
            # Update
            elif state.lower() == 'wip':
                click.echo(message=f"🆕 ToDo Status, {state} 🆕")
                return state
            # Delete
            elif state.lower() == 'done':
                click.echo(message=f"🆕 ToDo Status, {state} 🆕")
                return state
            elif state.lower() == 'missing':
                click.echo(message=f"🆕 ToDo Status, {state} 🆕")
                return state
            # None, Other
            else:
                click.echo(message="Exiting Editing Mode. Try again.")
                return None
    
    @staticmethod
    def checkmode(edits: str, index: int) -> str | None:
        """Check the mode."""
        if isinstance(edits, str):
            # Add
            if edits.lower() == App.values.Edit.ADD:
                click.echo(message="🆕 Adding note"
                                   f", in row {index} 🆕")
                return edits
            # Update
            elif edits.lower() == App.values.Edit.UPDATE:
                click.echo(message="🔂 Updating a Note"
                                   f", in row {index}...🔂")
                return edits
            # Delete
            elif edits.lower() == App.values.Edit.DELETE:
                click.echo(message="🗑️ Deleting a Note"
                                   f", in row {index}...🗑️")
                return edits
            # None, Other
            else:
                click.echo(message="Exiting Editing Mode. Try again.")
    
    @staticmethod
    def checkcommand(mode: str) \
            -> str | None:
        """Check the mode, translate to edit comand tyoe."""
        allowed = {App.values.Edit.ADD,
                   App.values.Edit.UPDATE, App.values.Edit.DELETE}
        if mode in allowed:
            if mode == App.values.Edit.ADD:
                return App.values.Edit.INSERT
            elif mode == App.values.Edit.UPDATE:
                return App.values.Edit.APPEND
            elif mode == App.values.Edit.DELETE:
                return App.values.Edit.CLEAR
        else:
            return None


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
        return value if switch else None
    
    @staticmethod
    def showrecord(data: pd.Series | pd.DataFrame,
                   sendtoeditor: bool = False,
                   displayon: bool = True,
                   debug: bool = False) -> Record | None:
        """Display Record.
        
        :param data: pd.Series | pd.DataFrame - Individual Record to display
        :param sendtoeditor: bool - Switch to send to the Editor or not.
        :param displayon: bool - Switch to display or not.
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
            
            if debug is True:
                rprint("Debug Mode: Show Record")
                inspector(individual)
            
            if displayon:
                if individual.card(consolecard=Webconsole.console) is not None:
                    window.printpanels(record=individual)
                else:
                    click.echo("Displaying Simple Card")
                    individual.card(consolecard=Webconsole.console)
            
            return Window.sendto(individual, sendtoeditor)
    
    @staticmethod
    def printpane(panel: str, printer: Console) -> None:
        """Print Pane.
        
        :param panel: str - Panel to print
        :param printer: Console - Console to print to
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
            
            return individual if sendtoeditor else None
    
    @staticmethod
    def showmodified(editeddata: pd.Series,
                     editor: Editor,
                     commandtype: str,
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
            # Was checking if Record.ismodified was truthy, if state persists
            # But a record's state between transactions are not kept in state
            # A new record per find/locate is created for a stateless record
            # So dropped this guard, as stateful transactions are not in scope.
            # State could be if time permits, if a lastmodified field is saved.
            # Is saved to the remote database, but not in the local record.
            # Therefore not in scope for version: 1.0.0.alpha+
            click.echo(f'Command Type: {commandtype}')
            if editor.editmode == commandtype:
                click.echo(editor.editmode)
                if debug is True:
                    click.echo(message="==========Displaying: "
                                       "Changes=========\n")
                # 1. Display the Edited record
                if dataview == 'show':  # show
                    window.showedited(editeddata=editeddata,
                                      debug=App.values.NOTRACING)
                elif dataview == 'compare':  # compare
                    click.echo(f"DataView Outside: {dataview}")
                    window.comparedata(editeddata=editeddata,
                                       editor=editor,
                                       debug=App.values.NOTRACING,
                                       debugdisplay=App.values.NOTRACING)  # noqa
                #  [DEBUG]
                if debug is True:
                    click.echo(message="=== [DEBUG] Saving: "
                                       "changes made [DEBUG]==\n")
                    click.echo(f" Modified: {editor.lastmodified} ")
            else:
                click.echo(message="No changes made. See above.")
            #
            if debug is True:
                click.echo(message="=====================================")
            # Switch confirmation on a command's type
            if commandtype == 'insert':
                click.echo(message=("🆕 A new note is now added "
                                    "🆕 at:" + editor.lastmodified))
            elif commandtype == 'append':
                click.echo(message="A note is updated at:"
                                   + editor.lastmodified)
            elif commandtype == 'clear':
                click.echo(message="A record's is now deleted at:"
                                   + editor.lastmodified)
            click.echo(message="Exiting: Command completed")
        else:
            click.echo(message="No changes made. Bulk edits not supported.")
        
        return None
    
    @staticmethod
    def comparedata(editeddata: pd.Series,
                    editor: Editor,
                    debug=False, debugdisplay=False) -> None:
        """Compare Old and New side by side.
        
        :param editeddata: pd.Series - Individual Record to display
        :param editor: Editor - Editor to use
        :param debug: bool - Switch to debug mode or not.
        :param debugdisplay: bool - Switch to debug display mode or not.
        :return: None
        """
        if debug is True:
            rprint(editeddata)
            inspector(editeddata)
        
        if editeddata.empty is False and editor.ismodified:
            # 0. Create the Old and New Records, locallt
            oldrecord: Record = editor.record
            newrecord: Record = Record(series=editor.newresultseries)
            # 1. Display the Edited recor
            left = oldrecord.editable(
                    consoleedit=Webconsole.console,
                    sendtolayout=App.values.DISPLAYING,
                    title="Original Record")
            right = newrecord.editable(
                    consoleedit=Webconsole.console,
                    sendtolayout=App.values.DISPLAYING,
                    title="Updated Record")
            # Compare Old with New, else just show the new
            if left is not None or right is not None:
                window.printpane(panel="bannerfull",
                                 printer=Webconsole.console)
                header = newrecord.header(
                        consolehead=Webconsole.console,
                        sendtolayout=App.values.Display.TOLAYOUT,
                        gridfit=True,
                        debug=debugdisplay)
                sidebyside = newrecord.comparegrid(
                        container=Webconsole.table,
                        left=left,
                        right=right,
                        sendtolayout=App.values.Display.TOLAYOUT,
                        fit=True,
                        debug=App.values.TRACING)
                footer = newrecord.footer(
                        consolefoot=Webconsole.console,
                        sendtolayout=App.values.Display.TOLAYOUT,
                        expand=False,
                        debug=debugdisplay)
                
                newrecord.panel(consolepane=Webconsole.console,
                                renderable=header,
                                fits=True,
                                sendtolayout=
                                App.values.Display.TOTERMINAL)  # noqa
                newrecord.panel(consolepane=Webconsole.console,
                                renderable=sidebyside,
                                fits=True,
                                sendtolayout=
                                App.values.Display.TOTERMINAL)  # noqa
            else:
                window.showedited(editeddata=editeddata, debug=debug)


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
    
    values: Val
    views: Views
    guard: Guard
    appdata: DataController
    data: pd.DataFrame
    range: int
    editmode: list[str] = ['none', 'add', 'update', 'delete']
    editaction: list[str] = ['insert', 'append', 'clear']
    CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
    
    def __init__(self, applicationdata: DataController) -> None:
        """Initialize."""
        self.values = Val()
        self.views = Views()
        self.guard = Guard()
        self.appdata = applicationdata
        self.data = self.appdata.dataframe
        self.range = len(self.data)
    
    @staticmethod
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context.
        
        :return: pd.DataFrame - Dataframe
        """
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    @property
    def get_range(self) -> int:
        """Get the range of the dataframe.
        
        :param self
        :return: int - Range of the dataframe
        """
        self.range = len(self.data)
        return self.range
    
    # Depends on ToDo command
    def command_todo(self, dataframe: pd.DataFrame,
                     todoview: str = 'All',
                     label: str = "Progress") -> None:
        """Display the dataframe by view option/choice.
        
        :param dataframe: pd.DataFrame - Dataframe to display
        :param todoview: str - View option
        :param label: str - Label to display
        :return: None """
        
        # Select the view
        def vues(choice: str) -> list[str]:
            """Select the (predefined) view -> Header. Columns
            
            :param choice: str - View option
            :return: list[str] - Columns """
            #
            if choice.lower() == self.views.All.lower():
                headers: list[str] = Head.ToDoAllView
            elif choice.lower() == self.views.Simple.lower():
                headers: list[str] = Head.ToDoSimpleView
            elif choice.lower() == self.views.Notes.lower():
                headers: list[str] = Head.ToDoNotesView
            elif choice.lower() == self.views.Done.lower():
                headers: list[str] = Head.ToDoProgressView
            elif choice.lower() == self.views.Grade.lower():
                headers: list[str] = Head.ToDoGradeView
            elif choice.lower() == self.views.Review.lower():
                headers: list[str] = Head.ToDoReviewView
            else:
                headers: list[str] = Head.ProjectView
            return headers
        
        # Configure the bulk ouput as Table
        self.output(data=dataframe, cols=vues(todoview), title=label)
    
    #
    def command_view(self, dataframe: pd.DataFrame,
                     viewer: list[str] = None,
                     label: str = 'Overview') -> None:
        """Display the dataframe.

        :param dataframe: pd.DataFrame - Dataframe to display
        :param viewer: list[str] - List of views to display
        :param label: str - Label to display
        :return: None """
        # Select the view's header
        headers: list[str] = Head.OverviewViews if viewer is None else viewer
        # Configure the bulk ouput as Table
        self.output(data=dataframe, cols=headers, title=label)
    
    #
    @staticmethod
    def output(data: pd.DataFrame,
               cols: list[str],
               title: str) -> None:
        """Command Output flow. Shared by common commands
        
        :param data: pd.DataFrame - Dataframe to display
        :param cols: list[str] - List of columns to display
        :param title: str - Title to display
        :return: None """
        # Configure the bulk ouput as Table with headers
        Webconsole.table = Webconsole.configure_table(headers=cols)
        # Display the sub frame dataview
        Display.display_subframe(dataframe=data,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=cols,
                                 viewfilter=title)
        # Signal from completion of command
        click.echo(message='Your data is refreshed/rehydrated')
    
    #
    def update_appdata(self, context, dataframe: pd.DataFrame) -> None:
        """Update the app data.

        :param context: click.Context - Click context
        :param dataframe: pd.DataFrame - Dataframe to update
        :return: None """
        # Update the context
        context.obj = dataframe
        # Update the appdata
        DataControl.dataframe = dataframe
        self.appdata.dataframe = dataframe
        self.data = dataframe


App: CriteriaApp = CriteriaApp(applicationdata=DataControl)
window: Window = Window()


# ########################################################################### #
# App Commands
# - Run
#   - load
#       - todo      -s | --select: Choose a sub view
#       - views     -s | --select: Choose a sub view
#   - find
#       - locate    -i -a | --index --axis
#                   index: input range
#                   axis: index search focus
#   - edit
#       - note      -m -i -n -a | --mode --index --note --axis
#                   mode: editmode: add, update, delete
#                   index: input range
#                   note: input note
#                   axis: index search focus
#       - progress  -m -i -n -a | --mode --index --note --axis
#                   mode: editmode: toggle
#                   index: input range
#                   note: input note
#                   axis: index search focus
# ########################################################################### #


# 0. Run: Base Command: Anchors all Intent and Actions
# Does not to anything but command achitecture/infrastructure and --help
@click.group(name=App.values.Run.cmd,
             context_settings=App.CONTEXT_SETTINGS, short_help='Type: --help')
@click.pass_context
def run(ctx: click.Context) -> None:  # noqa
    """Level: Run. Type: about to learn to use this CLI.
    
    \f
    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """


# 0.1 Run: Base Command: Clear
# Clears the REPL using click.clear()
@run.command("clear", help="Cmd: Clear the screen", short_help="Cmd: Clear the screen")
@click.pass_context
def clear(ctx: click.Context) -> None:  # noqa
    """Clear the screen."""
    click.echo("Screen cleared")
    click.clear()


# 1. Load Data: Have the user load the data:
# READ of CRUD Ops (Create, _READ_, Update, Delete)
# Load intents/actions does the bulk data loading
# Uses App.values.x.x(.x) String values for configuration.
@run.group(name=App.values.Load.cmd, short_help='Load Mode: Todos & Views')
@click.pass_context
def load(ctx: click.Context) -> None:  # noqa
    """INTENT: Load: => ACTIONS/Commands: todo, views:

    === === === === === === === === === === === === ===\n
    \b
    Start Typing:
    - Use 'tab' to autocomplete the current menu option,
    - Then 'space' to start the sub-menu.
    - Then 'tab' or 'enter' to complete \n
    ___\n
    \b
    Hit 'enter' to enter the prompt sequence for option.
    Can use the, e.g., `-o` on same line as command.
    However the , prompt entery is preferred.\n.
    ===\n
    \b
    ACTIONS/Commands:
    - todo
    ....'-s' selects | default: All.
    - views
    ....'-s' selects | default: Overview \n
    === === === === === === === === === === === === ===\n
    \f
    a) Get the dataframe from remote
    b) Check context for dataframe if is/is not present
    c) Display dataframe accoridngly
    

    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """
    click.secho(
            message="====================LOADING MODE=======================\n",
            fg='magenta', bg='white', bold=True)
    click.secho(
            message="========Load & Show All/Bulk Records (Table)===========\n",
            fg='magenta', bold=True)
    click.secho(
            message="==========Select Views: Show Selected Tasks============\n",
            fg='magenta', bold=True)
    click.secho(
            message="Entering loading & reading mode for all records.",
            fg='magenta', bg='white', bold=True)
    click.secho(
            message="Steps: \n"
                    "  1. Enter an load mode:                               \n"
                    "  2. Select Todo or Views task/action:                 \n"
                    "  3. For Todo: -= Tasks Zone for the Project           \n"
                    "     3.1 Choose All: Complete list an overview.        \n"
                    "     3.2 Choose Simple: A simple list of Todo.         \n"
                    "     3.3 Choose Notes: A list of Notes.                \n"
                    "     3.4 Choose Notes: A Todos that are Done.          \n"
                    "     3.5 Choose Grade: A Todos that are by Grade.      \n"
                    "     3.5 Choose Review...........................      \n"
                    "     ............................................      \n"
                    "  4. For Views: -=Review the Assignement & Criterias=- \n"
                    "     4.1 Choose Overview: Complete list an overview.   \n"
                    "     4.2 Choose Project: A view of projects. data.     \n"
                    "     4.3 Choose Criteria: A view of criteria.          \n"
                    "     4.4 Choose ToDos: A view of ToDos.                \n"
                    "     4.5 Choose References: An index of references.    \n"
                    "  5. Exits mode automatically.                         \n",
            fg='magenta', bold=styles.infobold, underline=True)
    click.secho(
            message="Prompts are available for each input. Hit: 'Enter'")
    App.update_appdata(context=ctx, dataframe=App.get_data())
    click.secho(
            message="Working data is now ... rehydrated.",
            blink=True)
    click.secho(
            message=f"You have rows 1 to {App.get_range} to work with",
            bold=styles.infobold)


# 2.1 Load Data: ToDo (Sub) Views
# Uses App.values.x.x(.x) String values for configuration.
@load.command(App.values.Todo.cmd,
              help=App.values.Todo.help, short_help='Load Mode: Todos Views')
@click.pass_context
@click.option(f'-selects', 'selects',
              type=click.Choice(choices=App.views.Todo,
                                case_sensitive=App.values.case),
              default=App.values.Todo.Selects.default,
              show_default=App.values.shown,
              prompt=App.values.Todo.Selects.prompt,
              help=App.values.Todo.Selects.help)
def todo(ctx, selects: str) -> None:
    """Load todos, and display different filters/views.
    
    \f
    :param ctx: click.Context
    :param selects: str: Views options to select by choice
    :return: None: Produces stdout --help text
    """
    # Get Data
    dataframe: pd.DataFrame = App.get_data()
    
    # Guard Clause Checks Choice
    def checkchoice(choice: str) -> str:
        """Guard Clause."""
        if choice is not None and isinstance(choice, str):
            return choice
        else:
            click.secho(message="Your selected option is not possible.\n "
                                "Try the commanď with one of these options: \n"
                                "Help: --help\n"
                                "Choices: All, Simple, Done, Grade, Review",
                        fg=styles.invalidfg,
                        bold=styles.invalidbold)  # noqa
    
    # Display
    try:
        App.command_todo(dataframe=dataframe,
                         todoview=checkchoice(choice=selects))
    except TypeError:
        App.command_todo(dataframe=dataframe)
    finally:
        App.update_appdata(context=ctx, dataframe=dataframe)


# 2.2 Load Data: Views (Sub) Views - These are assignments levels views
# Uses App.values.x.x(.x) String values for configuration.
@load.command(App.values.Views.cmd,
              help=App.values.Views.help, short_help='Load Mode: Selects views')
@click.option('-selects', 'selects',
              type=click.Choice(choices=App.views.Load,
                                case_sensitive=App.values.case),
              default=App.values.Views.Selects.default,
              show_default=App.values.shown,
              prompt=App.values.Views.Selects.prompt,
              help=App.values.Views.Selects.help)
@click.pass_context
def views(ctx, selects) -> None:
    """Load Reference/Index.
    
    \f
    :param ctx: click.Context
    :param selects: str: Select views options by choice options input
    :return: None: Produces stdout --help text
    """
    # Get Data
    dataframe: pd.DataFrame = App.get_data()
    
    # Guard Clause Checks Choice
    def checks(choice: str) -> str:
        """Guard Clause for View Choice
        
        :param choice: str: Choice
        :return: str: Choice else a styled invalid message
        """
        if choice is not None and isinstance(choice, str):
            return choice
        else:
            click.secho(message="Your selected option is not possible.\n "
                                "Try the commanď with one of these options: \n"
                                "Help: --help\n"
                                "Choices: All, Project, Criteria, "
                                "ToDo, Reference",
                        fg=styles.invalidfg,
                        bg=styles.invalidbg)  # noqa
    
    # Select the General Views
    def chooseviews(data: pd.DataFrame, choice: str) -> None:
        """Select the General Views.
        
        :param data: pd.DataFrame: Dataframe
        :param choice: str: Choice
        :return: None: Produces stdout"""
        if checks(choice) == App.views.Overviews:
            App.command_view(dataframe=data,
                             viewer=Head.OverviewViews,
                             label="Overview")  # noqa
        elif checks(choice) == App.views.Project:
            App.command_view(dataframe=data,
                             viewer=Head.ProjectView,
                             label="Project")
        elif checks(choice) == App.views.Criteria:
            App.command_view(dataframe=data,
                             viewer=Head.CriteriaView,
                             label="Criteria")
        elif checks(choice) == App.views.ToDos:
            App.command_view(dataframe=data,
                             viewer=Head.ToDoAllView,
                             label="Todos")
        elif checks(choice) == App.views.Reference:
            App.command_view(dataframe=data,
                             viewer=Head.ReferenceView,
                             label="Reference/Index")
        else:
            click.secho(message="No data viewable "
                                f"for the chosen option: {selects}",
                        fg=styles.warnfg,
                        bold=styles.warnbg)
    
    # Display The View Choice
    chooseviews(data=dataframe, choice=selects)
    # Update Global Data
    App.update_appdata(context=ctx, dataframe=dataframe)


# 3.0 Find: Locate: individual records from the bulk data
# Uses App.values.x.x(.x) String values for configuration.
@run.group(App.values.Find.cmd, short_help='Find Mode: Locate')
@click.pass_context
def find(ctx: click.Context) -> None:  # noqa
    """INTENT: Find: => ACTIONS/Commands: locate:
    
    === === === === === === === === === === === === ===\n
    \b
    Start Typing:
    - Use 'tab' to autocomplete the current menu option.
    - Then 'space' to start the sub-menu.
    - Then 'tab' or 'enter' complete. \n
    ___\n
    \b
    Hit 'enter' to enter the prompt sequence for option.
    Can use, e.g., `-o` flag on same line as command.
    However, prompt entery is preferred.\n
    ===\n
    \b
    ACTIONS/Commands:
    - locate
    ....'-i' index (range: 1 to last) | number only
    ....'-a' axis (default: index) | choose
    ===\n
    \b
    FUTURE: text search by 'column', 'row'.\n
    === === === === === === === === === === === === ===\n
    \f
    :param ctx: click.Context
    :return: None: Produces stdout --help text
    """
    
    click.secho(
            message="=====================FINDING MODE======================\n",
            fg='cyan', bg='white', bold=True)
    click.secho(
            message="===========Locate & Show Individual Records============\n",
            fg='cyan', bold=True)
    click.secho(
            message="Entering finding & reading mode for records.",
            fg='cyan', bg='white', bold=True)
    click.secho(message="Steps: \n"
                        "  1. Enter an find mode:                           \n"
                        "  2. Find a record:                                \n"
                        "  3. Enter a row's record index id, position nos.: \n"
                        "     Knowing a index/position is required.         \n"
                        "     Use Load -> ToDo or Load -> Views to id a row \n"
                        "  4. View an individual record, in a card format   \n"
                        "  5. Exits automatically.                          \n",
                fg='cyan', bold=styles.infobold, underline=True)
    click.secho(
            message="Prompts are available for each input.")
    App.update_appdata(context=ctx, dataframe=App.get_data())
    click.secho(
            message="Working data is now ... rehydrated.",
            blink=True)
    click.secho(
            message=f"You have rows 1 to {App.get_range} to work with",
            bold=styles.infobold)


# 3.1 Find: Locate: Index locations of an individual record
@find.group(name=App.values.Find.Locate.cmd, short_help='Find: Locate a record')
@click.option('--index', 'index',
              type=click.IntRange(
                      min=1,
                      max=App.get_range,
                      clamp=App.values.Find.Index.clamp),
              callback=Valid.index,
              help=f'{App.values.Find.Index.help}{App.get_range}: ',
              prompt=f'{App.values.Find.Index.help}{App.get_range}: ')
# Only one of these options is required, & search focus by index is the only feature.
# Future maintainability: for expanding search focuses: column, row.
@click.option('-a', '--axis', 'axis',
              type=click.Choice(choices=['index'],
                                case_sensitive=False),
              default='index',
              prompt=True,
              required=True)
@click.pass_context
def locate(ctx: click.Context, index: int,
           axis: str = Literal['index']) -> None:
    """Locate: a row: by index or searches term via index, column or row.
    
    \f
    :param ctx: click.Context
    :param index: int: The index of the row to locate
    :param axis: str: The axis to search in: Default: index
    :return: None: Display as stdout or stderr
    """
    debugOFF: bool = False  # noqa
    # Get the dataframe
    dataframe: pd.DataFrame = App.get_data()
    # If the axis is index, -a, --axis, then search the index
    if axis.lower() == 'index':
        # Get the result source
        resultframe = \
            Results.getrowdata(data=dataframe,
                               ix=index)
        # Check if the result is a single record
        if Record.checksingle(resultframe):
            # Debugging Flags
            debugON: bool = True  # noqa
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop. # noqa
            
            # Shows a result
            window.showrecord(data=resultframe,
                              debug=debugON)
        else:
            click.secho(message="The result is not a single record",
                        fg=styles.warnfg,
                        bold=styles.warnbold)  # noqa
    else:
        click.secho(message="Command did not run. Axes not implemented",
                    err=styles.toerror,
                    fg=styles.errfg,
                    bold=styles.errbold)  # noqa
    # Update appdata data
    App.update_appdata(context=ctx, dataframe=dataframe)


# 4. Edit: CUD Ops: Create, Read, Update, Delete.
# New (Add) | Create, Add commands -> None: by item, by row
@run.group(App.values.Edit.cmd, short_help='Edit Mode: Notes, & Progress')
@click.pass_context
def edit(ctx: click.Context) -> None:  # noqa: ANN101
    """Editing mode: enter editing for notes, todos, etc.
    
    === === === === === === === === === === === === ===\n
    \b
    Start Typing:
    - Use 'tab' to autocomplete the current menu option,
    - Then 'space' to start the sub-menu.
    - Then 'tab' or 'enter' to complete \n
    ___\n
    \b
    Hit 'enter' to enter the prompt sequence for option.
    Can use the, e.g., `-o` on same line as command.
    However the , prompt entery is preferred.\n.
    ===\n
    \b
    ACTIONS/Commands (and Options, Values):
    - note
    ....'-m' mode | choose: add, update, delete | required
    ....'-i' index | (range: 1 to last) | number only
    ....'-n' note | Enter short note, no limit. | required
    ....'-a' axis | choose: index | default: index
    - todo
    ....'-m' mode | choose: update | required
    ....'-i' index | (range: 1 to last) | number only
    ....'-s' status | choose: todo, not done | wip | done | required
    ....'-a' axis | choose: index | default: index
    \f
    :param ctx: click.Context
    :return: None: Display as stdout --help or when subcommands is called
    """
    click.secho(
            message="===================EDITING MODE========================\n",
            fg='blue', bold=True)
    click.secho(
            message="=====Find, Show & Edit, Save Individual Reccords=======\n",
            fg='blue', bold=True)
    click.secho(message="Entering editing mode for notes, todos, etc.         ",
                fg='blue', bg='white', bold=True)
    click.secho(message="Steps: \n"
                        "  1. Enter an edit mode:                           \n"
                        "  2. Find a record:                                \n"
                        "  3. Enter a row's record index id, position nos.: \n"
                        "     Knowing a index/position is required.         \n"
                        "     Use Load -> ToDo or Load -> Views to id a row \n"
                        "  4. Edit -> Notes by: add, update, delete or .....\n"
                        "  4. Edit -> Progress by: toggle: "
                        "ToDo, WIP, Done, Missed                            \n"
                        "  5. Save changes,                                 \n"
                        "  6. Exits automatically.                          \n",
                fg='blue', bold=styles.infobold,
                underline=True)
    click.secho(message="Prompts & Confirms used for a step by step process.")
    App.update_appdata(context=ctx, dataframe=App.get_data())
    click.secho(message="Working data is now ... rehydrated.", blink=True)
    click.secho(message=f"You have rows 1 to {App.get_range} to work with",
                bold=styles.infobold)


# 4.1 Edit: CRUD Ops: Read, Create Update, Delete:
# A Individual Record's Notes
@edit.command(App.values.Edit.Note.cmd, short_help='Edit: Modify a note')
@click.pass_context
# Edit Mode: add, update, delete
@click.option('--mode', 'mode',
              type=click.Choice(App.editmode,
                                case_sensitive=
                                App.values.Edit.Note.Mode.case),
              help=App.values.Edit.Note.Mode.help,
              callback=Valid.mode,
              prompt=App.values.Edit.Note.Mode.prompt,
              required=App.values.Edit.Note.Mode.required)
# Edit Mode: Row recorď to edit
@click.option('--index', 'index',
              type=click.IntRange(
                      min=App.values.Find.Index.min,
                      max=App.get_range,
                      clamp=App.values.Find.Index.clamp),
              callback=Valid.index,
              help=f'{App.values.Find.Index.help}{App.get_range}',
              prompt=f'BY ROW: ☑️ Select: 1 to {App.get_range}')
# Edit Mode: Note to link/append/clear to Row recorď on edit
@click.option('--note', 'note', type=str,
              help=App.values.Edit.Note.help,
              # callback=Valid.santitise,  # Callback: Input Validation: santitise
              prompt=App.values.Edit.Note.prompt)
# Edit Mode: Axis, or searchg focus, to locate record on.
@click.option('-a', '--axis', 'axis',
              type=click.Choice(choices=['index'],
                                case_sensitive=False),
              default='index',
              prompt=True,
              required=True)
def notepad(ctx,
            index: int,
            note: str,
            mode: str = Literal['add', 'update', 'delete'],
            axis: str = Literal['index', 'column', 'row']) -> None:
    """EDIT MODE: Notepad: Add, Update, Delete notes.
    
    \b
    ACTIONS/Commands (and Options, Values):
    - note
    ....'-m' mode | choose: add, update, delete | required
    ....'-i' index | (range: 1 to last) | number only
    ....'-n' note | Enter short note, no limit. | required
    ....'-a' axis | choose: index | default: index
    \f
    :param ctx: click.Context
    :param index: int: The index of the row to edit: 1 to Last row.
    :param note: str: The note to add, update, delete.
    :param mode: str: The mode to add, update, delete.
    :param axis: str: The axis to search in.
    :return: None: Display as stdout or stderr
    """
    # Debugging Flags
    debugON = True  # noqa
    # Rehydrtate dataframe from remote
    dataframe: pd.DataFrame = App.get_data()
    
    # - Check the index search focus (i.e. dimenson). Default: index
    # Only one dimension, i.e axis, is implemented: index,
    # Others are column, row: Future implementation.
    if axis.lower() == App.values.SEARCHFOCUS and note:
        # - Get the record
        resultframe = Results.getrowdata(data=dataframe,
                                         ix=index,
                                         debug=App.values.NOTRACING)
        if Record.checksingle(resultframe) and note is not None:
            # - Display the found result and - send to the editor
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=App.values.FORWARDING,
                                  displayon=App.values.HIDING,
                                  debug=App.values.NOTRACING)  # noqa
            # - Send the result to the editor
            if editing is not None:
                editor = Editor(
                        currentrecord=editing,
                        sourceframe=resultframe,
                        debug=App.values.NOTRACING)
                # - Edit note field of the record
                if index is not None:
                    click.secho(message="=====================================",
                                bg='white',
                                bold=True)
                    click.secho(message="Enter: edited mode: Notes",
                                blink=True)
                    # Edit Mode for Notes:
                    # Action/Tasks: Add/Insert, Update/Append, Delete/Clear
                    editor.editnote(edits=Valid.checkmode(edits=mode,
                                                          index=index),
                                    index=index,
                                    notepad=note,
                                    debug=App.values.NOTRACING)
                else:
                    click.secho(message="No changes made")
                    click.secho(message="Exiting: editing mode. No Note Added")
                # - Display the modified record
                click.secho(message="=====================================",
                            bg='white', bold=True)
                click.secho(message="Loading: edited record",
                            blink=True)
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype=Valid.checkcommand(mode),
                                    dataview='compare',
                                    debug=App.values.NOTRACING)
                # - Update the local app data
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
        else:
            click.secho(message="Exiting: editing mode: Adding a Note",
                        fg='bright_yellow',
                        bg='white',
                        bold=True)
        click.secho(message="=====================================",
                    bg='white', bold=True)
    else:
        click.secho(message="Try again, and use: \n"
                            "-m/--mode and select edit action: "
                            "add, update, delete\n"
                            "-i/--index and a number value\n"
                            "and axes: index",
                    fg='bright_yellow', bold=True)


# 4.1 Edit: CRUD Ops: Read, Create Update, Delete:
# A Individual Record's ToDo Status
@edit.command(App.values.Edit.ToDo.cmd, short_help='Edit: Toggle progress\' statuses')
@click.pass_context
@click.option('--index', 'index',
              type=click.IntRange(
                      min=App.values.Find.Index.min,
                      max=App.get_range,
                      clamp=App.values.Find.Index.clamp),
              callback=Valid.index,
              help=f'{App.values.Edit.ToDo.indexhelp}{App.get_range}: ',
              prompt=f'{App.values.Edit.ToDo.indexhelp}{App.get_range}: ')
@click.option('-status', 'status',
              type=click.Choice(choices=App.values.Edit.ToDo.Statuses,
                                case_sensitive=
                                App.values.Edit.ToDo.Status.case),
              help=App.values.Edit.ToDo.Status.help,
              prompt=App.values.Edit.ToDo.Status.prompt,
              required=App.values.Edit.ToDo.Status.required)
@click.option('-a', '--axis', 'axis',
              type=click.Choice(choices=['index'],
                                case_sensitive=False),
              default='index',
              prompt=True,
              required=True)
def progress(ctx: click.Context,
             index: int,
             status: str = Literal['Todo', 'WIP', 'Done', 'Missed'],
             axis: str = Literal['index', 'column', 'row']):
    """
    Edit a ToDo Status, on Progress column., by index.
    
    
    \f
    Progress and ToDo as reference names are related, with ToDo as an alias.
    
    :param ctx: click.Context: The click context
    :param index: int: The index of the record to edit
    :param status: str: The status of the ToDo: Todo, WIP, Done, Missed
    :param axis: str: The axis of the edit: index, column, row
    :return: None
    """
    # Debugging Flags
    dataframe: pd.DataFrame = App.get_data()
    
    # Check the index search focus (i.e. dimenson). Default: index
    # Only one dimension, i.e axis, is implemented: index,
    # Others are column, row: Future implementation.
    if axis.lower() == App.values.SEARCHFOCUS and status:
        # - Get the record
        resultframe = Results.getrowdata(data=dataframe,
                                         ix=index,
                                         single=App.values.SINGLE,
                                         debug=App.values.NOTRACING)
        if Record.checksingle(resultframe) \
                and Valid.checkstatus(status) is not None:
            # - Display the found result and - send to the editor
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=App.values.FORWARDING,
                                  displayon=App.values.HIDING,
                                  debug=App.values.NOTRACING)  # noqa
            # - Send the result to the editor
            if editing is not None:
                editor = Editor(
                        currentrecord=editing,
                        sourceframe=resultframe,
                        debug=App.values.NOTRACING)
                # - Edit note field of the record
                if index is not None:
                    click.secho(message="=================1====================",
                                bg='white',
                                bold=True)
                    click.secho(message="Enter: edited mode: ToDo & Progress",
                                blink=True)
                    # Edit Mode for Todos & Progress:
                    # Action/Tasks: Toggle/Progress Status:
                    # Todo, WIP, Done, Missed Valid.checktoggle(edits=mode)
                    # Moved the chckcing status lower to here, instead of Option
                    # Due to issues with callbacks and the REPL features
                    editor.editprogress(edits=App.values.Edit.ToDo.TOGGLE,
                                        index=index,
                                        choicepad=Valid.checkstatus(status),
                                        debug=App.values.TRACING)
                else:
                    click.secho(message="No changes made")
                    click.secho(message="Exiting: editing mode."
                                        " No Progress Updated")
                # - Display the modified record
                click.secho(message="=================2====================",
                            bg='white', bold=True)
                click.secho(message="Loading: edited record",
                            blink=True)
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='insert',
                                    dataview='compare',
                                    debug=App.values.NOTRACING)
                # - Update the local app data
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
        else:
            click.secho(message="Exiting: editing mode: Adding a Note",
                        fg='bright_yellow',
                        bg='white',
                        bold=True)
        click.secho(message="=====================================",
                    bg='white', bold=True)
    else:
        click.secho(message="Try again, and use: \n"
                            "-m/--mode and select edit action: "
                            "add, update, delete\n"
                            "-i/--index and a number value\n"
                            "and axes: index",
                    fg='bright_yellow', bold=True)


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
