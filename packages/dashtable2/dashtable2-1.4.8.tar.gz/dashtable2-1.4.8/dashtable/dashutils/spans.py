def get_span(spans, row, column):
    """
    Gets the span containing the [row, column] pair

    Parameters
    ----------
    spans : list of lists of lists
        A list containing spans, which are lists of [row, column] pairs
        that define where a span is inside a table.

    Returns
    -------
    span : list of lists
        A span containing the [row, column] pair
    """
    for i in range(len(spans)):
        if [row, column] in spans[i]:
            return spans[i]

    return None


def get_longest_line_length(text):
    """Get the length longest line in a paragraph"""
    lines = text.split("\n")
    length = 0

    for i in range(len(lines)):
        if len(lines[i]) > length:
            length = len(lines[i])

    return length


def get_span_char_height(span, row_heights):
    """
    Get the height of a span in the number of newlines it fills.

    Parameters
    ----------
    span : list of list of int
        A list of [row, column] pairs that make up the span
    row_heights : list of int
        A list of the number of newlines for each row in the table

    Returns
    -------
    total_height : int
        The height of the span in number of newlines
    """
    start_row = span[0][0]
    row_count = get_span_row_count(span)
    total_height = 0

    for i in range(start_row, start_row + row_count):
        total_height += row_heights[i]
    total_height += row_count - 1

    return total_height


def get_span_char_width(span, column_widths):
    """
    Sum the widths of the columns that make up the span, plus the extra.

    Parameters
    ----------
    span : list of lists of int
        list of [row, column] pairs that make up the span
    column_widths : list of int
        The widths of the columns that make up the table

    Returns
    -------
    total_width : int
        The total width of the span
    """

    start_column = span[0][1]
    column_count = get_span_column_count(span)
    total_width = 0

    for i in range(start_column, start_column + column_count):
        total_width += column_widths[i]

    total_width += column_count - 1

    return total_width


def get_span_column_count(span):
    """
    Find the length of a colspan.

    Parameters
    ----------
    span : list of lists of int
        The [row, column] pairs that make up the span

    Returns
    -------
    columns : int
        The number of columns included in the span

    Example
    -------
    Consider this table::

        +------+------------------+
        | foo  | bar              |
        +------+--------+---------+
        | spam | goblet | berries |
        +------+--------+---------+

    ::

        >>> span = [[0, 1], [0, 2]]
        >>> print(get_span_column_count(span))
        2
    """
    columns = 1
    first_column = span[0][1]

    for i in range(len(span)):
        if span[i][1] > first_column:
            columns += 1
            first_column = span[i][1]

    return columns


def get_span_row_count(span):
    """
    Gets the number of rows included in a span

    Parameters
    ----------
    span : list of lists of int
        The [row, column] pairs that make up the span

    Returns
    -------
    rows : int
        The number of rows included in the span

    Example
    -------
    Consider this table::

        +--------+-----+
        | foo    | bar |
        +--------+     |
        | spam   |     |
        +--------+     |
        | goblet |     |
        +--------+-----+

    ::

        >>> span = [[0, 1], [1, 1], [2, 1]]
        >>> print(get_span_row_count(span))
        3
    """
    rows = 1
    first_row = span[0][0]

    for i in range(len(span)):
        if span[i][0] > first_row:
            rows += 1
            first_row = span[i][0]

    return rows
