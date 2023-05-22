#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, ANN001, D415, RET505, I001, F405, F403
"""Module: PyCriteria Terminal App."""
# 1. Std Lib
from typing import Literal

import click  # type: ignore
# 2. 3rd Party
import rich
import rich.panel
from click_repl import register_repl  # type: ignore
from pandas import pandas as pd, DataFrame, Series  # type: ignore
from rich import pretty, print as rprint  # type: ignore

# 3. Local: Note the controller * intentionally imports all from the module
from commands import AboutUsage, Commands
from controller import (Controller, DataController, ColumnSchema, Headers,
                        Display, WebConsole, configuration, gspread,
                        Record, Inner, Editor, )
from sidecar import AppValues, ProgramUtils

# Note: Move third-party import `gspread` into a type-checking block

# Global Modules/Objects
# 1.1 Commands.py
About: AboutUsage = AboutUsage()
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
    """View."""
    
    Load: list[str] = ["Load", "Begins", "Project", "Criteria",
                       "ToDo", "Reference", "Refresh"]
    Todo: list[str] = ["ToDo", "All", "Simple", "Done", "Grade", "Review"]
    
    def __init__(self):
        """Initialize."""
        pass


view: View = View()


class Window:
    """Window: Arrange Layouts, Panels, Cards."""
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def sendto(value, switch: bool) -> Record | None:
        """Switch Record."""
        if switch:
            return value
        else:
            return None
    
    @staticmethod
    def showrecord(data: pd.Series | pd.DataFrame,
                   dimensions: tuple[int, int] = (40, 20),
                   sendtoeditor: bool = False,
                   debug: bool = False) -> Record | None:
        """Display Record."""
        if debug:
            rprint("Debug Mode: Show Record\n")
            rprint(data)
        elif data.empty is False:
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop.
            individual = Record(series=data, source=data)
            
            if not debug:
                rprint("Trace Mode: Show Record\n")
                rprint(individual)
            
            if individual.card(consolecard=Webconsole.console) is not None:
                # panel: rich.panel.Panel = individual.display(
                # consoledisplay=Webconsole.console,
                # sizing=dimensions,
                # sendtolayout=True)
                # Webconsole.console.print(panel)
                # Webconsole.terminal.updates(renderable=panel, target="current")
                # Webconsole.terminal.laidout(Webconsole.console)
                click.echo("========Displaying Full Card========")
                click.echo("=====================================")
                individual.header(Webconsole.console)
                individual.editable(Webconsole.console)
                individual.footer(Webconsole.console)
                click.echo("=================END================")
            else:
                click.echo("Displaying Simple Card")
                individual.card(consolecard=Webconsole.console)
            
            return Window.sendto(individual, sendtoeditor)
    
    @staticmethod
    def showedited(editeddata: pd.Series | pd.DataFrame,
                   dimensions: tuple[int, int] = (40, 20),
                   sendtoeditor: bool = False,
                   debug: bool = False) -> Record | None:
        """Display Edited Record."""
        if debug:
            rprint(editeddata)
        elif editeddata.empty is False:
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop.
            individual = Record(source=editeddata)
            if individual.card(consolecard=Webconsole.console) is not None:
                # panel: rich.panel.Panel = individual.display(
                # consoledisplay=Webconsole.console,
                # sizing=dimensions,
                # sendtolayout=True)
                # Webconsole.console.print(panel)
                # Webconsole.terminal.updates(renderable=panel, target="current")
                # Webconsole.terminal.laidout(Webconsole.console)
                individual.header(Webconsole.console)
                individual.editable(Webconsole.console)
                individual.footer(Webconsole.console)
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
        """Display Modified Record."""
        # Display single records
        if Record.checksingle(editeddata):
            if editor.ismodified and editor.lasteditmode == commandtype:
                if debug:
                    click.echo(message="==========Displaying: Changes=========\n")
                # 1. Display the Edited record
                if dataview == 'show':
                    window.showedited(editeddata=editeddata, debug=debug)
                elif dataview == 'compare':
                    window.comparedata(editeddata=editeddata,
                                       editor=editor,
                                       debug=False)
                #  [DEBUG]
                if debug:
                    click.echo(message="=== [DEBUG] Saving: changes made [DEBUG]==\n")
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
        shown: bool = True
        if debug:
            rprint(editeddata)
            rich.inspect(editeddata)
        elif editeddata.empty is False and editor.ismodified:
            oldrecord: Record = editor.record
            newrecord: Record = Record(series=editor.newresultseries)
            # 1. Display the Edited record
            
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
                newrecord.header(consolehead=Webconsole.console,
                                 gridfit=True)
                newrecord.comparegrid(container=Webconsole.table,
                                      left=left,
                                      right=right,
                                      fit=True)
                newrecord.footer(consolefoot=Webconsole.console,
                                 expand=False)
            else:
                window.showedited(editeddata=editeddata, debug=debug)


