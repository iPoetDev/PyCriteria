#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module: Run.py.

Web Terminal: Entry point.
"""
# 1. StdLib
import warnings

# 2.
# 3.
import controller

# ---
# Execute the main function as User Input entry point


def run():
    """The main function is the entry point of the program.
    It prints a welcome message and starts the app.

    :return: Nothing
    """
    # print(Settings.WELCOME)
    print("Hello World!")
    controller.main()
    # controller.Controller.load_criteria()


if __name__ == '__run__':
    warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
    run()
