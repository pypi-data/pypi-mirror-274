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
def is_datastruct(cls: type) -> bool:
    """
    Check if a class is a data structure defined in the cstructs.datastruct module.

    Args:
        cls (type): The class to check.

    Returns:
        bool: True if the class is a data structure, False otherwise.
    """
    return hasattr(cls, "__qualname__") and cls.__qualname__.startswith(
        "cstructs.datastruct."
    )
