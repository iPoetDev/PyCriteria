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

# 3. Local
from commands import AboutUsage, Commands
from controller import Controller, DataController, Display, Entry, WebConsole, configuration, rprint
from sidecar import AppValues, ProgramUtils

# Note: Move third-party import `gspread` into a type-checking block

# Global Modules/Objects
About: AboutUsage = AboutUsage()

Commands: Commands = Commands()
Actions: Controller = Controller()
AppValues: AppValues = AppValues()
DataControl: DataController = DataController(Actions.load_wsheet())

Display: Display = Display()
Entry: Entry = Entry()
Webconsole: WebConsole = WebConsole(configuration.Console.WIDTH,
                                    configuration.Console.HEIGHT)

ContextObject = NewType('ContextObject', Optional[object])


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
    def has_dataframe(ctx: click.Context, ctx_obj: object) -> bool:
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


@click.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx: click.Context) -> None:
    """Level: Run. Type: about to learn to use this CLI.
    
    Enter: $python app.py about
    This CLI has a multi-level command structure.
    https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html
    """
    click.echo(message=f' run: {ctx.info_name}')
    ctx.obj = {'debug': False}


@run.group(name='about')
def about() -> None:
    """About."""
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
def load(ctx: click.Context) -> None:
    """Load data from the current context, intentionally.
    
    a) Get the dataframe from remote
    b) Check context for dataframe if is/is not present
    c) Display dataframe accoridngly
    
    :param ctx: click.Context
    :return: None: Produces stdout
    """
    # click.echo(message=ctx.parent.info_name)
    # click.echo(message=ctx.info_name)
    click.echo(message=f' load: {ctx.info_name}')
    ctx.obj = DataControl.dataframe
    click.echo(message=f' data: {ctx.obj}')


@load.command(name='begins')
@click.pass_context
@click.pass_obj
def begins(ctx: click.Context, obj: Optional[object]) -> None:
    """Begin/Initiated/.
    
    :param ctx: click.Context: Passed Object, by pass_context.
    :param obj: click.Context.obj: Passed Object, by pass_obj.
    :return: None - Produces stdout output
    """
    
    rich.inspect(ctx)
    rich.print(f'Dataframe Context: {ctx}')
    
    def get_data() -> pd.DataFrame:
        """Get the dataframe from the context."""
        wsheet: gspread.Worksheet = Actions.load_wsheet()
        dataframe: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(wsheet=wsheet)
        return dataframe
    
    def display_data(dataframe: pd.DataFrame) -> None:
        """Display the dataframe."""
        WebConsole.set_table(Webconsole, dataframe=dataframe)
        Display.display_frame(dataframe=dataframe,
                              consoleholder=Webconsole.console,
                              consoletable=Webconsole.table)
    
    # Check Context and Display acoordingly
    
    df_ctx: pd.DataFrame = pd.DataFrame(data=ctx,
                                        dtype=object,
                                        copy=True)
    # Display Dataframe
    if Checks.has_dataframe(ctx=ctx, ctx_obj=obj):
        df_ctx: pd.DataFrame = get_data()
        display_data(dataframe=df_ctx)
        ctx.obj = df_ctx
    # When the dataframe context is empty
    elif df_ctx is None:
        df_ctx: pd.DataFrame = get_data()
        # Type checkes for correctness
        if Checks.has_dataframe(ctx=ctx, ctx_obj=df_ctx):
            display_data(dataframe=df_ctx)
            ctx.obj = df_ctx
        else:
            rprint('No data loaded. '
                   'There is a problem with type: dataframe.')
    else:
        rprint('No data loaded. Cause: Unknown.')


