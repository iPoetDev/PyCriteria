#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module App Settings and Environmental Vars."""
import dataclasses
from importlib import util as findlib
# 0.2 Core Modules
from pathlib import Path

import dotenv as dotenv_loader

from exceptions import ManagingExceptions as Graceful
from projectlogging import LOGRS


# Global String/Int Resources
# pylint: disable=R0902, too-many-instance-attributes
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
    TITLE: str = 'PyCriteria'  # pylint: disable=C0103
    PURPOSE: str = 'CLI to managing Project Criteria'  # pylint: disable=C0103
    WELCOME: str = f'Welcome to {TITLE} {PURPOSE} App.'  # pylint: disable=C0103
    # Data String/Int Resources
    FILENAME: str = 'PyCriteria'  # pylint: disable=C0103
    TAB_START: str = 'overview'  # pylint: disable=C0103
    SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]  # pylint: disable=C0103


class EnvirnomentalVars:
    """EnvirnomentalVars.
    Load .env file to develop with env vars early.
    
    :method: load_env: @staticmethod
    :method: success_load: @staticmethod
    """
    
    @staticmethod
    def load_env(library: str = 'dotenv'):
        """Load .env file to develop with env vars early."""
        if findlib.find_spec(library) is None:
            message: str = f'Module: {library} not found.'
            Graceful.env_notfound_status(
                    ModuleNotFoundError(message))
        else:
            EnvirnomentalVars.does_env_load(Settings.ENV)
    
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
            LOGRS.debug(success_message)
            return dotenv_loader.load_dotenv(dotenv_path=dotenv_path)


# Module Global Object Resources for Export
# pylint: disable=trailing-whitespace
Settings: Settings = Settings()
EnvirnomentalVars: EnvirnomentalVars = EnvirnomentalVars()  # pylint: disable=trailing-whitespace
