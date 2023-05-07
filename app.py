#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: PyCriteria Terminal App."""
# 1. Std Lib
import dataclasses

# 2. 3rd Party
import typer

# 3. Local
import controller

# 3rd Party: Commands: typer.Typer()
App: typer.Typer = typer.Typer()  # Parent Instance
# Sub Instances --> Sub Commands
Load: typer.Typer = typer.Typer()
Views: typer.Typer = typer.Typer()
Find: typer.Typer = typer.Typer()
Select: typer.Typer = typer.Typer()
Add: typer.Typer = typer.Typer()
Update: typer.Typer = typer.Typer()
Delete: typer.Typer = typer.Typer()

# Own Modules/Objects
Actions: controller.Controller = controller.Controller()
Display: controller.Display = controller.Display()
Webconsole: controller.WebConsole = controller.WebConsole()
Entry: controller.Entry = controller.Entry()


@dataclasses.dataclass
class AppValues:
    """App Values."""
    name: str = "PyCriteria"
    version: str = "0.1.1"
    lastmodified: str = "2023-05-07"
    epilogue: str = "PyCriteria Terminal App. (c) 2023, 2024, 2025. All rights reserved. @iPoetDev"
    richpanel: bool = True
    deprecated: bool = False
    
    @dataclasses.dataclass
    class Load:
        """Load Settings.
        :property: intro:str: typer panel/intro.
        :property: help:str: typer help.
        :property: quik:str: typer short_help.
        """
        cmd: str = "load"
        projects: str = "projects"
        criterias: str = "criteria"
        references: str = "reference"
        intro: str = "Load Settings."
        help: str = "Load Settings."
        quik: str = "Load Settings."
    
    @dataclasses.dataclass
    class Views:
        """Choose a View."""
        cmd: str = "views"
        allname: str = "all"
        list: str = "list"
        table: str = "table"
        columns: str = "columns"
        intro: str = "Select which view: List, Table, Columns."
        help: str = "Load Settings."
        quik: str = "Load Settings."
    
    @dataclasses.dataclass
    class Find:
        """Find Settings."""
        cmd: str = "find"
        items: str = "items"
        rows: str = "rows"
        columns: str = "columns"
        intro: str = "Find an items. By single item, rows, columns."
        help: str = "Find Settings."
        quik: str = "Find Settings."
    
    @dataclasses.dataclass
    class Select:
        """Add Settings."""
        cmd: str = "select"
        items: str = "items"
        rows: str = "rows"
        columns: str = "columns"
        intro: str = "Select to filter items. By single item, rows, columns"
        help: str = "Select Settings."
        quik: str = "Select Settings."
    
    @dataclasses.dataclass
    class Add:
        """Add Settings."""
        cmd: str = "add"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Add a new record: by cell or a single row."
        help: str = "Add Settings."
        quik: str = "Add Settings."
    
    @dataclasses.dataclass
    class Update:
        """Select (filterr) Settings."""
        cmd: str = "update"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Update an existing record: by cell or a single row."
        help: str = "Update Settings."
        quik: str = "Update Settings."
    
    @dataclasses.dataclass
    class Delete:
        """Select (filterr) Settings."""
        cmd: str = "delete"
        items: str = "items"
        rows: str = "rows"
        intro: str = "Delete an existing record: by cell/item or a single row."
        help: str = "Delete Settings."
        quik: str = "Delete Settings."
    
    @dataclasses.dataclass
    class Close:
        """Close Settings."""
        cmd: str = "close"
        intro: str = "Close the remote connection."
        help: str = "Close Settings."
        quik: str = "Close Settings."
    
    @dataclasses.dataclass
    class Exit:
        """Exit Settings."""
        cmd: str = "exit"
        intro: str = "Exit the terminal (and close the connection)."
        help: str = "Exit Settings."
        quik: str = "Exit Settings."


