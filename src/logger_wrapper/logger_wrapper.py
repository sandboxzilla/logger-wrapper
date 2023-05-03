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

import traceback
from collections.abc import Iterable
import time
import logging
from logging import handlers as hdls
from pathlib import PosixPath


class SingletonLogger(logging.Logger):
    """
    Custom logger class with configurable options for handlers and output format.

    Args (all optional):
        name (str): The name of the logger.
        app_name (str): The name of the application.
        level (int): The log level to be set for the logger.
        meta (bool): Whether or not to include metadata in the log output.
        date_filename (bool): Whether or not to include the date in the log file name.
        handlers (list[logging.Handler]): A list of logging handlers to be used by the logger.
    """
    __instance = None

    @staticmethod
    def __new__(cls,
                name: str = None,
                app_name: str = None,
                level: int = logging.DEBUG,
                meta: bool = True,
                date_filename: bool = True,
                handlers=None):

        if SingletonLogger.__instance is None:
            SingletonLogger.__instance = super.__new__(cls, name, level)
            SingletonLogger.__instance.setLevel(level)

            if handlers is None:
                handlers = [logging.StreamHandler()]

            SingletonLogger.__instance.app_name = app_name
            SingletonLogger.__instance.meta = meta
            SingletonLogger.__instance.handlers = handlers

            for handler in SingletonLogger.__instance.handlers:
                if not isinstance(handler, logging.Handler):
                    continue
                if isinstance(handler, logging.FileHandler):
                    if date_filename:
                        handler_dict = handler.__dict__.copy()
                        handler.close()
                        SingletonLogger.__instance.handlers.remove(handler)
                        del handler
                        name = PosixPath(handler_dict["baseFilename"])
                        if name.exists():
                            name.unlink()

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

                SingletonLogger.__instance.addHandler(hdlr=handler)

            SingletonLogger.set_default_format(app_name=app_name)
            SingletonLogger.__instance.get_output_path = SingletonLogger.get_output_path
            SingletonLogger.__instance.remove_handler = SingletonLogger.remove_handler
            SingletonLogger.__instance.version = SingletonLogger.version
            SingletonLogger.__instance.set_default_format = SingletonLogger.set_default_format

        return SingletonLogger.__instance

    @classmethod
    def set_default_format(cls, app_name: str = None):
        """
        Format the log message to a default format.

        Args:
            handler_type (logging.Handler): The handler type of interest.
                                            If None all handlers' output path
                                            will be returned in a list.
        """
        SingletonLogger.__instance.format_keys = ['%(asctime)s,']
        if app_name is not None:
            SingletonLogger.__instance.format_keys.append(f'{app_name},')
        if SingletonLogger.__instance.meta:
            SingletonLogger.__instance.format_keys.append('[%(levelname)s:')
            SingletonLogger.__instance.format_keys.append('pid=%(process)d:')
            SingletonLogger.__instance.format_keys.append('%(threadName)s:')
            SingletonLogger.__instance.format_keys.append('%(module)s:')
            SingletonLogger.__instance.format_keys.append('%(funcName)s:')
            SingletonLogger.__instance.format_keys.append('%(lineno)d],')
        SingletonLogger.__instance.format_keys.append('%(message)s')

        SingletonLogger.__instance.formatter = logging.Formatter(''.join(SingletonLogger.__instance.format_keys))
        for handler in SingletonLogger.__instance.handlers:
            handler.setFormatter(SingletonLogger.__instance.formatter)

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
        for handler in SingletonLogger.__instance.handlers:
            if isinstance(handler, logging.Handler):
                if handler_type and isinstance(handler, handler_type):
                    paths.append(str(handler.stream.name))
                elif isinstance(handler, (hdls.SysLogHandler,
                                          hdls.SocketHandler)):
                    paths.append(str(handler.address))
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
        for handler in SingletonLogger.__instance.handlers:
            if isinstance(handler, handler_type):
                SingletonLogger.__instance.handlers.remove(handler)

    @property
    def version(self):
        """
        A property that returns the current version of this class.

        Returns:
            str: The current version number.
        """
        return __version__


class LoggerWrapper(logging.Logger):
    """
    A helper class that subclasses the Logger class from the logging module and
    provides a configurable logger.
    This logger supports both file and console output with a specified format.

    Args:
        name (str, optional): The name of the logger also the
        prefix of the log files.
        Defaults to None.

        app_name (str, optional): The name of the application.

        instance_name (str, optional): The name of the LoggerWrapper instance.

        level (int, optional): the log level to set. Defaults to None.
        Default to DEBUG.

        date_filename (bool, optional): Whether to add a date to the
        filename when saving logs to a file.
        Defaults to True.

        handlers (list, optional): List of handlers to add to the logger.
        Defaults to [StreamHnadler].

    Returns:
        logging.Logger: A configured Logger instance.
    """

    def __init__(self,
                 name: str  = None,
                 app_name: str = None,
                 instance_name: str = None:
                 level: int = logging.DEBUG,
                 meta: bool = True,
                 date_filename: bool = True,
                 handlers=None):

        super.__init__(name, level=level)
        self.logger = SingletonLogger(name=name,
                                      app_name=app_name,
                                      level=level,
                                      meta=meta,
                                      date_filename=date_filename,
                                      handlers=handlers)

        if instance_name is not None:
            text = traceback.extract_stack()[-2][3]
            self.instance_name = text[:text.find('=')].strip()
            self.instance_id = id(self)
        else:
            self.instance_name = instance_name

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """=
        Log a message.
        """
        msg = f"{self.instance_name}: {msg}"
        self.logger._log(level, msg, args, exc_info, extra, stack_info)


if __name__ == "__main__":
    name = None
    handlers = [logging.StreamHandler(),
                logging.FileHandler("test.logs")
                ]
    log1 = LoggerWrapper(name="app", handlers=handlers)

    log2 = LoggerWrapper(name="test")

    log1_name = log1.instance_name
    log2_name = log1.instance_name

    print(str(log2.get_output_path()))
    print(str(log1.get_output_path()))

    print(log2.version)
    for count in range(10):
        if count == 5:
            log1.remove_handler(logging.StreamHandler)
        log1.info("test of " + str(count))
        log2.info("test of " + str(count))

    print(log1.version)
