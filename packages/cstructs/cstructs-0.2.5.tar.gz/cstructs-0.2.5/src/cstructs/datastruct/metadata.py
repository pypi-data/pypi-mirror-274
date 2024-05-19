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
from __future__ import annotations

import enum
import copy
import typing

from dataclasses import dataclass
from cstructs.nativetypes import NativeType
from cstructs.util import is_datastruct

from collections.abc import Iterator

if typing.TYPE_CHECKING:
    from cstructs.datastruct import Sequence, DataStruct


@dataclass
class MetadataItem:

    name: str
    type: NativeType | DataStruct
    size: int
    sequence: typing.Optional[Sequence]

    # these fields are set later on
    default: typing.Optional[typing.Any] = None
    offset: int = None
    value: typing.Any | list | typing.Generator = None

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        """
        Returns a string representation of the Metadata object.

        The string representation includes the type name, size in bytes, and the value of the Metadata object.
        If the value is a data structure, it is displayed with proper indentation and a horizontal line separating each line.
        If the value is an enum, it is displayed using its representation.

        Returns:
            str: A string representation of the Metadata object.
        """
        value_str = f"{self.value}"

        if is_datastruct(self.value.__class__):
            value_str = "\n" + str(self.value)
            value_str += "\n" + "-" * max(
                map(lambda s: len(s) - 1, value_str.split("\n"))
            )

        if isinstance(self.value, enum.Enum):
            value_str = repr(self.value)

        return f"{self.type.name} ({self.size} bytes) = {value_str}"


class StructMeta:
    """
    Represents the metadata for a datastruct.

    This class provides methods to add metadata items, iterate over the attributes,
    retrieve values associated with items, and get string representations of the datastruct.
    """

    def add_item(self, item: MetadataItem):
        """
        Adds a MetadataItem to the Metadata object.

        Args:
            item (MetadataItem): The MetadataItem to be added.

        Returns:
            None
        """
        setattr(self, item.name, item)

    def clone(self) -> typing.Self:
        """
        Creates a deep copy of the current instance.

        Returns:
            A new instance of the same type as the current instance, with all items deeply copied.
        """
        copy_metadata: StructMeta = type(self)()

        for item in self:
            copy_metadata.add_item(copy.deepcopy(item))

        return copy_metadata

    def __contains__(self, item):
        return hasattr(self, item)

    def __iter__(self) -> Iterator[MetadataItem]:
        """
        Iterates over the attributes of the object and yields their values.

        Yields:
            Any: The value of each non-callable attribute of the object.
        """
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                yield getattr(self, attr)

    def __getitem__(self, item) -> MetadataItem:
        """
        Retrieve the value associated with the given item.

        If the item is a string, it is assumed to be the name of an attribute
        and the corresponding value is returned. If the item is an integer,
        it is treated as an index and the value at that index in the internal
        dictionary is returned.

        Args:
            item: The item to retrieve the value for.

        Returns:
            The value associated with the given item.

        Raises:
            IndexError: If the item is an integer and it is out of range.
        """
        return (
            getattr(self, item)
            if isinstance(item, str)
            else [*self.__dict__.values()][item]
        )

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        """
        Returns a string representation of the datastruct.

        The string representation includes all the attributes of the
        datastruct in the format 'attribute_name: attribute_value'.

        Returns:
            str: A string representation of the datastruct.
        """
        return "\n".join([f"{key}: {value}" for key, value in self.__dict__.items()])
