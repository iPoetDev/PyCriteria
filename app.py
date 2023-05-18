#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, D415
"""Module: PyCriteria Terminal App."""
# 1. Std Lib
import typing
import warnings
from typing import NewType, Optional

# 2. 3rd Party
import click
import gspread  # noqa: TCH002
import pandas as pd
import rich
from click_repl import register_repl  # type: ignore
from rich import pretty  # type: ignore

# 3. Local
from commands import AboutUsage, Commands
from controller import (ColumnSchema, Controller, DataController, Display, Entry, Headers, WebConsole, configuration,
                        rprint, )
from sidecar import AppValues, ProgramUtils

# Note: Move third-party import `gspread` into a type-checking block

# Global Modules/Objects
About: AboutUsage = AboutUsage()

Commands: Commands = Commands()
Actions: Controller = Controller()
AppValues: AppValues = AppValues()
DataControl: DataController = DataController(Actions.load_wsheet())
Columns: ColumnSchema = ColumnSchema()
Head: Headers = Headers(labels=Columns)
Display: Display = Display()
Entry: Entry = Entry()
Webconsole: WebConsole = WebConsole(configuration.Console.WIDTH,
                                    configuration.Console.HEIGHT)
ContextObject = NewType('ContextObject', Optional[object])

pretty.install()


class CriteriaApp:
    """PyCriteria Terminal App."""
    
    values: AppValues
    
    def __init__(self):
        """Initialize."""
        self.values = AppValues()


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
        www.perplexity.ai/search/a2f9c214-11e8-4f7d-bf67-72bfe08126de?s=c
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


class ViewFilter:
    """View Filters."""
    
    def __init__(self):
        """Initialize."""
        pass
    
    ProjectView: str = "ProjectView"


@click.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx) -> None:
    """Level: Run. Type: about to learn to use this CLI.
    
    Enter: $python app.py about
    This CLI has a multi-level command structure.
    https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html
    """
    click.echo(message="Navigation: CLI: > Run > ... [Intent] > [Action]\n")
    click.echo(message=f'You are here: {ctx.info_name} \n')
    
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message="Navigation: CLI: > Run* > ... [Intent] > [Action]\n"
                           f'*: You are here: {crumb.title()}\n'
                           f'To go up a level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    # crumbs(context=ctx)
    ctx.obj = get_data()


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
    
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > {crumb.title()}*'
                           f'> [ACTION]\n *: You are here: {crumb.title()}\n'
                           f'To go up a level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    # crumbs(context=ctx)
    ctx.obj = get_data()
    # rich.inspect(ctx.obj)
    # rich.print(f'Context: {ctx.obj}')
    # click.echo(message=f' data: {ctx.obj}')


@load.command(name='begins')
@click.pass_context
def begins(ctx) -> None:
    """Begin/Initiated/.
    
    :param ctx: click.Context: Passed Object, by pass_context.
    :return: None - Produces stdout output
    """
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        WebConsole.table = Webconsole.set_datatable(dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=Webconsole.console,
                              consoletable=Webconsole.table)
    
    # Check Context and Display acoordingly
    # rich.inspect(ctx)
    
    # Display Dataframe
    # crumbs(context=ctx)
    display_data(dataframe=get_data())


@load.command(name=AppValues.Load.refresh)
@click.pass_context
def refresh(ctx: click.Context) -> None:
    """Load core / client side datasets (data frame).
    
    According to current (root?) context, refreshes the (as Pandas) Dataframe
    a) Refreshes the data from the source (Google Sheets) to a new dataframe.
    b) Compares the old dataframe to the new dataframe.
    c) If there are no changes,
        i: Displays the old dataframe.
        ii: Reloads the old dataframe to current context
    d) If there are changes,
        i: displays the changes,
       ii: updates the old dataframe with the new dataframe in current context.
    
    :param ctx: click.Context
        Assumes that the dataframe is already loaded in the root cmd context
    
    :return: None
    """
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')

    # Get Remote Sheet afresh
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=Actions.load_wsheet())
        return dataframe

    #
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        headers: list[str] = Head.OverviewViews
        Webconsole.table = Webconsole.configure_table(headers=headers)
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=headers,
                                 viewfilter='Overview')
        click.echo(message='Your data is refreshed/rehydrated')

    #
    def update_appdata(context, dataframe: pd.DataFrame) -> None:
        """Update the app data."""
        context.obj = newdataframe
        DataControl.dataframe = dataframe

    # crumbs(context=ctx)
    df_ctx: pd.DataFrame = get_data()
    if df_ctx is not None:
        # Core Datasets
        currentdataframe: pd.DataFrame = DataControl.dataframe
        newdataframe: pd.DataFrame = get_data()

        # Compare Frames Inner Function
        def compare_frames(olddata: pd.DataFrame, newdata: pd.DataFrame) -> bool:
            """Compare dataframes."""
            diff = olddata.compare(newdata, keep_shape=True, keep_equal=True)
            if not diff.empty:
                click.echo(message="Updated refreshed/rehydrated data")
                rprint(diff, flush=True)
                return False

            click.echo(message="No changes in refreshed/rehydrated data")
            return True

        # Test for changes
        if compare_frames(currentdataframe, newdataframe):
            # Display Current/Old Dataframe:
            # a: Display the dataframe, b: Update appdata
            display_data(dataframe=currentdataframe)
            update_appdata(context=ctx, dataframe=newdataframe)
        else:
            # Display New Dataframe:
            # a: Display the dataframe, b: Update appdata
            display_data(dataframe=newdataframe)
            update_appdata(context=ctx, dataframe=newdataframe)
    else:
        rprint("No data loaded.")


