"""
Color management for graphics
"""

from typing import Dict, Tuple
from ..core.color import Color


class ColorManager:
    """Color manager for graphics operations"""
    
    def __init__(self):
        self._color_cache: Dict[str, Tuple[int, int, int, int]] = {}
    
    def get_rgba(self, color: Color) -> Tuple[int, int, int, int]:
        """Get RGBA tuple from Color object"""
        cache_key = f"{color.red}_{color.green}_{color.blue}_{color.alpha}"
        
        if cache_key not in self._color_cache:
            self._color_cache[cache_key] = color.rgba
        
        return self._color_cache[cache_key]
    
    def get_rgb(self, color: Color) -> Tuple[int, int, int]:
        """Get RGB tuple from Color object"""
        return color.rgb
    
    def get_hex(self, color: Color) -> str:
        """Get hex string from Color object"""
        return color.hex
    
    def blend(self, color1: Color, color2: Color, ratio: float = 0.5) -> Color:
        """Blend two colors"""
        r = int(color1.red * (1 - ratio) + color2.red * ratio)
        g = int(color1.green * (1 - ratio) + color2.green * ratio)
        b = int(color1.blue * (1 - ratio) + color2.blue * ratio)
        a = int(color1.alpha * (1 - ratio) + color2.alpha * ratio)
        return Color(red=r, green=g, blue=b, alpha=a)
    
    def get_contrast_color(self, color: Color) -> Color:
        """Get contrast color (black or white) based on luminance"""
        luminance = (0.299 * color.red + 0.587 * color.green + 0.114 * color.blue) / 255
        return Color.black() if luminance > 0.5 else Color.white()