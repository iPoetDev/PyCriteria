#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module DataModel. Class Criteria :a flat simple data model for the criteria table."""

# 0.1 CoreLibraries
from dataclasses import dataclass  # field
from typing import List


@dataclass
class SheetData:
    """Class Criteria.: DataModel."""
    sheetname: str
    database: list[dict]


@dataclass
class CriteriaTopic:
    """Class CriteriaTopic.: DataModel."""
    criteria_topic: List[str]
    criteria_ref: str  # ReferenceKey to criteria and tier


@dataclass
# pylint: disable=R0902, too-many-instance-attributes
class Criteria:
    """Class Criteria.: DataModel
    Use a zip function to join these together, based on the criteria_ref.
    """
    row_id: int
    item_position: int
    criteria_group: str
    per_formance: str
    criteria_topic: str
    criteria_ref: str  # ReferenceKey to criteria and tier
    criteria_text: str
    linked_ref: str


@dataclass
class Tier:
    """Class Tier.: DataModel
    Use a zip function to join these together, based on the criteria_ref.
    """
    tier_label: str
    tier_prefix: str
    tier_depth: int
    per_formance: str
    criteria_ref: str  # ReferenceKey to criteria and tier


@dataclass
class ToDo:
    """Class ToDo.: DataModel."""
    todo_state: str
    todo_flag: int
    criteria_ref: str  # ReferenceKey to criteria and tier
# EoF
