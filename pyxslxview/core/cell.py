"""
Cell representation
"""

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .worksheet import Worksheet
    from .styles import CellStyle


@dataclass
class Cell:
    """Cell representation"""
    
    row: int
    col: int
    worksheet: "Worksheet"
    value: Optional[object] = None
    data_type: Optional[str] = None
    style: Optional[CellStyle] = None
    comment: Optional[str] = None
    hyperlink: Optional[str] = None
    formula: Optional[str] = None
    
    def __post_init__(self):
        if self.style is None:
            from .styles import CellStyle
            self.style = CellStyle()
        if self.data_type is None:
            self._infer_data_type()
    
    def _infer_data_type(self):
        """Infer data type from value"""
        if self.value is None:
            self.data_type = "blank"
        elif isinstance(self.value, bool):
            self.data_type = "boolean"
        elif isinstance(self.value, (int, float)):
            self.data_type = "number"
        elif isinstance(self.value, str):
            if self.value.startswith("="):
                self.data_type = "formula"
                self.formula = self.value
            else:
                self.data_type = "string"
        else:
            self.data_type = "string"
    
    @property
    def coordinate(self) -> str:
        """Get cell coordinate (e.g., 'A1')"""
        col_str = ""
        col = self.col
        while col > 0:
            col_str = chr(64 + (col % 26 if col % 26 != 0 else 26)) + col_str
            col = (col - 1) // 26
        return f"{col_str}{self.row}"
    
    def is_merged(self) -> bool:
        """Check if cell is part of merged range"""
        for merged_range in self.worksheet.merged_cells:
            if merged_range.contains(self.row, self.col):
                return True
        return False
    
    def is_merged_parent(self) -> bool:
        """Check if cell is the top-left of merged range"""
        for merged_range in self.worksheet.merged_cells:
            if (merged_range.min_row == self.row and 
                merged_range.min_col == self.col):
                return True
        return False
    
    def __str__(self) -> str:
        return f"{self.coordinate}: {self.value}"
    
    def __repr__(self) -> str:
        return (f"Cell(row={self.row}, col={self.col}, value={self.value}, "
                f"data_type='{self.data_type}', style={self.style})")