#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# mypy: ignore-missing-imports=True
"""Module Run GSheet."""

# 0.1 Core Imports
import logging
import sys

from typing import TextIO
from typing import Type
import warnings

# 0.2 Third Party Imports
from loguru import logger as LOGR  # type: ignore

# 0.3 Local Imports
from settings import Settings

SettingsConfig = Type[Settings]
Setting: SettingsConfig = Settings


# Logging
# pylint: disable=too-few-public-methods
class LogValues:
    """Log Values. This is a dataclass that holds the values for the loggers.
    Add methods to this class to configure the loggers later.
    Usage: Used in Loggers.configure_loguru() as a parameter.
    """
    SINK_CONSOLE: TextIO = sys.stderr
    SINK_ERROR: str = "error.log"
    SINK_PROJECT: str = "lovesand.log"
    ENABLED: bool = True
    DISABLED: bool = False
    FORMAT: str = "{time} | {level} || {message}"
    LEVEL: str = "DEBUG"
    METRE: str = "KB"
    ROTATEON: str = f"500 {METRE}"


# Config = Optional[Dict[str, List[Dict[str, Union[TextIO, str, bool]]]]]
class LOGGERS:
    """Loggers."""
    
    @staticmethod
    def configure_logging(logname: str, doeswarn: bool = True):
        """Classic logging & warnings configuration/filters.
        :param logname: Name of the log file.
        :type: str
        :param doeswarn: Enable warnings.
        :type: bool.
        """
        logging.basicConfig(filename=logname, level=logging.DEBUG)
        logging.captureWarnings(doeswarn)
        logging.info('Running on %s on port %d', Setting.HOST, Setting.HTTPS)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    @staticmethod
    def configure_loguru(values: LogValues):
        """Configure loguru logger.
        1: System Error
        2: Error Logging
        3: Project Logging.
        """
        # : list[dict[str, Union[TextIO, str, bool]]]
        config = \
            [
                    {
                            "sink": values.SINK_CONSOLE,
                            "colorize": values.ENABLED,
                            "format": values.FORMAT,
                            "level": "ERROR",
                            "enqueue": values.DISABLED,
                            "backtrace": values.ENABLED,
                            "diagnose": values.ENABLED,
                            },
                    {
                            "sink": values.SINK_ERROR,
                            "colorize": values.DISABLED,
                            "level": values.LEVEL,
                            "enqueue": values.ENABLED,
                            "format": values.FORMAT,
                            "backtrace": values.ENABLED,
                            "diagnose": values.ENABLED,
                            },
                    {
                            "sink": values.SINK_PROJECT,
                            "colorize": values.DISABLED,
                            "level": "INFO",
                            "enqueue": values.DISABLED,
                            "format": values.FORMAT,
                            "backtrace": values.ENABLED,
                            "diagnose": values.ENABLED,
                            },
                    ]
        
        LOGR.configure(handlers=config)
        return LOGR


logvalues: LogValues = LogValues()

LOGGERS.configure_logging(Setting.LOGS)

LOGRS = LOGGERS.configure_loguru(logvalues)
