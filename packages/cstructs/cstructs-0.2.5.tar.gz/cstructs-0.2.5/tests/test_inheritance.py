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
import io

from cstructs import datastruct, DataStruct, NativeTypes


def test_inheritance():
    """
    Test case for inheritance in datastructs.
    """

    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.uint32

    @datastruct(byteorder="big")
    class Test2(Test, metaclass=DataStruct):
        c: NativeTypes.u8

        def on_read(self):
            assert self.a == 1
            assert self.b == 2
            assert self.c == 3

    stream = io.BytesIO()
    stream.write(b"00 00 00 01")
    stream.write(b"00 00 00 02")
    stream.write(b"03")

    stream.seek(0)

    Test.read(stream)


def test_datastruct_as_typehint():
    """
    Test case for using a datastruct as a type hint.
    """
    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.uint32

    @datastruct(byteorder="big")
    class Test2(metaclass=DataStruct):
        a: Test
        b: NativeTypes.int32
        c: Test

        def on_read(self):
            assert self.a.a == 1
            assert self.a.b == 2
            assert self.b == -3
            assert self.c.a == 4
            assert self.c.b == 5

    stream = io.BytesIO()
    stream.write(bytes.fromhex("00 00 00 01"))
    stream.write(bytes.fromhex("00 00 00 02"))
    stream.write(bytes.fromhex("FF FF FF FD"))
    stream.write(bytes.fromhex("00 00 00 04"))
    stream.write(bytes.fromhex("00 00 00 05"))

    stream.seek(0)

    test = Test2.read(stream)

    assert test.a.a == 1
    assert test.a.b == 2
    assert test.b == -3
    assert test.c.a == 4
    assert test.c.b == 5
