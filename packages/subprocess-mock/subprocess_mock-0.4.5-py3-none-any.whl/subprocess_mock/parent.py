# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

"""

subprocess_mock.parent

Mocked Subprocesses with accessible I/O streams,
modified from the Python 3.6 subprocess module

Original subprocess module:
    Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se>

Mock modifications (c) 2024 by Rainer Schwarzbach

This module allows you connect MockProcess instances, connect to their
input/output/error pipes, and obtain their return codes.

Contents
========
Popen(...) – a class

This file is part of subprocess-mock.

subprocess-mock is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

subprocess-mock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import sys

import io
import logging
import multiprocessing
import os
import time
import signal
import builtins
import warnings
import errno
import threading

from subprocess import SubprocessError, TimeoutExpired
from time import monotonic as _time
from typing import Callable, Dict, IO, List, Optional, Tuple, Union

from subprocess_mock import child
from subprocess_mock import commons
from subprocess_mock import streams

if sys.platform == "win32":
    _MSWINDOWS = True
    _WNOHANG = 0

    # pylint: disable=too-few-public-methods
    class STARTUPINFO:
        """Windows: Startupinfo"""

        dwFlags = 0
        hStdInput = None
        hStdOutput = None
        hStdError = None
        wShowWindow = 0

    # pylint: enable=too-few-public-methods
else:
    _MSWINDOWS = False
    _WNOHANG = os.WNOHANG


__all__ = ["Popen"]


# This list holds Popen instances for which the underlying process had not
# exited at the time its __del__ method got called:
# those processes are wait()ed for synchronously from _cleanup()
# when a new Popen object is created, to avoid zombie processes.
_ACTIVE: List["Popen"] = []


def _cleanup():
    for inst in _ACTIVE[:]:
        # pylint: disable=protected-access
        res = inst._internal_poll_mock(_deadstate=sys.maxsize)
        # pylint: enable=protected-access
        if res is not None:
            try:
                _ACTIVE.remove(inst)
            except ValueError:
                # This can happen if two threads create a new Popen instance.
                # It's harmless that it was already removed, so ignore.
                pass
            #
        #
    #


_PLATFORM_DEFAULT_CLOSE_FDS = object()


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=attribute-defined-outside-init
# pylint: disable=unused-argument


class Popen:
    """Execute a child program in a new process.

    For a complete description of the arguments see the Python documentation.

    Arguments:
      args: A string, or a sequence of program arguments.

      bufsize: supplied as the buffering argument to the open() function when
          creating the stdin/stdout/stderr pipe file objects

      executable: A replacement program to execute.

      stdin, stdout and stderr: These specify the executed programs' standard
          input, standard output and standard error file handles, respectively.

      preexec_fn: (POSIX only) An object to be called in the child process
          just before the child is executed.

      close_fds: Controls closing or inheriting of file descriptors.

      shell: If true, the command will be executed through the shell.

      cwd: Sets the current directory before the child is executed.

      env: Defines the environment variables for the new process.

      universal_newlines: If true, use universal line endings for file
          objects stdin, stdout and stderr.

      startupinfo and creationflags (Windows only)

      restore_signals (POSIX only)

      start_new_session (POSIX only)

      pass_fds (POSIX only)

      encoding and errors: Text mode encoding and error handling to use for
          file objects stdin, stdout and stderr.

    Attributes:
        stdin, stdout, stderr, pid, returncode
    """

    _child_created = False  # Set here since __del__ checks it

    def __init__(
        self,
        args,
        bufsize=-1,
        executable=None,
        stdin=None,
        stdout=None,
        stderr=None,
        preexec_fn=None,
        close_fds=_PLATFORM_DEFAULT_CLOSE_FDS,
        shell=False,
        cwd=None,
        env=None,
        universal_newlines=False,
        startupinfo=None,
        creationflags=0,
        restore_signals=True,
        start_new_session=False,
        pass_fds=(),
        *,
        child_steps: Tuple[child.Step, ...] = (),
        orchestrator_callback: Optional[Callable] = None,
        capture_output: bool = False,
        encoding=None,
        errors=None,
    ) -> None:
        """Create new Popen instance."""
        _cleanup()
        # Held while anything is calling waitpid before returncode has been
        # updated to prevent clobbering returncode if wait() or poll() are
        # called from multiple threads at once.  After acquiring the lock,
        # code must re-check self.returncode to see if another thread just
        # finished a waitpid() call.
        self._waitpid_lock = threading.Lock()
        self._input = None
        self._communication_started = False
        if bufsize is None:
            bufsize = -1  # Restore default
        #
        if not isinstance(bufsize, int):
            raise TypeError("bufsize must be an integer")
        #
        if _MSWINDOWS:
            if preexec_fn is not None:
                raise ValueError("preexec_fn is not supported on Windows platforms")
            #
            any_stdio_set = (
                stdin is not None or stdout is not None or stderr is not None
            )
            if close_fds is _PLATFORM_DEFAULT_CLOSE_FDS:
                if any_stdio_set:
                    close_fds = False
                else:
                    close_fds = True
                #
            elif close_fds and any_stdio_set:
                raise ValueError(
                    "close_fds is not supported on Windows platforms"
                    " if you redirect stdin/stdout/stderr"
                )
            #
        else:
            # POSIX
            if close_fds is _PLATFORM_DEFAULT_CLOSE_FDS:
                close_fds = True
            #
            if pass_fds and not close_fds:
                warnings.warn("pass_fds overriding close_fds.", RuntimeWarning)
                close_fds = True
            #
            if startupinfo is not None:
                raise ValueError("startupinfo is only supported on Windows platforms")
            #
            if creationflags != 0:
                raise ValueError("creationflags is only supported on Windows platforms")
            #
        #
        self.args = args
        self.stdin: Union[IO, streams.ConnectionWrapper, None] = None
        self.stdout: Union[IO, streams.ConnectionWrapper, None] = None
        self.stderr: Union[IO, streams.ConnectionWrapper, None] = None
        self.pid: Optional[int] = None
        self.returncode: Optional[int] = None
        self.universal_newlines = universal_newlines
        self.encoding = encoding
        self.errors = errors
        self._orchestrator_callback = orchestrator_callback
        self._capture_output = capture_output
        self._text_mode = encoding or errors or universal_newlines
        encoding__ = self.encoding or sys.getdefaultencoding()
        errors__ = self.errors or "strict"
        # Input and output objects. The general principle is like
        # this:
        #
        # Parent                   Child
        # ------                   -----
        # p2cwrite   ---stdin--->  p2cread
        # c2pread    <--stdout---  c2pwrite
        # errread    <--stderr---  errwrite
        #
        # The parent and child objects are file descriptors on all platforms.
        # The parent objects are commons.NO_PIPE (-1) when not using PIPEs.
        # The child objects are -1 when not redirecting.
        (
            p2cread,
            p2cwrite,
            c2pread,
            c2pwrite,
            errread,
            errwrite,
        ) = self._get_handles(stdin, stdout, stderr)
        self._closed_child_pipe_fds = False
        try:
            # from the docs:
            # bufsize will be supplied as the corresponding argument
            # to the open() function when creating the stdin/stdout/stderr
            # pipe file objects:
            #   - 0 means unbuffered (read and write are one system call
            #     and can return short)
            #   - 1 means line buffered (only usable if text=True
            #     or universal_newlines=True)
            #   - any other positive value means use a buffer
            #     of approximately that size
            #   - negative bufsize (the default) means the system default
            #     of io.DEFAULT_BUFFER_SIZE will be used.
            #
            # pylint: disable=consider-using-with
            if p2cwrite != commons.NO_PIPE:
                if isinstance(p2cwrite, streams.Connection):
                    if self._text_mode:
                        self.stdin = streams.TextConnectionWriter(
                            p2cwrite,
                            bufsize,
                            encoding=encoding__,
                            errors=errors__,
                        )
                    else:
                        self.stdin = streams.ConnectionWriter(p2cwrite, bufsize)
                    #
                else:
                    self.stdin = io.open(p2cwrite, "wb", bufsize)
                #
            #
            if c2pread != commons.NO_PIPE:
                if isinstance(c2pread, streams.Connection):
                    if self._text_mode:
                        self.stdout = streams.TextConnectionReader(
                            c2pread,
                            bufsize,
                            encoding=encoding__,
                            errors=errors__,
                        )
                    else:
                        self.stdout = streams.ConnectionReader(c2pread, bufsize)
                    #
                else:
                    self.stdout = io.open(c2pread, "rb", bufsize)
                #
            #
            if errread != commons.NO_PIPE:
                if isinstance(errread, streams.Connection):
                    self.stderr = streams.ConnectionReader(errread, bufsize)
                    if self._text_mode:
                        self.stderr = streams.TextConnectionReader(
                            errread,
                            bufsize,
                            encoding=encoding__,
                            errors=errors__,
                        )
                    else:
                        self.stderr = streams.ConnectionReader(errread, bufsize)
                    #
                else:
                    self.stderr = io.open(errread, "rb", bufsize)
                #
            #
            # pylint: enable=consider-using-with
            self._execute_child(
                args,
                executable,
                pass_fds,
                cwd,
                env,
                shell,
                p2cread,
                p2cwrite,
                c2pread,
                c2pwrite,
                errread,
                errwrite,
                child_steps=child_steps,
            )
        except Exception as exc:
            # Cleanup if the child failed starting.
            for f in (self.stdin, self.stdout, self.stderr):
                if f is None:
                    continue
                #
                try:
                    f.close()
                except OSError:
                    pass  # Ignore EBADF or other errors.

            if not self._closed_child_pipe_fds:
                to_close = []
                if stdin == commons.PIPE:
                    to_close.append(p2cread)
                if stdout == commons.PIPE:
                    to_close.append(c2pwrite)
                if stderr == commons.PIPE:
                    to_close.append(errwrite)
                if hasattr(self, "_devnull"):
                    to_close.append(self._devnull)
                for fd in to_close:
                    if isinstance(fd, streams.Connection):
                        fd.close()
                    else:
                        try:
                            os.close(fd)
                        except OSError:
                            pass

            raise exc

    def _translate_newlines(
        self, data: Union[bytes, str], encoding: str, errors: str
    ) -> str:
        """Decode if necessary and translate newlines"""
        if isinstance(data, bytes):
            unicode_data = data.decode(encoding, errors)
        else:
            unicode_data = str(data)
        #
        return unicode_data.replace("\r\n", "\n").replace("\r", "\n")

    def __enter__(self) -> "Popen":
        """Context manager: enter"""
        return self

    # pylint: disable=redefined-builtin
    def __exit__(self, type, value, traceback) -> None:
        """Context manager: exit"""
        if self.stdout:
            self.stdout.close()
        #
        if self.stderr:
            self.stderr.close()
        #
        try:  # Flushing a BufferedWriter may raise an error
            if self.stdin:
                self.stdin.close()
            #
        finally:
            # Wait for the process to terminate, to avoid zombies.
            self.wait()
        #

    def __del__(self, _maxsize: int = sys.maxsize, _warn=warnings.warn) -> None:
        """Delete the instance"""
        if not self._child_created:
            # We didn't get to successfully create a child process.
            return
        #
        if self.returncode is None:
            # Not reading subprocess exit status creates a zombi process which
            # is only destroyed at the parent python process exit
            _warn(
                f"subprocess {self.pid} is still running",
                ResourceWarning,
                source=self,
            )
        #
        # In case the child hasn't been waited on, check if it's done.
        self._internal_poll_mock(_deadstate=_maxsize)
        if self.returncode is None and _ACTIVE is not None:
            # Child is still running, keep us alive until we can wait on it.
            _ACTIVE.append(self)
        #

    def _get_devnull(self) -> int:
        """return the /dev/null file"""
        if not hasattr(self, "_devnull"):
            self._devnull = os.open(os.devnull, os.O_RDWR)
        #
        return self._devnull

    def _stdin_write(self, input: Union[bytes, str]) -> None:
        """Write to standard input"""
        if self.stdin is None:
            return
        #
        if input:
            try:
                self.stdin.write(input)
            except BrokenPipeError:
                pass  # communicate() must ignore broken pipe errors.
            except OSError as exc:
                if exc.errno == errno.EINVAL:
                    # bpo-19612, bpo-30418: On Windows, stdin.write() fails
                    # with EINVAL if the child process exited or if the child
                    # process is still running but closed the pipe.
                    pass
                else:
                    raise
                #
            #
        #
        try:
            self.stdin.close()
        except BrokenPipeError:
            pass  # communicate() must ignore broken pipe errors.
        except OSError as exc:
            if exc.errno == errno.EINVAL:
                pass
            else:
                raise
            #
        #

    def communicate(
        self, input=None, timeout: Optional[int] = None
    ) -> Tuple[Union[bytes, str, None], Union[bytes, str, None]]:
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.

        The optional "input" argument should be data to be sent to the
        child process (if self.universal_newlines is True, this should
        be a string; if it is False, "input" should be bytes), or
        None, if no data should be sent to the child.

        communicate() returns a tuple (stdout, stderr).  These will be
        bytes or, if self.universal_newlines was True, a string.
        """

        if self._communication_started and input:
            raise ValueError("Cannot send input after starting communication")
        #
        if timeout is not None:
            endtime = _time() + timeout
        else:
            endtime = None
        #
        try:
            stdout, stderr = self._communicate(input, endtime)
        finally:
            self._communication_started = True
        #
        self.wait(timeout=self._remaining_time(endtime))
        return (stdout, stderr)

    def poll(self) -> Optional[int]:
        """Check if child process has terminated. Set and return returncode
        attribute."""
        return self._internal_poll_mock()

    def _remaining_time(self, endtime: Optional[float]) -> Optional[float]:
        """Convenience for _communicate when computing timeouts."""
        if endtime is None:
            return None
        #
        return endtime - _time()

    def _check_timeout(
        self, endtime: Optional[float], orig_timeout: Optional[float]
    ) -> None:
        """Convenience for checking if a timeout has expired."""
        if endtime is None:
            return
        #
        if _time() > endtime:
            raise TimeoutExpired(self.args, orig_timeout or 0)
        #

    #
    # POSIX methods
    #

    def _get_handles(self, stdin, stdout, stderr):
        """Construct and return tuple with IO objects:
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
        """
        p2cread, p2cwrite = commons.NO_PIPE, commons.NO_PIPE
        c2pread, c2pwrite = commons.NO_PIPE, commons.NO_PIPE
        errread, errwrite = commons.NO_PIPE, commons.NO_PIPE

        if stdin == commons.PIPE:
            p2cread, p2cwrite = multiprocessing.Pipe(duplex=False)
        elif stdin == commons.DEVNULL:
            p2cread = self._get_devnull()
        elif isinstance(stdin, int):
            p2cread = stdin
        elif stdin is not None:
            # Assuming file-like object
            p2cread = stdin.fileno()
        #
        if stdout == commons.PIPE:
            c2pread, c2pwrite = multiprocessing.Pipe(duplex=False)
        elif stdout == commons.DEVNULL:
            c2pwrite = self._get_devnull()
        elif isinstance(stdout, int):
            c2pwrite = stdout
        elif stdout is not None:
            # Assuming file-like object
            c2pwrite = stdout.fileno()
        #
        if stderr == commons.PIPE:
            errread, errwrite = multiprocessing.Pipe(duplex=False)
        elif stderr == commons.STDOUT:
            if c2pwrite != commons.NO_PIPE:
                errwrite = c2pwrite
            else:  # child's stdout is not set, use parent's stdout
                errwrite = sys.__stdout__.fileno()
            #
        elif stderr == commons.DEVNULL:
            errwrite = self._get_devnull()
        elif isinstance(stderr, int):
            errwrite = stderr
        elif stderr is not None:
            # Assuming file-like object
            errwrite = stderr.fileno()
        #
        return (p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

    def _execute_child(
        self,
        args,
        executable,
        pass_fds,
        cwd,
        env,
        shell,
        p2cread,
        p2cwrite,
        c2pread,
        c2pwrite,
        errread,
        errwrite,
        child_steps: Tuple[child.Step, ...] = (),
    ):
        """Execute program (POSIX version)"""

        if isinstance(args, (str, bytes)):
            args = [args]
        else:
            args = list(args)

        if shell:
            args = ["/bin/sh", "-c"] + args
            if executable:
                args[0] = executable

        if executable is None:
            executable = args[0]
        # orig_executable = executable

        # For transferring possible exec failure from child to parent.
        # Data format: "exception name:description"
        # Pickle is not used; it is complex and involves memory allocation.
        errpipe_read, errpipe_write = multiprocessing.Pipe(duplex=False)
        try:
            # We must avoid complex work that could involve
            # malloc or free in the child process to avoid
            # potential deadlocks, thus we do all this here.
            # and pass it to fork_exec()
            if env is not None:
                env_list = []
                for k, v in env.items():
                    k = os.fsencode(k)
                    if b"=" in k:
                        raise ValueError("illegal environment variable name")
                    #
                    env_list.append(k + b"=" + os.fsencode(v))
                #
            else:
                env_list = None  # Use execv instead of execve.
            #
            # fds_to_keep = set(pass_fds)
            # fds_to_keep.add(errpipe_write)
            logging.debug("[parent] Starting %r subprocess …", args)
            self.mocked_child_process = multiprocessing.Process(
                target=child.run_process,
                args=child_steps,
                kwargs={
                    commons.KW_STDIN: p2cread,
                    commons.KW_STDOUT: c2pwrite,
                    commons.KW_STDERR: errwrite,
                    "error_channel": errpipe_write,
                },
            )
            logging.debug("[parent] … process created")
            self.mocked_child_process.start()
            self.pid = self.mocked_child_process.pid
            self._child_created = True
            #
            # close child pipelines
            # self._devnull is not always defined.
            devnull_fd = getattr(self, "_devnull", None)
            if (
                p2cread != -1
                and p2cwrite != -1
                and p2cread != devnull_fd
                and isinstance(p2cread, int)
            ):
                os.close(p2cread)
            if (
                c2pwrite != -1
                and c2pread != -1
                and c2pwrite != devnull_fd
                and isinstance(c2pwrite, int)
            ):
                os.close(c2pwrite)
            if (
                errwrite != -1
                and errread != -1
                and errwrite != devnull_fd
                and isinstance(errwrite, int)
            ):
                os.close(errwrite)
            if devnull_fd is not None:
                os.close(devnull_fd)
            # Prevent a double close of these fds from __init__ on error.
            self._closed_child_pipe_fds = True

            # Wait for exec to fail or succeed; possibly raising an
            # exception (limited in size)
            errpipe_data = bytearray()
            while not errpipe_read.poll():
                logging.debug("[parent] … waiting for process %s startup", self.pid)
                time.sleep(0.05)
            #
            try:
                errpipe_data.extend(errpipe_read.recv_bytes())
            except EOFError:
                pass
            #
        finally:
            # be sure the FD is closed no matter what
            errpipe_read.close()
        #
        if errpipe_data:
            try:
                if isinstance(self.pid, int):
                    numeric_pid: int = self.pid
                else:
                    numeric_pid = 1
                #
                pid, sts = os.waitpid(numeric_pid, 0)
                if pid == self.pid:
                    self._handle_exitstatus(sts)
                else:
                    self.returncode = sys.maxsize
                #
            except ChildProcessError:
                pass
            #
            try:
                exception_name, err_msg_bin = bytes(errpipe_data).split(b":")
                # The encoding here should match the encoding
                # written in by the subprocess implementations
                # like _posixsubprocess
                err_msg = err_msg_bin.decode()
            except ValueError:
                exception_name = b"SubprocessError"
                err_msg = f"Bad exception data from child: {bytes(errpipe_data)!r}"
            #
            child_exception_type = getattr(
                builtins,
                exception_name.decode("ascii"),
                SubprocessError,
            )
            raise child_exception_type(err_msg)
        #

    # pylint: disable=invalid-name
    def _handle_exitstatus(
        self,
        sts: int,
    ) -> int:
        """All callers to this function MUST hold self._waitpid_lock."""
        # This method is called (indirectly) by __del__, so it cannot
        # refer to anything outside of its local scope.
        # if _WIFSIGNALED(sts):
        #     returncode = -_WTERMSIG(sts)
        # elif _WIFEXITED(sts):
        #     returncode = _WEXITSTATUS(sts)
        # elif _WIFSTOPPED(sts):
        #     returncode = -_WSTOPSIG(sts)
        # else:
        #     # Should never happen
        #     raise subprocess.SubprocessError("Unknown child exit status!")
        #
        # WIFSTOPPED = sts & 0x7f == 0x7f
        # WIFSIGNALLED = sts & 0x7f == 0x00, 0x7f
        # WIFEXITED = sts & 0x7f == 0x00
        # WTERMSIG(sts) = sts & 0x7f
        # WEXITSTATUS(sts) = sts >> 8
        # WSTOPSIG(sts) = sts >> 8
        signal_part = sts & 0x7F
        rc_part = sts >> 8
        if signal_part not in (0x00, 0x7F):
            returncode = -signal_part
        elif signal_part == 0x0:
            returncode = rc_part
        elif signal_part == 0x7F:
            returncode = -rc_part
        else:
            # Should never happen
            raise SubprocessError("Unknown child exit status!")
        #
        return returncode

    def _internal_poll_mock(self, _deadstate: Optional[int] = None) -> Optional[int]:
        """Check if child process has terminated.
        Sets and returns returncode attribute.
        """
        if self.mocked_child_process.exitcode is None:
            return None
        #
        if self._orchestrator_callback is not None:
            self._orchestrator_callback(self)
        #
        self.returncode = self.mocked_child_process.exitcode
        logging.debug("[parent] received returncode: %s", self.returncode)
        return self.returncode

    def _old_internal_poll(
        self,
        _deadstate=None,
        _waitpid=os.waitpid,
        _WNOHANG=_WNOHANG,
        _ECHILD=errno.ECHILD,
    ):
        """Check if child process has terminated.  Returns returncode
        attribute.

        This method is called by __del__, so it cannot reference anything
        outside of the local scope (nor can any methods it calls).

        """
        if self.returncode is None:
            # pylint: disable=consider-using-with
            if not self._waitpid_lock.acquire(False):
                # Something else is busy calling waitpid.  Don't allow two
                # at once.  We know nothing yet.
                return None
            #
            try:
                if self.returncode is not None:
                    return self.returncode  # Another thread waited.
                #
                pid, sts = os.waitpid(self.pid, _WNOHANG)
                if pid == self.pid:
                    self._handle_exitstatus(sts)
                #
            except OSError as e:
                if _deadstate is not None:
                    self.returncode = _deadstate
                elif e.errno == _ECHILD:
                    # This happens if SIGCLD is set to be ignored or
                    # waiting for child processes has otherwise been
                    # disabled for our process.  This child is dead, we
                    # can't get the status.
                    # http://bugs.python.org/issue15756
                    self.returncode = 0
                #
            finally:
                self._waitpid_lock.release()
            #
        #
        return self.returncode

    def wait(self, timeout=None, endtime: Optional[float] = None) -> Optional[int]:
        """Wait for child process to terminate.  Returns returncode
        attribute."""
        if self.returncode is not None:
            return self.returncode

        if endtime is not None:
            warnings.warn(
                "'endtime' argument is deprecated; use 'timeout'.",
                DeprecationWarning,
                stacklevel=2,
            )
        if endtime is not None or timeout is not None:
            if endtime is None:
                endtime = _time() + timeout
            elif timeout is None:
                timeout = self._remaining_time(endtime)

        if endtime is not None:
            # Enter a busy loop if we have a timeout.  This busy loop was
            # cribbed from Lib/threading.py in Thread.wait() at r71065.
            delay = 0.0005  # 500 us -> initial delay of 1 ms
            while True:
                # pylint: disable=consider-using-with
                if self._waitpid_lock.acquire(False):
                    try:
                        self._internal_poll_mock()
                        if self.returncode is not None:
                            break
                        #
                    finally:
                        self._waitpid_lock.release()
                    #
                #
                remaining = self._remaining_time(endtime)
                if remaining is not None and remaining <= 0:
                    raise TimeoutExpired(self.args, timeout or 0)
                #
                delay = min(delay * 2, remaining or 0.05, 0.05)
                time.sleep(delay)
            #
        else:
            while self.returncode is None:
                with self._waitpid_lock:
                    self._internal_poll_mock()
                    if self.returncode is not None:
                        break
                    #
                #
            #
        #
        return self.returncode

    def _communicate(
        self, input, endtime: Optional[float]
    ) -> Tuple[Union[bytes, str, None], Union[bytes, str, None]]:
        """Communicate and return the (stdout, stderr) tuple"""
        if self.stdin and not self._communication_started:
            # Flush stdin buffer.  This might block, if the user has
            # been writing to .stdin in an uncontrolled fashion.
            try:
                self.stdin.flush()
            except BrokenPipeError:
                pass  # communicate() must ignore BrokenPipeError.
            #
            if not input:
                try:
                    self.stdin.close()
                except BrokenPipeError:
                    pass  # communicate() must ignore BrokenPipeError.
                #
            #
        #
        stdout: Optional[Union[bytes, str]] = None
        stderr: Optional[Union[bytes, str]] = None
        stdout_collect: List[Union[bytes, str]] = []
        stderr_collect: List[Union[bytes, str]] = []
        # Only create this mapping if we haven't already.
        if not self._communication_started:
            self._fileobj2output: Dict[
                Union[IO, streams.ConnectionWrapper], List[Union[bytes, str]]
            ] = {}
            self._pipe_broken = {}
            if self.stdout:
                self._fileobj2output[self.stdout] = []
                self._pipe_broken[self.stdout] = False
            #
            if self.stderr:
                self._fileobj2output[self.stderr] = []
                self._pipe_broken[self.stderr] = False
            #
        #
        if self.stdout:
            stdout_collect = self._fileobj2output[self.stdout]
        #
        if self.stderr:
            stderr_collect = self._fileobj2output[self.stderr]
        #
        self._save_input(input)
        if self._input and isinstance(self.stdin, streams.ConnectionWriter):
            logging.debug("[parent] writing chunk to child: %r", self._input)
            try:
                self.stdin.write(self._input)
            except BrokenPipeError:
                pass
            finally:
                self.stdin.close()
            #
        #
        while True:
            time.sleep(0.05)
            for fileobj in (self.stdout, self.stderr):
                if not fileobj:
                    continue
                #
                if self._pipe_broken.get(fileobj, True):
                    continue
                #
                try:
                    data = fileobj.read()
                except BrokenPipeError:
                    logging.warning("[parent] Pipe broken: %r", fileobj)
                    self._pipe_broken[fileobj] = True
                else:
                    if data:
                        logging.debug("[parent] Got data from %r: %r", fileobj, data)
                        self._fileobj2output[fileobj].append(data)
                    #
                #
            #
            if all(probe for probe in self._pipe_broken.values()):
                break
            #
            if not self.mocked_child_process.is_alive():
                break
            #
        #
        self.wait(timeout=self._remaining_time(endtime))
        joiner: Union[bytes, str] = "" if self._text_mode else b""
        # All data exchanged.  Translate lists into strings.
        if self.stdout is not None:
            stdout = joiner.join(stdout_collect)  # type: ignore
        #
        if self.stderr is not None:
            stderr = joiner.join(stderr_collect)  # type: ignore
        #
        # Translate newlines, if requested.
        # This also decodes bytes into strings if required
        if self._text_mode:
            encoding = self.encoding or sys.getdefaultencoding()
            errors = self.errors or "strict"
            if stdout is not None:
                stdout = self._translate_newlines(
                    stdout,
                    encoding,
                    errors,
                )
            #
            if stderr is not None:
                stderr = self._translate_newlines(
                    stderr,
                    encoding,
                    errors,
                )
            #
        #
        return (stdout, stderr)

    def _save_input(self, input__: Union[bytes, str]) -> None:
        """This method is called from the _communicate_with_*() methods
        so that if we time out while communicating, we can continue
        sending input if we retry.
        """
        if self.stdin and self._input is None:
            self._input_offset = 0
            self._input = input__
        #

    def send_signal(self, sig: int) -> None:
        """Send a signal to the process."""
        # Skip signalling a process that we know has already died.
        if self.returncode is None and isinstance(self.pid, int):
            os.kill(self.pid, sig)
        #

    def terminate(self) -> None:
        """Terminate the process with SIGTERM"""
        self.mocked_child_process.terminate()

    def kill(self) -> None:
        """Kill the process with SIGKILL"""
        self.send_signal(signal.SIGKILL)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
