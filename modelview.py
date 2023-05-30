#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN101, I001, ARG002
"""Module: Model & View for the Terminal App."""


class Views:
    """Views.

        :property: View.Load
        :property: View.Todo
        """
    # Views
    Overviews: str = "Overviews"
    Project: str = "Project"
    Criteria: str = "Criteria"
    Reference: str = "Reference"
    ToDos: str = "ToDo"
    #
    All: str = "All"
    Simple: str = "Simple"
    Notes: str = "Notes"
    Done: str = "Done"
    Grade: str = "Grade"
    Review: str = "Review"
    ToDo: str = "ToDo"
    
    Load: list[str] = ["Overview", "Project", "Criteria",
                       "ToDo", "Reference"]
    Todo: list[str] = ["All", "Simple", "Notes", "Done",
                       "Grade", "Review"]
    
    SearchAxes: list[str] = ["index", "row", "column"]
    LocateAxis: list[str] = ["index"]
    
    def __init__(self):
        """Initialize."""
        pass


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
    # Row: str = "RowID"
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
    CriteriaView: list[str] = [c.Position, c.Topic,
                               c.Reference, c.Criteria, c.Notes]
    ProjectView: list[str] = [c.Position, c.Tier, c.DoD, c.Reference,
                              c.Progress]
    # ToDoView: Command
    ToDoAllView: list[str] = [c.Position, c.Performance, c.DoD, c.Criteria,
                              c.Progress, c.Notes]
    ToDoSimpleView: list[str] = [c.Position, c.Criteria]
    ToDoNotesView: list[str] = [c.Position, c.Progress, c.Notes]
    ToDoProgressView: list[str] = [c.Position, c.Criteria, c.Progress, c.DoD]
    ToDoGradeView: list[str] = [c.Position, c.Criteria,
                                c.Performance, c.DoD]
    ToDoReviewView: list[str] = [c.Reference, c.Criteria,
                                 c.Notes, c.Progress]
    #
    NotesView: list[str] = [c.Position, c.Criteria, c.Notes]
    ReferenceView: list[str] = [c.Position, c.Reference, c.Related]
    ViewFilter: list[str] = ["Overview", "Criteria",
                             "Project", "ToDo", "References"]
    ToDoChoices: list[str] = ["All", "Simple", "Notes", "Progress", "Grade", "Review"]
    HeadersChoices: list[str] = ["Position", "Tier", "Performance",
                                 "Criteria", "Progress", "Notes"]
    
    def __init__(self, labels: ColumnSchema) -> None:
        """Headers."""
        self.c = labels


Head: Headers = Headers(labels=ColumnSchema())

# Path: modelview.py
