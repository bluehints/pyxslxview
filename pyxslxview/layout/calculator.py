"""
Layout calculator
"""

from typing import Tuple, Dict
from ..core.cell import Cell
from ..core.worksheet import Worksheet
from .measurer import Measurer


class LayoutCalculator:
    """Layout calculator"""
    
    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet
        self.measurer = Measurer()
        self._cell_sizes: Dict[Tuple[int, int], Tuple[float, float]] = {}
        self._column_widths: Dict[int, float] = {}
        self._row_heights: Dict[int, float] = {}
    
    def calculate_cell_size(self, cell: Cell) -> Tuple[float, float]:
        """Calculate cell size"""
        if (cell.row, cell.col) not in self._cell_sizes:
            self._cell_sizes[(cell.row, cell.col)] = self.measurer.measure_cell(cell)
        return self._cell_sizes[(cell.row, cell.col)]
    
    def calculate_column_width(self, col: int) -> float:
        """Calculate column width"""
        if col not in self._column_widths:
            max_width = 0.0
            
            for (row, c), cell in self.worksheet.cells.items():
                if c == col:
                    width, _ = self.calculate_cell_size(cell)
                    max_width = max(max_width, width)
            
            col_obj = self.worksheet.columns.get(col)
            if col_obj and col_obj.width > 0:
                max_width = max(max_width, col_obj.width * 7.5)
            
            self._column_widths[col] = max(max_width, 64.0)
        
        return self._column_widths[col]
    
    def calculate_row_height(self, row: int) -> float:
        """Calculate row height"""
        if row not in self._row_heights:
            max_height = 0.0
            
            for (r, col), cell in self.worksheet.cells.items():
                if r == row:
                    _, height = self.calculate_cell_size(cell)
                    max_height = max(max_height, height)
            
            row_obj = self.worksheet.rows.get(row)
            if row_obj and row_obj.height > 0:
                max_height = max(max_height, row_obj.height)
            
            self._row_heights[row] = max(max_height, 20.0)
        
        return self._row_heights[row]
    
    def calculate_merged_cells(self):
        """Calculate merged cell layout"""
        for merged_range in self.worksheet.merged_cells:
            max_width = 0.0
            max_height = 0.0
            
            for row in range(merged_range.min_row, merged_range.max_row + 1):
                height = self.calculate_row_height(row)
                max_height += height
            
            for col in range(merged_range.min_col, merged_range.max_col + 1):
                width = self.calculate_column_width(col)
                max_width += width
            
            merged_range.width = max_width
            merged_range.height = max_height
    
    def calculate_worksheet_size(self) -> Tuple[float, float]:
        """Calculate total worksheet size"""
        total_width = 0.0
        total_height = 0.0
        
        for col in range(1, self.worksheet.max_col + 1):
            total_width += self.calculate_column_width(col)
        
        for row in range(1, self.worksheet.max_row + 1):
            total_height += self.calculate_row_height(row)
        
        return (total_width, total_height)
    
    def get_cell_position(self, row: int, col: int) -> Tuple[float, float]:
        """Get cell position (x, y)"""
        x = 0.0
        for c in range(1, col):
            x += self.calculate_column_width(c)
        
        y = 0.0
        for r in range(1, row):
            y += self.calculate_row_height(r)
        
        return (x, y)
    
    def get_cell_rect(self, row: int, col: int):
        """Get cell rectangle"""
        x, y = self.get_cell_position(row, col)
        width = self.calculate_column_width(col)
        height = self.calculate_row_height(row)
        
        from ..graphics.canvas import Rectangle
        return Rectangle(x, y, width, height)
    
    def clear_cache(self):
        """Clear calculation cache"""
        self._cell_sizes.clear()
        self._column_widths.clear()
        self._row_heights.clear()