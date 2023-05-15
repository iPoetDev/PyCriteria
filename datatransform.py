#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: E501

"""Module DataTranform: Manipulating the data from the sheet.

@2023-05-05
1) Fetching subsets with filters for matching rows
2) Fetching subsets with filters for unique columns values: Search by column
3) Select a range of data.
"""
import re
# 0.1: Standard Library Imports
from typing import NoReturn

import gspread  # type: ignore
# 0.2 Third Party Modules
from rich import print as rprint  # type: ignore

# 0.3: Custom/Own Modules
import connections

# Google Sheet Connection: Global Object
connector: connections.GoogleConnector = connections.GoogleConnector()


class DataTransform:
    """Class DataTransform: Manipulating the data from the sheet.
    
    @2023-05-05
    Property
    --------
    :property wsheet: gspread.Worksheet: The worksheet to extract the data from.
    

    Methods:
    --------
    :method __init__: Constructor.
    :method column_uniques: Extracts the unique values from a column in a sheet.
    :method get_data: Select a subset of data from the worksheet.
    :method get_datamax: Selects a subset of data from the worksheet.
    :method fetch_a_row: Fetches a row from the worksheet.
    :method fetch_by_status: Fetches rows from the worksheet that match the given criteria group.
    :method fetch_by_reference: Fetches rows that match the given criteria group.
    :method fetch_by_lo: Fetches rows that match the given learning outcome (lo).
    :method fetch_by_grade: Fetches rows that match the given performance grade level.
    :method fetch_by_position: Fetches rows that match a given row position.
    :method fetch_a_column: Fetches rowsthat matches the given column range/dimension.
    :method fetch_a_range: Fetches rows from the worksheet that matches a given range (start, end).
    :method read_data: Reads the data by a given row.
    """
    
    wsheet: gspread.Worksheet
    a1pattern: str
    
    def __init__(self):
        """Constructor."""
        self.wsheet: gspread.Worksheet
        self.a1pattern: str = '\\d+(\\.\\d+){0,2}'
    
    @staticmethod
    def column_uniques(wsheet: gspread.Worksheet,
                       column_header: str,
                       row_headings: int = 1,
                       step: int = 1) -> list[str]:
        """@2023-05-05 - Used to filter the topics from a column in a sheet.
        
        Extracts the unique values from a column in a sheet.
        :param wsheet: Gspread.Worksheet: The worksheet to extract the data from.
        :param column_header: str: The column header to extract the data from.
        :param row_headings: int: The row number of the column header.
        :param step: int: The number of columns to step over to get to the column of data.
        :return: list[str]: A list of unique values from the given column.
        """
        # Get the index of the Criteria Topics column
        header_row = wsheet.row_values(row_headings)
        # Zero-indexed column index PLUS step
        column_index = header_row.index(column_header) + step
        # Get the last row of the sheet
        latest_row = len(wsheet.get_all_values())
        # Extract the column of topics from the data set
        # The slice [row_headings:latest_row]: extracts row values only by
        # specified row_headings to latest_row.
        colvalues = wsheet.col_values(column_index)[row_headings:latest_row]
        # Split compound values by semicolon and build a unique set of topics
        # PyLint: Consideration of using an inline comprehension (i.e. a set;
        # and split the values by semicolon
        # https://peps.python.org/pep-0709/
        # https://sparkbyexamples.com/python/python-set-comprehension/
        unique_values = {uniquevalue for value
                         in colvalues for uniquevalue
                         in value.split(';') if uniquevalue}
        # Return the unique values list[str]
        return list(unique_values)
    
    @staticmethod
    def get_data(wsheet: gspread.Worksheet, filterd: str = 'H1:01') -> list[str]:
        """@2023-05-05.
        
        Selects a subset of data from the worksheet using an A1 range filter.
        Relies on the columns to be in the string A1 notion for the filter
        Relies on the columns to be immutable in ordering
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param filterd: str: The filter to apply to the data.
        A1 notation for the filter.
        :return: list[str]: The filtered data.
        """
        dataset: list[str] = wsheet.get_values(filterd)
        return dataset
    
    @staticmethod
    def get_datamax(wsheet: gspread.Worksheet, filterd: str = "H1:01") -> list[str]:
        """@2023-05-05 Get the latest row id/count and do something.
        
        Selects a subset of data from the worksheet.
        Relies on the columns to be in the string A1 notion for the filter
        Relies on the columns to be immutable in ordering
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param filterd: str: The filter to apply to the data.
        A1 notation for the filter.
        :return: List[str]: The filtered data.
        """
        dataset = wsheet.get_values(filterd)
        len(wsheet.get_values())  # pylint: disable=unused-variable
        rprint(dataset)
        return dataset
    
    @staticmethod
    def fetch_a_row(wsheet: gspread.Worksheet, row: int) -> list[str]:
        """@2023-05-05 Fetches a row from the worksheet.
        
        Uses the implicit zero-based index.
        
        :alias: fetch_by_position
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param row: int: The row number to extract the data from.
        :return: list[str]: The row values.
        """
        return wsheet.row_values(row)
    
    @staticmethod
    def fetch_by_status(wsheet: gspread.Worksheet,
                        todoflag: int,
                        column_filter: int = 12) -> list[str]:
        """Fetches rows from the worksheet to match a given todo status.
        
        @2023-05-05
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param todoflag: int: The todo status to extract the data from.
        :param column_filter: int: The column number to filter the data from.
        :return: list[str]: List of matching rows.
        """
        all_rows = wsheet.get_all_values()
        return [row for row in all_rows if row[column_filter] == todoflag]
    
    @staticmethod
    def fetch_by_reference(wsheet: gspread.Worksheet,
                           reference: str,
                           column_filter: int = 10) -> list[str] | NoReturn:
        """@2023-05-05 Match the given criteria group, fetch the row.
        
        Parameters:
        -----------
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param reference: str: The reference to extract the data from.
        :param column_filter: int: The column number to filter the data from.
        :return: list[str] | NoReturn: List of matching rows or nothing.
        """
        all_rows = wsheet.get_all_values()
        try:
            if not re.match(r'\\d+(\\.\\d+){0,2}', reference):
                raise ValueError('Invalid reference')
        except ValueError as err:
            rprint(f'[red]Error: {err}[/red]')
            return NoReturn
        
        return [row for row in all_rows if row[column_filter] == reference]
    
    @staticmethod
    def fetch_by_lo(wsheet: gspread.Worksheet,
                    criteria_group: str,
                    column_filter: int = 7) -> list[str]:
        """@2023-05-05.
        
        Fetches rows from the worksheet that match the given criteria group.
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param criteria_group: str: The criteria group to extract the data from.
        :param column_filter: int: The column number to filter the data from.
        :return: list[str]: list of matching rows.
        """
        all_rows = wsheet.get_all_values()
        return [row for row in all_rows if row[column_filter] == criteria_group]
    
    @staticmethod
    def fetch_by_grade(wsheet: gspread.Worksheet,
                       performance: str,
                       column_filter: int = 6) -> list[str]:
        """@2023-05-05.
        
        Fetches rows from the worksheet that match the given grade type.
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param performance: str: The performance to extract the data from: Pass, Merit, Distinction.
        :param column_filter: int: The column number to filter the data from.
        :return: list[str]: list of matching rows.
        """
        all_rows = wsheet.get_all_values()
        return [row for row in all_rows if row[column_filter] == performance]
    
    @staticmethod
    def fetch_by_position(wsheet: gspread.Worksheet,
                          posindex: int,
                          column_filter: int = 1) -> list[str]:
        """@2023-05-05
        Fetches rows from the worksheet that match the given criteria group.
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param posindex: int: The positional id to extract the data from.
        :param column_filter: int: The column number to filter the data from.
        :return: list[str]: list of matching rows.
        """
        all_rows = wsheet.get_all_values()
        return [row for row in all_rows if row[column_filter] == str(posindex)]
    
    @staticmethod
    def fetch_a_column(wsheet: gspread.Worksheet,
                       column: int) -> list[str]:
        """@2023-05-05
        Fetches a column from the worksheet.
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param column: int: The column number to extract the data from.
        :return: list[str]: list of matching rows.
        """
        return wsheet.col_values(column)
    
    @staticmethod
    def fetch_a_range(wsheet: gspread.Worksheet,
                      start: int, end: int) -> list[str]:
        """@ 2023-05-05
        Fetches a range from the worksheet.
        :param wsheet: gspread.Worksheet: The worksheet to extract the data from.
        :param start: int: The start of the range.
        :param end: int: The end of the range.
        :return: list[str]: list of matching rows.
        """
        return wsheet.get(start, end)
    
    # pylint: disable=unnecessary-pass
    @staticmethod
    def read_data(row: list[str]):
        """Reads the data per row."""
        pass


