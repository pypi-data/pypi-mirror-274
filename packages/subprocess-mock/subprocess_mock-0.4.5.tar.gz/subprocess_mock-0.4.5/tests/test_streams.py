# -*- coding: utf-8 -*-

"""

tests.test_streams

Unit test the streams module


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

# import logging

from multiprocessing import Pipe
from unittest import TestCase

from subprocess_mock import streams


class BaseConnectionWrapper(TestCase):
    """Test the ConnectionWrapper() base class"""

    maxDiff = None

    def setUp(self):
        """Initialize connections"""
        self.read_conn, self.write_conn = Pipe(duplex=False)

    def tearDown(self):
        """Initialize connections"""
        self.read_conn.close()
        self.write_conn.close()


class ConnectionWrapper(BaseConnectionWrapper):
    """Test the ConnectionWrapper() base class"""

    def test_attribute_buffer_size(self) -> None:
        """.buffer_size attribute as initialized"""
        with self.subTest("default"):
            wrapper = streams.ConnectionWrapper(self.read_conn)
            self.assertEqual(wrapper.buffer_size, io.DEFAULT_BUFFER_SIZE)
        #
        bufsize = 23
        with self.subTest("as initialized", bufsize=bufsize):
            wrapper = streams.ConnectionWrapper(self.read_conn, buffer_size=bufsize)
            self.assertEqual(wrapper.buffer_size, bufsize)
        #
        bufsize = 1
        with self.subTest("changed to 0", bufsize=bufsize):
            wrapper = streams.ConnectionWrapper(self.read_conn, buffer_size=bufsize)
            self.assertEqual(wrapper.buffer_size, 0)
        #
        bufsize = -25
        with self.subTest("negative value changed to system default", bufsize=bufsize):
            wrapper = streams.ConnectionWrapper(self.read_conn, buffer_size=bufsize)
            self.assertEqual(wrapper.buffer_size, io.DEFAULT_BUFFER_SIZE)
        #

    def test_property_connection(self) -> None:
        """.connection property is the connection as initialized"""
        wrapper = streams.ConnectionWrapper(self.read_conn)
        self.assertIs(wrapper.connection, self.read_conn)

    def test_property_raw(self) -> None:
        """.raw property is an empty bytearray"""
        wrapper = streams.ConnectionWrapper(self.read_conn)
        self.assertEqual(wrapper.raw, bytearray())

    def test_close_and_closed(self) -> None:
        """.close() method and .closed property"""
        wrapper = streams.ConnectionWrapper(self.read_conn)
        with self.subTest("pre-close"):
            self.assertFalse(wrapper.closed)
        #
        wrapper.close()
        with self.subTest("post-close"):
            self.assertTrue(wrapper.closed)
        #

    def test_disabled_methods(self) -> None:
        """.seek(), .read(), .write() and .flush()
        – disabled in the base class
        """
        wrapper = streams.ConnectionWrapper(self.read_conn)
        for method, capability, args in (
            (wrapper.seek, "seekable", (0,)),
            (wrapper.read, "readable", ()),
            (wrapper.write, "writable", (b"",)),
            (wrapper.flush, "writable", ()),
        ):
            with self.subTest(f"{method!r}", capability=capability):
                self.assertRaisesRegex(  # type: ignore
                    ValueError,
                    f"^This stream is not {capability}",
                    method,
                    *args,
                )
            #
        #

    def test_readable_connection(self) -> None:
        """Writable subclass initialized with a readable
        instead of a writable connection
        """
        self.assertRaisesRegex(
            ValueError,
            '^"connection" argument must be writable\\.$',
            streams.ConnectionWriter,
            self.read_conn,
        )

    def test_writable_connection(self) -> None:
        """Readable subclass initialized with a writable
        instead of a readable connection
        """
        self.assertRaisesRegex(
            ValueError,
            '^"connection" argument must be readable\\.$',
            streams.ConnectionReader,
            self.write_conn,
        )


class ConnectionReader(BaseConnectionWrapper):
    """Test the ConnectionReader() class"""

    def test_read_and_tell(self) -> None:
        """.read() and .tell() methods"""
        wrapper = streams.ConnectionReader(self.read_conn)
        total_bytes = 0
        with self.subTest("read all"):
            written_data = b"testdata"
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read()
            total_bytes += len(written_data)
            self.assertEqual(read_data, written_data)
        #
        with self.subTest("read a part"):
            written_data = b"longer message"
            number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read(number_of_bytes)
            total_bytes += number_of_bytes
            self.assertEqual(read_data, written_data[:number_of_bytes])
        #
        with self.subTest("tell() result", expected=total_bytes):
            self.assertEqual(wrapper.tell(), total_bytes)
        #
        size = -7
        with self.subTest("negative values smaller than -1 not accepted", size=size):
            self.assertRaisesRegex(
                ValueError,
                "^invalid number of bytes to read",
                wrapper.read,
                size,
            )
        #

    def test_read1(self) -> None:
        """.read1() method"""
        wrapper = streams.ConnectionReader(self.read_conn)
        total_bytes = 0
        with self.subTest("read1 a part"):
            written_data = b"longer message"
            old_number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read1(old_number_of_bytes)
            total_bytes += old_number_of_bytes
            self.assertEqual(read_data, written_data[:old_number_of_bytes])
        #
        with self.subTest("read1 another part"):
            new_number_of_bytes = 2
            read_data = wrapper.read1(new_number_of_bytes)
            total_bytes += new_number_of_bytes
            self.assertEqual(read_data, written_data[old_number_of_bytes:total_bytes])
        #
        with self.subTest("read1 0 bytes"):
            read_data = wrapper.read1(0)
            self.assertEqual(read_data, b"")
        #
        with self.subTest("tell() result", expected=total_bytes):
            self.assertEqual(wrapper.tell(), total_bytes)
        #
        size = -1
        with self.subTest("negative values not accepted", size=size):
            self.assertRaisesRegex(
                ValueError,
                "^number of bytes to read must be positive",
                wrapper.read1,
                size,
            )
        #

    def test_peek_and_tell(self) -> None:
        """.peek() and .tell() methods"""
        wrapper = streams.ConnectionReader(self.read_conn)
        with self.subTest("read all"):
            written_data = b"testdata"
            number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            poke_data = wrapper.peek(number_of_bytes)
            self.assertEqual(poke_data, written_data[:number_of_bytes])
        #
        with self.subTest("tell() result", expected=0):
            self.assertEqual(wrapper.tell(), 0)
        #


class TextConnectionReader(BaseConnectionWrapper):
    """Test the ConnectionReader() class"""

    def test_read_and_tell(self) -> None:
        """.read() and .tell() methods"""
        wrapper = streams.TextConnectionReader(self.read_conn)
        total_bytes = 0
        with self.subTest("read all"):
            written_data = b"testdata"
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read()
            total_bytes += len(written_data)
            self.assertEqual(read_data, written_data.decode())
        #
        with self.subTest("read a part"):
            written_data = b"longer message"
            number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read(number_of_bytes)
            total_bytes += number_of_bytes
            self.assertEqual(read_data, written_data[:number_of_bytes].decode())
        #
        with self.subTest("tell() result", expected=total_bytes):
            self.assertEqual(wrapper.tell(), total_bytes)
        #
        size = -7
        with self.subTest("negative values smaller than -1 not accepted", size=size):
            self.assertRaisesRegex(
                ValueError,
                "^invalid number of bytes to read",
                wrapper.read,
                size,
            )
        #

    def test_read1(self) -> None:
        """.read1() method"""
        wrapper = streams.TextConnectionReader(self.read_conn)
        total_bytes = 0
        with self.subTest("read1 a part"):
            written_data = b"longer message"
            old_number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            read_data = wrapper.read1(old_number_of_bytes)
            total_bytes += old_number_of_bytes
            self.assertEqual(read_data, written_data[:old_number_of_bytes].decode())
        #
        with self.subTest("read1 another part"):
            new_number_of_bytes = 2
            read_data = wrapper.read1(new_number_of_bytes)
            total_bytes += new_number_of_bytes
            self.assertEqual(
                read_data,
                written_data[old_number_of_bytes:total_bytes].decode(),
            )
        #
        with self.subTest("read1 0 bytes"):
            read_data = wrapper.read1(0)
            self.assertEqual(read_data, "")
        #
        with self.subTest("tell() result", expected=total_bytes):
            self.assertEqual(wrapper.tell(), total_bytes)
        #
        size = -1
        with self.subTest("negative values not accepted", size=size):
            self.assertRaisesRegex(
                ValueError,
                "^number of bytes to read must be positive",
                wrapper.read1,
                size,
            )
        #

    def test_peek_and_tell(self) -> None:
        """.peek() and .tell() methods"""
        wrapper = streams.TextConnectionReader(self.read_conn)
        with self.subTest("read all"):
            written_data = b"testdata"
            number_of_bytes = 4
            self.write_conn.send_bytes(written_data)
            poke_data = wrapper.peek(number_of_bytes)
            self.assertEqual(poke_data, written_data[:number_of_bytes].decode())
        #
        with self.subTest("tell() result", expected=0):
            self.assertEqual(wrapper.tell(), 0)
        #


class ConnectionWriterBase(BaseConnectionWrapper):
    """Base class for *ConnectionWriter() classes"""

    def _try_read_all(self):
        """Try to read all data"""
        data = b""
        while self.read_conn.poll():
            try:
                data += self.read_conn.recv_bytes()
            except EOFError:
                break
            #
        #
        return data


class ConnectionWriter(ConnectionWriterBase):
    """Test the ConnectionWriter() class"""

    def test_write(self) -> None:
        """.write() method"""
        wrapper = streams.ConnectionWriter(self.write_conn)
        total_bytes = 0
        written_data = b"testdata"
        total_bytes += wrapper.write(written_data)
        read_data = self._try_read_all()
        with self.subTest("write and read"):
            self.assertEqual(read_data, written_data)
        #
        with self.subTest("number of bytes written"):
            self.assertEqual(total_bytes, len(written_data))
        #
        with self.subTest("text data not accepted"):
            self.assertRaisesRegex(
                ValueError,
                "^This stream accepts binary data only\\.",
                wrapper.write,
                "unicode",
            )
        #

    def test_flush(self) -> None:
        """.flush() method"""
        wrapper = streams.ConnectionWriter(self.write_conn)
        conn_data = b"testdata"
        wrapper.raw.extend(conn_data)
        with self.subTest("No data read before flush"):
            self.assertEqual(self._try_read_all(), b"")
        #
        wrapper.flush()
        with self.subTest("All data read after flush"):
            self.assertEqual(self._try_read_all(), conn_data)
        #


class TextConnectionWriter(ConnectionWriterBase):
    """Test the TextConnectionWriter() class"""

    def test_write_line_buffered(self) -> None:
        """.write() method, line buffered"""
        wrapper = streams.TextConnectionWriter(self.write_conn, buffer_size=1)
        total_bytes = 0
        first_written_data = "no-lf "
        total_bytes += wrapper.write(first_written_data)
        read_data = self._try_read_all()
        with self.subTest("write without LF"):
            self.assertEqual(read_data, b"")
        #
        line_3 = "line 3"
        written_data = f"testdata\nline 2\n{line_3}"
        expected_read_data = b"no-lf testdata\nline 2\n"
        total_bytes += wrapper.write(written_data)
        read_data = self._try_read_all()
        with self.subTest("write and read"):
            self.assertEqual(read_data, expected_read_data)
        #
        with self.subTest("number of bytes written"):
            self.assertEqual(total_bytes, len(expected_read_data))
        #
        with self.subTest("binary data not accepted"):
            self.assertRaisesRegex(
                ValueError,
                "^This stream accepts text data only\\.",
                wrapper.write,
                b"binary content",
            )
        #
        with self.subTest("read remainder after close"):
            wrapper.close()
            read_data = self._try_read_all()
            self.assertEqual(read_data, line_3.encode())
        #

    def test_write_unbuffered(self) -> None:
        """.write() method, not buffered"""
        wrapper = streams.TextConnectionWriter(self.write_conn, buffer_size=0)
        total_bytes = 0
        first_written_data = "no-lf "
        total_bytes += wrapper.write(first_written_data)
        read_data = self._try_read_all()
        with self.subTest("write without LF"):
            self.assertEqual(read_data, first_written_data.encode())
        #
        written_data = "testdata\nline 2\nline 3"
        expected_read_data = b"testdata\nline 2\nline 3"
        total_bytes += wrapper.write(written_data)
        read_data = self._try_read_all()
        with self.subTest("write and read"):
            self.assertEqual(read_data, expected_read_data)
        #
        with self.subTest("number of bytes written"):
            self.assertEqual(
                total_bytes, len(first_written_data) + len(expected_read_data)
            )
        #
        with self.subTest("binary data not accepted"):
            self.assertRaisesRegex(
                ValueError,
                "^This stream accepts text data only\\.",
                wrapper.write,
                b"binary content",
            )
        #
        with self.subTest("read remainder after close"):
            wrapper.close()
            read_data = self._try_read_all()
            self.assertEqual(read_data, b"")
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
