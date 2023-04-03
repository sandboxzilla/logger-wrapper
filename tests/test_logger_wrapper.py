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
import time
import tempfile
import unittest
from pathlib import Path
from contextlib import contextmanager
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) + '/src'
os.sys.path.insert(0, parentdir)
parentdir = parentdir + '/log_wrapper'
os.sys.path.insert(0, parentdir)

from logger_wrapper import LoggerWrapper


class TestLoggingHelper(unittest.TestCase):
    def setUp(self):
        # create a temporary directory to store logs
        self.logs_dir = tempfile.mkdtemp()
        self.file_path = str(os.path.join(self.logs_dir, "test_log_wrapper.log"))
        self.logger = LoggerWrapper(name="test_log_wrapper",
                                    date_filename=False,
                                    handlers=[logging.StreamHandler(), logging.FileHandler(self.file_path)])

    def tearDown(self):
        self.logger.remove_handler(logging.Handler)

        # remove the temporary logs directory
        shutil.rmtree(self.logs_dir)

    def test_file_logging(self):
        # given

        # when
        self.logger.debug("debug message")
        self.logger.info("info message")
        self.logger.warning("warning message")
        self.logger.error("error message")
        self.logger.critical("critical message")
        time.sleep(1)

        # then
        with open(self.file_path, "r") as f:
            contents = f.read()
            self.assertIn("debug message", contents)
            self.assertIn("info message", contents)
            self.assertIn("warning message", contents)
            self.assertIn("error message", contents)
            self.assertIn("critical message", contents)

    def test_get_output_path(self):
        # given
        expected_paths = ['<stderr>', self.file_path]

        # when
        paths = self.logger.get_output_path()

        # then
        self.assertListEqual(paths, expected_paths)

    def test_remove_handler(self):
        # given
        old_num_handlers = len(self.logger.handlers)

        # when
        self.logger.remove_handler(logging.StreamHandler)
        new_num_handlers = len(self.logger.handlers)

        # then
        self.assertEqual(new_num_handlers, old_num_handlers - 1)

    def test_version_property(self):
        # given
        expected_version = "0.0.1"

        # when
        version = LoggerWrapper.version

        # then
        self.assertEqual(version, expected_version)


if __name__ == "__main__":
    unittest.main()
