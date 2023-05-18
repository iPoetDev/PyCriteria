#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module App Settings and Environmental Vars."""
# 0.1 Standard Imports
import dataclasses


# 0.1.2 Targeted Imports
from importlib import util as findlib
from pathlib import Path
from typing import Dict
from typing import NoReturn
from typing import Union

# 0.2 Third Party Modules
import dotenv as dotenv_loader  # type: ignore

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
    WELCOME: str = f'Welcome to {TITLE} {PURPOSE} App.'  # pylint: disable=C0103
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


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class TableSettings:
    """TableSettings."""
    CRITERIA_FILTER: Dict[str, str] = \
        {"H1": "CriteriaGroup",
         "I1": "CriteriaTopic",
         "J1": "CriteriaRef",
         "K1": "Criteria",
         "L1": "Progress",
         "M1": "ToDoFlag",
         "N1": "Notes"}
    METADATA_FILTER: Dict[str, str] = \
        {"A1": "RowID",
         "B1": "Position",
         "C1": "Tier",
         "D1": "TierPrefix",
         "E1": "TierDepth",
         "F1": "DoD",
         "G1": "Performance",
         }
    HEADERS_RANGE: str = 'A1:O1'
    COLUMN_RANGE: str = 'A:O'
    ROW_START_POS: str = '1'
    ROW_END_POS: str = '71'
    DATA_RANGE: str = 'A2:071'
    TOTAL_RANGE: str = 'A1:071'


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
        # With statement / Context management to load .env file and handle closure of path/files
        success_message: str = f'Successfully loaded {filename} file.'
        # Get the path of the .env file
        dotenv_path: Path = Path(filename)
        # Open the .env file and then load/close the .env file if a file exists
        with dotenv_path.open(encoding=encode):
            print(success_message)
            # LOGRS.debug(success_message)
            if dotenv_loader.load_dotenv(dotenv_path=dotenv_path,
                                         verbose=True,
                                         override=True,
                                         encoding=encode):
                return True
        
        return False
