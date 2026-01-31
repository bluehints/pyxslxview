"""
Paginator for page layout
"""

from dataclasses import dataclass
from typing import List
from ..core.worksheet import Worksheet
from ..layout.calculator import LayoutCalculator


@dataclass
class Page:
    """Page representation"""
    
    page_number: int
    row_start: int
    row_end: int
    col_start: int
    col_end: int
    x_offset: float = 0.0
    y_offset: float = 0.0
    width: float = 0.0
    height: float = 0.0
    
    @property
    def rows(self) -> int:
        """Get number of rows"""
        return self.row_end - self.row_start + 1
    
    @property
    def cols(self) -> int:
        """Get number of columns"""
        return self.col_end - self.col_start + 1


class Paginator:
    """Paginator for page layout"""
    
    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet
        self.page_setup = worksheet.page_setup
        self.page_margins = worksheet.page_margins
        self.calculator = LayoutCalculator(worksheet)
    
    def paginate(self) -> List[Page]:
        """Generate pages"""
        pages = []
        
        printable_width = self._get_printable_width()
        printable_height = self._get_printable_height()
        
        self.calculator.calculate_merged_cells()
        
        total_rows = self.worksheet.max_row
        total_cols = self.worksheet.max_col
        
        row_start = 1
        page_num = 1
        
        while row_start <= total_rows:
            rows_on_page = self._calculate_rows_on_page(row_start, printable_height)
            row_end = min(row_start + rows_on_page - 1, total_rows)
            
            col_start = 1
            while col_start <= total_cols:
                cols_on_page = self._calculate_cols_on_page(col_start, printable_width)
                col_end = min(col_start + cols_on_page - 1, total_cols)
                
                page = Page(
                    page_number=page_num,
                    row_start=row_start,
                    row_end=row_end,
                    col_start=col_start,
                    col_end=col_end,
                    width=self._get_page_width(col_start, col_end),
                    height=self._get_page_height(row_start, row_end),
                )
                
                pages.append(page)
                page_num += 1
                col_start = col_end + 1
            
            row_start = row_end + 1
        
        return pages
    
    def _get_printable_width(self) -> float:
        """Get printable width"""
        return (self.page_setup.paper_width - 
                self.page_margins.left - 
                self.page_margins.right)
    
    def _get_printable_height(self) -> float:
        """Get printable height"""
        return (self.page_setup.paper_height - 
                self.page_margins.top - 
                self.page_margins.bottom -
                self.page_margins.header -
                self.page_margins.footer)
    
    def _calculate_rows_on_page(self, start_row: int, max_height: float) -> int:
        """Calculate number of rows that fit on a page"""
        current_height = 0.0
        rows = 0
        
        for row in range(start_row, self.worksheet.max_row + 1):
            row_height = self.calculator.calculate_row_height(row)
            
            if current_height + row_height > max_height and rows > 0:
                break
            
            current_height += row_height
            rows += 1
        
        return max(1, rows)
    
    def _calculate_cols_on_page(self, start_col: int, max_width: float) -> int:
        """Calculate number of columns that fit on a page"""
        current_width = 0.0
        cols = 0
        
        for col in range(start_col, self.worksheet.max_col + 1):
            col_width = self.calculator.calculate_column_width(col)
            
            if current_width + col_width > max_width and cols > 0:
                break
            
            current_width += col_width
            cols += 1
        
        return max(1, cols)
    
    def _get_page_width(self, start_col: int, end_col: int) -> float:
        """Get page width"""
        width = 0.0
        for col in range(start_col, end_col + 1):
            width += self.calculator.calculate_column_width(col)
        return width
    
    def _get_page_height(self, start_row: int, end_row: int) -> float:
        """Get page height"""
        height = 0.0
        for row in range(start_row, end_row + 1):
            height += self.calculator.calculate_row_height(row)
        return height
    
    def get_page_for_cell(self, row: int, col: int, pages: List[Page]) -> Page:
        """Get page containing cell"""
        for page in pages:
            if (page.row_start <= row <= page.row_end and
                page.col_start <= col <= page.col_end):
                return page
        return None