# -*- coding: utf-8 -*-

"""

tests.test_functions

Unit test the functions module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of subprocess-mock.

subprocess-mock is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

subprocess-mock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import subprocess

from unittest import TestCase
from unittest.mock import patch

from subprocess_mock import commons
from subprocess_mock import functions


SUBPROCESS_RUN = "subprocess.run"
SYS_STDOUT = "sys.stdout"
SYS_STDERR = "sys.stderr"
ECHO_COMMAND = "echo"


class Run(TestCase):
    """Test the run() function"""

    maxDiff = None

    def test_filter(self) -> None:
        """Program filtering stdin"""
        # pylint: disable=unreachable
        with patch(SUBPROCESS_RUN, new=functions.run):
            input_data = "lower case"
            command = ["tr", "[:lower:]", "[:upper:]"]
            result = subprocess.run(  # type:ignore
                command,
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=False,
            )
            with self.subTest("call arguments"):
                self.assertEqual(result.args, command)
            #
            with self.subTest(commons.KW_RETURNCODE):
                self.assertEqual(result.returncode, commons.RETURNCODE_OK)
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
