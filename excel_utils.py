"""
=========================================================
Excel Utilities
Project : BOM Automation Tool
Author  : Banumathi
=========================================================
"""

from openpyxl import load_workbook
from openpyxl.styles import Font


def load_excel(file_path):
    """Load an Excel workbook."""
    return load_workbook(file_path)


def save_excel(workbook, file_path):
    """Save an Excel workbook."""
    workbook.save(file_path)


def find_header_column(sheet, header_name, header_row=8):
    """Find a header column by name."""

    for cell in sheet[header_row]:
        if str(cell.value).strip() == header_name:
            return cell.column

    return None


def format_header(sheet, header_row=1):
    """Make header row bold."""

    for cell in sheet[header_row]:
        cell.font = Font(bold=True)


def auto_fit_columns(sheet):
    """Auto-adjust column widths."""

    for column_cells in sheet.columns:

        length = 0
        column = column_cells[0].column_letter

        for cell in column_cells:

            try:
                if len(str(cell.value)) > length:
                    length = len(str(cell.value))
            except:
                pass

        sheet.column_dimensions[column].width = length + 2