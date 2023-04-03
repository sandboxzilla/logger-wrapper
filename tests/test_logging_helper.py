#!/bin/python3

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

import inspect
import logging
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import contextmanager
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) + '/src'
os.sys.path.insert(0, parentdir)
parentdir = parentdir + '/logging_helper'
os.sys.path.insert(0, parentdir)

from logging_helper import LoggingHelper


class TestLoggingHelper(unittest.TestCase):
    def setUp(self):
        # create a temporary directory to store logs
        self.logs_dir = tempfile.mkdtemp()

    def tearDown(self):
        # remove the temporary logs directory
        shutil.rmtree(self.logs_dir)

    def test_file_logging(self):
        # given
        log_path = Path(self.logs_dir, "test_file_handler.log")
        logger = LoggingHelper(name="test_file_handler",
                               date_filename=False,
                               handlers=[logging.FileHandler(str(log_path))])

        # when
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.critical("critical message")

        # then
        with open(log_path, "r") as f:
            contents = f.read()
            self.assertIn("debug message", contents)
            self.assertIn("info message", contents)
            self.assertIn("warning message", contents)
            self.assertIn("error message", contents)
            self.assertIn("critical message", contents)

    def test_get_output_path(self):
        # given
        file_path = str(os.path.join(self.logs_dir, "test_get_output_path.log"))
        logger = LoggingHelper(name="test_get_output_path",
                               date_filename=False,
                               handlers=[logging.StreamHandler(), logging.FileHandler(file_path)])
        expected_paths = ['<stderr>', file_path]

        # when
        paths = logger.get_output_path()

        # then
        self.assertListEqual(paths, expected_paths)

    def test_remove_handler(self):
        # given
        logger = LoggingHelper(name="test_remove_handler")
        old_num_handlers = len(logger.handlers)

        # when
        logger.remove_handler(logging.StreamHandler)
        new_num_handlers = len(logger.handlers)

        # then
        self.assertEqual(new_num_handlers, old_num_handlers - 1)

    def test_version_property(self):
        # given
        expected_version = "0.0.1"

        # when
        version = LoggingHelper.version

        # then
        self.assertEqual(version, expected_version)
