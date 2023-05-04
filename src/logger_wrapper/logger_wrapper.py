#!/bin/python3
"""
 **[LoggerWrapper Package]**

This package provides a wrappers for the built - in logging.Logger:

**PseudoSingletonLogger::**

The PseudoSingletonLogger class inherits the logging.Logger and
instentiates a singleton for each logger name give.
PsudoSigletonLogger pre-configures some of the common tasks like
formating to force a standard logging format.
If given the optiopnal 'app_name' the name of the application is used in the header.
If given the 'use_instance' flag a space is allocated for the instance name
for the client class to inject during logging.
The PsudoSigletonLogger class has the following methods::

    *set_default_format(logger_name: str = None, app_name: str = None, use_instance: bool = False)*
    Sets the default logging format for the given logger_name.  If no logger_name
    provided the loggger instance used.

    *get_output_path(logger_name: str = None, handler_type: logging.Handler=None):*
    Tries to retrieve a list of output targets for the handler that matches the
    type passed in. If handler_type is None, all the targets for all the registered
    handlers are returned.
    If no logger_name than the default is the last_logger instance used.
    *NOTE:* Not fully tested for all handler types

    *remove_handler(logger_name: str = None, handler_type: logging.Handler=None):*
    Removes the handlers that matches the type passed in. If the handler_type
    is None or the handler_type is not registered, none of the handlers will
    be removed.  If an abstract handler is given, all handler that have inherited
    will be removed.
    If no logger_name than the default is the last_logger instance used.

    *version():*  The package version.

**LoggerWrapper::**

The LoggerWrapper class inherits the logging.Logger and retrieves the
PsudoSigletonLogger class insance to pre-configure some of the common tasks like
formating to force a standard logging format.
If given the optional 'app_name' the name of the application is used in the header.
Unlike the 'instance name', the 'app_name' is not as easily changeable.
LoggerWrapper injects the instance name in the log message header.
The instance name is optionaly provided during initialization.  If not provided
it's pulled from the stack.  The instance name can also be changed by the
*change_instance_name* method
Unlike the PseudoSingletonLogger class, the LoggerWrapper instances are
not a singleton nor a psedo-singleton.
The LoggerWrapper class has the following methods::

    *change_instance_name(self, instance_name: str):*
    Changes the instance name to use in the log message header.

    *_log(level, msg, args,*
            *exc_info=None, extra=None,*
            *stack_info=False, stacklevel: int = 1)*
    Overwrites the logging.Logger._log method to inject the instance name in
    the log message header.

 **Example Usage::**

<code >
import logging
from logging import handlers as hdls
from pathlib import Path

if __name__ == "__main__":
    log_path = Path(".logs", "test.log")
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(),
                logging.FileHandler(log_path)]
    log1 = LoggerWrapper(app_name="LoggerWrapper Demo",
                         handlers=handlers,
                         meta=True,
                         date_filename=False)

    log2 = LoggerWrapper()
    print(log2.version)

    print(str(log1.get_output_path()))

    for count in range(10):
        if count == 5:
            log1.remove_handler(logging.StreamHandler)
        log1.info("test of " + str(count))
        log2.info("test of " + str(count))

    print(str(log2.get_output_path()))
    print(log1.version)
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
__version__ = '0.1.0'

import traceback
from collections.abc import Iterable
import time
import logging
from logging import handlers as hdls
from pathlib import Path, PosixPath


class PseudoSingletonLogger(logging.Logger):
    """
    Custom logger class with configurable options for handlers and output format.

    Args (all optional):
        name (str): The name of the logger.  Each name will have itsown instance.
        app_name (str): The name of the application.
        level (int): The log level to be set for the logger.
        meta (bool): Whether or not to include metadata in the log output.
        date_filename (bool): Whether or not to include the date in the log file name.
        handlers (list[logging.Handler]): A list of logging handlers to be used by the logger.
    """
    __instance = {"root": None}
    __last_instance = None

    @staticmethod
    def __new__(cls,
                name: str = "root",
                app_name: str = None,
                level: int = logging.DEBUG,
                meta: bool = True,
                use_instance: bool = False,
                date_filename: bool = True,
                handlers=None):

        if name not in PseudoSingletonLogger.__instance or PseudoSingletonLogger.__instance[name] is None:
            __this_instance = logging.getLogger(name=name)
            name = __this_instance.name
            __this_instance.setLevel(level)

            __this_instance.logger_name = name

            if handlers is None:
                handlers = [logging.StreamHandler()]

            __this_instance.app_name = app_name
            __this_instance.meta = meta
            __this_instance.handlers = handlers

            for handler in __this_instance.handlers:
                if not isinstance(handler, logging.Handler):
                    continue
                if isinstance(handler, logging.FileHandler):
                    if date_filename:
                        handler_dict = handler.__dict__.copy()
                        handler.close()
                        __this_instance.handlers.remove(handler)
                        del handler
                        file_name = PosixPath(handler_dict["baseFilename"])
                        if file_name.exists():
                            file_name.unlink()

                        file_name.parent.mkdir(parents=True, exist_ok=True)

                        sfx = file_name.suffix
                        if len(sfx) == 0:
                            sfx = '.log'

                        handler = logging.FileHandler(filename=str(PosixPath(file_name.parent,
                                                                             file_name.stem +
                                                                             time.strftime("_%Y%m%d%H%M%S") +
                                                                             sfx)),
                                                      mode=handler_dict["mode"],
                                                      encoding=handler_dict["encoding"],
                                                      delay=handler_dict["delay"],
                                                      errors=handler_dict["errors"])

                __this_instance.addHandler(hdlr=handler)

            PseudoSingletonLogger.__instance[name] = __this_instance
            PseudoSingletonLogger.set_default_format(logger_name=name,
                                                     app_name=app_name,
                                                     use_instance=use_instance)

            PseudoSingletonLogger.__instance[name].get_output_path = PseudoSingletonLogger.get_output_path
            PseudoSingletonLogger.__instance[name].remove_handler = PseudoSingletonLogger.remove_handler
            PseudoSingletonLogger.__instance[name].version = PseudoSingletonLogger.version
            PseudoSingletonLogger.__instance[name].set_default_format = PseudoSingletonLogger.set_default_format

        PseudoSingletonLogger.__last_instance = PseudoSingletonLogger.__instance[name]
        return PseudoSingletonLogger.__last_instance

    @classmethod
    def set_default_format(cls,
                           logger_name: str = None,
                           app_name: str = None,
                           use_instance: bool = False):
        """
        Format the log message to a default format.

        Args:
            app_name (str, optional): The application name.
            use_instance (bool, optional): A flag to indicate that we will be using the instance name.
        """
        if logger_name is not None:
            __local_instance = PseudoSingletonLogger.__instance[logger_name]
        else:
            __local_instance = PseudoSingletonLogger.__last_instance

        __local_instance.format_keys = ['%(asctime)s,']
        if app_name is not None:
            __local_instance.format_keys.append(f'{app_name},')
        if __local_instance.meta:
            __local_instance.format_keys.append('[%(levelname)s:')
            __local_instance.format_keys.append('pid=%(process)d:')
            __local_instance.format_keys.append('%(threadName)s:')
        if use_instance:
            __local_instance.format_keys.append('%(instanceName)s:')
        if __local_instance.meta:
            __local_instance.format_keys.append('%(module)s:')
            __local_instance.format_keys.append('%(funcName)s:')
            __local_instance.format_keys.append('%(lineno)d],')
        __local_instance.format_keys.append('%(message)s')

        __local_instance.formatter = logging.Formatter(''.join(__local_instance.format_keys))
        for handler in __local_instance.handlers:
            handler.setFormatter(__local_instance.formatter)

    @classmethod
    def get_output_path(cls,
                        logger_name: str = None,
                        handler_type: logging.Handler = None) -> Iterable[str]:
        """=
        Get the output path of specific handler type or all registered handlers.

        Args:
            handler_type (logging.Handler): The handler type of interest.
                                            If None all handlers' output path
                                            will be returned in a list.
        NOTE: Not fully tested
        """
        if logger_name is None or logger_name not in PseudoSingletonLogger.__instance:
            _local_logger = PseudoSingletonLogger.__last_instance
        else:
            _local_logger = PseudoSingletonLogger.__instance[logger_name]

        paths = []
        for handler in _local_logger.handlers:
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
    def remove_handler(cls,
                       handler_type: logging.Handler,
                       logger_name: str = None):
        """
        Remove a specific handler type from the logger instance.

        Args:
            handler_type (logging.Handler): The handler type to be removed.
                                            If the top level handler (logging.Handler)
                                            is given, all handlers will be removed.
        """
        if logger_name is None:
            logger_name = PseudoSingletonLogger.__last_instance.logger_name

        for handler in PseudoSingletonLogger.__instance[logger_name].handlers:
            if isinstance(handler, handler_type):
                PseudoSingletonLogger.__instance[logger_name].handlers.remove(handler)

    @classmethod
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

        meta (bool, optional): Flag indicated whether to adding location data
        to the header.
        Default to True.

        date_filename (bool, optional): Whether to add a date to the
        filename when saving logs to a file.
        Defaults to True.

        handlers (list, optional): List of handlers to add to the logger.
        Defaults to [StreamHnadler].

    Returns:
        logging.Logger: A configured Logger instance.
    """

    def __init__(self,
                 name: str = 'root',
                 app_name: str = None,
                 instance_name: str = None,
                 level: int = logging.DEBUG,
                 meta: bool = True,
                 date_filename: bool = True,
                 handlers=None):

        super().__init__(name, level=level)
        if instance_name is None:
            text = traceback.extract_stack()[-2][3]
            self.instance_name = text[:text.find('=')].strip()
        else:
            self.instance_name = instance_name

        self.logger = PseudoSingletonLogger(name=name,
                                            app_name=app_name,
                                            use_instance=True,
                                            level=level,
                                            meta=meta,
                                            date_filename=date_filename,
                                            handlers=handlers)

        self.get_output_path = self.logger.get_output_path
        self.remove_handler = self.logger.remove_handler
        self.version = self.logger.version
        self.set_default_format = self.logger.set_default_format

    def change_instance_name(self, instance_name: str):
        """
        change_instance_name Change the isntance name

        The instance name is set by default in the initialization.
        This method provides the ability to change the name after initialization.

        Args:
            instance_name (str): The new name to use for the instanceName label.
        """
        self.instance_name = instance_name

    # pylint: disable=protected-access
    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, stacklevel: int = 1):
        """Log a message."""
        if extra is not None:
            extra["instanceName"] = self.instance_name
        else:
            extra = {"instanceName": self.instance_name}
        self.logger._log(level=level,
                         msg=msg,
                         args=args,
                         exc_info=exc_info,
                         extra=extra,
                         stack_info=stack_info,
                         stacklevel=stacklevel + 1)


if __name__ == "__main__":
    log_path = Path(".logs", "test.log")
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(),
                logging.FileHandler(log_path)]
    log1 = LoggerWrapper(app_name="LoggerWrapper Demo",
                         handlers=handlers,
                         meta=True,
                         date_filename=False)

    log2 = LoggerWrapper()
    print(log2.version)

    print(str(log1.get_output_path()))

    for count in range(10):
        if count == 5:
            log1.remove_handler(logging.StreamHandler)
        log1.info("test of " + str(count))
        log2.info("test of " + str(count))

    print(str(log2.get_output_path()))
    print(log1.version)
