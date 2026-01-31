"""
Helper functions
"""

import re
from typing import Tuple


class Helpers:
    """Helper functions"""
    
    CELL_REF_PATTERN = re.compile(r"^([A-Z]+)(\d+)$")
    RANGE_REF_PATTERN = re.compile(r"^([A-Z]+)(\d+):([A-Z]+)(\d+)$")
    
    @staticmethod
    def parse_cell_reference(ref: str) -> Tuple[int, int]:
        """Parse cell reference (e.g., 'A1') to (row, col)"""
        match = Helpers.CELL_REF_PATTERN.match(ref)
        if not match:
            raise ValueError(f"Invalid cell reference: {ref}")
        
        col_str, row_str = match.groups()
        
        col = 0
        for char in col_str:
            col = col * 26 + (ord(char.upper()) - ord('A') + 1)
        
        row = int(row_str)
        return (row, col)
    
    @staticmethod
    def cell_reference_to_tuple(ref: str) -> Tuple[int, int]:
        """Convert cell reference to (row, col) tuple"""
        return Helpers.parse_cell_reference(ref)
    
    @staticmethod
    def tuple_to_cell_reference(row: int, col: int) -> str:
        """Convert (row, col) tuple to cell reference (e.g., 'A1')"""
        col_str = ""
        temp = col
        while temp > 0:
            temp -= 1
            col_str = chr(65 + (temp % 26)) + col_str
            temp //= 26
        return f"{col_str}{row}"
    
    @staticmethod
    def parse_range_reference(ref: str) -> Tuple[int, int, int, int]:
        """Parse range reference (e.g., 'A1:B10') to (row1, col1, row2, col2)"""
        match = Helpers.RANGE_REF_PATTERN.match(ref)
        if not match:
            raise ValueError(f"Invalid range reference: {ref}")
        
        col1_str, row1_str, col2_str, row2_str = match.groups()
        
        col1 = 0
        for char in col1_str:
            col1 = col1 * 26 + (ord(char.upper()) - ord('A') + 1)
        
        col2 = 0
        for char in col2_str:
            col2 = col2 * 26 + (ord(char.upper()) - ord('A') + 1)
        
        row1 = int(row1_str)
        row2 = int(row2_str)
        
        return (row1, col1, row2, col2)
    
    @staticmethod
    def tuple_to_range_reference(row1: int, col1: int, row2: int, col2: int) -> str:
        """Convert (row1, col1, row2, col2) tuple to range reference"""
        ref1 = Helpers.tuple_to_cell_reference(row1, col1)
        ref2 = Helpers.tuple_to_cell_reference(row2, col2)
        return f"{ref1}:{ref2}"
    
    @staticmethod
    def get_column_letter(col: int) -> str:
        """Get column letter from column number (1-indexed)"""
        col_str = ""
        temp = col
        while temp > 0:
            temp -= 1
            col_str = chr(65 + (temp % 26)) + col_str
            temp //= 26
        return col_str
    
    @staticmethod
    def get_column_number(letter: str) -> int:
        """Get column number from column letter"""
        col = 0
        for char in letter:
            col = col * 26 + (ord(char.upper()) - ord('A') + 1)
        return col
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """Linear interpolation between a and b"""
        return a + (b - a) * t
    
    @staticmethod
    def is_valid_cell_reference(ref: str) -> bool:
        """Check if string is a valid cell reference"""
        return Helpers.CELL_REF_PATTERN.match(ref) is not None
    
    @staticmethod
    def is_valid_range_reference(ref: str) -> bool:
        """Check if string is a valid range reference"""
        return Helpers.RANGE_REF_PATTERN.match(ref) is not None
    
    @staticmethod
    def normalize_string(s: str) -> str:
        """Normalize string (trim and lowercase)"""
        return s.strip().lower()
    
    @staticmethod
    def safe_divide(a: float, b: float, default: float = 0.0) -> float:
        """Safe division with default value"""
        if b == 0:
            return default
        return a / b
    
    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number with specified decimals"""
        return f"{value:.{decimals}f}"
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix