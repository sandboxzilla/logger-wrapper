#!/bin/python3

"""
logger_wrapper package

Author: Erol Yesin/Sandboxzilla
Version: 0.1.0

This package provides a wrapper for the built-in logging packages:

1.  PseudoSingletonLogger: A class that wraps the logging.Logger to hrlp stadarize the log entries.

2.  LoggerWrapper: A class that wraps the logging.Logger.
    This class injects instance name into a standarized log messages.
    This class uses the PseudoSingletonLogger class.
    Using this class, you can set the instance name in the logger.
    This class uses the logging.Logger class.

For detailed documentation and example usage, refer to the README.md file.

Copyright (c) 2023. Erol Yesin/SandboxZilla

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
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from .logger_wrapper import LoggerWrapper, PseudoSingletonLogger
