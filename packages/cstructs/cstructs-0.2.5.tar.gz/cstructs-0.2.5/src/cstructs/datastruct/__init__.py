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
import dataclasses
import io
import typing

from cstructs.exc import (
    InvalidByteOrder,
    InvalidTypeDef,
    InvalidSequence,
    InvalidMember,
    SequenceLengthMismatch,
)
from cstructs.datastruct.metadata import StructMeta, MetadataItem
from cstructs.nativetypes import NativeType, NativeTypes
from cstructs.util import is_datastruct


_byteorder_map = {"native": "@", "little": "<", "network": "!", "big": ">"}


@dataclasses.dataclass
class MemberRef:
    """
    Represents a reference to a datastruct member.

    Attributes:
        member_name (str): The name of the member.
    """

    member_name: str


@dataclasses.dataclass
class Sequence:
    """
    Represents a datastruct sequence.

    Attributes:
        size (int | MemberRef): The size of the sequence. Defaults to 1.
        encoding (str): The encoding used for the sequence. Defaults to "ascii".
        enforce_length (bool): Whether to enforce the length of the sequence. Defaults to False.
        lazy (bool): Whether to lazily evaluate the sequence. Defaults to False.
    """

    size: int | MemberRef = 1
    encoding: str = "ascii"
    enforce_length: bool = False
    lazy: bool = False


@dataclasses.dataclass(frozen=True)
class Member:
    """
    Represents a datastruct member.

    Attributes:
        type (typing.Any | NativeType): The type of the member.
        sequence (typing.Optional[Sequence]): The sequence type of the member, if provided.
        default (typing.Optional[typing.Any]): The default value of the member, if provided.
    """

    type: typing.Any | NativeType = None
    sequence: typing.Optional[Sequence] = None
    default: typing.Optional[typing.Any] = None


def _lazy_loader(
    cls, ntype: NativeType, stream: io.IOBase, size: int
) -> typing.Generator[typing.Any, None, None]:
    for i in range(size):
        yield ntype.read(stream, _byteorder_map[cls.byteorder])


