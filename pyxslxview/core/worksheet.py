"""
Worksheet representation
"""

from dataclasses import dataclass, field
from typing import Dict, List, TYPE_CHECKING, Tuple

from ..core.cell import Cell
from ..core.range import Range

if TYPE_CHECKING:
    from ..core.workbook import Workbook


@dataclass
class PageSetup:
    """Page setup configuration"""
    
    paper_size: str = "A4"
    orientation: str = "portrait"
    scale: int = 100
    fit_to_width: int = 1
    fit_to_height: int = 0
    first_page_number: int = 1
    use_first_page_number: bool = False
    horizontal_centered: bool = False
    vertical_centered: bool = False
    
    @property
    def paper_width(self) -> float:
        """Get paper width in points"""
        sizes = {
            "A4": (595.28, 841.89),
            "A3": (841.89, 1190.55),
            "Letter": (612, 792),
            "Legal": (612, 1008),
        }
        return sizes.get(self.paper_size, (595.28, 841.89))[0]
    
    @property
    def paper_height(self) -> float:
        """Get paper height in points"""
        sizes = {
            "A4": (595.28, 841.89),
            "A3": (841.89, 1190.55),
            "Letter": (612, 792),
            "Legal": (612, 1008),
        }
        return sizes.get(self.paper_size, (595.28, 841.89))[1]


@dataclass
class PageMargins:
    """Page margins configuration"""
    
    left: float = 0.75
    right: float = 0.75
    top: float = 1.0
    bottom: float = 1.0
    header: float = 0.5
    footer: float = 0.5


@dataclass
class Row:
    """Row configuration"""
    
    height: float = 15.0
    hidden: bool = False
    collapsed: bool = False
    outline_level: int = 0


@dataclass
class Column:
    """Column configuration"""
    
    width: float = 8.43
    hidden: bool = False
    collapsed: bool = False
    outline_level: int = 0


@dataclass
class Worksheet:
    """Worksheet representation"""
    
    name: str
    workbook: "Workbook"
    cells: Dict[Tuple[int, int], Cell] = field(default_factory=dict)
    merged_cells: List[Range] = field(default_factory=list)
    rows: Dict[int, Row] = field(default_factory=dict)
    columns: Dict[int, Column] = field(default_factory=dict)
    page_setup: PageSetup = field(default_factory=PageSetup)
    page_margins: PageMargins = field(default_factory=PageMargins)
    hidden: bool = False
    selected: bool = False
    tab_color: object = None
    
    def cell(self, row: int, col: int) -> Cell:
        """Get or create cell"""
        if (row, col) not in self.cells:
            self.cells[(row, col)] = Cell(row=row, col=col, worksheet=self)
        return self.cells[(row, col)]
    
    def get_row(self, row: int) -> Row:
        """Get or create row configuration"""
        if row not in self.rows:
            self.rows[row] = Row()
        return self.rows[row]
    
    def get_column(self, col: int) -> Column:
        """Get or create column configuration"""
        if col not in self.columns:
            self.columns[col] = Column()
        return self.columns[col]
    
    def merge_cells(self, range_str: str):
        """Merge cells in range"""
        min_row, max_row, min_col, max_col = self._parse_cell_range(range_str)
        merged_range = Range(
            min_row=min_row, max_row=max_row,
            min_col=min_col, max_col=max_col, worksheet=self
        )
        self.merged_cells.append(merged_range)
    
    def _parse_cell_range(self, range_str: str):
        """Parse cell range string"""
        parts = range_str.split(":")
        start = self._parse_cell_reference(parts[0])
        end = self._parse_cell_reference(parts[1])
        return (start[0], end[0], start[1], end[1])
    
    def _parse_cell_reference(self, ref: str):
        """Parse cell reference (e.g., 'A1') to row, col"""
        col_str = ""
        row_str = ""
        
        for char in ref:
            if char.isalpha():
                col_str += char
            elif char.isdigit():
                row_str += char
        
        col = 0
        for char in col_str:
            col = col * 26 + (ord(char.upper()) - ord('A') + 1)
        
        row = int(row_str)
        return (row, col)
    
    @property
    def max_row(self) -> int:
        """Get maximum row number with data"""
        if not self.cells:
            return 0
        return max(row for row, _ in self.cells.keys())
    
    @property
    def max_col(self) -> int:
        """Get maximum column number with data"""
        if not self.cells:
            return 0
        return max(col for _, col in self.cells.keys())
    
    def __str__(self) -> str:
        return f"Worksheet('{self.name}', {len(self.cells)} cells)"
    
    def __repr__(self) -> str:
        return (f"Worksheet(name='{self.name}', workbook={self.workbook}, "
                f"cells={len(self.cells)}, merged_cells={len(self.merged_cells)})")