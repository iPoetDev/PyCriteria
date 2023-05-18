#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, D415, ANN001
"""Module Connection Management."""

# 0.1 Core Imports
import dataclasses
import socket
import ssl

from typing import Tuple

from google.oauth2.service_account import Credentials  # type: ignore

# 0.2 Core Modules
import gspread  # type: ignore

# 0.3 Project Logging
from exceptions import ManagingExceptions as Graceful
from settings import Settings


# pylint: disable=C0103
@dataclasses.dataclass
class ConnectExceptions:
    """Connection Exceptions.: Static Class for Exception Objects."""
    # 0.5 Exceptions: base GSpread Error
    GSPREADERROR: gspread.exceptions.GSpreadException = \
        gspread.exceptions.GSpreadException  # pylint: disable=C0103
    # API Error
    APIERROR: gspread.exceptions.APIError = \
        gspread.exceptions.APIError  # pylint: disable=C0103
    # Trying to open a non-existent or inaccessible worksheet
    WORKSHEETERROR: gspread.exceptions.WorksheetNotFound = \
        gspread.exceptions.WorksheetNotFound  # pylint: disable=C0103
    # Trying to open non-existent or inaccessible spreadsheet.
    SPEADSHEETERROR: gspread.exceptions.SpreadsheetNotFound = \
        gspread.exceptions.SpreadsheetNotFound  # pylint: disable=C0103