class CriteriaApp:
    """PyCriteria Terminal App."""
    
    app: typer.Typer
    Load: typer.Typer
    info: str
    name: str = "PyCriteria Terminal App."
    
    def __init__(self):
        """Initialize."""
        self.app = App
        self.configure_subcommands()
        self.info = str(self.app.info)
    
    @staticmethod
    def configure_subcommands():
        """Configure commands."""
        # GET Commands
        App.add_typer(Load, name=AppValues.Load.projects)
        App.add_typer(Load, name=AppValues.Load.criterias)
        App.add_typer(Load, name=AppValues.Load.references)
        # READ Commands: Views, Find, Select/Filter
        App.add_typer(Views, name=AppValues.Views.allname)
        App.add_typer(Views, name=AppValues.Views.list)
        App.add_typer(Views, name=AppValues.Views.table)
        App.add_typer(Views, name=AppValues.Views.columns)
        App.add_typer(Find, name=AppValues.Find.items)
        App.add_typer(Find, name=AppValues.Find.rows)
        App.add_typer(Find, name=AppValues.Find.columns)
        App.add_typer(Select, name=AppValues.Select.items)
        App.add_typer(Select, name=AppValues.Select.rows)
        App.add_typer(Select, name=AppValues.Select.columns)
        # CREATE Commands
        App.add_typer(Add, name=AppValues.Add.items)
        App.add_typer(Add, name=AppValues.Add.rows)
        # UPDATE Commands
        App.add_typer(Update, name=AppValues.Update.items)
        App.add_typer(Update, name=AppValues.Update.rows)
        # DELETE Commands
        App.add_typer(Delete, name=AppValues.Delete.items)
        App.add_typer(Delete, name=AppValues.Delete.rows)
    
    @staticmethod
    def loadconfigure():
        """Load Configure."""
        Load.rich_help_panel = True


# 1. Load Data: Have the user load the data: by project, by criteria, by reference
@App.command(AppValues.Load.cmd)
def load():
    """Load."""


@Load.command(AppValues.Load.criterias)
def criteria():
    """Load criteria."""


@Load.command(AppValues.Load.projects)
def project():
    """Load project (metadata)."""


@Load.command(AppValues.Load.references)
def reference():
    """Load project (metadata)."""


@Views.command(AppValues.Views.allname)
def showall():
    """Shows/Views all data."""


@Views.command(AppValues.Views.list)
def listing():
    """Views data in a list."""


@Views.command(AppValues.Views.table)
def table():
    """Views data in a table."""


@Views.command(AppValues.Views.columns)
def columnar():
    """Load data in table."""


# 2. Find
@App.command(AppValues.Find.cmd)
def find():
    """Add."""


@Select.command(AppValues.Find.items)
def finditem():
    """Select item."""


@Select.command(AppValues.Find.rows)
def findrow():
    """Select row(s)."""


@Select.command(AppValues.Find.columns)
def findcolumn():
    """Select a column(s)."""


# 2. Select
@App.command(AppValues.Select.cmd)
def select():
    """Add."""


@Select.command(AppValues.Select.items)
def selectitem():
    """Select item."""


@Select.command(AppValues.Select.rows)
def selectrow():
    """Select row(s)."""


@Select.command(AppValues.Select.columns)
def selectcolumn():
    """Select a column(s)."""


# New (Add) | Create, Add commands: by item, by row
@App.command(AppValues.Add.cmd)
def add():
    """Add."""


@Add.command(AppValues.Add.items)
def additem():
    """Add item."""


@Add.command(AppValues.Add.rows)
def addrow():
    """Add row(s)."""


@App.command(AppValues.Update.cmd)
def update():
    """Update."""


@Update.command(AppValues.Update.items)
def updateitem():
    """Update item."""


@Update.command(AppValues.Update.rows)
def updaterow():
    """Update row(s)."""


@App.command(AppValues.Delete.cmd)
def delete():
    """Add."""


@Delete.command(AppValues.Delete.items)
def deleteitem():
    """Delete item."""


@Delete.command(AppValues.Delete.rows)
def deleterow():
    """Delete row(s)."""
