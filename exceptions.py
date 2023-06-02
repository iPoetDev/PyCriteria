#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# noqa: W293 blank line contains whitespace
# - Without global file level rule, using # noqa: is not possible
"""Module Exception Status and Graceful recovery.

Usage:
-------------------------
- ExceptionValues: Global Settings for the Exceptions logic.
                Anti cyclic references
- ManagingExceptions: Gracefully handle exceptions for datasources,
                Exceptions for API shutdowns, errros, and HTTP 429,
                See: https://github.com/iPoetDev/PyCriteria/issues/32

Linting:
-------------------------
- pylint: disable=
            trailing-whitespace
            too-few-public-methods,
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
:imports: sys

3rd Paty Imports
:imports: rich

:class: Settings
:class: EnvirnomentalVars -
Used to load environmental variables from .env file.
"""

# 0.1: Standard Library Imports
import sys

from rich import print as rprint


class ExceptionValues:
    """Exception Values."""
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
    def exiting_status(error: Exception, message: str) -> None:
        """Make an exiting exception.
        
        Make an exiting exception.
        1. Log the error
        2. Print the error
        3. Exit the program.
        
        Parameters
        ----------
            :param error: Exception
            :param message: str
            

        Returns:
        ----------
            :return: NoReturn
        """
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        rprint(_output)
        sys.exit(1)
    
    @staticmethod
    def input_correction(error: Exception, message: str, kind: str) -> str:
        """Gracefully allow a user to recover from a *NotFound exception.
        
        Parameters
        ----------
            :param error: Exception: The exception to handle
            :param message: str: The error message to Display
            :param kind: str: File or Tab type
            

        Returns:
        ----------
            :return: value_str: str: Returns a string for a file|tab name
        """
        # Log the error and print it
        _error_context: str = f'{str(error).title}'
        _output: str = f'{_error_context}: {error}: {message}'
        # Status, Success and Prompt messages
        _status: str = f'{_output}'
        _success: str = 'User input:'
        _prompt: str = f"Enter the new {kind} name:"
        # Prompt User from Console/Std.In
        while True:
            rprint(_status)
            _value_str = input(_prompt)
            rprint(_value_str)
            if ManagingExceptions.validate_input(_value_str):
                rprint(_success, _value_str)
                break
        
        return _value_str
    
    @staticmethod
    def creds_correction(credentials: str,
                         file_type: str,
                         message: str) -> str:
        """Make an exiting exception.
        
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
        _prompt: str = f"Enter the new {credentials} #" \
                       "name with .json as extension:"
        # 3. Prompt User from Console/Std.In
        while True:
            rprint(_status)
            value_str = input(_prompt)
            rprint(value_str)
            if ManagingExceptions.validate_input(value_str):
                rprint(_success, value_str)
                break
        # 4. Return the new credentials' filename
        return value_str
    
    @staticmethod
    def validate_input(value_str: str) -> bool:
        """Validate the input.
        
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
            rprint(f"{error}: {_goodinput}")
            return False
        # 4. Return True if valid
        return True


ManagedExceptions: ManagingExceptions = ManagingExceptions()
