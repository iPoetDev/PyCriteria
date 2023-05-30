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
# 0.1.2 Targeted Imports
from importlib import util as findlib
from pathlib import Path
from typing import NoReturn, Union

# 0.2 Third Party Modules
import dotenv as dotenv_loader  # type: ignore
from rich import print as rprint  # type: ignore

# 0.3 Local/Own Imports
from exceptions import ManagingExceptions as Graceful


# Global String/Int Resources
# pylint: disable=too-few-public-methods, too-many-instance-attributes
@dataclasses.dataclass
class Settings:
    """Settings."""
    # Disable (C0103)
    # plylint: disable=C0301
    # https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/invalid-name.html
    DOMAINHOST: str = 'www.google.com'  # pylint: disable=C0103
    HOST: str = 'www.googleapis.com'  # pylint: disable=C0103
    APIHOST: str = 'www.googleapis.com'  # pylint: disable=C0103
    HTTPS: int = 443  # pylint: disable=C0103
    LOGS: str = 'goggle-py.log'  # pylint: disable=C0103
    ENV: str = '.env'  # pylint: disable=C0103
    ENCODE: str = 'UTF-8'  # pylint: disable=C0103
    # Data String/Int Resources
    CRED_FILE: str = 'creds.json'  # pylint: disable=C0103
    SHEET_NAME: str = 'PyCriteria'  # pylint: disable=C0103
    TAB_NAME: str = 'Data'  # pylint: disable=C0103
    TITLE: str = 'PyCriteria'  # pylint: disable=C0103
    PURPOSE: str = 'CLI to managing Project Criteria'  # pylint: disable=C0103
    WELCOME: str = \
        f'Welcome to {TITLE} {PURPOSE} App.'  # pylint: disable=C0103
    ON: bool = True  # pylint: disable=C0103
    OFF: bool = False  # pylint: disable=C0103
    # Data String/Int Resources
    FILENAME: str = 'PyCriteria'  # pylint: disable=C0103
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


class EnvirnomentalVars:
    """EnvirnomentalVars.
    
    Load .env file to develop with env vars early.
    
    :method: load_env: @staticmethod
    :method: success_load: @staticmethod
    """
    
    @staticmethod
    def load_env(library: str = 'dotenv') -> Union[bool, NoReturn]:
        """Load .env file to develop with env vars early.
        
        Parameters
        ----------
            :param library: str = 'dotenv' as default, err mandatory library.

        Return:
        ----------
            - If module is found, then .ENV loads: True or False
            - If module is not found, then NoReturn for a system exit.
            :return: Union[bool, NoReturns].
            
        """
        if findlib.find_spec(library) is None:
            message: str = f'Module: {library} not found.'
            sysexit: NoReturn = Graceful.env_notfound_status(
                    ModuleNotFoundError(message))
            return sysexit
        
        return bool(EnvirnomentalVars.does_env_load(Settings.ENV))
    
    @staticmethod
    def does_env_load(filename: str, encode: str = Settings.ENCODE) -> bool:
        """Checks if the .ENV file loads.
        
        Usage: Used when dotenv module is successfully loaded.
        
        Parameters:
        ----------
            :param filename: str,
            :param encode: str = Settings.ENCODE
            

        Returns:
        ----------
            :return: bool - If the .ENV loads: True or False
        """
        # With statement / Context management to
        # load .env file and handle closure of path/files
        success_message: str = f'Successfully loaded {filename} file.'
        # Get the path of the .env file
        dotenv_path: Path = Path(filename)
        # Open the .env file and then load/close the .env file if a file exists
        with dotenv_path.open(encoding=encode):
            rprint(success_message)
            # LOGRS.debug(success_message)
            if dotenv_loader.load_dotenv(dotenv_path=dotenv_path,
                                         verbose=True,
                                         override=True,
                                         encoding=encode):
                return True
        
        return False