@load.command(name=AppValues.Load.projects)
@click.pass_context
def project(ctx) -> None:
    """Load Projects. (data frame)."""
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        headers: list[str] = Head.ProjectView
        Webconsole.table = Webconsole.configure_table(headers=headers)
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=headers,
                                 viewfilter='Project')
    
    # crumbs(context=ctx)
    display_data(dataframe=get_data())


@load.command(name=AppValues.Load.criterias)
@click.pass_context
def criteria(ctx) -> None:
    """Load project (metadata)."""
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        headers: list[str] = Head.CriteriaView
        Webconsole.table = Webconsole.configure_table(headers=headers)
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=headers)
    
    crumbs(context=ctx)
    display_data(dataframe=get_data())


@load.command("todo", help="Load todo list. Select views to display.")
@click.pass_context
@click.option('-d', '--display',
              type=str,
              default='All',
              show_default=True,
              help="Choose a display: from All, Simple, Done, Grade, Review")
@click.option('-s', '--selects',
              type=click.Choice(Head.ToDoChoices),
              default='All',
              show_default=True,
              help="Choose a option: from All, Simple, Done, Grade, Review")
def todo(ctx, display: str, selects: str) -> None:
    """Load todos, and display different filters/views."""
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame, viewoption: str = 'All') -> None:
        """Display the dataframe by view option."""
        
        def select_view(view: str) -> list[str]:
            """Select the view."""
            if view.lower() == 'All'.lower():
                headers: list[str] = Head.ToDoAllView
            elif view.lower() == 'Simple'.lower():
                headers: list[str] = Head.ToDoDoDView
            elif view.lower() == 'Done'.lower():
                headers: list[str] = Head.ToDoGradeView
            elif view.lower() == 'Grade'.lower():
                headers: list[str] = Head.ToDoReviewView
            elif view.lower() == 'Review'.lower():
                headers: list[str] = Head.ToDoGradeView
            else:
                headers: list[str] = Head.ProjectView
            return headers
        
        Webconsole.table = Webconsole.configure_table(
                headers=select_view(view=viewoption))
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=select_view(view=viewoption),
                                 viewfilter='ToDo')
    
    # crumbs(context=ctx)
    dataf: pd.DataFrame = get_data()
    try:
        if display is not None:
            display_data(dataframe=dataf, viewoption=display)
        elif selects is not None:
            display_data(dataframe=dataf, viewoption=selects)
        elif display == selects:
            display_data(dataframe=dataf, viewoption=selects)
        else:
            display_data(dataframe=dataf, viewoption=selects)
    except TypeError:
        display_data(dataframe=dataf)
        rich.print(f"You entered the wrong option: {display.lower()}\n"
                   f"Please try again@ All, Simple, Done, Grade or Review")


load.add_command(todo)


@load.command(AppValues.Load.references)
@click.pass_context
def reference(ctx) -> None:
    """Load Reference/Index."""
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        headers: list[str] = Head.ReferenceView
        Webconsole.table = Webconsole.configure_table(headers=headers)
        Display.display_subframe(dataframe=dataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table,
                                 headerview=headers,
                                 viewfilter='References')
    
    # crumbs(context=ctx)
    display_data(dataframe=get_data())


# 2. Find
@run.group(AppValues.Find.cmd)
@click.pass_context
def find(ctx: click.Context) -> None:
    """Find: Find item, row(s), column(s)."""
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    # crumbs(context=ctx)
    ctx.obj = get_data()


