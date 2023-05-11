#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: Run.py.

Web Terminal: Entry point.
"""
# 1. StdLib
import subprocess

import typer
from rich import print as rprint

import controller
# 3. Local/Own
from app import AppValues as Values

# 2. 3rd Party
# ---
# Execute the main function as User Input entry point
# Execute a typer.run() function as a CLI entry point

cli = typer.Typer(name=Values.app,
                  epilog=Values.epilogue,
                  add_completion=Values.OFF,
                  no_args_is_help=Values.ON, )


# cli.add_typer(app.App,name=Values.name,help="PyCriteria Terminal App.",no_args_is_help=True)

@cli.command("start")
def run():
    """The main function is the entry point of the program.
    It prints a welcome message and starts the app.

    :return: Nothing
    """
    # print(Settings.WELCOME)
    print("Hello World!")
    controller.main()


def entry():
    """The main function is the entry point of the program.
    It prints a welcome message and starts the app."""
    run_subprocess()


# Define the function to run the subprocess
def run_subprocess():
    """Run the subprocess.
    
    This calls the Python script using the subprocess module.
    A: set the initial command to call the script
    B: starts the subprocess in a loop until the user enters an exit command.
    C:
    exit command.
    
    Source:
    ------------------
    This code comes from 3rd Party Source, in its entirety.
    This function was compiled from the following source: NotionAI
    I am a subscriber.
    Subsprocessing is outside of the scope of the assignement, by topics,.
    
    Example:
    Thought:
        I searched for how to run a Python script from another file.
        Credits: https://www.w3docs.com/snippets/python/how-can-i-make-one-python-file-run-another.html # noqa
    Problem to solve
        1. Default.js called Pty.spwand("python", "run.py")
        2. Needed to have more control over the immediate exection of the app.py
        3. The goal is to have a sub-process to blink wait
           i. For a user input, or sequences
           ii. Without exiting the main process or subprocess.
    Notion AI: prompt generatoring
    To call a Python file in a long-running subprocess until a user enters
        an exit command, you can use the subprocess module in Python.
    It gave me a suggestion from
    1: It gave me a while loop to call the subprocess
    2: It gave me a way to exit the subprocess wusing a context manager.
    3: It gave a way to use a while loop to call a subprocess and a context manager.
    
    It evaluated and rated the options of the subprocess module.
    1: This solution is simple and easy to understand
    2: This solution is cleaner than solution 1 as it doesn't require a while loop.
    3: This solution is more complex than the other two solutions,
        but it provides more control over the subprocess.
        
    ADR: Decided to use a directly referenced code from option 3.
    """
    # Set the initial command to call the Python script
    cmd = ['python', 'app.py']
    
    # Start the subprocess in a loop until the user enters an exit command
    #
    exit_flag = False
    while not exit_flag:
        # Within the loop, run the subprocess using the Popen() method
        # Starts the subprocess and returns a Popen object
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            # Use the `communicate()` to wait for the subprocess to finish
            # Capture the output and error message
            output, error = p.communicate()
            
            # Print the output and error messages
            rprint(output.decode, flush=True)
            rprint(error.decode(), flush=False)
            
            # Ask the user if they want to exit
            user_input = input("Enter 'exit' to stop the subprocess: ")
            
            # If the user enters 'exit', break out of the loop
            if user_input == 'exit':
                exit_flag = True


if __name__ == '__run__':
    # controller.warn()
    entry()
