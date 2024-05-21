
from typing import List, Any


def ensure_table_strings(table: List[List[Any]]):
    """
    Force each cell in the table to be a string

    Parameters
    ----------
    table : list of lists

    Returns
    -------
    table : list of lists of str
    """
    return [
        list(map(str, row)) for row in table
    ]