class DataStruct(type):
    """
    Metaclass for defining datastructs.

    This metaclass provides functionality for reading data from a binary stream and constructing an instance of the datastruct.
    It also provides a method for initializing an empty instance of said datastruct.

    Attributes:
        on_read (typing.Callable[[], None] | None): A callback function to be called after reading data from a binary stream.
        on_write (typing.Callable[[type, bytearray], None] | None): A callback function to be called after all data has been serialized it takes in one parameter, a bytearray, containing the serialized data..
        meta (StructMeta | None): The metadata that describes the structure of the data.
        byteorder (str | None): Specifies the byte order of the data.
        size (int | None): Specifies the size of the data in bytes.
        serialize (typing.Callable[[], bytearray] | None): A function for serializing the data. It is added later to the class, as an instance method of the datastruct.

    Methods:
        read(cls, stream: typing.BinaryIO) -> Any: Reads data from a binary stream and constructs an instance of the class.
        init_empty(cls) -> Any: Initializes an empty instance of the class.
    """

    def __new__(cls, *args, **kwargs):
        cls.on_read: typing.Callable[[], None] | None = None
        cls.on_write: typing.Callable[[bytearray], None] | None = None
        cls.meta: StructMeta | None = None
        cls.byteorder: str | None = None
        cls.size: int | None = None
        cls.serialize: typing.Callable[[], bytearray] | None = None

        return type.__new__(cls, *args, **kwargs)

    def read_sequence(
        cls, item: MetadataItem, copy_metadata: StructMeta, stream: typing.BinaryIO
    ):
        """
        Reads a sequence of values from a binary stream.

        Args:
            cls (type): The class object for the datastruct.
            item (MetadataItem): The metadata item representing the sequence.
            copy_metadata (StructMeta): A clone of the metadata for the datastruct.
            stream (typing.BinaryIO): The binary stream to read from.

        Returns:
            list | collections.abc.Sequence: The list of values read from the stream.

        Raises:
            InvalidTypeDef: If the sequence type is not specified.
            InvalidSequence: If the referred member is not found or if the size is not an integer.
        """
        seq = item.sequence

        # probably redundant
        if item.type is None:
            raise InvalidTypeDef("Must specify Sequence type.")

        if isinstance(seq.size, MemberRef):
            ref = seq.size

            # make sure the referred member already exists in the struct
            if ref.member_name not in copy_metadata:
                raise InvalidSequence(f"Failed to find member '{ref.member_name}'.")

            seq.size = copy_metadata[ref.member_name].value

            # ensure that the size is int based
            if not isinstance(seq.size, int):
                raise InvalidSequence(
                    f"Expected int based size for {item.name}, got {type(seq.size)} instead."
                )

        seq_type = item.type
        if not is_datastruct(seq_type):
            seq_type = seq_type(seq.encoding, seq.enforce_length)

        if seq.lazy:
            return _lazy_loader(cls, seq_type, stream, seq.size)

        values = []
        for i in range(seq.size):
            if is_datastruct(seq_type):
                values.append(cls.read_datastruct(item, stream))

                continue

            values.append(seq_type.read(stream, _byteorder_map[cls.byteorder]))

        # iterable check(NativeTypes char, bytestring)
        if not is_datastruct(seq_type) and seq_type.name in (
            "bytestring",
            "char",
        ):
            values = seq_type.python_type().join(values)

        if len(values) == 0:
            values = item.default

        return values

    def read_datastruct(cls, item: MetadataItem, stream: typing.BinaryIO):
        """
        Reads a datastruct from a binary stream.

        Args:
            item (MetadataItem): The metadata item representing the datastruct.
            stream (typing.BinaryIO): The binary stream to read from.

        Returns:
            The deserialized datastruct.

        Raises:
            Any exceptions that occur during the deserialization process.
        """
        struct_type: DataStruct = item.type
        copy_metadata = struct_type.meta.clone()

        for struct_item in copy_metadata:
            if struct_item.sequence is not None:
                struct_item.value = struct_type.read_sequence(
                    struct_item, copy_metadata, stream
                )

                continue

            if is_datastruct(struct_item.type):
                struct_item.value = struct_type.read_datastruct(struct_item, stream)

                continue

            struct_item.value = struct_item.type.read(
                stream, _byteorder_map[struct_type.byteorder]
            )[0]

            if struct_item.default is not None:
                if (
                    struct_item.type == NativeTypes.bytestring
                    or struct_item.type == NativeTypes.char
                ):
                    if len(struct_item.value) == 0:
                        struct_item.value = struct_item.default
                else:
                    if struct_item.value == 0:
                        struct_item.value = struct_item.default

        self = struct_type(**{p.name: p.value for p in copy_metadata})

        if struct_type.on_read is not None:
            struct_type.on_read(self)

        return self

    def read(cls, stream: typing.BinaryIO) -> typing.Any:
        """
        Reads data from a binary stream and constructs an instance of the class.

        Args:
            stream (typing.BinaryIO): The binary stream to read from.

        Returns:
            The constructed instance of the class.

        Raises:
            TypeError: If the stream is not a binary stream.
        """
        if not isinstance(stream, io.IOBase):
            raise TypeError("Expected a binary stream")

        copy_metadata: StructMeta = cls.meta.clone()

        for item in copy_metadata:
            if item.sequence is not None:
                item.value = cls.read_sequence(item, copy_metadata, stream)

                continue

            if is_datastruct(item.type):
                item.value = cls.read_datastruct(item, stream)

                continue

            item.value = item.type.read(stream, _byteorder_map[cls.byteorder])[0]

            if item.default is not None:
                if item.type == NativeTypes.bytestring or item.type == NativeTypes.char:
                    if len(item.value) == 0:
                        item.value = item.default
                else:
                    if item.value == 0:
                        item.value = item.default

        self = cls(**{p.name: p.value for p in copy_metadata})

        if cls.on_read is not None:
            cls.on_read(self)

        return self

    def init_empty(cls) -> typing.Any:
        """
        Initializes an empty instance of the class.

        Returns:
            An empty instance of the class.
        """
        for item in cls.meta:
            if item.sequence is not None:
                seq = item.sequence

                if item.type.name == "bytestring":
                    item.value = b"\x00" * seq.size
                elif item.type.name == "char":
                    item.value = "\x00" * seq.size
                else:
                    item.value = [0] * seq.size

                continue

            item.value = None

        return cls(**{p.name: p.value for p in cls.meta})


