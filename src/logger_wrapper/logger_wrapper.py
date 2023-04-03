#!/bin/python3
"""
 **[LoggerWrapper Package]**

This package provides a wrapper for the built - in logging.Logger:

**LoggerWrapper:**

The LoggerWrapper class wraps the logging.Logger class to pre-configure some of
the common tasks like formating.

The LoggerWrapper class has the following methods::

    *get_output_path(handler_type: logging.Handler=None):*  Tries to retrieve
    a list of output targets of the handler that matches the type passed in.
    If handler_type is None, all the output targets for all the registered
    handlers are returned.
    *NOTE:* Not fully tested

    *remove_handler(handler_type: logging.Handler=None):*  Removes the handlers
    that matches the type passed in . If the handler_type is None or the
    handler_type is not registered, none of the handlers will be removed.
    If an abstract handler is given, all handler that have inherited will
    be removed.

    *version():*  The package version.

 **Example Usage::**

<code >
import logging
from logging import handlers as hdls

if __name__ == "__main__":
    name = None
    handlers = [logging.StreamHandler(), hdls.SysLogHandler(address='/dev/log')]
    log = LoggerWrapper(name=name,
                        level=logging.DEBUG,
                        date_filename=True,
                        meta=True,
                        handlers=handlers)

    print("version: " + log.version)

    for count in range(10):
        if count == 5:
            log.remove_handler(logging.StreamHandler)
        log.info("test of " + str(count))
< / code >

    Copyright (c)  2023.  Erol Yesin/Sandboxzilla

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""
__author__ = 'Erol Yesin'
__version__ = '0.0.1'

from collections.abc import Iterable
from gettext import install
import time
import logging
from logging import handlers as hdls
from pathlib import PosixPath


class LoggerWrapper(logging.Logger):
    """
    A helper class that subclasses the Logger class from the logging module and
    provides a configurable logger.
    This logger supports both file and console output with a specified format.

    Args:
        name (str or PosixPath, optional): The name of the logger also the
        prefix of the log files.
        Defaults to None.

        level (int, optional): the log level to set. Defaults to None.
        Default to DEBUG.

        date_filename (bool, optional): Whether or not to add a date to the
        filename when saving logs to a file.
        Defaults to True.

        handlers (list, optional): List of handlers to add to the logger.
        Defaults to [StreamHnadler].

    Returns:
        logging.Logger: A configured Logger instance.
    """
    __instance = None

    def __new__(cls,
                name: str | PosixPath = None,
                level: int = logging.DEBUG,
                meta: bool = True,
                date_filename: bool = True,
                handlers: Iterable[logging.Handler] = [logging.StreamHandler()]) -> logging.Logger:

        if LoggerWrapper.__instance is None:

            LoggerWrapper.__instance = logging.getLogger(name=str(name))
            LoggerWrapper.__instance.setLevel(level=level)

            if meta:
                LoggerWrapper.__instance.formatter = logging.Formatter(
                    '%(asctime)s,[%(levelname)s:pid=%(process)d:%(threadName)s:%(module)s:%(funcName)s:%(lineno)d],%(message)s')
            else:
                LoggerWrapper.__instance.formatter = logging.Formatter('%(asctime)s,%(message)s')

            for handler in handlers:
                if not isinstance(handler, logging.Handler):
                    continue
                if isinstance(handler, logging.FileHandler):
                    if date_filename:
                        handler_dict = handler.__dict__.copy()
                        handler.close()
                        del handler

                        name = PosixPath(handler_dict["baseFilename"])
                        name.parent.mkdir(parents=True, exist_ok=True)

                        sfx = name.suffix
                        if len(sfx) == 0:
                            sfx = '.log'

                        handler = logging.FileHandler(filename=str(PosixPath(name.parent,
                                                                             name.stem +
                                                                             time.strftime("_%Y%m%d%H%M%S") +
                                                                             sfx)),
                                                      mode=handler_dict["mode"],
                                                      encoding=handler_dict["encoding"],
                                                      delay=handler_dict["delay"],
                                                      errors=handler_dict["errors"])

                handler.setFormatter(LoggerWrapper.__instance.formatter)
                LoggerWrapper.__instance.addHandler(handler)

            LoggerWrapper.__instance.get_output_path = cls.get_output_path
            LoggerWrapper.__instance.remove_handler = cls.remove_handler
            LoggerWrapper.__instance.version = cls.version

        return LoggerWrapper.__instance

    @classmethod
    def get_output_path(cls, handler_type: logging.Handler = None) -> Iterable[str]:
        """=
        Get the output path of specific handler type or all registered handlers.

        Args:
            handler_type (logging.Handler): The handler type of interest.
                                            If None all handlers' output path
                                            will be returned in a list.
        NOTE: Not fully tested
        """
        paths = []
        for handler in LoggerWrapper.__instance.handlers:
            if isinstance(handler, logging.Handler):
                if handler_type and isinstance(handler, handler_type):
                    paths.append(str(handler.stream.name))
                elif isinstance(handler, (hdls.SysLogHandler,
                                          hdls.SocketHandler)):
                    paths.append(str(handler.stream.address))
                elif isinstance(handler, hdls.SMTPHandler):
                    paths.append(handler.toaddrs)
                elif isinstance(handler, hdls.BufferingHandler):
                    paths.append("<mem>")
                elif isinstance(handler, hdls.HTTPHandler):
                    paths.append(handler.url)
                elif isinstance(handler, hdls.QueueHandler):
                    paths.append("<queue>")
                elif isinstance(handler, logging.StreamHandler):
                    paths.append(handler.stream.name)
        return paths

    @classmethod
    def remove_handler(cls, handler_type: logging.Handler):
        """
        Remove a specific handler type from the logger instance.

        Args:
            handler_type (logging.Handler): The handler type to be removed.
                                            If the top level handler (logging.Handler)
                                            is given, all handlers will be removed.
        """
        for handler in LoggerWrapper.__instance.handlers:
            if isinstance(handler, handler_type):
                LoggerWrapper.__instance.handlers.remove(handler)

    @classmethod
    @property
    def version(cls):
        """
        A property that returns the current version of this class.

        Returns:
            str: The current version number.
        """
        return __version__


if __name__ == "__main__":
    name = None
    handlers = [logging.StreamHandler(),
                hdls.SysLogHandler(address='/dev/log'),
                ]
    log = LoggerWrapper(name=name,
                        level=logging.DEBUG,
                        date_filename=True,
                        meta=True,
                        handlers=handlers)

    print("version: " + log.version)

    print(str(log.get_output_path()))

    for count in range(10):
        time.sleep(0.499)
        if count == 5:
            log.remove_handler(logging.StreamHandler)
        log.info("test of " + str(count))
