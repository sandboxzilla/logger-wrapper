#
#  Copyright (c) 2023  Erol Yesin/SandboxZilla
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify,
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import inspect
import time
import logging
from logging import handlers as hdls
from pathlib import PosixPath
import unittest

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) + '/src'
os.sys.path.insert(0, parentdir)
from logging_helper import LoggingHelper


class TestLoggingHelper(unittest.TestCase):
    def setUp(self):
        self.name = 'test_logger'
        self.level = logging.DEBUG
        self.date_filename = True
        self.meta = True
        self.handlers = [logging.StreamHandler(), hdls.SysLogHandler(address='/dev/log')]
        self.logger = LoggingHelper(name=self.name,
                                    level=self.level,
                                    meta=self.meta,
                                    date_filename=self.date_filename,
                                    handlers=self.handlers)

    def test_init(self):
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(str(self.logger.name), self.name)
        self.assertEqual(self.logger.level, self.level)
        if self.date_filename:
            self.assertIn('2023', self.logger.handlers[1].baseFilename)
        if self.console_output:
            self.assertIsInstance(
                self.logger.handlers[0], logging.StreamHandler)

    def test_add_file_handler(self):
        name = 'test_handler'
        handler = LoggingHelper.add_file_handler(log=self.logger, name=name)
        self.assertIsInstance(handler, logging.Handler)
        self.assertEqual(handler.name, name)
