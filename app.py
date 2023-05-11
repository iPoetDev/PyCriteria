#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: PyCriteria Terminal App."""
# 1. Std Lib
import typing

# 2. 3rd Party
import click
import pandas as pd
from prompt_toolkit import PromptSession

# 3. Local
from commands import AboutUsage, Commands, pass_dataframe_context
from controller import (Controller, DataController, Display, WebConsole,
                        Entry, rprint, configuration, )
from sidecar import AppValues, ProgramUtils

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


class CriteriaApp:
    """PyCriteria Terminal App."""
    
    values: AppValues
    
    def __init__(self):
        """Initialize."""
        self.values = AppValues()


@click.group(name=AppValues.Start.cmd)
def start() -> None:
    """Main. Starts a local CLI REPL"""
    click.echo(message=AppValues.Start.welcome)
    session: PromptSession = PromptSession(completer=Commands.nest_auto)
    
    while True:
        try:
            text = session.prompt('PyCriteria >  ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print('You entered:', text)
    print('GoodBye!')


@start.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx: click.Context) -> None:
    """Level: Run. Type: about to learn to use this CLI.
    
    Enter: $python app.py about
    This CLI has a multi-level command structure.
    https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html
    """
    click.echo(message=ctx.info_name)


@run.group(name="about")
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


# 1. Load Data: Have the user load the data: by project, by criteria, by reference
@run.group(name=AppValues.Load.cmd)
@pass_dataframe_context
def load(ctx: click.Context) -> None:
    """Load."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    Display.display_frame(dataframe=ctx.obj.dataframe,
                          consoleholder=Webconsole.console,
                          consoletable=Webconsole.table)


@load.command(name=AppValues.Load.projects)
@pass_dataframe_context
def project(ctx) -> None:
    """Load project (metadata)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    Display.display_frame(dataframe=ctx.obj.dataframe,
                          consoleholder=Webconsole.console,
                          consoletable=Webconsole.table)


@load.command(name=AppValues.Load.criterias)
@pass_dataframe_context
def criteria(ctx: click.Context) -> None:
    """Load criteria."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    Display.display_frame(dataframe=ctx.obj.dataframe,
                          consoleholder=Webconsole.console,
                          consoletable=Webconsole.table)


@load.command(AppValues.Load.references)
@pass_dataframe_context
def reference(ctx: click.Context) -> None:
    """Load references (metadata)."""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    ProgramUtils.inspectcontext(ctx)
    Display.display_frame(dataframe=ctx.obj.dataframe,
                          consoleholder=Webconsole.console,
                          consoletable=Webconsole.table)


# 2. Find
@run.group(AppValues.Find.cmd)
@pass_dataframe_context
def find(ctx: click.Context) -> None:
    """Find: Find item, row(s), column(s)"""
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)


@find.command(name="search")
@click.option('--header', type=str,
              help='Column\'s header label to search')
@click.option('--query', type=str,
              help='String query to search for')
@pass_dataframe_context
def search(ctx, header: str, query: str):
    """Search: a column: by header and query."""
    click.echo(message=ctx.info_name)
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.parent.parent.info_name)
    
    #
    if not isinstance(header, str) or isinstance(query, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + 'for header and query.'),
                err=True)
    #
    searchresult: pd.DataFrame
    click.echo(message=ctx.parent.info_name)
    click.echo(message=ctx.info_name)
    
    #
    if not isinstance(header, str) or isinstance(query, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + 'for header and query.'),
                err=True)
    #
    searchresult: pd.DataFrame
    if header is not None and query is not None:
        df = ctx.obj.dataframe
        searchresult: pd.DataFrame = \
            df[df[header].astype(str).str.contains(query)]
        click.echo(
                message=f'The rows with "{query}" '
                        f'in column\'s "{header}" are:\n'
                        f'{searchresult}')
        output: tuple[str, str, pd.DataFrame] = header, query, searchresult
        Display.display_frame(dataframe=searchresult,
                              consoleholder=Webconsole.console,
                              consoletable=Webconsole.table)
        click.echo("===============================")
        Display.display_search(output=output,
                               consoleholder=Webconsole.console,
                               consoletable=Webconsole.table)
        click.echo("===============================")
    #
    else:
        click.echo(
                message='Please provide both column and query options.',
                err=True)


run.add_command(search)


# 2. Select

@run.group(AppValues.Select.cmd)
@pass_dataframe_context
def select(ctx: click.Context) -> None:
    """ Select: Select an item, a row, a column.
        Use --help to see the options and actions (sub commands)
        Intent level (L2): command path category.
        Does nothing, is a path option to action (sub commands.)"""
    click.echo(message=ctx.info_name)
    click.echo(message=ctx.parent.info_name)


@select.command(AppValues.Select.items)
@click.option('--linenumber', type=int,
              help='Line number to find. Check the display')
@click.option('--header', type=str,
              help='Column\'s header, text, to find. Check the display')
@pass_dataframe_context
def item(ctx, linenumber: int, header: str) -> None | typing.NoReturn:
    """ Select an item:
        Action subcommand: Parent Intent: Select.
        i: By row's linenumber number (int),
        i: By column's header text (str)."""
    if not isinstance(linenumber, int) or not isinstance(header, str):
        click.echo(
                message=('Please provide a number, for linenumber,'
                         + 'not text etc. \n'
                         + 'Please provide a text, for header,'
                         + 'not a number etc. \n'),
                err=True)
    
    if linenumber is not None and header is not None:
        df = ctx.obj.dataframe
        value: pd.DataFrame = df.loc[linenumber, header]
        click.echo(
                message=f'The value at line nos. {linenumber} and '
                        f'column\'s header "{header}" is {value}')
        output: tuple[str, int, pd.DataFrame] = \
            header, linenumber, value
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    else:
        click.echo(message='Please provide both row and column options.')


