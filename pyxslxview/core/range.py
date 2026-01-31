"""
Cell range representation
"""

from dataclasses import dataclass
from typing import Iterator, Tuple


@dataclass
class Range:
    """Cell range representation"""
    
    min_row: int
    max_row: int
    min_col: int
    max_col: int
    worksheet = None
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get range size (rows, cols)"""
        return (self.max_row - self.min_row + 1, self.max_col - self.min_col + 1)
    
    @property
    def rows(self) -> int:
        """Get number of rows"""
        return self.max_row - self.min_row + 1
    
    @property
    def cols(self) -> int:
        """Get number of columns"""
        return self.max_col - self.min_col + 1
    
    def contains(self, row: int, col: int) -> bool:
        """Check if cell is in range"""
        return (self.min_row <= row <= self.max_row and 
                self.min_col <= col <= self.max_col)
    
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        """Iterate over cell coordinates"""
        for row in range(self.min_row, self.max_row + 1):
            for col in range(self.min_col, self.max_col + 1):
                yield (row, col)
    
    def __str__(self) -> str:
        def col_to_letter(c):
            return "" if c == 0 else chr(64 + c) + col_to_letter((c - 1) // 26)
        return f"{col_to_letter(self.min_col)}{self.min_row}:{col_to_letter(self.max_col)}{self.max_row}"
    
    def __repr__(self) -> str:
        return f"Range(min_row={self.min_row}, max_row={self.max_row}, min_col={self.min_col}, max_col={self.max_col})"