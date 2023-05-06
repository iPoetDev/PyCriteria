#!/user/bin/env python3
# pylint: disable=trailing-whitespace
"""Module Run GSheet."""
from contextlib import asynccontextmanager
import sys
import warnings

from loguru import logger

# ---
# Execute the main function as User Input entry point
# pylint: disable=[no-member]
# @logcatcher.catch(onerror=lambda _: sys.exit(1))

def logging(levelint: int, on_off: int = 0):
    """Main Logging.
    :return: Nothing, just executes the add logging function.
    :rtype: Typing.NoReturn.
    """
    formatr: str = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</>"
            + " | <level>{level: <8}</level>"
            + " | <cyan>{name}</cyan>"
            + ":<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            + "| < level > {extra} </level > ")
    level: list[str] = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    toggle: list[bool] = [False, True]
    logname: str = "pycriteria.log"
    logger.add(
            logname,
            format=formatr,
            level=level[levelint],
            colorize=toggle[1],
            backtrace=toggle[on_off],
            diagnose=toggle[on_off],
            enqueue=toggle[on_off]
            )


@asynccontextmanager
async def main_logging(levelint, on_off: int = 0):
    """Main Logging."""
    formatr: str = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</>"
            + " | <level>{level: <8}</level>"
            + " | <cyan>{name}</cyan>"
            + ":<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            + "| < level > {extra} </level > ")
    level: list[str] = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    toggle: list[bool] = [False, True]
    
    try:
        logger.add(
                sys.stderr,
                format=formatr,
                level=level[levelint],
                colorize=toggle[1],
                backtrace=toggle[on_off],
                diagnose=toggle[on_off],
                enqueue=toggle[on_off]
                )
        yield
    finally:
        logger.info("=== End of Logging ===")


@logger.catch(onerror=lambda _: sys.exit(0))
def run():
    """The main function is the entry point of the program.
    It prints a welcome message and starts the app.

    :return: Nothing
    :doc-author: Trelent
    """
    # print(Settings.WELCOME)
    print("Hello World!")
    # controller.Controller.load_criteria()


if __name__ == '__run__':
    warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
    logging(1, 1)
    run()
