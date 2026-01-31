"""
Document representation
"""

from dataclasses import dataclass, field
from typing import Optional
from .workbook import Workbook


@dataclass
class Document:
    """Document root object, managing the entire XLSX file"""
    
    filepath: Optional[str] = None
    workbook: Optional[Workbook] = None
    shared_strings: Optional[list] = field(default_factory=list)
    styles: Optional[dict] = field(default_factory=dict)
    theme: Optional[dict] = field(default_factory=dict)
    
    def load(self, filepath: str):
        """Load XLSX file"""
        from ..parser.xlsx_parser import XLSXParser
        
        self.filepath = filepath
        parser = XLSXParser(filepath)
        parsed_doc = parser.parse()
        
        self.workbook = parsed_doc.workbook
        self.shared_strings = parsed_doc.shared_strings
        self.styles = parsed_doc.styles
        self.theme = parsed_doc.theme
    
    def save(self, filepath: str):
        """Save document"""
        pass
    
    @property
    def worksheets(self):
        """Get all worksheets"""
        if self.workbook:
            return self.workbook.worksheets
        return []
    
    def __str__(self) -> str:
        if self.workbook:
            return f"Document('{self.filepath}', {len(self.workbook.worksheets)} worksheets)"
        return f"Document('{self.filepath}')"
    
    def __repr__(self) -> str:
        return (f"Document(filepath='{self.filepath}', workbook={self.workbook}, "
                f"shared_strings={len(self.shared_strings)}, styles={len(self.styles)})")