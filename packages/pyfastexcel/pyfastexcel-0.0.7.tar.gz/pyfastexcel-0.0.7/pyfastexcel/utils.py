from __future__ import annotations

import re
import string
from typing import Any, Literal

from openpyxl_style_writer import CustomStyle


def set_custom_style(style_name: str, style: CustomStyle) -> None:
    from .driver import ExcelDriver

    ExcelDriver.set_custom_style(style_name, style)


def validate_and_register_style(style: CustomStyle) -> None:
    from .driver import ExcelDriver

    if not isinstance(style, CustomStyle):
        raise TypeError(
            f'Invalid type ({type(style)}). Style should be a CustomStyle object.',
        )
    set_custom_style(f'Custom Style {ExcelDriver._STYLE_ID}', style)
    ExcelDriver._STYLE_ID += 1


def validate_and_format_value(
    value: Any,
    set_default_style: bool = True,
) -> tuple[Any, Literal['DEFAULT_STYLE']] | Any:
    # Convert non-numeric value to string
    value = f'{value}' if not isinstance(value, (int, float, str)) else value
    # msgpec does not support np.float64, so we should convert
    # it to python float.
    value = float(value) if isinstance(value, float) else value

    return (value, 'DEFAULT_STYLE') if set_default_style else value


def separate_alpha_numeric(input_string: str):
    alpha_part = re.findall(r'[a-zA-Z]+', input_string)
    num_part = re.findall(r'[0-9]+', input_string)
    return alpha_part[0], num_part[0]


def _is_valid_column(column: str) -> bool:
    column = column.upper()
    index = 0
    for c in column:
        index = index * 26 + (ord(c) - ord('A')) + 1
    return 1 <= index <= 16384


def column_to_index(column: str) -> int:
    if not isinstance(column, str):
        raise TypeError(f'Invalid type ({type(column)}). Column should be a string.')
    if len(column) > 3:
        raise ValueError(f"Invalid column ({column}). Maximum Column is 'XFD'.")
    if not all(c in string.ascii_uppercase for c in column):
        raise ValueError(f'Invalid column ({column}). Column should be in uppercase.')
    if not _is_valid_column(column):
        raise ValueError(f"Invalid column ({column}). Maximum Column is 'XFD'.")
    column = column.upper()
    index = 0
    for c in column:
        index = index * 26 + (ord(c) - ord('A')) + 1
    return index


def index_to_column(index: int) -> str:
    if not isinstance(index, int):
        raise TypeError(f'Invalid type ({type(index)}). Index should be a string.')
    if index < 1 or index > 16384:
        raise ValueError(f'Invalid index ({index}). Index should less and equal to 16384.')
    name = ''
    while index > 0:
        index, r = divmod(index - 1, 26)
        name = chr(r + ord('A')) + name
    return name


def excel_index_to_list_index(index: str) -> tuple[int, int]:
    alpha, num = separate_alpha_numeric(index)
    column = column_to_index(alpha)
    row = int(num)
    return row - 1, column - 1


def extract_numeric_part(cell_location: str) -> str | None:
    numeric_part = re.search(r'\d+', cell_location)
    if numeric_part:
        return numeric_part.group()
