"""
Workbook representation
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .worksheet import Worksheet


@dataclass
class Workbook:
    """Workbook representation"""
    
    worksheets: List["Worksheet"] = field(default_factory=list)
    active_sheet_index: int = 0
    calculation_mode: str = "auto"
    
    def add_worksheet(self, name: str) -> "Worksheet":
        """Add a new worksheet"""
        from .worksheet import Worksheet
        ws = Worksheet(name=name, workbook=self)
        self.worksheets.append(ws)
        return ws
    
    def get_worksheet(self, name: str) -> Optional["Worksheet"]:
        """Get worksheet by name"""
        for ws in self.worksheets:
            if ws.name == name:
                return ws
        return None
    
    @property
    def active(self) -> Optional["Worksheet"]:
        """Get active worksheet"""
        if 0 <= self.active_sheet_index < len(self.worksheets):
            return self.worksheets[self.active_sheet_index]
        return None
    
    def __str__(self) -> str:
        return f"Workbook({len(self.worksheets)} worksheets)"
    
    def __repr__(self) -> str:
        return (f"Workbook(worksheets={len(self.worksheets)}, "
                f"active_sheet_index={self.active_sheet_index}, "
                f"calculation_mode='{self.calculation_mode}')")