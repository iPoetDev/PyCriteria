#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Connection Management."""

# 0.1 Core Imports
import sys

# 0.2 Local Imports
from projectlogging import LOGRS
from settings import Settings


# pylint: disable=too-few-public-methods
class ManagingExceptions:
    """
    Managing Exceptions Gracefully.
    :method: env_notfound_status: @staticmethod
    :method: exiting_exception: @staticmethod
    :method: input_correction: @staticmethod
    :method: creds_correction: @staticmethod
    """
    
    @staticmethod
    def env_notfound_status(notfound: ModuleNotFoundError,
                            module: str = 'dotenv',
                            setting: str = Settings.ENV):
        """dotenv exception handler."""
        error_context: str = f'{str(notfound)}: {module}'
        issue_message: str = f'Could not load {setting} file.'
        guidance_message: str = \
            'Import python-dotenv to load external \n'
        guidance_message += f'{setting} or check the ENV file path. '
        output: str = f'{error_context}: {issue_message} - {guidance_message}'
        LOGRS.error(output)
        print(output)
    
    @staticmethod
    def exiting_status(error: Exception, message: str):
        """
        Make an exiting exception.
        1. Log the error
        2. Print the error
        3. Exit the program
        Parameters
        ----------
            :param error: Exception
            :type: Exception
            :param message: str
            :type: str
        Returns
        ----------
            :return: None
        """
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        LOGRS.error(_output)
        print(_output)
        sys.exit(1)
    
    @staticmethod
    def input_correction(error: Exception, message: str, kind: str):
        """
        Gracefully allow a user to recover from a *NotFound exception.
        Parameters
        ----------
            :param error: Exception
            :type: Exception
            :param message: str
            :type: str
            :param kind: str: File or Tab
            :type: str
        Returns
        ----------
            :return: value_str - Returns a string for a file|tab name
            :rtype: str
        """
        # Log the error and print it
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        LOGRS.error(_output)
        # Status, Success and Prompt messages
        _status: str = f'{_output}'
        _success: str = 'User input:'
        _prompt: str = f"Enter the new {kind} name:"
        # Prompt User from Console/Std.In
        while True:
            print(_status)
            _value_str = input(_prompt)
            LOGRS.info(f"{_success}: {_value_str}")
            print(_value_str)
            if ManagingExceptions.validate_input(_value_str):
                print(_success, _value_str, sep=" ")
                LOGRS.info(f"{_success}: {_value_str} is Valid")
                break
        
        return _value_str
    
    @staticmethod
    def creds_correction(credentials: str, file_type: str, message: str):
        """
            Gracefully allow a user to recover from a *NotFound exception.
            Seek a new credentials' filename from the user by prompting them.
            
            Parameters
            ----------
                :param credentials: str: Credentials file name
                :param file_type: str: Credentials file's extension is json
                :param message: str: File or Tab
                
            Returns
            ----------
                :returns: value_str: str:  Returns a string for a file|tab name
                
            """
        # Log the error and print it
        _assert_context: str = 'Assert: Credentials File'
        _output: str = f'1: {_assert_context}: \n '
        _output += f'2: {credentials} has a extension of .{file_type} \n'
        _output += f'3: {message}'
        LOGRS.error(_output)
        # Status, Success and Prompt messages
        _status: str = f'{_output}'
        _success: str = 'New Cred\'s filename + .json:'
        _prompt: str = f"Enter the new {credentials} name with .json as extension:"
        # Prompt User from Console/Std.In
        while True:
            print(_status)
            value_str = input(_prompt)
            LOGRS.info(f"User input: {value_str}")
            print(value_str)
            if ManagingExceptions.validate_input(value_str):
                print(_success, value_str, sep=" ")
                LOGRS.info(f"{_success}: {value_str} is Valid")
                break
        
        return value_str
    
    @staticmethod
    def validate_input(value_str: str):
        """
        Validate the input.
        1: Asserting of string type
        2: Checking for length is 0
        
        Parameters
        ----------
            :param value_str: string input to validate
            :type: str
            
        Returns
        ----------
            :return: True if valid else False
            :rtype: bool
            
        Raises
        ----------
            :raises ValueError: if not string or length is 0
        """
        _badtype: str = "Incorrect Type. Must be string."
        _badvalue: str = "Incorrect Value."
        _goodinput: str = "Please enter a correct input to proceed."
        try:
            if not isinstance(value_str, str):
                raise ValueError(_badtype)
            
            if not value_str:
                raise ValueError(_badvalue)
        
        except ValueError as error:
            print(f"{error}: {_goodinput}")
            return False
        
        return True
