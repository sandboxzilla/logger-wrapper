#!/bin/python3

"""
log_helper package

Author: Erol Yesin
Version: 0.0.1

This package provides a wrapper for the built-in logging packages:

1.  LoggingHelper: A class for creating and managing events with callback
    routines.
    This class can be used independently of TimerEvent for handling
    general event-driven scenarios without any time-based requirements.

For detailed documentation and example usage on each class, refer to their
respective module files.

Copyright (c) 2023.  Erol Yesin/SandboxZilla

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

from .logger_wrapper import LoggerWrapper