@load.command(name=AppValues.Load.refresh)
@click.pass_context
@click.pass_obj
def refresh(ctx: click.Context, obj: Optional[object]) -> None:
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
    :param obj: click.Context.obj
    
    :return: None
    """
    root_ctx: click.Context = ctx.find_root()
    click.echo(message=root_ctx.info_name)
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    
    click.echo(message=ctx.find_object(pd.DataFrame))
    
    ProgramUtils.inspectcontext(ctx)
    #
    df_ctx: pd.DataFrame | object | None = obj
    if df_ctx is not None and \
            isinstance(obj, pd.DataFrame):
        # Core Datasets
        olddataframe: pd.DataFrame = pd.DataFrame(df_ctx)
        refreshed_data: pd.DataFrame = \
            DataControl.load_dataframe_wsheet(Actions.load_wsheet())
        newdataframe: pd.DataFrame = refreshed_data.dataframe
        
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
        if compare_frames(olddataframe, newdataframe):
            # Display Current/Old Dataframe:
            # a: Display the dataframe, c: Update ctx.obj
            Display.display_data(dataframe=olddataframe,
                                 consoleholder=Webconsole,
                                 consoletable=Webconsole.table)
            ctx.obj = olddataframe
        else:
            # Display New Dataframe:
            # a: Display the dataframe, c: Update ctx.obj
            Display.display_data(dataframe=newdataframe,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table)
            ctx.obj = newdataframe
    else:
        rprint("No data loaded.")


@load.command(name=AppValues.Load.projects)
@click.pass_context
@click.pass_obj
def project(ctx: click.Context, obj: Optional[object]) -> None:
    """Load project (metadata)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    
    # Check Context, and DF Typing
    if not Checks.has_dataframe(ctx, obj):
        rprint('No Data loaded. Incorrect type ')
        return
    
    if obj is not None and \
            isinstance(obj, pd.DataFrame):
        Display.display_data(dataframe=pd.DataFrame(obj),
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)