class QueryFinder:
    def __init__(self, locationquery, dataset):
        self.sheet_name = locationquery.split('!')[0] if '!' in locationquery else None
        self.query = locationquery.split('!')[-1]
        self.dataset = dataset
        self.max_row = len(dataset.get('values', []))
        self.max_col = max([len(row) for row in dataset['values']]) if dataset.get('values') else 0
        self.header_row = 0
        
        if self.max_row > 0 and all(isinstance(cell, str) for cell in dataset['values'][0]):
            self.header_row = 1
    
    def find_cell(self, cell) -> str | None:
        if cell[0].isalpha() and cell[1:].isdigit():
            col = ord(cell[0].lower()) - 97
            row = int(cell[1:]) - 1
            if col < self.max_col and row < self.max_row:
                return self.dataset['values'][row][col]
        return None
    
    def find_range(self, start_cell, end_cell) -> list[str] | None:
        start_col = ord(start_cell[0].lower()) - 97
        start_row = int(start_cell[1:]) - 1
        end_col = ord(end_cell[0].lower()) - 97
        end_row = int(end_cell[1:]) - 1
        if start_col < self.max_col and start_row < self.max_row and end_col < self.max_col and end_row < self.max_row:
            return [[self.dataset['values'][i][j] for j in range(start_col, end_col + 1)] for i in
                    range(start_row, end_row + 1)]
        return None
    
    def find_column(self, column) -> list[str] | None:
        col = ord(column.lower()) - 97
        if col < self.max_col:
            if self.header_row == 1:
                return [self.dataset['values'][i][col] for i in range(self.header_row, self.max_row)]
            else:
                return [self.dataset['values'][i][col] for i in range(self.max_row)]
        return None
    
    def find_row(self, row) -> list[str] | None:
        row = int(row) - 1
        if row < self.max_row:
            if self.header_row == 1:
                return self.dataset['values'][row]
            else:
                return self.dataset['values'][row + 1]
        return None
    
    def get_query(self) -> str | list[str] | None:
        if ':' in self.query:
            cells = self.query.split(':')
            if len(cells) == 1:
                return self.find_cell(cells[0])
            else:
                start, end = cells
                if len(start) == 1 and len(end) == 1:
                    return self.find_column(start)
                elif len(start) > 1 and len(end) == 1:
                    return self.find_row(start)
                elif len(start) == 1 and len(end) > 1:
                    return self.find_column(start)
                else:
                    return self.find_range(start, end)
        else:
            return self.find_cell(self.query)


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Filter:
    """Class Filter: Providin filter for data."""
    named_range: str
    start_reference: str
    end_reference: str
    start_row: str
    end_row: str
    start_column: str
    end_column: str
    start_int: int
    end_int: int
    pattern: str
    
    def __init__(self, filterd: str) -> None:
        """Constructor.
        Take a filter in A1 notation and convert it to a named range, and attributes.
        :param filterd: str: The filter to apply to the data.
        :raises ValueError: If the filter is not in A1 notation.
        """
        pattern = r'^[A-Z]\\d+:[A-Z]\\d+$'
        valuemessage: str = ('Invalid filter format.\n'
                             + 'The format should be in A1 notation, '
                             + 'e.g. A1:B1.\n')
        valuemessage += f'The filter provided was: {filterd} \n'
        valuemessage += f'The pattern was: {pattern}\n'
        try:
            if not re.findall(pattern, filterd):
                raise ValueError(valuemessage)
        except ValueError as err:
            print(err)
        else:
            self.named_range = filterd
            self.start_reference = filterd.split(':')[0]
            self.end_reference = filterd.split(':')[1]
            self.start_column = self.start_reference[0]
            self.end_column = self.end_reference[0]
            self.start_row = self.start_reference[1]
            self.end_row = self.end_reference[1]
            self.start_int = int(self.start_row)
            self.end_int = int(self.end_row)
            self.pattern = '^([1-9]|[1-9]\\d|100)$'
    
    def update_endint(self, end_int: int):
        """Updates the end_int attribute."""
        self.end_int = end_int
    
    def update_endrow(self, maxrow: str):
        """Updates the end_row property, when tested for str and for numbers only pattern
        :param maxrow: str: The end row of the filter.
        :raises TypeError: If the maxrow is not a string, from 1-100.
        """
        if isinstance(maxrow, str) and re.match(self.pattern, maxrow):
            self.end_reference = f"{self.end_column}{maxrow}"
        else:
            raise TypeError(f'maxrow: {maxrow} '
                            f'must be a string containing only '
                            f'numbers from 1 to 100')
    
    def update_endreference(self, maxrow: str):
        """@2023-05-05
        Updates the end_reference property, when tested for str and for numbers only pattern
        :param maxrow: str: The end row of the filter.
        :raises TypeError: If the maxrow is not a string, from 1-100.
        """
        if isinstance(maxrow, str) and re.match(self.pattern, maxrow):
            self.end_reference = f'{self.end_column}{maxrow}'
        else:
            raise TypeError(f'maxrow: {maxrow}  '
                            f'must be a string containing only'
                            f'numbers from 1 to 100')
