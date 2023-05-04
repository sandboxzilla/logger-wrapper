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

import logging
import os
import unittest
from pathlib import Path
import tempfile


src_dir = Path(str(Path.cwd().parent),
               'logger-wrapper',
               'src',
               'logger_wrapper')
os.sys.path.insert(0, str(src_dir))

from logger_wrapper import PseudoSingletonLogger, LoggerWrapper, __version__


class PseudoSingletonLoggerTests(unittest.TestCase):
    """
    A class for unit testing the PseudoSingletonLogger class.
    """

    def test_singleton_logger(self):
        """
        Tests that the PseudoSingletonLogger class correctly handles multiple instances.
        """
        logger1a = PseudoSingletonLogger(name="test_singleton_logger")
        logger1b = PseudoSingletonLogger(name="test_singleton_logger")

        # Test that the two instances are the same
        self.assertIs(logger1a, logger1b)

        # Test that the instance name is set correctly
        self.assertEqual(logger1a.logger_name, "test_singleton_logger")
        self.assertEqual(logger1b.logger_name, "test_singleton_logger")

    def test_get_output_path(self):
        """
        Tests that the get_output_path method returns the correct output path.
        """
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = PseudoSingletonLogger(name="test_get_output_path",
                                       date_filename=False,
                                       handlers=handlers)

        # Test that the output path is correct
        output_path = logger.get_output_path()
        temp_file.close()
        path_str = ",".join(output_path)
        self.assertIn(temp_file.name, path_str)
        self.assertIn("<stderr>", path_str)

    def test_remove_stream_handler(self):
        """
        Tests that the remove_handler method correctly removes the file handler.
        """
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = PseudoSingletonLogger(name="test_remove_handler",
                                       date_filename=False,
                                       handlers=handlers)

        self.assertEqual(len(logger.handlers), 2)
        logger.remove_handler(logging.StreamHandler)
        self.assertEqual(len(logger.handlers), 1)
        self.assertNotIn(logging.StreamHandler, logger.handlers)
        self.assertIn(temp_file.name, logger.handlers[0].baseFilename)

    def test_version(self):
        """
        Tests that the version method returns the correct version number.
        """
        logger = PseudoSingletonLogger(name="test_version")

        # Test that the version number is correct
        self.assertEqual(logger.version, __version__)

    def test_set_default_format(self):
        """
        Tests that the set_default_format method correctly sets the logging format.
        """
        logger = PseudoSingletonLogger(name="test_set_default_format",
                                       app_name="test_set_default_format",
                                       use_instance=True)

        # Test that the logging format is correctly set
        logger.set_default_format(logger_name="test_set_default_format",
                                  app_name="test_set_default_format",
                                  use_instance=True)
        self.assertIn("%(asctime)s,", logger.format_keys)
        self.assertIn("test_set_default_format,", logger.format_keys)
        self.assertIn("[%(levelname)s:", logger.format_keys)
        self.assertIn("pid=%(process)d:", logger.format_keys)
        self.assertIn("%(threadName)s:", logger.format_keys)
        self.assertIn("%(instanceName)s:", logger.format_keys)
        self.assertIn("%(funcName)s:", logger.format_keys)
        self.assertIn("%(lineno)d],", logger.format_keys)
        self.assertIn("%(message)s", logger.format_keys)


