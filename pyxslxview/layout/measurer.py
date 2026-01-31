"""
Measurer for layout calculations
"""

from typing import Tuple
from ..core.cell import Cell
from ..core.font import Font
from ..graphics.font import FontManager


class Measurer:
    """Measurer for layout calculations"""
    
    def __init__(self):
        self.font_manager = FontManager()
        self.indent_width = 7.5
    
    def measure_content(self, cell: Cell) -> Tuple[float, float]:
        """Measure content dimensions"""
        if not cell.value or cell.data_type == "blank":
            return (0.0, 0.0)
        
        font = cell.style.font
        text = str(cell.value)
        
        text_width, text_height = self.font_manager.measure_text(font, text)
        
        if cell.style.alignment.wrap_text:
            max_width = self._get_max_cell_width(cell)
            lines = self._wrap_text(text, max_width, font)
            text_width = max_width
            text_height = len(lines) * text_height * 1.2
        
        return (text_width, text_height)
    
    def measure_cell(self, cell: Cell) -> Tuple[float, float]:
        """Measure cell dimensions including padding"""
        content_width, content_height = self.measure_content(cell)
        
        indent = cell.style.alignment.indent
        padding = indent * self.indent_width
        
        width = content_width + padding * 2
        height = content_height
        
        row = cell.worksheet.rows.get(cell.row)
        col = cell.worksheet.columns.get(cell.col)
        
        if row:
            height = max(height, row.height)
        if col:
            width = max(width, col.width)
        
        return (width, height)
    
    def measure_text(self, font: Font, text: str) -> Tuple[float, float]:
        """Measure text dimensions"""
        return self.font_manager.measure_text(font, text)
    
    def _get_max_cell_width(self, cell: Cell) -> float:
        """Get maximum cell width"""
        col = cell.worksheet.columns.get(cell.col)
        if col:
            return col.width * 7.5
        return 100.0
    
    def _wrap_text(self, text: str, max_width: float, font: Font) -> list:
        """Wrap text to fit within max width"""
        lines = []
        words = text.split()
        
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width, _ = self.font_manager.measure_text(font, test_line)
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines