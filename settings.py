#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: I001
# noqa: W293 blank line contains whitespace
# - Without global file level rule, using # noqa: is not possible
"""Module Backend Settings and Environmental Vars.

Usage:
-------------------------
- Settings: Global Settings for the Controller, Connectiors
- EnvirnomentalVars: Load .env file to develop with env vars early.
  :deprecated: JS is used to load and recreate CREDS fromheroku CONFIG_VARS

Linting:
-------------------------
- pylint: disable=
            trailing-whitespace
            too-few-public-methods,
            too-many-instance-attributes
- ruff: noqa:
        I001:     unsorted-imports
                Import block is unsorted or unformatted
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
:imports: dataclasses, importlib, pathlib, typing

3rd Paty Imports
:imports: dotenv, rich

Custom Authored Libraries
:imports: exceptions

:class: Settings
:class: TableSettings - Used to load environmental variables from .env file.
:class: EnvirnomentalVars - Used to load environ variables from .env file.
"""
# 0.1 Standard Imports
import dataclasses

# 0.2 Third Party Modules
from rich import print as rprint  # type: ignore


# Global String/Int Resources
# pylint: disable=too-few-public-methods, too-many-instance-attributes
@dataclasses.dataclass
class Settings:
    """Settings."""
    # plylint: disable=C0301
    ENCODE: str = 'UTF-8'
    # Data String/Int Resources
    CRED_FILE: str = 'creds.json'
    SHEET_NAME: str = 'PyCriteria'
    TAB_NAME: str = 'Data'
    # Data String/Int Resources
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]  # pylint: disable=C0103
    
    @dataclasses.dataclass(frozen=True)
    class Console:
        """Config."""
        WIDTH: int = 150  # pylint: disable=C0103
        HEIGHT: int = 48  # pylint: disable=C0103

# End of Settings Module
# Ruff Checke, Pep8CI Checked, Now Dead Code, Some Passing
# Timestamp: 2022-06-02T18:45, copywrite (c) 2022-2025, Charles J Fowler