@load.command(name=AppValues.Load.criterias)
@click.pass_context
@click.pass_obj
def criteria(ctx: click.Context, obj: Optional[object]) -> None:
    """Load project (metadata)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    
    # Check Context, and DF Typing
    if not Checks.has_dataframe(ctx, obj):
        rprint('No Data loaded. Incorrect type ')
        return
    
    if obj is not None and \
            isinstance(obj, pd.DataFrame):
        Display.display_data(dataframe=pd.DataFrame(obj),
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)


@load.command(AppValues.Load.references)
@click.pass_context
@click.pass_obj
def reference(ctx: click.Context, obj: Optional[object]) -> None:
    """Load references (metadata)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    
    # Check Context, and DF Typing
    if not Checks.has_dataframe(ctx, obj):
        rprint('No Data loaded. Incorrect type ')
        return
    
    if obj is not None and \
            isinstance(obj, pd.DataFrame):
        Display.display_data(dataframe=pd.DataFrame(obj),
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
        return
    
    click.echo(message="Command did not run", err=True)
    return


# 2. Find
@run.group(AppValues.Find.cmd)
@click.pass_context
@click.pass_obj
def find(ctx: click.Context, obj: Optional[object]) -> None:
    """Find: Find item, row(s), column(s)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    click.echo(message=obj)


@find.command(name="search")
@click.option('--header', type=str,
              help='Column\'s header label to search')
@click.option('--query', type=str,
              help='String query to search for')
@click.pass_context
@click.pass_obj
def search(ctx: click.Context, obj: Optional[object], header: str, query: str) -> None:
    """Search: a column: by header and query.
    
    :param ctx: click.Context
    :param obj: click.Context.object: Alias/Context.obj for dataframe
    :param header: str: Column's header label to search
    :param query: str: String query to search for
    :return: None: Display as stdout or stderr
    """
    # Context Trace: Remove
    click.echo(message=ctx.info_name)
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.parent.parent.info_name)
    
    # Not rasing errors, gently reminding/correcting user to enter correct data
    if Checks.isnot_querytype(header=header, query=query):
        click.echo(message="Please use text for header's name and query")
        return
    
    df: object | None = obj
    
    if obj is not None:
        # Checks query completness and Context, and DF Typing/Existence
        searchresult: pd.DataFrame
        if Checks.is_querycomplete(header=header, query=query) \
                and Checks.has_dataframe(ctx, ctx_obj=obj):
            df: pd.DataFrame = pd.DataFrame(obj)
            # Current data: Remove after testing
            Display.display_data(dataframe=df,
                                 consoleholder=Webconsole.console,
                                 consoletable=Webconsole.table)
            click.echo("===============================")
            # Result from a query, and asusrances, as feedback
            searchresult: pd.DataFrame = \
                df[df[header].astype(str).str.contains(query)]
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
        #
        else:
            click.echo(
                    message='Please provide a header name and query text, both.',
                    err=True)
    
    click.echo(message="Command did not run", err=True)
    return


run.add_command(search)


# 2. Select
@run.group(AppValues.Select.cmd)
@click.pass_context
@click.pass_obj
def select(ctx: click.Context, obj: Optional[object]) -> None:
    """Select: Select an item, a row, a column.
    
    Use --help to see the options and actions (sub commands)
    Intent level (L2): command path category.
    Does nothing, is a path option to action (sub commands.).
    """
    click.echo(message=ctx.info_name)
    click.echo(message=ctx.parent.info_name)
    click.echo(message=obj)


@select.command(AppValues.Select.items)
@click.option('--linenumber', type=int,
              help='Line number to find. Check the display')
@click.option('--header', type=str,
              help='Column\'s header, text, to find. Check the display')
@click.pass_context
@click.pass_obj
def item(ctx: click.Context, obj: Optional[object], linenumber: int, header: str) -> None:
    """Select an item.
    
    Action subcommand: Parent Intent: Select.
    i: By row's linenumber number (int),
    i: By column's header text (str).
    """
    click.echo(message=ctx.info_name)
    #
    if not isinstance(linenumber, int) or not isinstance(header, str):
        click.echo(
                message=('Please provide a number, for linenumber,'
                         + 'not text etc. \n'
                         + 'Please provide a text, for header,'
                         + 'not a number etc. \n'),
                err=True)
    #
    if obj is not None:
        if linenumber is not None and header is not None \
                and Checks.has_dataframe(ctx, ctx_obj=obj):
            df: pd.DataFrame = pd.DataFrame(obj)
            value: pd.DataFrame = df.loc[linenumber, header]
            Webconsole.set_table(dataframe=value)
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
    
    click.echo(message="Command did not run", err=True)


@select.command(AppValues.Select.rows)
@click.option('--linenumber',
              type=int,
              help=('Line Nos (Position) to query of a single row. '
                    + 'Check the display'))
@click.pass_context
@click.pass_obj
def row(ctx: click.Context, obj: Optional[object], linenumber: int) \
        -> None | typing.NoReturn:
    """Select a row.
    
    Action: subcommand: Parent Intent: Select
    i: By row line number (id/position):
    Refer to and check display for linenumber.
    """
    #
    click.echo(message=ctx.info_name)
    if not isinstance(linenumber, int):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {linenumber}'),
                err=True)
    #
    if obj is not None:
        if linenumber is not None and Checks.has_dataframe(ctx, ctx_obj=obj):
            df = pd.DataFrame(obj)
            row_data: pd.DataFrame = df.query('position == @linenumber')
            Webconsole.set_table(dataframe=row_data)
            click.echo(
                    message=f'The row with ID {linenumber} is:\n'
                            f'{row_data}')
            output: tuple[int, pd.DataFrame] = linenumber, row_data
            Display.display_selection(output=output,
                                      consoleholder=Webconsole.console,
                                      consoletable=Webconsole.table)
        #
        else:
            click.echo(message=f'Please provide a row\'s {linenumber}.')
    
    click.echo(message="Command did not run", err=True)
    return None


@select.command(AppValues.Select.columns)
@click.option('--header',
              type=str,
              help='Column\'s header label to query, Check the display')
@click.pass_context
@click.pass_obj
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
    if obj is not None:
        if header is not None and Checks.has_dataframe(ctx, ctx_obj=obj):
            df: pd.DataFrame = pd.DataFrame(obj)
            column_data: pd.DataFrame = df[header]
            click.echo(
                    message=(f'The column\'s header "{header}" is:\n'
                             + f'{column_data}'))
            output: tuple[str, pd.DataFrame] = header, column_data
            Webconsole.set_table(dataframe=column_data)
            Display.display_selection(output=output,
                                      consoleholder=Webconsole.console,
                                      consoletable=Webconsole.table)
        #
        else:
            click.echo(message=f'Please provide a column\'s. {header}. \n'
                               'And please check/refresh the dataset')
        
        return None
    # If no dataframe, does not run cmd
    click.echo(message="Command did not run", err=True)
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
        Webconsole.set_table(dataframe=column_data)
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
        """Delete item: Find an item,.
        
        clear the item's content/reset to default.
        """
    
    @delete.command(AppValues.Delete.rows)
    @click.pass_context
    @click.pass_obj
    def deleterow(self, ctx: click.Context, obj: Optional[object]) -> None:  # noqa: ANN101
        """Delete row(s).
        
        Find a row, by id, and delete the row:
        at end or by its position.
        """  # noqa: D415


register_repl(run)

if __name__ == "__main__":
    traceable: str = "Enable tracemalloc to get the object allocation traceback"
    warnings.filterwarnings("ignore",
                            message=traceable, )
    ProgramUtils.warn()
    click.echo("Hello")
    run()
