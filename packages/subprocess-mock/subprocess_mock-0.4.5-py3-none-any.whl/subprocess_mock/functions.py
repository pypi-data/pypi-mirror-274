# -*- coding: utf-8 -*-

"""

subprocess_mock.functions

Functions mocking subprocess standard library functions behavior

Original subprocess module:
    Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se>

Mock modifications (c) 2024 by Rainer Schwarzbach

This file is part of subprocess-mock.

subprocess-mock is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

subprocess-mock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

from typing import Tuple

from subprocess_mock import workflow


__all__ = [
    "call",
    "check_call",
    "getstatusoutput",
    "getoutput",
    "check_output",
    "run",
]


def call(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    timeout, then return the returncode attribute.

    See the call() method of the StoringRunner class below for details.
    """
    return workflow.Orchestrator().call(*popenargs, timeout=timeout, **kwargs)


def check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    See the check_call() method of the StoringRunner class below for details.
    """
    return workflow.Orchestrator().check_call(*popenargs, **kwargs)


def check_output(*popenargs, timeout=None, **kwargs):
    r"""Run command with arguments and return its output.

    See the check_output() method of the StoringRunner class below
    for details.
    """
    return workflow.Orchestrator().check_output(*popenargs, timeout=timeout, **kwargs)


# pylint: disable=redefined-builtin
def run(
    *popenargs,
    input=None,
    timeout=None,
    check=False,
    **kwargs,
):
    """Run command with arguments and return a CompletedProcess instance.

    See the run() method of the StoringRunner class below for details.
    """
    return workflow.Orchestrator().run(
        *popenargs, input=input, timeout=timeout, check=check, **kwargs
    )


# pylint: disable=redefined-builtin

# Various tools for executing commands and looking at their output and status.
#


def getstatusoutput(cmd) -> Tuple[int, str]:
    """Return (exitcode, output) of executing cmd in a shell.

    See the getstatusoutput() method of the StoringRunner class below
    for details.
    """
    return workflow.Orchestrator().getstatusoutput(cmd)


def getoutput(cmd) -> str:
    """Return output (stdout or stderr) of executing cmd in a shell.

    See the getoutput() method of the StoringRunner class below for details.
    """
    return workflow.Orchestrator().getoutput(cmd)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
