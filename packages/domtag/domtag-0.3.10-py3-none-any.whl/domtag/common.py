"""Common scripts"""

from io import BytesIO
from pathlib import Path
from typing import Optional, Union, Callable, BinaryIO

import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet


def adjust_column_width_openpyxl(
        worksheet: Worksheet,
        min_width: int = 15,
        max_width: Optional[int] = 50,
        fixed_width: Optional[int] = None,
) -> None:
    """Adjust column width to fit the content, for a given Excel sheet

    :param worksheet: openpyxl worksheet
    :param min_width: Minimum width of a column, if it is empty
    :param max_width: The maximum width of a column
    :param fixed_width: If this value is provided,
        it will apply to all the columns
    :return: Does not return anything, changes the worksheet inplace
    """
    column_widths = []
    for row in worksheet.values:
        for i, cell in enumerate(row):
            cell_len = min_width
            if len(column_widths) > i:
                if cell is not None and cell != '':
                    cell_len = len(str(cell))
                if cell_len > column_widths[i]:
                    column_widths[i] = cell_len
            else:
                column_widths += [cell_len]
    for i, column_width in enumerate(column_widths, 1):
        width = column_width
        if fixed_width is not None:
            width = fixed_width
        if max_width is not None:
            width = min(width, max_width)
        worksheet.column_dimensions[
            get_column_letter(i)].width = width


def save_to_excel_sheets_output(dfs: dict[str, pd.DataFrame],
                                path: Optional[Union[str, Path]] = None,
                                styling_func: Optional[Callable] = None,
                                styling_func_axis: int = 1,
                                ) -> BinaryIO:
    """Save dictionary of dataframes into an Excel file where each sheet name
    is the corresponding key of the dictionary

    :param dfs: Dictionary, where keys are sheet names and values are DFs
    :param path: String to output path or Path object
    :param styling_func: Optional function for styling the Excel sheets
    :param styling_func_axis: Axis along which the styling is applied
    :return:
    """
    if path is None:
        path = BytesIO()
    elif isinstance(path, str):
        path = Path(path)
    elif not isinstance(path, Path):
        raise TypeError(f"Expected string or Path object, got {type(path)}")
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for sheet_name, df in dfs.items():
            if styling_func:
                df.style.apply(
                    styling_func,
                    axis=styling_func_axis).to_excel(excel_writer=writer,
                                                     sheet_name=sheet_name)
            else:
                df.to_excel(excel_writer=writer, sheet_name=sheet_name)
            sheet = writer.sheets[sheet_name]
            adjust_column_width_openpyxl(sheet)
        writer.save()
    return path
