#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, ANN001, D415, RET505, I001, F405, F403
"""Module: PyCriteria Terminal App."""
# 1. Std Lib
from typing import Literal, NewType, Optional

# 2. 3rd Party
import rich
from click_repl import register_repl  # type: ignore
from rich import pretty  # type: ignore

# 3. Local: Note the controller * intentionally imports all from the module
from commands import AboutUsage, Commands
from controller import *
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


class View:
    """View."""
    
    Load: list[str] = ["Load", "Begins", "Project", "Criteria", "ToDo", "Reference", "Refresh"]
    Todo: list[str] = ["ToDo", "All", "Simple", "Done", "Grade", "Review"]
    
    def __init__(self):
        """Initialize."""
        pass


view: View = View()


class CriteriaApp:
    """PyCriteria Terminal App."""
    
    values: AppValues
    
    def __init__(self):
        """Initialize."""
        self.values = AppValues()
    
    @staticmethod
    def crumbs(context: click.Context) -> None:
        """Display the command navigation crumbs."""
        root: str = "BASE: Run"
        click.echo(message="Navigation: CLI: > Run > ... [Intent] > [Action]\n")
        if context.info_name is not None:
            crumb: str = context.info_name
        else:
            crumb: str = root
        click.echo(message=f'Navigation: CLI: > Run > ... > Load'
                           f'> {crumb.title()}*\n *: You are here: {crumb.title()}\n'
                           f'To go up one or two level, enter, each time:  ..  \n'
                           f'To Exit: ctrl + d  \n')
    
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
                    case: bool = False, echo: bool = False) -> pd.DataFrame:  # noqa
        """Search the dataframe."""
        searchresult: pd.DataFrame = \
            frame[frame[label].astype(str).str.contains(searchstr,
                                                        case=case)]
        
        if echo:
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
            -> pd.DataFrame | None:
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
        result: pd.DataFrame | None
        if index:
            result: pd.DataFrame = App.index(frame=frame,
                                             index=index,
                                             zero=zero)
        elif searchterm:
            # Search across all columns for the position value
            result: pd.DataFrame = App.search_rows(frame=frame,
                                                   searchterm=searchterm,
                                                   exact=strict)
            if result.empty is not False:
                click.echo(f"Found: {result}")
            else:
                click.echo(f"Could not find {search}")
        else:
            click.echo("Please provide either an index or searches term")
            return None
        
        return result | None
    
    @staticmethod
    def index(frame: pd.DataFrame,
              index: int = None,
              zero: bool = True) \
            -> pd.DataFrame | None:
        """Get the index from the dataframe."""
        if zero and index is not None:
            result: pd.DataFrame = frame.iloc[index - 1] \
                if index >= 0 else frame.iloc[index]
            click.echo(f"Found: {result} for zero index {index - 1}")
            return result
        elif not zero and index is not None:
            result: pd.DataFrame = frame.iloc[index] \
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


App: CriteriaApp = CriteriaApp()


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


Guard: Checks = Checks()


@click.group(name=AppValues.Run.cmd)
@click.pass_context
def run(ctx) -> None:
    """Level: Run. Type: about to learn to use this CLI.
    
    This CLI has a multi-level command structure.
    https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html
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


@load.command("todo", help="Load todo list. Select views to display.")
@click.pass_context
@click.option('-d', '--display',
              type=str,
              default='All',
              show_default=True,
              help="Choose a display: from All, Simple, Done, Grade, Review")
@click.option('-s', '--selects',
              type=click.Choice(choices=Head.ToDoChoices),
              default='All',
              show_default=True,
              help="Choose a option: from All, Simple, Done, Grade, Review")
def todo(ctx, display: str, selects: str) -> None:
    """Load todos, and display different filters/views."""
    # App.crumbs(context=ctx)
    dataframe: pd.DataFrame = App.get_data()
    
    def viewopt(inputs: str, choice: str) -> str:
        """Choose a view input source to display."""
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


@load.command("views", help="Load views. Select views to display.")
@click.option('-d', '--display',
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


@find.command("keyword", help="Load todo list. Select views to display.")
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
    """Load todos, and display different filters/views."""
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
        # Build the Queryset: header, query, searchresult for display
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
        # Build the Queryset: header, query, searchresult for display
        Display.display_data(dataframe=searchresult,
                             consoleholder=Webconsole.console,
                             consoletable=Webconsole.table)
    else:
        click.echo(message="Command did not run", err=True)
    
    App.update_appdata(context=ctx, dataframe=sourcedata)
    return


run.add_command(searches)


@find.command(name="locate", help="Locate row(s), via index, column, row.")
@click.option('-s', '--searches', type=str,
              help='Search for a string in the dataframe',
              prompt=True,
              optional=True)
@click.option('-i', '--index',
              type=click.IntRange(
                      min=1,
                      max=len(DataControl.dataframe),
                      clamp=True),
              help=f'Select between 1 and f{len(DataControl.dataframe)}',
              prompt=True,
              optional=True)
@click.option('-a', '--axis',
              type=click.Choice(['index', 'column', 'row'],
                                case_sensitive=False),
              help='Choose axis to seach in/by. Default: row',
              default='row',
              prompt=True,
              required=True)
@click.pass_context
def locate(ctx: click.Context, index: int, searchterm: str,
           axis: str = Literal['index', 'column', 'row']) -> None:
    """Locate: a row: by index or searches term via index, column or row."""
    
    # Define the function to get the row frames
    def getrowframe(data: pd.DataFrame,
                    ix: int, st: str) -> pd.DataFrame | None:
        """Get a row from a dataframe by index or searches term."""
        if ix and not st:
            result = App.rows(frame=data, index=ix)
        elif ix and st:
            result = App.rows(frame=data, index=ix, searchterm=st)
        elif not ix and st:
            result = App.rows(frame=data, searchterm=st)
        else:
            return None
        
        return result
    
    # Get the dataframe
    dataframe: pd.DataFrame = App.get_data()
    if axis.lower() == 'index':
        resultframe: pd.DataFrame = \
            getrowframe(data=dataframe, ix=index, st=searchterm)
        rich.print(resultframe)
        # App.display_todo(dataframe=resultframe)
    elif axis.lower() == 'columns':
        click.echo(message="Please use the searches command to searches columns")
    elif axis.lower() == 'rows':
        resultframe: pd.DataFrame = \
            getrowframe(data=dataframe, ix=index, st=searchterm)
        rich.print(resultframe)
        # App.display_todo(dataframe=resultframe)
    else:
        click.echo(message="Command did not run. Invalid axis", err=True)
    
    App.update_appdata(context=ctx, dataframe=dataframe)


run.add_command(locate)


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
