"""
Cell styles
"""

from dataclasses import dataclass, field
from .font import Font
from .alignment import Alignment
from .border import Border
from .fill import Fill


@dataclass
class CellStyle:
    """Complete cell style"""
    
    font: Font = field(default_factory=Font)
    alignment: Alignment = field(default_factory=Alignment)
    border: Border = field(default_factory=Border)
    fill: Fill = field(default_factory=Fill)
    number_format: str = "General"
    protection_locked: bool = True
    protection_hidden: bool = False
    quote_prefix: bool = False
    
    def __str__(self) -> str:
        return f"CellStyle(font={self.font}, align={self.alignment})"
    
    def __repr__(self) -> str:
        return (f"CellStyle(font={self.font}, alignment={self.alignment}, "
                f"border={self.border}, fill={self.fill}, "
                f"number_format='{self.number_format}')")