@select.command(AppValues.Select.rows)
@click.option('--linenumber',
              type=int,
              help=('Line Nos (Position) to query of a single row. '
                    + 'Check the display'))
@pass_dataframe_context
def row(ctx, linenumber: int) -> None | typing.NoReturn:
    """ Select a row:
        Action: subcommand: Parent Intent: Select
        i: By row line number (id/position):
        Refer to and check display for linenumber"""
    #
    if not isinstance(linenumber, int):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {linenumber}'),
                err=True)
    #
    if linenumber is not None:
        df = ctx.obj.dataframe
        row_data: pd.DataFrame = df.query('position == @linenumber')
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


@select.command(AppValues.Select.columns)
@click.command(name="select 1 column")
@click.option('--header',
              type=str,
              help='Column\'s header label to query, Check the display')
@pass_dataframe_context
def column(ctx, header: str) -> None | typing.NoReturn:
    """Select a column: by column's header"""
    # Check foŕ parameter's type
    if not isinstance(header, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {header}'),
                err=True)
    #
    if header is not None:
        df = ctx.obj.dataframe
        column_data: pd.DataFrame = df[header]
        click.echo(
                message=(f'The column\'s header "{header}" is:\n'
                         + f'{column_data}'))
        output: tuple[str, pd.DataFrame] = header, column_data
        Display.display_selection(output=output,
                                  consoleholder=Webconsole.console,
                                  consoletable=Webconsole.table)
    #
    else:
        click.echo(message=f'Please provide a column\'s. {header}')


def acolumnselect(ctx, header: str) -> None | tuple[str, pd.DataFrame]:
    """Select a column: by column's header"""
    # Check foŕ parameter's type
    if not isinstance(header, str):
        click.echo(
                message=('Please provid text, not numbers etc, '
                         + f'for column\'s header: {header}'),
                err=True)
    #
    if header is not None:
        df = ctx.obj.dataframe
        column_data: pd.DataFrame = df[header]
        click.echo(
                message=(f'The column\'s header "{header}" is:\n'
                         + f'{column_data}'))
        output: tuple[str, pd.DataFrame] = header, column_data
        return output
    #
    else:
        click.echo(message=f'Please provide a column\'s. {header}')
        return None


class CRUD:
    """CRUD: Create, Read, Update, Delete"""
    
    # New (Add) | Create, Add commands -> None: by item, by row
    @run.group(AppValues.Add.cmd)
    def add(self) -> None:
        """Add: Create item, row(s)"""
    
    @add.command(AppValues.Add.items)
    def additem(self) -> None:
        """Add item.: Append/Create an item by a location/coordinate"""
    
    @add.command(AppValues.Add.rows)
    def addrow(self) -> None:
        """Add row(s).: Append/Create a row to the table: either at end, or insert."""
    
    @run.group(AppValues.Update.cmd)
    def update(self) -> None:
        """Update: Update item, row(s)"""
    
    @update.command(AppValues.Update.items)
    def updateitem(self) -> None:
        """Update item.: Find an item, update the item"""
    
    @update.command(AppValues.Update.rows)
    def updaterow(self) -> None:
        """Update row(s): Find a row, by id, and update the row."""
    
    @run.group(AppValues.Delete.cmd)
    def delete(self) -> None:
        """Delete: Delete item(s), row(s)"""
    
    @delete.command(AppValues.Delete.items)
    def deleteitem(self) -> None:
        """Delete item: Find an item, clear the item's content/reset to default."""
    
    @delete.command(AppValues.Delete.rows)
    def deleterow(self) -> None:
        """Delete row(s).: Find a row, by id, and delete the row: at end or by its position."""


if __name__ == "__main__":
    ProgramUtils.warn()
    print("Hello")
    run()
