"""
Border styles for cells
"""

from dataclasses import dataclass
from typing import Literal
from .color import Color


BorderStyle = Literal["none", "thin", "medium", "dashed", "dotted", "thick", "double", 
                     "hair", "mediumDashed", "dashDot", "mediumDashDot", "dashDotDot",
                     "mediumDashDotDot", "slantDashDot"]


@dataclass
class SideBorder:
    """Single side border"""
    
    style: BorderStyle = "none"
    color: Color = None
    
    def __post_init__(self):
        if self.color is None:
            self.color = Color.black()
    
    def is_visible(self) -> bool:
        """Check if border is visible"""
        return self.style != "none"
    
    def __str__(self) -> str:
        return f"{self.style} {self.color}"
    
    def __repr__(self) -> str:
        return f"SideBorder(style='{self.style}', color={self.color})"


@dataclass
class Border:
    """Cell border representation"""
    
    left: SideBorder = None
    right: SideBorder = None
    top: SideBorder = None
    bottom: SideBorder = None
    diagonal: SideBorder = None
    diagonal_up: bool = False
    diagonal_down: bool = False
    outline: bool = True
    
    def __post_init__(self):
        if self.left is None:
            self.left = SideBorder()
        if self.right is None:
            self.right = SideBorder()
        if self.top is None:
            self.top = SideBorder()
        if self.bottom is None:
            self.bottom = SideBorder()
        if self.diagonal is None:
            self.diagonal = SideBorder()
    
    def has_any_border(self) -> bool:
        """Check if any border is visible"""
        return (self.left.is_visible() or self.right.is_visible() or 
                self.top.is_visible() or self.bottom.is_visible())
    
    def __str__(self) -> str:
        return f"Border({self.left}, {self.right}, {self.top}, {self.bottom})"
    
    def __repr__(self) -> str:
        return (f"Border(left={self.left}, right={self.right}, top={self.top}, "
                f"bottom={self.bottom}, diagonal={self.diagonal})")