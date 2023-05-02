#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Run GSheet."""

# 0.1 CoreLibraries
import sys

# 0.2 ThirdPartyLibraries
import loguru as logcatcher  # type: ignore


# 0.3 LocalLibraries & Settings
# from projectlogging import LOGRS


# ---
# Execute the main function as User Input entry point
# pylint: disable=[no-member]
@logcatcher.catch(onerror=lambda _: sys.exit(1))
def main():
    """
    The main function is the entry point of the program.
    It prints a welcome message and starts the app.

    :return: Nothing
    :doc-author: Trelent
"""
    # print(Settings.WELCOME)
    print("Hello World!")


if __name__ == '__run__':
    main()
