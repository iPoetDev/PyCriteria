#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Exception Status and Graceful recovery."""

# 0.1: Standard Library Imports
import sys

from typing import NoReturn


class ExceptionValues:
    """Exception Values.
    Introduced to remove cylic dependencies/imports.
    """
    ENV: str = '.env'


# pylint: disable=too-few-public-methods
class ManagingExceptions:
    """Managing Exceptions Gracefully.
    :method: env_notfound_status: @staticmethod
    :method: exiting_exception: @staticmethod
    :method: input_correction: @staticmethod
    :method: creds_correction: @staticmethod.
    """
    
    @staticmethod
    def env_notfound_status(notfound: ModuleNotFoundError,
                            module: str = 'dotenv',
                            setting: str = ExceptionValues.ENV) -> NoReturn:
        """@2023-05-05
        Dotenv exception handler.
        
        Parameters
        ----------
        :param notfound: ModuleNotFoundError: The exception to handle
        :param module: str: The module name
        :param setting: str: The ENV filename name
        

        Returns:
        ----------
        :return: NoReturn
        """
        error_context: str = f'{str(notfound)}: {module}'
        issue_message: str = f'Could not load {setting} file.'
        guidance_message: str = \
            'Import python-dotenv to load external \n'
        guidance_message += f'{setting} or check the ENV file path. '
        output: str = f'{error_context}: {issue_message} - {guidance_message}'
        print(output)
        return NoReturn
    
    @staticmethod
    def exiting_status(error: Exception, message: str):
        """@2023-05-05
        Make an exiting exception.
        1. Log the error
        2. Print the error
        3. Exit the program.
        
        Parameters
        ----------
            :param error: Exception
            :type: Exception
            :param message: str
            :type: str
        """
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        print(_output)
        sys.exit(1)
    
    @staticmethod
    def input_correction(error: Exception, message: str, kind: str) -> str:
        """@2023-05-05
        Gracefully allow a user to recover from a *NotFound exception.
        
        Parameters
        ----------
            :param error: Exception: The exception to handle
            :param message: str: The error message to display
            :param kind: str: File or Tab type
            

        Returns:
        ----------
            :return: value_str: str: Returns a string for a file|tab name
        """
        # Log the error and print it
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        # LOGRS.error(_output)
        # Status, Success and Prompt messages
        _status: str = f'{_output}'
        _success: str = 'User input:'
        _prompt: str = f"Enter the new {kind} name:"
        # Prompt User from Console/Std.In
        while True:
            print(_status)
            _value_str = input(_prompt)
            print(_value_str)
            if ManagingExceptions.validate_input(_value_str):
                print(_success, _value_str, sep=" ")
                break
        
        return _value_str
    
    @staticmethod
    def creds_correction(credentials: str, file_type: str, message: str) -> str:
        """@2023.05.03
        Gracefully allow a user to recover from a *NotFound exception.
        Seek a new credentials' filename from the user by prompting them.
        
        Parameters
        ----------
        :param credentials: str: Credentials file name
        :param file_type: str: Credentials file's extension is json
        :param message: str: File or Tab
        

        Returns:
        ----------
        :returns: value_str: str:  Returns a string for a file|tab name
        
        """
        # 1. Log the error and print it
        _assert_context: str = 'Assert: Credentials File'
        _output: str = f'1: {_assert_context}: \n '
        _output += f'2: {credentials} has a extension of .{file_type} \n'
        _output += f'3: {message}'
        # 2. Status, Success and Prompt messages
        _status: str = f'{_output}'
        _success: str = 'New Cred\'s filename + .json:'
        _prompt: str = f"Enter the new {credentials} name with .json as extension:"
        # 3. Prompt User from Console/Std.In
        while True:
            print(_status)
            value_str = input(_prompt)
            print(value_str)
            if ManagingExceptions.validate_input(value_str):
                print(_success, value_str, sep=" ")
                break
        # 4. Return the new credentials' filename
        return value_str
    
    @staticmethod
    def validate_input(value_str: str) -> bool:
        """Validate the input. @2023.05.03
        1: Asserting of string type
        2: Checking for length is 0.
        
        Parameters
        ----------
            :param value_str: string input to validate
            :type: str
            

        Returns:
        ----------
            :return: True if valid else False
            :rtype: bool
            

        Raises:
        ----------
            :raises ValueError: if not string or length is 0
        """
        # 1. Init Validation info messages
        _badtype: str = "Incorrect Type. Must be string."
        _badvalue: str = "Incorrect Value."
        _goodinput: str = "Please enter a correct input to proceed."
        # 2. Test the input types and values for validity
        try:
            if not isinstance(value_str, str):
                raise ValueError(_badtype)
            
            if not value_str:
                raise ValueError(_badvalue)
        # 3. Handle the exceptions
        except ValueError as error:
            print(f"{error}: {_goodinput}")
            return False
        # 4. Return True if valid
        return True


ManagedExceptions: ManagingExceptions = ManagingExceptions()
