"""
Fill styles for cells
"""

from dataclasses import dataclass
from typing import Literal, Optional, List
from .color import Color


FillType = Literal["none", "solid", "pattern", "gradient"]
PatternType = Literal["none", "solid", "mediumGray", "darkGray", "lightGray", "darkHorizontal",
                     "darkVertical", "darkDown", "darkUp", "darkGrid", "darkTrellis",
                     "lightHorizontal", "lightVertical", "lightDown", "lightUp", "lightGrid",
                     "lightTrellis", "gray125", "gray0625"]
GradientType = Literal["linear", "path"]


@dataclass
class GradientStop:
    """Gradient stop"""
    
    position: float
    color: Color
    
    def __repr__(self) -> str:
        return f"GradientStop(pos={self.position}, color={self.color})"


@dataclass
class GradientFill:
    """Gradient fill"""
    
    gradient_type: GradientType = "linear"
    degree: float = 0.0
    left: float = 0.0
    right: float = 0.0
    top: float = 0.0
    bottom: float = 0.0
    stops: List[GradientStop] = None
    
    def __post_init__(self):
        if self.stops is None:
            self.stops = []
    
    def __repr__(self) -> str:
        return f"GradientFill(type={self.gradient_type}, stops={len(self.stops)})"


@dataclass
class PatternFill:
    """Pattern fill"""
    
    pattern_type: PatternType = "none"
    fg_color: Color = None
    bg_color: Color = None
    
    def __post_init__(self):
        if self.fg_color is None:
            self.fg_color = Color.black()
        if self.bg_color is None:
            self.bg_color = Color.white()
    
    def __repr__(self) -> str:
        return f"PatternFill(pattern={self.pattern_type}, fg={self.fg_color}, bg={self.bg_color})"


@dataclass
class Fill:
    """Cell fill representation"""
    
    fill_type: FillType = "none"
    fg_color: Color = None
    bg_color: Color = None
    pattern_type: PatternType = "none"
    gradient: Optional[GradientFill] = None
    
    def __post_init__(self):
        if self.fg_color is None:
            self.fg_color = Color.white()
        if self.bg_color is None:
            self.bg_color = Color.white()
    
    @classmethod
    def solid(cls, color: Color) -> "Fill":
        """Create solid fill"""
        return cls(fill_type="solid", fg_color=color)
    
    @classmethod
    def pattern(cls, pattern_type: PatternType, fg_color: Color, 
                bg_color: Optional[Color] = None) -> "Fill":
        """Create pattern fill"""
        if bg_color is None:
            bg_color = Color.white()
        return cls(fill_type="pattern", pattern_type=pattern_type, 
                   fg_color=fg_color, bg_color=bg_color)
    
    @classmethod
    def gradient_fill(cls, grad: GradientFill) -> "Fill":
        """Create gradient fill"""
        return cls(fill_type="gradient", gradient=grad)
    
    def __str__(self) -> str:
        if self.fill_type == "none":
            return "Fill(none)"
        elif self.fill_type == "solid":
            return f"Fill(solid: {self.fg_color})"
        elif self.fill_type == "pattern":
            return f"Fill(pattern: {self.pattern_type})"
        elif self.fill_type == "gradient":
            return f"Fill(gradient: {self.gradient})"
        return "Fill(unknown)"
    
    def __repr__(self) -> str:
        return (f"Fill(fill_type='{self.fill_type}', fg_color={self.fg_color}, "
                f"bg_color={self.bg_color}, pattern_type='{self.pattern_type}', "
                f"gradient={self.gradient})")