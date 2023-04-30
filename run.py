#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Run GSheet."""

# 0.1 CoreLibraries
import sys

# 0.2 ThirdPartyLibraries
import loguru as logcatcher  # type: ignore

# 0.3 LocalLibraries & Settings
from projectlogging import LOGRS
from settings import Settings


# ---
# Execute the main function as User Input entry point
# pylint: disable=[no-member]
@logcatcher.catch(onerror=lambda _: sys.exit(1))
def main():
    """Main function to run the app."""
    print(Settings.WELCOME)
    LOGRS.info(Settings.WELCOME)
    LOGRS.info("Starting...")
    # TODO: Add your code here
    LOGRS.info("Done!")
    print("Done!")


if __name__ == '__run__':
    main()
