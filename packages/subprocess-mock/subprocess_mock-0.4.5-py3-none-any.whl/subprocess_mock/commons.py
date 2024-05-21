# -*- coding: utf-8 -*-

"""

subprocess_mock.commons

subprocess-mock common definitions

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


# Magic numbers
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL
NO_PIPE = -1  # to be used instead of literal -1

KW_ARGS = "args"
KW_CHECK = "check"
KW_INPUT = "input"
KW_RETURNCODE = "returncode"
KW_STDIN = "stdin"
KW_STDERR = "stderr"
KW_STDOUT = "stdout"

RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
