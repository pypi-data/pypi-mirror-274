# -*- coding: utf-8 -*-

"""

subprocess_mock.child

subprocess child related classes

Copyright (C) 2024 Rainer Schwarzbach

This file is part of subprocess-mock.

subprocess-mock is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

subprocess-mock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import io
import logging
import sys
import time

from typing import Any, Callable, Iterator, Optional, Tuple, Type, Union

from subprocess_mock import commons
from subprocess_mock import streams


def get_stream_and_encoding(
    selector: Any,
    standard_stream: Any,
    name: str,
    mode: str = "wb",
) -> Tuple[Any, Optional[str]]:
    """Get a stream and the appropriate encoding"""
    logging.debug("[child] connecting stream %r …", name)
    if isinstance(selector, streams.Connection):
        if selector.readable:
            wrapper: Type[streams.ConnectionWrapper] = streams.ConnectionReader
            logging.debug("[child] … using read wrapper %r", wrapper)
        elif selector.writable:
            wrapper = streams.ConnectionWriter
            logging.debug("[child] … using write wrapper %r", wrapper)
        else:
            raise ValueError(f"object ({selector!r}) must be read- or writable")
        #
        return wrapper(selector), None
    #
    if isinstance(selector, io.BufferedIOBase):
        logging.debug("[child] … using bytes stream %r", selector)
        return selector, None
    #
    if isinstance(selector, io.TextIOBase):
        logging.debug(
            "[child] … using text stream %r with encoding %r",
            selector,
            selector.encoding,
        )
        return selector, selector.encoding
    #
    if isinstance(selector, int) and selector > 0:
        # pylint: disable=consider-using-with, unspecified-encoding
        stream = io.open(selector, mode=mode)
        logging.debug("[child] … using file descriptor %s as %r", selector, stream)
        return stream, None
    #
    if selector != commons.NO_PIPE:
        raise TypeError(f"Unsupported object ({selector!r} of type {type(selector)})")
    #
    try:
        stream = standard_stream.buffer
    except AttributeError:
        # assume a text stream
        logging.debug(
            "[child] … using standard stream (text) %r with encoding %r",
            standard_stream,
            standard_stream.encoding,
        )
        return standard_stream, standard_stream.encoding
    #
    logging.debug("[child] … using standard stream (binary) %r", stream)
    return stream, None


def write_to_stream(
    stream: Any,
    message: Union[bytes, str],
    encoding: Optional[str] = None,
) -> None:
    """Prepare the message for writing to a stream
    with the specified encoding.
    If emcoding is None, convert the message to bytes if required.
    """
    if isinstance(stream, (io.BufferedIOBase, streams.ConnectionWrapper)):
        if isinstance(message, bytes):
            stream.write(message)
        else:
            stream.write(message.encode())
        #
        stream.flush()
    elif isinstance(stream, io.TextIOBase):
        if isinstance(message, str):
            stream.write(message)
        else:
            if encoding is None:
                unicode_message = message.decode()
            else:
                unicode_message = message.decode(encoding)
            #
            stream.write(unicode_message)
        #
        stream.flush()
    else:
        try:
            stream.write(message.encode())  # type: ignore
        except AttributeError:
            stream.write(message)
        finally:
            stream.flush()
        #
    #


class Step:
    """Program primitives base class"""

    requires_stdin: bool = False

    def __init__(self) -> None:
        """Store the argument(s) if required"""

    def run_in(self, process: "Process") -> None:
        """Run in the specified process"""
        raise NotImplementedError

    def show_args(self) -> str:
        """String representation of the arguments"""
        return ""

    def __repr__(self) -> str:
        """String representation of the instance"""
        return f"{self.__class__.__name__}({self.show_args()})"

    def __hash__(self) -> int:
        """Return a hash value"""
        return hash(repr(self))

    def __eq__(self, other) -> bool:
        """Return a hash value"""
        return self.__class__ == other.__class__ and repr(self) == repr(other)


class Filter(Step):
    """Program primitive: read from standard input,
    filter it through the provided function
    and write the result to stdout.
    The function must accept str as input,
    or bytes if binary is set True.
    Its output may be either bytes or str.
    """

    requires_stdin = True

    def __init__(self, function: Callable, binary: bool = False) -> None:
        """Store the argument(s) if required"""
        self.__function = function
        self.__binary = binary

    def show_args(self) -> str:
        """String representation of the arguments"""
        return repr(self.__function)

    def run_in(self, process: "Process") -> None:
        """Run in the specified process"""
        input_data = process.read_from_stdin()
        logging.debug("[child] read from stdin: %r", input_data)
        if isinstance(input_data, bytes):
            raw_data = bytes(input_data)
            text_data = raw_data.decode()
        elif isinstance(input_data, str):
            text_data = str(input_data)
            raw_data = text_data.encode()
        else:
            raise TypeError(f"Invalid input data: {input_data!r}")
        #
        if self.__binary:
            output_data = self.__function(raw_data)
        else:
            output_data = self.__function(text_data)
        #
        process.write_stdout(output_data)


class SetReturncode(Step):
    """Program primitive: set returncode to the provided value"""

    def __init__(self, returncode: int) -> None:
        """Store the argument(s) if required"""
        self.__returncode = returncode

    def show_args(self) -> str:
        """String representation of the arguments"""
        return f"{self.__returncode}"

    def run_in(self, process: "Process") -> None:
        """Run in the specified process"""
        process.set_returncode(self.__returncode)


class Sleep(Step):
    """Program primitive: sleep the given amount of seconds"""

    def __init__(self, seconds: Union[float, int]) -> None:
        """Store the argument(s) if required"""
        self.__seconds = float(seconds)

    def show_args(self) -> str:
        """String representation of the arguments"""
        return f"{self.__seconds}"

    def run_in(self, process: "Process") -> None:
        """Run in the specified process"""
        time.sleep(self.__seconds)


class WriteOutput(Step):
    """Program primitive:
    write the provided message to standard output.
    Conversion between str and bytes takes place automatically
    if required.
    """

    def __init__(self, message: Union[bytes, str]) -> None:
        """Store the argument(s) if required"""
        self.message = message

    def show_args(self) -> str:
        """String representation of the arguments"""
        return f"{self.message!r}"

    def run_in(self, process: "Process") -> None:
        """Run in the specified program"""
        process.write_stdout(self.message)


class WriteError(WriteOutput):
    """Program primitive:
    write the provided message to standard error.
    Conversion between str and bytes takes place automatically
    if required.
    """

    def run_in(self, process: "Process") -> None:
        """Run in the specified process"""
        process.write_stderr(self.message)


class Program:
    """Program as a sequence of steps"""

    def __init__(self, *steps: Step) -> None:
        """Store the steps"""
        self.steps: Tuple[Step, ...] = steps

    def __iter__(self) -> Iterator[Step]:
        """Iterator over the steps"""
        return iter(self.steps)

    def __repr__(self) -> str:
        """Return a string representation"""
        return f"{self.__class__.__name__}{repr(self.steps)}"

    def __hash__(self) -> int:
        """Return a hash value"""
        return hash(repr(self))

    def __eq__(self, other) -> bool:
        """Return a hash value"""
        return self.steps == other.steps


# pylint: disable=too-many-instance-attributes


class Process:
    """Mocked (child) process used in subprocess_mock.parent.Popen instances"""

    def __init__(
        self,
        *steps: Step,
        stdin: Any = commons.NO_PIPE,
        stderr: Any = commons.NO_PIPE,
        stdout: Any = commons.NO_PIPE,
    ):
        """Initialize and start running"""
        self.__program: Program = Program(*steps)
        logging.debug("[child] initialized with program: %r", self.__program)
        self.__redirected = {
            commons.KW_STDIN: stdin != commons.NO_PIPE,
            commons.KW_STDERR: stderr != commons.NO_PIPE,
            commons.KW_STDOUT: stdout != commons.NO_PIPE,
        }
        self.__stdin = get_stream_and_encoding(stdin, sys.stdin, "stdin", mode="rb")[0]
        self.__stderr, self.__stderr_encoding = get_stream_and_encoding(
            stderr, sys.stderr, "stderr"
        )
        self.__stdout, self.__stdout_encoding = get_stream_and_encoding(
            stdout, sys.stdout, "stdout"
        )
        self.__returncode = commons.RETURNCODE_OK
        self.__read_stdin: Union[bytes, str] = b""

    def read_from_stdin(self) -> Union[bytes, str]:
        """Read from standard input, proxy method for steps"""
        data = self.__read_stdin
        self.__read_stdin = b""
        return data

    def set_returncode(self, returncode: int):
        """Set returncode, proxy method for steps"""
        logging.debug("[child] setting returncode: %r", returncode)
        self.__returncode = returncode

    def write_stderr(self, message: Union[bytes, str]):
        """Write message to stderr, proxy method for steps"""
        logging.debug("[child] writing to stderr: %r", message)
        write_to_stream(self.__stderr, message, encoding=self.__stderr_encoding)

    def write_stdout(self, message: Union[bytes, str]):
        """Write message to stdout, proxy method for steps"""
        logging.debug("[child] writing to stdout: %r", message)
        write_to_stream(self.__stdout, message, encoding=self.__stdout_encoding)

    def run(self) -> int:
        """Read once and blocking from stdin if any step requires it.
        Otherwise, try a non-blocking read.
        Run the steps one after another.
        Return the returncode.
        """
        if any(step.requires_stdin for step in self.__program):
            self.__read_stdin = self.__stdin.read(blocking=True)
        else:
            self.__read_stdin = self.__stdin.read()
        #
        logging.debug("[child] read from stdin: %r", self.__read_stdin)
        for step in self.__program:
            step.run_in(self)
        #
        try:
            self.__stdout.flush()
        except BrokenPipeError as exc:
            logging.error("while flushing stdout: %s", exc)
        #
        try:
            self.__stderr.flush()
        except BrokenPipeError as exc:
            logging.error("while flushing stderr: %s", exc)
        #
        try:
            if self.__redirected[commons.KW_STDOUT]:
                self.__stdout.close()
            #
        except BrokenPipeError as exc:
            logging.error("while closing stdout: %s", exc)
        #
        try:
            if self.__redirected[commons.KW_STDERR]:
                self.__stderr.close()
            #
        except BrokenPipeError as exc:
            logging.error("while closing stderr: %s", exc)
        #
        logging.debug("[child] Returncode is %s", self.__returncode)
        return self.__returncode


def run_process(
    *steps: Step,
    stdin: Any = commons.NO_PIPE,
    stderr: Any = commons.NO_PIPE,
    stdout: Any = commons.NO_PIPE,
    error_channel: streams.Connection,
) -> int:
    """Initialize and start a process. Return its returncode."""
    # pylint: disable=broad-exception-caught
    try:
        process = Process(
            *steps,
            stdin=stdin,
            stderr=stderr,
            stdout=stdout,
        )
    except Exception as exc:
        error_channel.send_bytes(
            ":".join(
                (
                    exc.__class__.__name__,
                    str(exc),
                )
            ).encode()
        )
        return commons.RETURNCODE_ERROR
    else:
        error_channel.send_bytes(b"")
    finally:
        error_channel.close()
    #
    logging.debug("[child] starting …")
    sys.exit(process.run())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
