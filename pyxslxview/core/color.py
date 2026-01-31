"""
Color management for cell styles
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Color:
    """Color representation"""
    
    red: int = 0
    green: int = 0
    blue: int = 0
    alpha: int = 255
    theme: Optional[int] = None
    indexed: Optional[int] = None
    auto: bool = False
    
    def __post_init__(self):
        """Validate color values"""
        if not (0 <= self.red <= 255):
            raise ValueError(f"Red value must be between 0 and 255, got {self.red}")
        if not (0 <= self.green <= 255):
            raise ValueError(f"Green value must be between 0 and 255, got {self.green}")
        if not (0 <= self.blue <= 255):
            raise ValueError(f"Blue value must be between 0 and 255, got {self.blue}")
        if not (0 <= self.alpha <= 255):
            raise ValueError(f"Alpha value must be between 0 and 255, got {self.alpha}")
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        """Get RGB tuple"""
        return (self.red, self.green, self.blue)
    
    @property
    def rgba(self) -> Tuple[int, int, int, int]:
        """Get RGBA tuple"""
        return (self.red, self.green, self.blue, self.alpha)
    
    @property
    def hex(self) -> str:
        """Get hex color string"""
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"
    
    @property
    def hex_alpha(self) -> str:
        """Get hex color string with alpha"""
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"
    
    @classmethod
    def from_hex(cls, hex_str: str) -> "Color":
        """Create color from hex string"""
        hex_str = hex_str.lstrip("#")
        
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return cls(red=r, green=g, blue=b)
        elif len(hex_str) == 8:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            a = int(hex_str[6:8], 16)
            return cls(red=r, green=g, blue=b, alpha=a)
        else:
            raise ValueError(f"Invalid hex color string: {hex_str}")
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: int = 255) -> "Color":
        """Create color from RGB values"""
        return cls(red=r, green=g, blue=b, alpha=a)
    
    @classmethod
    def black(cls) -> "Color":
        """Get black color"""
        return cls(red=0, green=0, blue=0)
    
    @classmethod
    def white(cls) -> "Color":
        """Get white color"""
        return cls(red=255, green=255, blue=255)
    
    @classmethod
    def get_red(cls) -> "Color":
        """Get red color"""
        return cls(red=255, green=0, blue=0)
    
    @classmethod
    def get_green(cls) -> "Color":
        """Get green color"""
        return cls(red=0, green=255, blue=0)
    
    @classmethod
    def get_blue(cls) -> "Color":
        """Get blue color"""
        return cls(red=0, green=0, blue=255)
    
    def __str__(self) -> str:
        return self.hex
    
    def __repr__(self) -> str:
        return f"Color(red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha})"