# noinspection Style,Annotator
class GoogleConnector:
    # noinspection Style
    """Google sheet connector class.
    
    Method
    ----------
        :Method: connect_to_remote: @staticmethod
        :Method: get_source: @staticmethod
        :Method: open_sheet: @staticmethod
        :Method: fetch_data: @staticmethod
        :Method: notfound_prompt: @staticmetho.
    """
    
    # noinspection SpellCheckingInspection
    @staticmethod
    def connect_to_remote(credential_file,
                          file_type: str = "json") \
            -> gspread.client.Client:  # noqa: ANN205, ANN001
        """Synchronously connects to a Google Sheet using.
        
        1: Cred.json file
        2: Maybe checks a type of file by extension str, not mime type, defaults: json
        3: Scopes: Global.
        
        Parameters
        ----------
            :param credential_file: str
            :type: str
            :param file_type: str
            :default: json
            :type: str
            

        Returns:
        ----------
            A Scoped Credentialed Client
            :return: _creds.with_scopes(SCOPE)
            :rtype: gspread.client.Client
            

        Raises:
        ----------
            Both exit the program
            :raises: NotImplementedError
            :raises: Exception
        """
        ftype = file_type.lower()
        _output: str = f'Credential file must be a json file: Given type: {ftype}'
        
        # Authorise current client
        notimplmessage: str = 'Credentials must be scoped correctly.'
        credentials: str = credential_file
        _creds = Credentials.from_service_account_file(credentials)
        try:
            if not _creds.requires_scopes:
                raise NotImplementedError(notimplmessage)
        
        except NotImplementedError as _notimplemented:
            _output = GoogleConnector.notfound_prompt(
                    _notimplemented, credential_file)
            Graceful.exiting_status(_notimplemented, _output)
        
        return _creds.with_scopes(Settings.SCOPE)
    
    @staticmethod
    def get_source(credentials,
                   file_name: str) \
            -> gspread.Spreadsheet:  # noqa: ANN205, ANN001
        """Connects/opens to a Google Sheet synchronously else exit for now.
        
        Parameters
        ----------
            :param credentials: Google sheet scoped credentials
            :param file_name: Google sheet file name
            :type: str
        Returns
        ----------
            :return: Spreadsheet
            :rtype: gspread.spreadsheet.Spreadsheet
        Raises
        ----------
            :raises: gspread.exceptions.SpreadsheetNotFound.
        """
        # Authorise current client
        kind: str = "file"
        _gsheet: gspread.Client = gspread.authorize(credentials)
        try:
            # Tests if existing sheet is the same aśa the configured filename
            return _gsheet.open(file_name)
        except ConnectExceptions.SPEADSHEETERROR as _notfound:
            _output: str = GoogleConnector.notfound_prompt(_notfound, file_name)
            # Gracefully handle this error by asking user to enter a correct file name
            newtitle = Graceful.input_correction(_notfound, _output, kind)
            return _gsheet.open(newtitle)
    
    @staticmethod
    def open_sheet(file: gspread.Spreadsheet, tab: str) -> gspread.Worksheet:
        """Opens a given Google spreadsheet's tab by tab name.
        
        Parameters
        ----------
            :param file: Google sheet file
            :type: gspread.spreadsheet.Spreadsheet
            :param tab: Google sheet tab name
            :type:str
            

        Returns:
        ----------
            :return: worksheet
            :rtype: gspread.worksheet.Worksheet
            

        Raises:
        ----------
            Gracefully handle this error by asking user to enter a correct tab name
            :raises: gspread.exceptions.WorksheetNotFound
            :returns: worksheet
            :rtype: gspread.worksheet.Worksheet
        """
        kind: str = "tab"
        try:
            return file.worksheet(tab)
        except ConnectExceptions.WORKSHEETERROR as _notfound:
            # Gracefully handle this error by asking user to enter a correct file name
            newtab = Graceful.input_correction(_notfound, tab, kind)
            return file.worksheet(newtab)
    
    @staticmethod
    def fetch_data(sheet: gspread.Worksheet) -> list[str] | None:
        """Fetch the data from the Google sheet.
        
        Parameters
        ----------
            :param sheet:
            :type: gspread.worksheet.Worksheet
            

        Returns:
        ----------
            :return: sheet.get_all_values()
            :rtype: list[str]
            

        Raises:
        ----------
            Exits the program
            :raise: gspread.exceptions.GSpreadException: General Spreadsheet Exception
        """
        try:
            return sheet.get_all_values()
        except ConnectExceptions.GSPREADERROR as _error:
            _output: str = GoogleConnector.notfound_prompt(
                    notfound=_error,
                    name=sheet.title)
            nofetch: None = Graceful.exiting_status(_error, _output)
            return nofetch
    
    @staticmethod
    # pylint: disable=line-too-long
    def notfound_prompt(
            notfound,
            name: str) -> str:  # pylint: disable=line-too-long # noqa: ANN001
        """Builds a prompt the correct file name or tab name based on error type.

        Parameters
        ----------
        :param notfound: The error that was raised
        :type: gspread.exceptions.GSpreadException,
               gspread.exceptions.WorksheetNotFound,
               gspread.exceptions.SpreadsheetNotFound,
               NotImplementedError
        :param name: The name of the file or tab
        :type name: str
        Returns:
        ----------
        :return: str
        :rtype: str
        """
        toggle: Tuple[str, str, str, str, str] = ("api", "file", "tab", "data", "json")
        if isinstance(notfound, NotImplementedError):
            output = f"API Issue: Not Implemented Error: {notfound}\\n"
            output += "Check your connection or the Google Sheets API.\\n"
            output += "Alternatively check the credential filename"
            output += f"or extension (.{toggle[4]}).\\n"
            output += "Or check the scopes for the right scopes (.json).\\n"
            output += "Please enter the correct credential file name +"
            output += f" .\"{toggle[4]}\". Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.SpreadsheetNotFound):
            output = f"Spreadsheet Exception: {notfound}\\n"
            output += "Go to the Google Sheet or Google Drive and copy the file name.\\n"
            output += f"Please enter the correct file name. Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.WorksheetNotFound):
            output = f"Worksheet Exception: {notfound}\\n"
            output += "Go to the Google Sheet and copy the tab name.\\n"
            output += f"Please enter the correct tab name. Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.GSpreadException):
            output = f"Worksheet Data Exception: {notfound}\\n"
            output += "Can not retrieve sheet data\\n"
            output += f"Please check your settings and the sheet data. Previous: {name}"
        else:
            raise ConnectExceptions.GSPREADERROR(notfound)
        
        return output


class SSLManager:
    """SSL Manager.
    
    :method open_ssl_connection: Opens secure connects to outside network
    :method close_ssl_connection: Closes secure connects to outside network.
    """
    sslsock: ssl.SSLSocket
    
    def __init__(self):
        """Initialise SSL Manager."""
        self.sslsock: ssl.SSLSocket = SSLManager.open_ssl_connection()
    
    @staticmethod
    def open_ssl_connection() -> ssl.SSLSocket:
        """Opens secure connects to outside network
        
        :return: _ssl
        :rtype: SSLSocket.
        """
        _connection: ssl.SSLContext = ssl.create_default_context()
        _socket: socket = \
            socket.socket(
                    family=socket.AF_INET, type=socket.SOCK_STREAM)
        _ssl: ssl.SSLSocket = \
            _connection.wrap_socket(_socket,
                                    server_hostname=Settings.DOMAINHOST)
        _ssl.connect((Settings.DOMAINHOST, Settings.HTTPS))
        return _ssl
    
    @staticmethod
    def close_ssl_connection(sslsock: ssl.SSLSocket) -> None:
        """Closes secure connects to outside network
        
        Clears the sslsock variable from memory.
        """
        sslsock.close()
