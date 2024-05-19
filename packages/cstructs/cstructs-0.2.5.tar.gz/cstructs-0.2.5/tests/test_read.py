# --------------------------------------------------------------------------------------
#  Copyright(C) 2023 yntha                                                             -
#                                                                                      -
#  This program is free software: you can redistribute it and/or modify it under       -
#  the terms of the GNU General Public License as published by the Free Software       -
#  Foundation, either version 3 of the License, or (at your option) any later          -
#  version.                                                                            -
#                                                                                      -
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY     -
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A     -
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.            -
#                                                                                      -
#  You should have received a copy of the GNU General Public License along with        -
#  this program. If not, see <http://www.gnu.org/licenses/>.                           -
# --------------------------------------------------------------------------------------
import pytest
import io

from cstructs import datastruct, NativeTypes, DataStruct, Sequence, Member, MemberRef
from typing import Annotated


def test_read_basic():
    """
    Test case for reading basic data from a stream.
    """

    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint8
        b: NativeTypes.uint8

        def on_read(
            self,
        ):
            assert self.a == 1
            assert self.b == 2

    stream = io.BytesIO(bytes.fromhex("01 02"))
    test = Test.read(stream)

    assert test.a == 1
    assert test.b == 2


def test_read_complex():
    """
    Test case for reading complex data using a datastruct.
    """

    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint16
        b: NativeTypes.uint32
        c: NativeTypes.i32
        d: NativeTypes.uint64
        e: Annotated[bytes, Member(NativeTypes.bytestring, Sequence(4))]
        f: Annotated[str, Member(NativeTypes.char, Sequence(12))]
        g: Annotated[str, Member(NativeTypes.char, Sequence(encoding="latin1"))]
        h: Annotated[int, Member(NativeTypes.u8, default=123)]

    stream = io.BytesIO()

    stream.write(bytes.fromhex("0001"))
    stream.write(bytes.fromhex("00000002"))
    stream.write(bytes.fromhex("fffffffd"))
    stream.write(bytes.fromhex("0000000000000004"))
    stream.write(bytes.fromhex("01020304"))
    stream.write(b"Hello World!")
    stream.write(bytes.fromhex("BF"))
    stream.write(bytes.fromhex("00"))

    stream.seek(0)

    test = Test.read(stream)

    assert test.a == 1
    assert test.b == 2
    assert test.c == -3
    assert test.d == 4
    assert test.e == b"\x01\x02\x03\x04"
    assert test.f == "Hello World!"
    assert test.g == "¿"


def test_read_datastruct_sequence():
    """
    Test case for reading a datastruct with a sequence of nested datastructs.
    """
    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint16
        b: Annotated[
            str, Member(NativeTypes.char, Sequence(MemberRef("a")), "Default Value")
        ]

    @datastruct(byteorder="big")
    class Test2(metaclass=DataStruct):
        a: NativeTypes.uint16
        b: Annotated[list, Member(Test, Sequence(MemberRef("a")))]

        def on_read(self):
            assert self.a == 3

            assert self.b[0].a == 7
            assert self.b[0].b == "!!yntha"
            assert self.b[1].a == 0x15
            assert self.b[1].b == "@kilozz on discord ;)"
            assert self.b[2].a == 0
            assert self.b[2].b == "Default Value"

    stream = io.BytesIO()

    stream.write(bytes.fromhex("00 03"))
    stream.write(bytes.fromhex("00 07"))
    stream.write(bytes.fromhex("21 21 79 6E 74 68 61"))
    stream.write(bytes.fromhex("00 15"))
    stream.write(
        bytes.fromhex("40 6B 69 6C 6F 7A 7A 20 6F 6E 20 64 69 73 63 6F 72 64 20 3B 29")
    )
    stream.write(bytes.fromhex("00 00"))

    stream.seek(0)

    test = Test2.read(stream)
