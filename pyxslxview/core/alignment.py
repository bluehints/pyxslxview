"""
Alignment styles for cells
"""

from dataclasses import dataclass
from typing import Literal


HorizontalAlign = Literal["left", "center", "right", "fill", "justify", "centerContinuous", "distributed"]
VerticalAlign = Literal["top", "center", "bottom", "justify", "distributed"]


@dataclass
class Alignment:
    """Cell alignment representation"""
    
    horizontal: HorizontalAlign = "left"
    vertical: VerticalAlign = "bottom"
    text_rotation: int = 0
    wrap_text: bool = False
    shrink_to_fit: bool = False
    indent: int = 0
    text_rotation_mode: Literal["normal", "stacked"] = "normal"
    justify_last_line: bool = False
    
    def __str__(self) -> str:
        return f"Alignment(h={self.horizontal}, v={self.vertical}, wrap={self.wrap_text})"
    
    def __repr__(self) -> str:
        return (f"Alignment(horizontal='{self.horizontal}', vertical='{self.vertical}', "
                f"text_rotation={self.text_rotation}, wrap_text={self.wrap_text}, "
                f"indent={self.indent})")