def datastruct(
    cls: typing.Optional[type] = None, /, *, byteorder: str = "native"
) -> typing.Callable[..., type]:
    """
    Decorator function for creating dataclasses capable of parsing and serialization.

    Args:
        cls (type, optional): The class to decorate. If not provided, the decorator is returned.
        byteorder (str, optional): The byte order to use for serialization. Defaults to "native".

    Returns:
        Callable[..., type]: The decorated class or the decorator itself.

    Raises:
        InvalidByteOrder: If the provided byte order is invalid.
        InvalidTypeDef: If the type definition for a field is invalid.

    Example usage:
        @datastruct
        class MyStruct:
            field1: int
            field2: str
    """
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    def decorator(struct_cls):
        dataclass_cls = dataclasses.dataclass(struct_cls)

        dataclass_cls.byteorder = byteorder
        dataclass_cls.meta = StructMeta()

        for field in dataclasses.fields(dataclass_cls):
            if field.default != dataclasses.MISSING:
                raise InvalidMember(
                    "Use `typing.Annotated[type, cstructs.Member()]` to specify default values."
                )

            is_annotated = typing.get_origin(field.type) is typing.Annotated

            if (
                not isinstance(field.type, NativeType)
                and not is_datastruct(field.type)
                and not is_annotated
            ):
                raise InvalidTypeDef(
                    f"Invalid type definition for {field.name}: {field.type}"
                )

            if is_annotated:
                _, member = typing.get_args(field.type)

                if not isinstance(member, Member):
                    raise InvalidMember(
                        f"Expected a cstructs.Member, but got {type(member)} instead."
                    )

                item_name = field.name

                # is this member a sequence? if so, then size = member.type.size * seq.size
                if member.sequence is not None and isinstance(
                    member.sequence, Sequence
                ):
                    # metadataitem.size needs to be worked on in a future commit
                    if isinstance(member.sequence.size, MemberRef):
                        item_size = 0
                    else:
                        item_size = member.sequence.size
                else:
                    item_size = member.type.size

                item_typedef = member.type
                item_sequence = member.sequence
                item_default = member.default
            else:
                item_name = field.name
                item_size = field.type.size
                item_typedef = field.type
                item_sequence = None
                item_default = None

            dataclass_cls.meta.add_item(
                MetadataItem(
                    item_name, item_typedef, item_size, item_sequence, item_default
                )
            )

        def serializer(self) -> bytearray:
            buf = bytearray()

            for item in self.meta:
                if is_datastruct(item.type):
                    buf.extend(item.type.serialize())

                    continue

                if item.sequence is not None:
                    attr = getattr(self, item.name)

                    if item.sequence.enforce_length and len(attr) != item.sequence.size:
                        raise SequenceLengthMismatch()

                    for i in range(item.sequence.size):
                        if attr is None:
                            value = None
                        else:
                            if item.type.name == "bytestring":
                                value = attr[i].to_bytes(1, byteorder="big")
                            else:
                                value = attr[i]

                        buf.extend(
                            item.type.serialize(value, _byteorder_map[self.byteorder])
                        )

                    continue

                buf.extend(
                    item.type.serialize(
                        getattr(self, item.name), _byteorder_map[self.byteorder]
                    )
                )

            if self.__class__.on_write is not None:
                self.on_write(buf)

            return buf

        setattr(dataclass_cls, "serialize", serializer)

        dataclass_cls.size = sum([item.size for item in dataclass_cls.meta])
        dataclass_cls.__qualname__ = f"cstructs.datastruct.{dataclass_cls.__name__}"

        return dataclass_cls

    if cls is None:
        return decorator

    return decorator(cls)
