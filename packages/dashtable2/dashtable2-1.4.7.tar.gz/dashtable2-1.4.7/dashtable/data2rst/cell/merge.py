
from typing import Optional, Literal
from typing_extensions import TypeAlias

from .cell import Cell


MERGE_DIRECTION: TypeAlias = Optional[Literal["LEFT", "RIGHT", "BOTTOM", "TOP"]]


def _merge_border_strings(s1: str, s2: str) -> str:
    """
    merges takes first string with + replaces from second string

    >>> _merge_border_strings('+====+======+', '--+----------')
    '+=+==+======+'
    """
    assert len(s1) == len(s2)
    return ''.join(
        '+' if '+' in (v1, v2) else v1
        for v1, v2 in zip(s1, s2)
    )


def get_merge_direction(cell1: Cell, cell2: Cell) -> MERGE_DIRECTION:
    """
    Determine the side of cell1 that can be merged with cell2.

    This is based on the location of the two cells in the table as well
    as the compatibility of their height and width.

    For example these cells can merge::

         cell1    cell2      merge "RIGHT"

        +-----+  +------+   +-----+------+
        | foo |  | dog  |   | foo | dog  |
        |     |  +------+   |     +------+
        |     |  | cat  |   |     | cat  |
        |     |  +------+   |     +------+
        |     |  | bird |   |     | bird |
        +-----+  +------+   +-----+------+

    But these cells cannot merge::

        +-----+  +------+
        | foo |  | dog  |
        |     |  +------+
        |     |  | cat  |
        |     |  +------+
        |     |
        +-----+

    Parameters
    ----------
    cell1 : dashtable.data2rst.Cell
    cell2 : dashtable.data2rst.Cell

    Returns
    -------
        The side onto which cell2 can be merged
    """
    cell1_left = cell1.column
    cell1_right = cell1.column + cell1.column_count
    cell1_top = cell1.row
    cell1_bottom = cell1.row + cell1.row_count

    cell2_left = cell2.column
    cell2_right = cell2.column + cell2.column_count
    cell2_top = cell2.row
    cell2_bottom = cell2.row + cell2.row_count

    if (cell1_right == cell2_left and cell1_top == cell2_top and
            cell1_bottom == cell2_bottom and
            cell1.right_sections >= cell2.left_sections):
        return "RIGHT"

    elif (cell1_left == cell2_left and cell1_right == cell2_right and
            cell1_top == cell2_bottom and
            cell1.top_sections >= cell2.bottom_sections):
        return "TOP"

    elif (cell1_left == cell2_left and
          cell1_right == cell2_right and
          cell1_bottom == cell2_top and
          cell1.bottom_sections >= cell2.top_sections):
        return "BOTTOM"

    elif (cell1_left == cell2_right and
          cell1_top == cell2_top and
          cell1_bottom == cell2_bottom and
          cell1.left_sections >= cell2.right_sections):
        return "LEFT"

    return None


def merge_cells(cell1: Cell, cell2: Cell, direction: MERGE_DIRECTION):
    """
    Combine the side of cell1's grid text with cell2's text.

    For example::

         cell1    cell2      merge "RIGHT"

        +-----+  +------+   +-----+------+
        | foo |  | dog  |   | foo | dog  |
        |     |  +------+   |     +------+
        |     |  | cat  |   |     | cat  |
        |     |  +------+   |     +------+
        |     |  | bird |   |     | bird |
        +-----+  +------+   +-----+------+

    Parameters
    ----------
    cell1 : dashtable.data2rst.Cell
    cell2 : dashtable.data2rst.Cell
    direction :
    """

    cell1_lines = cell1.text.split("\n")
    cell2_lines = cell2.text.split("\n")

    if direction == "RIGHT":
        for i in range(len(cell1_lines)):
            cell1_lines[i] = cell1_lines[i] + cell2_lines[i][1:]
        cell1.text = "\n".join(cell1_lines)
        cell1.column_count += cell2.column_count

    elif direction == "TOP":

        new_lines = cell2_lines[:-1] + [
            _merge_border_strings(cell2_lines[-1], cell1_lines[0])
        ] + cell1_lines[1:]

        # if cell1_lines[0].count('+') > cell2_lines[-1].count('+'):
        #     cell2_lines.pop(-1)
        # else:
        #     cell1_lines.pop(0)
        # cell2_lines.extend(cell1_lines)

        cell1.text = "\n".join(new_lines)
        cell1.row_count += cell2.row_count
        cell1.row = cell2.row
        cell1.column = cell2.column

    elif direction == "BOTTOM":
        # if cell1.is_header or cell1_lines[-1].count('+') > cell2_lines[0].count('+'):
        #     cell2_lines.pop(0)
        # else:
        #     cell1_lines.pop(-1)
        # cell1_lines.extend(cell2_lines)

        new_lines = cell1_lines[:-1] + [
            _merge_border_strings(cell1_lines[-1], cell2_lines[0])
        ] + cell2_lines[1:]
        cell1.text = "\n".join(new_lines)
        cell1.row_count += cell2.row_count

    elif direction == "LEFT":
        for i in range(len(cell1_lines)):
            cell1_lines[i] = cell2_lines[i][:-1] + cell1_lines[i]
        cell1.text = "\n".join(cell1_lines)
        cell1.column_count += cell2.column_count
        cell1.row = cell2.row
        cell1.column = cell2.column



