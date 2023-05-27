#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: F841, ANN101, ANN001, D415, RET505, I001,
"""Module: PyCriteria Logging.

This module contains the logging configuration for the PyCriteria package.
This module was code generated assisted / generated by PerplexityAI
https://www.perplexity.ai/search/56ba87c6-09f7-4451-a106-7b5aa99a3231?s=criteria
"""
import sys
from typing import Literal

from loguru import logger


class ConnectionLogger:
    """ConnectionLogger Class.: for logging GSpread and Remote connections
    
    Initialises a Loguru logger and
    adds a file handler to log messages to a file named "gspread.log".
    The log_request method logs an HTTP request, and the log_socket method logs a socket.
    
    :method log_request: Log a HTTP request.
    :method log_socket: Log a local socket.
    :method log_connection: Log a connection., switch by mode
    """
    
    def __init__(self, verbosity: bool = True, compression: str = "zip", size: str = "10 MB"):
        self.logger = logger
        self.logger.add("connection.log",
                        rotation=size,
                        compression=compression,
                        diagnose=verbosity,
                        backtrace=verbosity,
                        catch=verbosity)
    
    def log_request(self, request):
        """Log a HTTP request."""
        self.logger.info(f"HTTP request: {request}")
    
    def log_socket(self, socket):
        """Log a local socket."""
        self.logger.info(f"Socket: {socket}")
    
    def log_connection(self,
                       response: str = "",
                       socket: str = "",
                       mode: Literal["http", "socket", "verbose"] = "http"):
        """Log a connection., switch by type"""
        if mode == "http":
            self.logger.info(f"HTTP connection: {response}")
        elif mode == "socket":
            self.logger.info(f"Socket connection: {socket}")
        elif mode == "verbose":
            self.logger.info(f"Verbose connection: {response}")
            self.logger.info(f"Socket connection: {socket}")


class AppLogger:
    """AppLogger Class.
    
     Initialises a Loguru logger and adds two handlers:
     1: one that logs messages to a file named "app.log" and
     2: another that logs messages to the console.
        The log methods logs a message at the INFO level.
        
    :method log: Log a message at the INFO level.
    :method remote: Log a message at the INFO level.
    """
    filesink: str = "app.log"
    infoformat: str = "INFO: {time} {level} {message}"
    compression: str = "zip"
    httpget: str
    socket: str
    color: bool = True
    
    def __init__(self, sink: str = "", httprequest: str = "",
                 socket: str = "",
                 verbosity: bool = True,
                 compression: str = "zip",
                 rotation: str = "10 MB"):
        # Set Properties
        self.filesink = sink if sink != "" else "app.log"
        self.http11get = httprequest if httprequest != "" \
            else "GET /api/data HTTP/1.1"
        #
        self.socketaddress = socket if socket != "" \
            else "127.0.0.1:8080"
        
        # Loguru logger
        self.logger = logger
        # File handler
        self.logger.add("app.log",
                        rotation=rotation,
                        compression=self.compression,
                        diagnose=verbosity,
                        catch=verbosity)
        # Console handler
        self.logger.add(sys.stderr,
                        format=self.infoformat,
                        colorize=self.color,
                        diagnose=verbosity,
                        backtrace=verbosity,
                        catch=verbosity)
        # Connection Logging
        self.connection = ConnectionLogger(
                verbosity=verbosity,
                compression=compression,
                size=rotation)
    
    def log(self,
            message,
            mode: Literal["http", "socket", "verbose"] = "http"):
        """Log a message at the INFO level."""
        self.logger.info(message)
        if mode == "http":
            self.connection.log_request(message)
        elif mode == "socket":
            self.connection.log_socket(message)
    
    def remote(self,
               message,
               mode: Literal["http", "socket", "verbose"] = "http"):
        """Log a message at the INFO level."""
        if mode == "http":
            self.connection.log_request(message)
        elif mode == "socket":
            self.connection.log_socket(message)
