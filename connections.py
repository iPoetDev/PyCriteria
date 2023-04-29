#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Connection Management."""

# 0.1 Core Imports
import dataclasses
import socket
import ssl

from typing import Tuple

from google.oauth2.service_account import Credentials

# 0.2 Core Modules
import gspread

# 0.3 Project Logging
# 0.3 Local/Own Modules/Library
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
    # Trying to open non-existent or inaccessible worksheet. worksheet(title
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
    def connect_to_remote(credential_file, file_type: str = "json"):
        """Synchronously connects to a Google Sheet using
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
        kind: str = "api"
        _creds = Credentials.from_service_account_file(credentials)
        # assert isinstance(_creds.with_scopes, SCOPE)
        try:
            if not _creds.requires_scopes:
                raise NotImplementedError(notimplmessage)
        
        except NotImplementedError as _notimplemented:
            _output: str = GoogleConnector.notfound_prompt(
                    _notimplemented, credential_file, kind)
            Graceful.exiting_status(_notimplemented, _output)
        
        return _creds.with_scopes(Settings.SCOPE)
    
    @staticmethod
    def get_source(credentials: Credentials, file_name: str) -> gspread.Spreadsheet:
        """Connects/opens to a Google Sheet synchronously else exit for now
        Parameters
        ----------
            :param credentials: Google sheet scoped credentials
            :type: google.auth.service_account.Credentials
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
        _gsheet: gspread.Client = gspread.authorize(credentials)
        _kind: str = "file"
        try:
            # Tests if existing sheet is the same aśa the configured filename
            return _gsheet.open(file_name)
        except ConnectExceptions.SPEADSHEETERROR as _notfound:
            _output: str = GoogleConnector.notfound_prompt(_notfound, file_name, _kind)
            # Gracefully handle this error by asking user to enter a correct file name
            newtitle = Graceful.input_correction(_notfound, _output, _kind)
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
    def fetch_data(sheet: gspread.Worksheet):
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
            :raises: Exception
        """
        kind: str = "tab"
        try:
            return sheet.get_all_values()
        except ConnectExceptions.GSPREADERROR as _error:
            _output: str = GoogleConnector.notfound_prompt(_error, sheet.title, kind)
            Graceful.exiting_status(_error, _output)
            return None
    
    @staticmethod
    # pylint: disable=line-too-long
    def notfound_prompt(
            notfound: (gspread.exceptions.GSpreadException,
                       gspread.exceptions.WorksheetNotFound,
                       gspread.exceptions.SpreadsheetNotFound,
                       NotImplementedError),
            name: str,
            kind: str) -> str:  # pylint: disable=line-too-long
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
        :param kind: The type of the missing resource (file or tab)
        :type kind: str

        Returns:
        ----------
        :return: str
        :rtype: str
        """
        toggle: Tuple[str, str, str, str, str] = ("api", "file", "tab", "data", "json")
        if isinstance(notfound, NotImplementedError) and toggle[0] == kind.lower():
            output = f"API Issue: Not Implemented Error: {notfound}\\n"
            output += "Check your connection or the Google Sheets API.\\n"
            output += "Alternatively check the credential filename"
            output += f"or extension (.{toggle[4]}).\\n"
            output += "Or check the scopes for the right scopes (.json).\\n"
            output += "Please enter the correct credential file name +"
            output += f" .\"{toggle[4]}\". Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.SpreadsheetNotFound) \
                and toggle[1] == kind.lower():
            output = f"Spreadsheet Exception: {notfound}\\n"
            output += "Go to the Google Sheet or Google Drive and copy the file name.\\n"
            output += f"Please enter the correct file name. Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.WorksheetNotFound) \
                and toggle[2] == kind.lower():
            output = f"Worksheet Exception: {notfound}\\n"
            output += "Go to the Google Sheet and copy the tab name.\\n"
            output += f"Please enter the correct tab name. Previous: {name}"
        elif isinstance(notfound, gspread.exceptions.GSpreadException) \
                and toggle[3] == kind.lower():
            output = f"Worksheet Data Exception: {notfound}\\n"
            output += "Can not retrieve sheet data\\n"
            output += f"Please check your settings and the sheet data. Previous: {name}"
        else:
            raise ConnectExceptions.GSPREADERROR(notfound)
        
        return output


class SSLManager:
    """SSL Manager
    :method open_ssl_connection: Opens secure connects to outside network
    :method close_ssl_connection: Closes secure connects to outside network.
    """
    
    sslsock: ssl.SSLSocket = None
    
    @staticmethod
    def open_ssl_connection():
        """Opens secure connects to outside network
        :return: _ssl
        :rtype: SSLSocket.
        """
        _connection = ssl.create_default_context()
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _ssl = _connection.wrap_socket(_socket, server_hostname=Settings.DOMAINHOST)
        _ssl.connect((Settings.DOMAINHOST, Settings.HTTPS))
        return _ssl
    
    @staticmethod
    def close_ssl_connection(sslsock: ssl.SSLSocket):
        """Closes secure connects to outside network
        Clears the sslsock variable from memory.
        """
        sslsock.close()
