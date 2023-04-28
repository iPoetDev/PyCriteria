#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module App Settings and Environmental Vars."""
# 0.2 Core Modules
from pathlib import Path

import dotenv as dotenv_loader

from exceptions import ManagingExceptions as Graceful
from projectlogging import LOGRS


# Global String/Int Resources
class Settings:
    """ Settings."""
    DOMAINHOST: str = 'www.google.com'
    HOST: str = 'www.googleapis.com'
    APIHOST: str = 'www.googleapis.com'
    HTTPS: int = 443
    LOGS: str = 'goggle-py.log'
    ENV: str = '.env'
    ENCODE: str = 'UTF-8'
    # Data String/Int Resources
    CRED_FILE: str = 'creds.json'
    TITLE: str = 'Love Sandwiches'
    PURPOSE: str = 'Data Automation'
    WELCOME: str = f'Welcome to {TITLE} {PURPOSE} App.'
    # Data String/Int Resources
    FILENAME: str = 'LoveSandwiches'
    TAB_SALES: str = 'sales'
    TAB_STOCK: str = 'stock'
    TAB_SURPLUS: str = 'surplus'
    SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]


class EnvirnomentalVars:
    """
    EnvirnomentalVars.
    Load .env file to develop with env vars early.
    
    :method: load_env: @staticmethod
    :method: success_load: @staticmethod
    """
    
    @staticmethod
    def load_env():
        """
        Load .env file to develop with env vars early.
        """
        try:
            from dotenv import load_dotenv
        except ModuleNotFoundError as modulenotfound:
            Graceful.env_notfound_status(modulenotfound)
        else:
            EnvirnomentalVars.does_env_load(Settings.ENV)
    
    @staticmethod
    def does_env_load(filename: str, encode: str = Settings.ENCODE) -> bool:
        """
        Checks if the .ENV file loads.
        Usage: Used when dotenv module is successfully loaded
        
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