window: Window = Window()


class CriteriaApp:
    """PyCriteria Terminal App."""
    
    values: AppValues
    
    def __init__(self, values: AppValues):
        """Initialize."""
        self.values = values
    
    @staticmethod
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs."""
        root: str = "BASE: Run"
        click.echo(message="Navigation: CLI: > Run > ... [Intent] > [Action]\n")
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
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    @staticmethod
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        WebConsole.table = Webconsole.set_datatable(dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=Webconsole.console,
                              consoletable=Webconsole.table,
                              headerview=Head.OverviewViews)
    
    @staticmethod
    def update_appdata(context, dataframe: pd.DataFrame) -> None:
        """Update the app data."""
        context.obj = dataframe
        DataControl.dataframe = dataframe
    
    @staticmethod
    def display_view(dataframe: pd.DataFrame,
                     viewer: list[str] = None,
                     label: str = 'Overview') -> None:
        """Display the dataframe."""
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
        """Display the dataframe by view option."""
        
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
        """Query the dataframe."""
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
        """Search the dataframe."""
        searchresult: pd.DataFrame = \
            frame[frame[label].astype(str).str.contains(searchstr,
                                                        case=case)]
        
        if echos:
            click.echo(
                    message=f'The rows with "{searches}" in column\'s'
                            f' "{label}" are:\n {searchresult}')
        
        return searchresult
    
    @staticmethod
    def byposition(frame: pd.DataFrame,
                   position: str) -> pd.DataFrame | None:
        """Filter the dataframe."""
        mask: pd.DataFrame | pd.Series = \
            frame.apply(lambda column: column.astype(str).str.contains(position))
        
        result: pd.DataFrame | None
        if isinstance(mask, pd.DataFrame):
            result: pd.DataFrame = frame.loc[mask.any(axis=1)]
        elif isinstance(mask, pd.Series):
            result: pd.DataFrame = frame[mask]
        elif frame[position].any():
            result: pd.DataFrame = frame
        else:
            click.echo(message=f'No results found for "{position}"',
                       err=True)
            return None
        
        return result
    
    @staticmethod
    def search_rows(frame: pd.DataFrame,
                    searchterm: str,
                    exact: bool = False) \
            -> pd.DataFrame | None:
        """Search across all columns for the searches team"""
        if searchterm is None or isinstance(searchterm, str):
            return None
        # Search across all columns for the searches text/str value
        mask = frame.apply(lambda column: column.astype(str).str.contains(searchterm))
        #
        if exact:
            return frame.loc[mask.all(axis=1)]
        
        return frame.loc[mask.any(axis=1)]
    
    @staticmethod
    def rows(frame: pd.DataFrame,
             index: int = None,
             searchterm: str = None,
             strict: bool = False,
             zero: bool = True) \
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
            
        return pd.DataFrame | None: - Expect a result or None
        """
        result: pd.DataFrame | pd.Series | None
        if index:
            result = App.index(frame=frame, index=index, zero=zero)  # noqa
        elif searchterm:
            # Search across all columns for the position value
            result = App.search_rows(frame=frame, searchterm=searchterm, exact=strict)
            if result.empty is not False:
                click.echo(f"Found: {result}")
            else:
                click.echo(f"Could not find {search}")
        else:
            click.echo("Please provide either an index or searches term")
            return None
        
        return result
    
    @staticmethod
    def index(frame: pd.DataFrame,
              index: int = None,
              zero: bool = True) \
            -> pd.DataFrame | pd.Series | None:
        """Get the index from the dataframe."""
        if zero and index is not None:
            result = frame.iloc[index - 1] \
                if index >= 0 else frame.iloc[index]
            click.echo(f"Found: {result} for zero index {index - 1}")
            return result
        elif not zero and index is not None:
            result = frame.iloc[index] \
                if index > 0 else frame.iloc[index]
            click.echo(f"Found: {result} for standard index {index}")
            return result
        else:
            click.echo(f"Could not find index {index}")
            return None
    
    @staticmethod
    def value(frame: pd.DataFrame | pd.Series,
              row: int = None,
              column: int | str = None,
              direct: bool = False) -> str | None:
        """Get the value from the dataframe."""
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
        """Get the results from the query."""
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
    """Checks."""
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def isnot_context(ctx: click.Context) -> bool:
        """Tests dataframe context."""
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
        """
        return isinstance(ctx, pd.DataFrame) if True else False
    
    @staticmethod
    def isnot_querytype(header: str,
                        query: str) -> bool:
        """Tests Search Query."""
        return not isinstance(header, str) or not isinstance(query, str)
    
    @staticmethod
    def is_querycomplete(header: str,
                         query: str) -> bool:
        """Tests for Empty Serach."""
        return header is not None or query is not None
    
    @staticmethod
    def compare_frames(olddata: pd.DataFrame, newdata: pd.DataFrame) -> bool:
        """Compare dataframes."""
        diff = olddata.compare(newdata, keep_shape=True, keep_equal=True)
        if not diff.empty:
            click.echo(message="Updated refreshed/rehydrated data")
            rprint(diff, flush=True)
            return False
        
        click.echo(message="No changes in refreshed/rehydrated data")
        return True
    
    @staticmethod
    def santitise(s: str) -> str | None:
        """Sanitise strings."""
        empty: str = ''
        if s != empty and isinstance(s, str):
            return s.strip() if s else None
        else:
            click.echo(message="Searching by index only. No keywords.")
            return None


Guard: Checks = Checks()


class Results:
    """Results."""
    
    def __init__(self):
        """Initialize."""
        pass
    
    @staticmethod
    def getrowframe(data: pd.DataFrame,
                    ix: int, st: str, debug: bool = False) -> pd.Series | pd.DataFrame | None:
        """Get a row from a dataframe by index or searches term."""
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
                click.echo(f"GetRowFrame(): Found a set of records")
                rich.inspect(result)
            return result
        else:
            click.echo(f"GetRowFrame(): Found something: undefined")
            if debug:
                rich.inspect(result)
            return None


@click.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx) -> None:
    """Level: Run. Type: about to learn to use this CLI.
    
    """
    # App.crumbs(context=ctx)
    appdata: pd.DataFrame = App.get_data()
    App.update_appdata(context=ctx, dataframe=appdata)


@run.group(name='about')
@click.pass_context
def about(ctx) -> None:
    """About. A Man page for this CLI."""
    
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > About'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up a level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    crumbs(context=ctx)
    # Man Page
    AboutUsage.describe_usage()
    rprint("========================================")
    AboutUsage.example_usage()
    rprint("========================================")
    AboutUsage.loadmodel_usage()
    AboutUsage.findmodel_usage()
    AboutUsage.selectmodel_usage()
    rprint("========================================")
    AboutUsage.addmodel_usage()
    AboutUsage.updatemodel_usage()
    AboutUsage.deletemodel_usage()


# 1. Load Data: Have the user load the data:
# A) The app initialies a remote google connection;
# B) Loads Intent intentionally allows the user to load the data.
@run.group(name=AppValues.Load.cmd)
@click.pass_context
def load(ctx) -> None:
    """Load data from the current context, intentionally.
    
    a) Get the dataframe from remote
    b) Check context for dataframe if is/is not present
    c) Display dataframe accoridngly
    
    :param ctx: click.Context
    :return: None: Produces stdout
    """
    #
    # crumbs(context=ctx)
    ctx.obj = App.get_data()


@load.command(name='begins')
@click.pass_context
def begins(ctx) -> None:
    """Begin/Initiated/.
    
    :param ctx: click.Context: Passed Object, by pass_context.
    :return: None - Produces stdout output
    """
    #
    dataframe: pd.DataFrame = App.get_data()
    App.display_data(dataframe=dataframe)
    App.update_appdata(context=ctx, dataframe=dataframe)


@load.command(name=AppValues.Load.refresh)
@click.pass_context
def refresh(ctx: click.Context) -> None:
    """Load core / client side datasets (data frame).
    
    :param ctx: click.Context
        Assumes that the dataframe is already loaded in the root cmd context
    :return: None
    """
    # App.crumbs(context=ctx)
    df_ctx: pd.DataFrame = App.get_data()
    if df_ctx is not None:
        # Core Datasets
        currentdataframe: pd.DataFrame = DataControl.dataframe
        newdataframe: pd.DataFrame = App.get_data()
        # Test for changes
        if Guard.compare_frames(currentdataframe, newdataframe):
            # Display Current/Old Dataframe:
            # a: Display the dataframe, b: Update appdata
            App.display_view(dataframe=currentdataframe,
                             viewer=Head.OverviewViews)
            App.update_appdata(context=ctx, dataframe=newdataframe)
        else:
            # Display New Dataframe:
            # a: Display the dataframe, b: Update appdata
            App.display_view(dataframe=newdataframe,
                             viewer=Head.OverviewViews)
            App.update_appdata(context=ctx, dataframe=newdataframe)
    else:
        rprint("No data loaded.")


@load.command(name=AppValues.Load.projects)
@click.pass_context
def project(ctx) -> None:
    """Load Projects. (data frame)."""
    # crumbs(context=ctx)
    dataframe: pd.DataFrame = App.get_data()
    App.display_view(dataframe=dataframe,
                     viewer=Head.ProjectView,
                     label="Project")
    App.update_appdata(context=ctx, dataframe=dataframe)


@load.command(name=AppValues.Load.criterias)
@click.pass_context
def criteria(ctx) -> None:
    """Load project (metadata)."""
    # crumbs(context=ctx)
    dataframe: pd.DataFrame = App.get_data()
    App.display_view(dataframe=dataframe,
                     viewer=Head.CriteriaView,
                     label="Criteria")
    App.update_appdata(context=ctx, dataframe=dataframe)


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
    """Load todos, and Display different filters/views."""
    # App.crumbs(context=ctx)
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
        rprint(f"You entered the wrong option: {display.lower()}\n"
               f"Please try again@ All, Simple, Done, Grade or Review")  # noqa
    
    finally:
        App.update_appdata(context=ctx, dataframe=dataframe)


load.add_command(todo)


@load.command(AppValues.Load.references)
@click.pass_context
def reference(ctx) -> None:
    """Load Reference/Index."""
    # crumbs(context=ctx)
    dataframe: pd.DataFrame = App.get_data()
    App.display_view(dataframe=dataframe,
                     viewer=Head.ReferenceView,
                     label="Reference/Index")
    App.update_appdata(context=ctx, dataframe=dataframe)


@load.command("views", help="Load views. Select views to Display.")
@click.option('-d', '--Display',
              type=click.Choice(choices=view.Load),
              default='All', show_default=True)
@click.pass_context
def views(ctx, display) -> None:
    """Load Reference/Index."""
    # crumbs(context=ctx)
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
def find(ctx: click.Context) -> None:
    """Find: Find item, row(s), column(s)."""
    # crumbs(context=ctx)
    dataframe: pd.DataFrame = App.get_data()
    App.update_appdata(context=ctx, dataframe=dataframe)


@find.command("keyword", help="Load todo list. Select views to Display.")
@click.pass_context
@click.option('-q', '--query',
              type=str,
              default='All',
              show_default=True,
              help="Keyword to searches")
@click.option('-s', '--selects',
              type=click.Choice(Head.ToDoChoices),
              default='All',
              show_default=True,
              help="Choose a option: from All, Simple, Done, Grade, Review")
def keyword(ctx, query: str, selects: str) -> None:
    """Load todos, and Display different filters/views."""
    #
    sourcedata: pd.DataFrame = App.get_data()
    filteredata: pd.DataFrame = \
        App.query_data(dataframe=sourcedata, querystring=query)
    resultsvalues: pd.DataFrame = \
        App.get_results(sourceframe=sourcedata, filterframe=filteredata)
    #
    try:
        if selects is not None:
            App.display_todo(dataframe=filteredata, viewoption=selects)
            rich.print('Retrive: intersect of rows/cols\n'
                       f" {resultsvalues}\n")
        else:
            App.display_todo(dataframe=filteredata)
    except TypeError:
        App.display_todo(dataframe=App.get_data())
        rich.print(f"You entered the wrong option: {selects.lower()}\n"
                   f"Please try again@ All, Simple, Done, Grade or Review")
    
    App.update_appdata(context=ctx, dataframe=sourcedata)


load.add_command(keyword)


@find.command(name="searches",
              help="Search: a column: by column name and single word query.")
@click.option('--header', type=str,
              help='Column\'s header label to searches')
@click.option('--query', type=str,
              help='String query to searches for')
@click.pass_context
def search(ctx: click.Context, header: str, query: str) -> None:
    """Search: a column: by header and query.
    
    :param ctx: click.Context
    :param header: str: Column's header label to searches
    :param query: str: String query to searches for
    :return: None: Display as stdout or stderr
    """
    # Checks query completness and Context, and DF Typing/Existence
    sourcedata: pd.DataFrame = App.get_data()
    searchresult: pd.DataFrame
    # crumbs(context=ctx)
    if Guard.is_querycomplete(header=header, query=query):
        # Result from a query, and asusrances, as feedback
        searchresult: pd.DataFrame = App.search_data(frame=sourcedata,
                                                     label=header,
                                                     searchstr=query)
        # Build the Queryset: header, query, searchresult for Display
        Display.display_data(dataframe=searchresult,
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
    else:
        click.echo(message="Command did not run", err=True)
    
    App.update_appdata(context=ctx, dataframe=sourcedata)


run.add_command(search)


@find.command(name="searches")
@click.option('-l', '--label',
              type=click.Choice(Head.HeadersChoices),
              default='Criteria',
              show_default=True,
              prompt=True,
              help="Select label: Position, DoD, Performance, "
                   "Criteria, Progress, Notes.")
@click.option('-q', '--query', type=str,
              help='Use a single Keyword')
@click.pass_context
def searches(ctx: click.Context, label: str, query: str) -> None:
    """Search: a column: by header and query.

    :param ctx: click.Context:
    :param label: str: The Column label to pick from
    :param query: str: String query to searches for
    :return: None: Display as stdout or stderr
    """
    # Not rasing errors, gently reminding/correcting user to enter correct data
    if Guard.isnot_querytype(header=label, query=query):
        click.echo(message="Please use text for header's name and query")
        return
    
    # Checks query completness and Context, and DF Typing/Existence
    sourcedata: pd.DataFrame = App.get_data()
    searchresult: pd.DataFrame
    # crumbs(context=ctx)
    if Guard.is_querycomplete(header=label, query=query):
        # Result from a query, and asusrances, as feedback
        searchresult: pd.DataFrame = App.search_data(frame=sourcedata,
                                                     label=label,
                                                     searchstr=query)
        # Build the Queryset: header, query, searchresult for Display
        Display.display_data(dataframe=searchresult,
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
    else:
        click.echo(message="Command did not run", err=True)
    
    App.update_appdata(context=ctx, dataframe=sourcedata)
    return


run.add_command(searches)


@find.command(name="locate", help="Locate row(s), via index, column, row.")
@click.option('-s', '--searches', 'searche', type=str,
              help='Search for a string in the dataframe',
              prompt=True,
              default='')
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help=f'Select between 1 and f{len(DataControl.dataframe)}',
              prompt=True)
@click.option('-a', '--axis',
              type=click.Choice(['index', 'column', 'row'],
                                case_sensitive=False),
              help='Choose axis to seach in/by. Default: row',
              default='row',
              prompt=True,
              required=True)
@click.pass_context
def locate(ctx: click.Context, index: int, searche: str,
           axis: str = Literal['index', 'column', 'row']) -> None:
    """Locate: a row: by index or searches term via index, column or row."""
    searchterm: str = Guard.santitise(searche)
    
    # Define the function to get the row frames
    def getrowframe(data: pd.DataFrame,
                    ix: int, st: str) -> pd.Series | pd.DataFrame | None:
        """Get a row from a dataframe by index or searches term."""
        if ix and not st:
            result = App.rows(frame=data, index=ix)
            rich.inspect(result)
        elif ix and st:
            result = App.rows(frame=data, index=ix, searchterm=st)
        elif not ix and st:
            result = App.rows(frame=data, searchterm=st)
        else:
            return None
        
        if isinstance(result, pd.Series):
            click.echo(f"Found a record")
            return result
        elif isinstance(result, pd.DataFrame):
            click.echo(f"Found a set of records")
            return result
        else:
            click.echo(f"Found something: undefined")
            return None
    
    # Get the dataframe
    dataframe: pd.DataFrame = App.get_data()
    if axis.lower() == 'index':
        resultframe = \
            getrowframe(data=dataframe, ix=index, st=searchterm)
        
        # if isinstance(resultframe, pd.Series):
        # click.echo(f"Found: \n {getrowframe(data=dataframe, ix=index, st=searchterm)}")
        # click.echo(resultframe.values)
        # rich.inspect(resultframe)
        # return None
        
        if Record.checksingle(resultframe):
            # Individual record holds the singular record, handles displays
            # Selecting different calls on the individual record yields
            # different displays/outputs.
            # Only displays a pd.Series, implicitly.
            # Not designed for results >1, unless part of a loop. # noqa
            window.showrecord(data=resultframe, debug=True)
        
        else:
            click.echo(message="The result is not a single record")
    elif axis.lower() == 'column':
        click.echo(message="Please use the searches command to searches columns")
    elif axis.lower() == 'row' and searchterm is not None:
        resultframe: pd.DataFrame = \
            getrowframe(data=dataframe, ix=index, st=searchterm)
        rich.print(resultframe)
        # App.display_todo(dataframe=resultframe)
    else:
        click.echo(message="Command did not run. Invalid axis", err=True)
    
    App.update_appdata(context=ctx, dataframe=dataframe)


run.add_command(locate)


# CRUD: Create, Read, Update, Delete.

# New (Add) | Create, Add commands -> None: by item, by row
@run.group("edit🎬", help="🎬 Edit: Enter editing mode. 🎬")
@click.pass_context
def edit(ctx: click.Context) -> None:  # noqa: ANN101
    """Editing mode: enter editing for notes, todos, etc."""
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
              help='Optionally leave blank when searching by a string, i.e. searches\n'
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
    """Add a new note to a record

    Append by a location/coordinate.
    """
    debugON = True
    debugOFF = False
    # A) Rehydrtate dataframe from remote
    dataframe: pd.DataFrame = App.get_data()
    # B) Search by index (-i, --index option, default/only choice)
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
                if index is not None:
                    editor.addingnotes(notes=note,
                                       location=index,
                                       debug=debugOFF)
                else:
                    editor.addingnotes(notes=note, debug=debugOFF)
                # Display Record with Modified Data
                click.echo(message=f"=====================================")
                click.echo(message=f"Loading: edited record")
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='insert',
                                    dataview='compare',
                                    debug=debugON)
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            # Else, exit
            else:
                click.echo(message=f"Exiting: editing mode")
        # Bulk Editing not possible.
        else:
            click.echo(message="The result is not a single record", err=True)
    # Features Flag: Text Searches Branch. Future to implement.
    else:
        click.echo(message="Text searches is not yet implemented\n"
                           "Use searches with no input\n"
                           "Try again, using -i/--index and a number value"
                           "and axes: index")


@edit.command("updatenote🔂", help="🔂 Append a note in current record's note 🔂")
@click.pass_context
@click.option('-s', '--searches', 'searche', type=str,
              help='SEARCH TERM:✋ Leave blank if known location/row, i.e. index\n'
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
              prompt=f'BY ROW: ☑️ MUST: Select between 1 and {len(DataControl.dataframe)}: ')
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
    """Update to a record

    Append by a location/coordinate.
    """
    # Fetch the dataframe
    dataframe: pd.DataFrame = App.get_data()
    if axis.lower() == 'index':
        resultframe = Results.getrowframe(data=dataframe,
                                          ix=index,
                                          st=Guard.santitise(searche))
        if Record.checksingle(resultframe) and note is not None:
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=True)  # noqa
            if editing is not None:
                editor = Editor(currentrecord=editing,
                                sourceframe=resultframe)
                if index is not None:
                    editor.updatingnotes(notes=note,
                                         location=index)
                else:
                    click.echo(message=f"No changes made")
                    click.echo(message=f"Exiting: editing mode")
                # Display Record with Modified Data
                click.echo(message=f"Loading: edited record")
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='append')
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            else:
                click.echo(message=f"Exiting: editing mode")
        else:
            click.echo(message="The result is not a single record", err=True)
    else:
        click.echo(message="Text searches is not yet implemented\n"
                           "Use searches with no input\n"
                           "Try again, using -i/--index and a number value"
                           "and axes: index")


@edit.command("deletenote🗑️", help="🗑️Clears the note(s) from a record's line/row🗑️")
@click.pass_context
@click.option('-s', '--searches', 'searche', type=str,
              help='SEARCH TERM:✋ Leave blank if known location/row, i.e. index\n'
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
              prompt=f'BY ROW: ☑️ Select between 1 and {len(DataControl.dataframe)}: ',
              required=True)
@click.option('-n', '--note', 'note', type=str,
              help='NOTE: ⭕ Clears the note. Hit Enter. Default:  , a blank string',
              prompt="NOTE: ⭕ ⬇️ Hit enter, to continue: ",
              confirmation_prompt="This will delete the note, ⬇️ hit enter, no input:",
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
    """Delete item: Find an item.

    Clear the item's content/reset to default.
    """
    dataframe: pd.DataFrame = App.get_data()
    if axis.lower() == 'index' and searche == '':
        click.echo(f"🗑️ Deleting a Note, in {index}...🗑️")
        resultframe = Results.getrowframe(data=dataframe,
                                          ix=index,
                                          st=Guard.santitise(searche))
        if Record.checksingle(resultframe) and note is not None:
            editing = \
                window.showrecord(data=resultframe,
                                  sendtoeditor=True)  # noqa
            if editing is not None:
                editor = Editor(currentrecord=editing,
                                sourceframe=resultframe)  # noqa
                if index is not None:
                    editor.deletingnotes(notes=note, location=index)
                else:
                    editor.deletingnotes(notes=note)
                click.echo(message=f"Loading: edited record")
                window.showmodified(editeddata=editor.newresultseries,
                                    editor=editor,
                                    commandtype='clear')
                App.update_appdata(context=ctx,
                                   dataframe=editor.newresultframe)
            else:
                click.echo(message=f"Exiting: editing mode: no deletes made")
        else:
            click.echo(message="The result is not a single record \n"
                               "Try again.", err=True)
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
    click.echo(message="PyCriteria: A simple CLI for managing Code Institute's criteria\n"
                       "=================================================================\n"
                       "\n"
                       "GETTING STARTED\n"
                       "Type --help to get started\n"
                       "Hold ctrl + d to exit \n"
                       "Hold ctrl + c to abort \n"
                       "Tab completion is available\n"
                       "\n"
                       "=================================================================\n"
                       "\n"
                       "CLI COMMANDS / REPL\n"
                       "1: BASE: run (app.py). INFO only.\n"
                       "2: INTENT: (load, find, add, update, delete). INFO only.\n"
                       
                       "3: ACTION: per INTENT the actionable sub-commands with options\n"
                       "4: OPTIONS: per ACTION the options to perform the action\n"
                       "NB: Each command can have multiple options\n"
                       "\n"
                       "=================================================================\n"
                       "\n"
                       "CLI DATA: REMOTE & LOCAL\n"
                       "DATA: The data remotely pulled from Google Sheets (the remote).\n"
                       "NB: Each command rehydrates/refreshes local data from the remote.\n"
                       "  - This rehydration pattern is more expensive per command.\n"
                       "  - It does ensure most recent data is pulled from the remote.\n"
                       "  - An app local copy is stored globally, and updated per command.\n"
                       "  - A scoped copy is used per command as active data.\n"
                       "\n"
                       "=================================================================\n"
                       "\n"
                       "CLI ENVIRONMENT & MAKING MISTAKES\n"
                       "This CLI runs within its own sub shell/enviornment/REPL.\n"
                       " - 🚧 As such it is tollerant to user input and user errors. 🚧\n"
                       " - There will be commands input errors, as with any cli app.\n"
                       " - These types of errors are part of the cli environment/repl.\n"
                       " - Just try the command again, and enter in the correct input.\n"
                       "\n"
                       "=================================================================\n"
                       "\n"
                       "CLI COMMANDS & OPTIONS\n"
                       "CLI uses multi-level command structure, similar to 'aws cli'.\n"
                       " - This means that you can type a ACTION command and EITHER: \n"
                       " a) then hit enter to enter a prompts sequence, to enter values.\n"
                       " OR \n"
                       " b) at a ACTION enter using -o or --option then a value/input\n"
                       "    - e.g. '-o' with single hyphen is same as '--option'.\n"
                       " NB: 'o' or 'option' is for illustrative purposes only\n"
                       "\n"
                       "=================================================================\n"
                       "QUICK START\n"
                       "\n"
                       "Get started by typing: either --help or load, find, edit"
                       "\n"
                       "Use 'tab' when typing in command's first letters for autocomplete\n"
                       "\n"
                       "Then press 'space' to show the subcommands sub-menus\n")  # noqa
    run()
