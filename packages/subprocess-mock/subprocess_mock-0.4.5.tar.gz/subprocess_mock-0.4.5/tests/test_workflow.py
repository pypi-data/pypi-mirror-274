# -*- coding: utf-8 -*-

"""

tests.test_workflow

Unit test the workflow module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of subprocess-mock.

subprocess-mock is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

subprocess-mock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import logging
import subprocess

from unittest import TestCase
from unittest.mock import patch

from subprocess_mock import commons
from subprocess_mock import child
from subprocess_mock import workflow


SUBPROCESS_RUN = "subprocess.run"
SYS_STDOUT = "sys.stdout"
SYS_STDERR = "sys.stderr"
ECHO_COMMAND = "echo"


class Orchestrator(TestCase):
    """Test the Orchestrator class"""

    maxDiff = None

    # pylint: disable=protected-access

    def test_run_filter(self) -> None:
        """.run() method – Program filtering stdin"""
        # pylint: disable=unreachable
        orchestrator = workflow.Orchestrator()
        with patch(SUBPROCESS_RUN, new=orchestrator.run):
            input_data = b"Please Swap Case"
            expected_result = b"pLEASE sWAP cASE"
            command = ["tr", "whatever"]
            orchestrator.add_program(
                *command, program=child.Program(child.Filter(str.swapcase))
            )
            result = subprocess.run(
                command,
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            with self.subTest("call arguments"):
                self.assertEqual(result.args, command)
            #
            with self.subTest(commons.KW_RETURNCODE):
                self.assertEqual(result.returncode, commons.RETURNCODE_OK)
            #
            with self.subTest(commons.KW_STDOUT):
                self.assertEqual(result.stdout, expected_result)
            #
            with self.subTest(commons.KW_STDERR):
                self.assertEqual(result.stderr, b"")
            #
            with self.subTest("mock call result was registered"):
                last_result = orchestrator.get_last_result()
                self.assertIs(result, last_result[1])
            #
        #

    def test_run_vs_non_mocked(self) -> None:
        """.run() method – Mocked call compared to a non-mocked call"""
        real_output = "real output"
        mock_output = "mock output"
        mock_error_output = "mock error output"
        echo_command = [ECHO_COMMAND, "-n", real_output]
        run_kwargs = {
            commons.KW_STDOUT: subprocess.PIPE,
            commons.KW_STDERR: None,
        }
        orchestrator = workflow.Orchestrator()
        msg_prefix = "Non-mocked call:"
        result = subprocess.run(  # type: ignore
            echo_command, check=True, **run_kwargs
        )
        with self.subTest(f"{msg_prefix} {commons.KW_RETURNCODE}"):
            self.assertEqual(result.returncode, commons.RETURNCODE_OK)
        #
        expected_stdout = real_output.encode()
        with self.subTest(
            f"{msg_prefix} {commons.KW_STDOUT}",
            expected_stdout=expected_stdout,
        ):
            self.assertEqual(result.stdout, expected_stdout)
        #
        with self.subTest(f"{msg_prefix} call result was not registered"):
            self.assertEqual(orchestrator.all_results, [])
        #
        with patch(SUBPROCESS_RUN, new=orchestrator.run):
            orchestrator.add_program(
                *echo_command,
                program=child.Program(
                    child.WriteOutput(mock_output),
                    child.WriteError(mock_error_output),
                ),
            )
            result = subprocess.run(  # type: ignore
                echo_command, check=False, **run_kwargs
            )
            with self.subTest("call arguments"):
                self.assertEqual(result.args, echo_command)
            #
            with self.subTest(commons.KW_RETURNCODE):
                self.assertEqual(result.returncode, commons.RETURNCODE_OK)
            #
            expected_stdout = mock_output.encode()
            with self.subTest(commons.KW_STDOUT, expected_stdout=expected_stdout):
                self.assertEqual(result.stdout, expected_stdout)
            #
            with self.subTest(commons.KW_STDERR):
                self.assertIsNone(result.stderr)
            #
            with self.subTest("mock call result was registered"):
                last_result = orchestrator.get_last_result()
                self.assertIs(result, last_result[1])
            #
        #

    def test_set_returncode(self) -> None:
        """.run() method – Set returncode"""
        command = ["false"]
        orchestrator = workflow.Orchestrator()
        orchestrator.add_program(
            *command,
            program=child.Program(child.SetReturncode(commons.RETURNCODE_ERROR)),
        )
        with patch(SUBPROCESS_RUN, new=orchestrator.run):
            with self.subTest(
                "Exception is raised with nonzero returncode and check=True"
            ):
                self.assertRaises(
                    subprocess.CalledProcessError,
                    subprocess.run,
                    command,
                    check=True,
                )
            #
            logging.warning("Results store: %r", orchestrator.all_results)
            last_result = orchestrator.get_last_result()
            with self.subTest("Result was registered"):
                self.assertEqual(last_result[1].args, command)
            #
            with self.subTest("Returncode was recorded"):
                self.assertEqual(last_result[1].returncode, commons.RETURNCODE_ERROR)
            #
        #
        #

    def test_run_stdout_only(self) -> None:
        """.run() method – Output to stdout only"""
        orchestrator = workflow.Orchestrator()
        with patch(SUBPROCESS_RUN, new=orchestrator.run):
            output_data = "foo bar 1"
            error_data = "error data 1"
            command = [ECHO_COMMAND, output_data]
            orchestrator.add_program(
                *command,
                program=child.Program(
                    child.WriteOutput(output_data),
                    child.WriteError(error_data),
                ),
            )
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=None,
                check=False,
            )
            with self.subTest("call arguments"):
                self.assertEqual(result.args, command)
            #
            with self.subTest(commons.KW_RETURNCODE):
                self.assertEqual(result.returncode, commons.RETURNCODE_OK)
            #
            with self.subTest(commons.KW_STDOUT):
                self.assertEqual(result.stdout, output_data.encode())
            #
            with self.subTest(commons.KW_STDERR):
                self.assertIsNone(result.stderr)
            #
            with self.subTest("mock call result was registered"):
                last_result = orchestrator.get_last_result()
                self.assertIs(result, last_result[1])
            #
        #

    def test_run_stderr_only(self) -> None:
        """.run() method – Output to stderr only"""
        orchestrator = workflow.Orchestrator()
        with patch(SUBPROCESS_RUN, new=orchestrator.run):
            output_data = "foo bar 2"
            error_data = "error data 2"
            command = [ECHO_COMMAND, output_data]
            orchestrator.add_program(
                *command,
                program=child.Program(
                    child.WriteOutput(output_data),
                    child.WriteError(error_data),
                ),
            )
            result = subprocess.run(
                command,
                stdout=None,
                stderr=subprocess.PIPE,
                check=False,
            )
            with self.subTest("call arguments"):
                self.assertEqual(result.args, command)
            #
            with self.subTest(commons.KW_RETURNCODE):
                self.assertEqual(result.returncode, commons.RETURNCODE_OK)
            #
            with self.subTest(commons.KW_STDOUT):
                self.assertIsNone(result.stdout)
            #
            with self.subTest(commons.KW_STDERR):
                self.assertEqual(result.stderr, error_data.encode())
            #
            with self.subTest("mock call result was registered"):
                last_result = orchestrator.get_last_result()
                self.assertIs(result, last_result[1])
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