class LoggerWrapperTest(unittest.TestCase):
    """
    A class for unit testing the LoggerWrapper class.
    """

    def setUp(self):
        """Create a new instance of LoggerWrapper for each test."""
        pass
        # self.handlers = [logging.StreamHandler(), logging.FileHandler("test.log")]
        # self.logger = LoggerWrapper(app_name="testLoggerWrapper",
        #                             instance_name="lwUnitTest",
        #                             handlers=self.handlers,
        #                             meta=True,
        #                             date_filename=False)

    def test_console_logging(self):
        """
        Tests that the LoggerWrapper class correctly logs messages to the console.
        """
        logger = LoggerWrapper(name="test_console_logging",
                               instance_name="test_console_logging",)

        logger.info("test message")
        self.assertEqual(len(logger.logger.handlers), 1)
        self.assertIsInstance(logger.logger.handlers[0], logging.StreamHandler)

    def test_file_logging(self):
        """
        Tests that the LoggerWrapper class correctly logs messages to a file.
        """
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name="test_file_logging",
                               instance_name="test_file_logging",
                               date_filename=False,
                               handlers=handlers)

        logger.info("test message added to file")
        with open(temp_file.name, "r") as f:
            contents = f.read()
        self.assertIn("test message added to file", contents)

    def test_instance_name(self):
        """
        Tests that the LoggerWrapper class correctly sets the instance name.
        """
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]

        logger = LoggerWrapper(name="test_instance_name",
                               instance_name="test_instance_name",
                               date_filename=False,
                               handlers=handlers)

        logger.info("test message 1 added to file")
        with open(temp_file.name, "r") as f:
            contents = f.read()
        self.assertNotIn("new_instance_name", contents)

        logger.change_instance_name("new_instance_name")

        logger.info("test message 2 added to file")
        with open(temp_file.name, "r") as f:
            contents = f.read()

        self.assertIn("new_instance_name", contents)

    def test_log_message(self):
        """Ensure that the LoggerWrapper logs messages correctly"""
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name="test_log_message",
                               instance_name="test_log_message",
                               date_filename=False,
                               handlers=handlers)

        logger.log(level=10, msg="Test message")
        # You can then check the log file to make sure that the message was logged correctly
        # For example:
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn("DEBUG", content)
        self.assertIn("Test message", content)
        self.assertIn("test_log_message", content)
        self.assertIn("MainThread", content)
        self.assertIn("test_logger_wrapper", content)

    def test_log_debug_message(self):
        """Ensure that the log_debug_message method logs debug messages correctly"""
        level = "DEBUG"
        message = "Debug message"
        instance_name = "test_log_debug_message"
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name=instance_name,
                               instance_name=instance_name,
                               date_filename=False,
                               handlers=handlers)

        logger.debug(message)
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn(level, content)
        self.assertIn(message, content)
        self.assertIn(instance_name, content)
        self.assertIn("test_logger_wrapper", content)

    def test_log_info_message(self):
        """Ensure that the log_info_message method logs info messages correctly"""
        level = "INFO"
        message = "Info message"
        instance_name = "test_log_info_message"
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name=instance_name,
                               instance_name=instance_name,
                               date_filename=False,
                               handlers=handlers)

        logger.info(message)
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn(level, content)
        self.assertIn(message, content)
        self.assertIn(instance_name, content)
        self.assertIn("test_logger_wrapper", content)

    def test_log_warning_message(self):
        """Ensure that the log_warning_message method logs warning messages correctly"""
        level = "WARNING"
        message = "Warning message"
        instance_name = "test_log_warning_message"
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name=instance_name,
                               instance_name=instance_name,
                               date_filename=False,
                               handlers=handlers)

        logger.warning(message)
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn(level, content)
        self.assertIn(message, content)
        self.assertIn(instance_name, content)
        self.assertIn("test_logger_wrapper", content)

    def test_log_error_message(self):
        """Ensure that the log_error_message method logs error messages correctly"""
        level = "ERROR"
        message = "Error message"
        instance_name = "test_log_error_message"
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name=instance_name,
                               instance_name=instance_name,
                               date_filename=False,
                               handlers=handlers)

        logger.error(message)
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn(level, content)
        self.assertIn(message, content)
        self.assertIn(instance_name, content)
        self.assertIn("test_logger_wrapper", content)

    def test_log_critical_message(self):
        """Ensure that the log_critical_message method logs critical messages correctly"""
        level = "CRITICAL"
        message = "Critical message"
        instance_name = "test_log_critical_message"
        temp_file = tempfile.NamedTemporaryFile()
        handlers = [logging.StreamHandler(), logging.FileHandler(temp_file.name)]
        logger = LoggerWrapper(name=instance_name,
                               instance_name=instance_name,
                               date_filename=False,
                               handlers=handlers)

        logger.critical(message)
        with open(temp_file.name) as f:
            content = f.read()
        self.assertIn(level, content)
        self.assertIn(message, content)
        self.assertIn(instance_name, content)
        self.assertIn("test_logger_wrapper", content)


if __name__ == '__main__':
    unittest.main()