@find.command(name="search")
@click.option('--header', type=str,
              help='Column\'s header label to search')
@click.option('--query', type=str,
              help='String query to search for')
@click.pass_context
def search(ctx: click.Context, header: str, query: str) -> None:
    """Search: a column: by header and query.
    
    :param ctx: click.Context
    :param header: str: Column's header label to search
    :param query: str: String query to search for
    :return: None: Display as stdout or stderr
    """
    
    # Context Trace: Remove
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    # Not rasing errors, gently reminding/correcting user to enter correct data
    if Checks.isnot_querytype(header=header, query=query):
        click.echo(message="Please use text for header's name and query")
        return
    
    # Checks query completness and Context, and DF Typing/Existence
    dataf: pd.DataFrame = get_data()
    searchresult: pd.DataFrame
    # crumbs(context=ctx)
    if Checks.is_querycomplete(header=header, query=query):
        # Current data: Remove after testing
        Display.display_data(dataframe=dataf,
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
        click.echo("===============================")
        # Result from a query, and asusrances, as feedback
        searchresult: pd.DataFrame = \
            dataf[dataf[header].astype(str).str.contains(query)]
        click.echo(
                message=f'The rows with "{query}" '
                        f'in column\'s "{header}" are:\n'
                        f'{searchresult}')
        # Build the Queryset: header, query, searchresult for display
        output: tuple[str, str, pd.DataFrame] = header, query, searchresult
        Display.display_data(dataframe=searchresult,
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
        click.echo("===============================")
        # Remove one after testing
        Display.display_search(output=output,
                               consoleholder=Webconsole.console,
                               consoletable=Webconsole.table)
        click.echo("===============================")
    
    click.echo(message="Command did not run", err=True)
    return


run.add_command(search)


# 2. Select
@run.group(AppValues.Select.cmd)
@click.pass_context
def select(ctx: click.Context) -> None:
    """Select: Select an item, a row, a column.
    
    Use --help to see the options and actions (sub commands)
    Intent level (L2): command path category.
    Does nothing, is a path option to action (sub commands.).
    """
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > {crumb.title()}'
                           f'> [ACTION]*\n *: You are here: {crumb.title()}\n'
                           f'To go up a level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    # crumbs(context=ctx)
    dataf: pd.DataFrame = get_data()
    DataControl.dataframe = dataf


@select.command(AppValues.Select.items)
@click.option('--linenumber', type=int,
              help='Line number to find. Check the display')
@click.option('--header', type=str,
              help='Column\'s header, text, to find. Check the display')
@click.pass_context
def item(ctx: click.Context, linenumber: int, header: str) -> None:
    """Select an item.
    
    Action subcommand: Parent Intent: Select.
    i: By row's linenumber number (int),
    i: By column's header text (str).
    """
    
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        parent: str = context.parent.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > {parent.title()}'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    #
    if not isinstance(linenumber, int) or not isinstance(header, str):
        click.echo(
                message=('Please provide a number, for linenumber,'
                         + 'not text etc. \n'
                         + 'Please provide a text, for header,'
                         + 'not a number etc. \n'),
                err=True)
    #
    # crumbs(context=ctx)
    if linenumber is not None and header is not None:
        df: pd.DataFrame = get_data()
        value: pd.DataFrame = df.loc[linenumber, header]
        Webconsole.table = Webconsole.set_datatable(dataframe=value)
        click.echo(
                message=f'The value at line nos. {linenumber} and '
                        f'column\'s header "{header}" is {value}')
        output: tuple[str, int, pd.DataFrame] = \
            header, linenumber, value
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    #
    else:
        click.echo(message='Please provide both row and column options.')


@select.command(AppValues.Select.rows)
@click.pass_context
@click.option('--linenumber',
              type=int,
              help=('Line Nos (Position) to query of a single row. '
                    + 'Check the display'))
def row(ctx: click.Context, linenumber: int) \
        -> None | typing.NoReturn:
    """Select a row.
    
    Action: subcommand: Parent Intent: Select
    i: By row line number (id/position):
    Refer to and check display for linenumber.
    """
    
    #
    def crumbs(context) -> None:
        """Display the command navigation crumbs."""
        crumb: str = context.info_name
        parent: str = context.parent.info_name
        click.echo(message=f'Navigation: CLI: > Run > ... > {parent.title()}'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
    #
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    #
    if not isinstance(linenumber, int):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {linenumber}'),
                err=True)
    #
    # crumbs(context=ctx)
    if linenumber is not None:
        df: pd.DataFrame = get_data()
        row_data: pd.DataFrame = df.query('position == @linenumber')
        Webconsole.table = Webconsole.set_datatable(dataframe=row_data)
        click.echo(
                message=f'The row with ID {linenumber} is:\n'
                        f'{row_data}')
        output: tuple[int, pd.DataFrame] = linenumber, row_data
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    #
    else:
        click.echo(message=f'Please provide a row\'s {linenumber}.', err=True)


@select.command(AppValues.Select.columns)
@click.pass_context
@click.option('--header',
              type=str,
              help='Column\'s header label to query, Check the display')
def column(ctx: click.Context, obj: Optional[object], header: str) \
        -> None | typing.NoReturn:
    """Select a column: by column's header."""
    # Check foŕ parameter's type
    click.echo(message=ctx.info_name)
    #
    if not isinstance(header, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {header}'),
                err=True)
    #
    
    if header is not None:
        df: pd.DataFrame = pd.DataFrame(obj)
        column_data: pd.DataFrame = df[header]
        click.echo(
                message=(f'The column\'s header "{header}" is:\n'
                         + f'{column_data}'))
        output: tuple[str, pd.DataFrame] = header, column_data
        Webconsole.table = Webconsole.set_datatable(dataframe=column_data)
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    #
    else:
        click.echo(message=f'Please provide a column\'s. {header}. \n'
                           'And please check/refresh the dataset')
    
    return None


def acolumnselect(dataframe: pd.DataFrame, header: str) \
        -> None | tuple[str, pd.DataFrame]:
    # sourcery skip: extract-method
    """Select a column: by column's header.

    :param dataframe: DataframeContext: Dataframe to find
    :param header: str: Column's header
    :return: None | tuple[str, pd.DataFrame]: Column's header and data
    """
    #
    if not isinstance(header, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {header}'),
                err=True)
        return None
    #
    if header is None:
        click.echo(message=f'Please provide a column\'s. {header}', err=True)
    #
    else:
        assert isinstance(dataframe, pd.DataFrame)  # noqa: S101
        df: pd.DataFrame = dataframe
        column_data: pd.DataFrame = df[header]
        click.echo(
                message=(f'The column\'s header "{header}" is:\n'
                         + f'{column_data}'))
        output: tuple[str, pd.DataFrame] = header, column_data
        Webconsole.table = Webconsole.set_datatable(dataframe=column_data)
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    # Return to stdout: Display output
    return None


class CRUD:
    """CRUD: Create, Read, Update, Delete."""
    
    # New (Add) | Create, Add commands -> None: by item, by row
    @run.group(AppValues.Add.cmd)
    @click.pass_context
    @click.pass_obj
    def add(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Add: Create item, row(s)."""
    
    @add.command(AppValues.Add.items)
    @click.pass_context
    @click.pass_obj
    def additem(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Add item.: Append/Create an item.
        
        Append by a location/coordinate.
        """
    
    @add.command(AppValues.Add.rows)
    @click.pass_context
    @click.pass_obj
    def addrow(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Add row(s).: Append/Create a row to the table: either at end, or insert."""
    
    @run.group(AppValues.Update.cmd)
    @click.pass_context
    @click.pass_obj
    def update(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Update: Update item, row(s)."""
    
    @update.command(AppValues.Update.items)
    @click.pass_context
    @click.pass_obj
    def updateitem(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Update item.: Find an item, update the item."""
    
    @update.command(AppValues.Update.rows)
    @click.pass_context
    @click.pass_obj
    def updaterow(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Update row(s): Find a row, by id, and update the row."""
    
    @run.group(AppValues.Delete.cmd)
    @click.pass_context
    @click.pass_obj
    def delete(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Delete: Delete item(s), row(s)."""
    
    @delete.command(AppValues.Delete.items)
    @click.pass_context
    @click.pass_obj
    def deleteitem(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Delete item: Find an item.
        
        Clear the item's content/reset to default.
        """
    
    @delete.command(AppValues.Delete.rows)
    @click.pass_context
    @click.pass_obj
    def deleterow(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Delete row(s).
        
        Find a row, by id, and delete the row:
        at end or by its position.
        """  # noqa: D415


# Click Command repl is run from this function
# See https://www.perplexity.ai/search/085c28b9-d6e8-4ea2-8234-783d7f1a054c?s=c
register_repl(run)

if __name__ == "__main__":
    traceable: str = "Enable tracemalloc to get the object allocation traceback"
    warnings.filterwarnings("ignore",
                            message=traceable, )
    ProgramUtils.warn()
    click.echo("Hello")
    run()
