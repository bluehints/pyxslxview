"""
Canvas abstraction for graphics operations
"""

from typing import Tuple
from dataclasses import dataclass
from ..core.color import Color
from ..core.font import Font
from .color import ColorManager
from .font import FontManager
from .image import ImageManager

try:
    from PIL import ImageDraw
except Exception:
    ImageDraw = None


@dataclass
class Point:
    """Point in 2D space"""
    
    x: float
    y: float


@dataclass
class Rectangle:
    """Rectangle in 2D space"""
    
    x: float
    y: float
    width: float
    height: float
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    @property
    def center_x(self) -> float:
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
    
    def contains(self, point: Point) -> bool:
        """Check if point is inside rectangle"""
        return (self.left <= point.x <= self.right and 
                self.top <= point.y <= self.bottom)


class Canvas:
    """Canvas abstraction for graphics operations"""
    
    def __init__(self, width: int, height: int, background_color: Color = None):
        self.width = width
        self.height = height
        self.background_color = background_color or Color.white()
        
        self.color_manager = ColorManager()
        self.font_manager = FontManager()
        self.image_manager = ImageManager()
        
        self._current_font = None
        self._current_color = None
        self._current_line_width = 1.0
        self._current_line_style = "solid"
        
        self._image = None
        self._draw = None
    
    def create(self):
        """Create canvas surface"""
        try:
            from PIL import Image, ImageDraw
            
            bg = self.background_color.rgba
            self._image = Image.new("RGBA", (self.width, self.height), bg)
            self._draw = ImageDraw.Draw(self._image)
            
            return True
        except Exception:
            return False
    
    def clear(self, color: Color = None):
        """Clear canvas"""
        if color is None:
            color = self.background_color
        
        try:
            from PIL import Image
            
            bg = color.rgba
            self._image = Image.new("RGBA", (self.width, self.height), bg)
            if ImageDraw:
                self._draw = ImageDraw.Draw(self._image)
        except Exception:
            pass
    
    def set_font(self, font: Font):
        """Set current font"""
        self._current_font = font
    
    def set_text_color(self, color: Color):
        """Set text color"""
        self._current_color = color
    
    def set_line_color(self, color: Color):
        """Set line color"""
        self._current_color = color
    
    def set_fill_color(self, color: Color):
        """Set fill color"""
        self._current_color = color
    
    def set_line_width(self, width: float):
        """Set line width"""
        self._current_line_width = width
    
    def set_line_style(self, style: str):
        """Set line style"""
        self._current_line_style = style
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw line"""
        if self._draw is None or self._current_color is None:
            return
        
        try:
            color = self.color_manager.get_rgba(self._current_color)
            width = self._current_line_width
            
            self._draw.line([(x1, y1), (x2, y2)], fill=color, width=int(width))
        except Exception:
            pass
    
    def draw_rect(self, rect: Rectangle):
        """Draw rectangle outline"""
        if self._draw is None or self._current_color is None:
            return
        
        try:
            color = self.color_manager.get_rgba(self._current_color)
            width = self._current_line_width
            
            self._draw.rectangle(
                [(rect.left, rect.top), (rect.right, rect.bottom)],
                outline=color,
                width=int(width)
            )
        except Exception:
            pass
    
    def fill_rect(self, rect: Rectangle):
        """Fill rectangle"""
        if self._draw is None or self._current_color is None:
            return
        
        try:
            color = self.color_manager.get_rgba(self._current_color)
            
            self._draw.rectangle(
                [(rect.left, rect.top), (rect.right, rect.bottom)],
                fill=color
            )
        except Exception:
            pass
    
    def draw_text(self, x: float, y: float, text: str):
        """Draw text"""
        if self._draw is None or self._current_font is None or self._current_color is None:
            return
        
        try:
            font_obj = self.font_manager.get_font(self._current_font)
            color = self.color_manager.get_rgba(self._current_color)
            
            if font_obj["font"]:
                self._draw.text((x, y), text, font=font_obj["font"], fill=color)
        except Exception:
            pass
    
    def draw_multiline_text(self, x: float, y: float, text: str, line_height: float = None):
        """Draw multiline text"""
        if self._draw is None or self._current_font is None or self._current_color is None:
            return
        
        try:
            font_obj = self.font_manager.get_font(self._current_font)
            color = self.color_manager.get_rgba(self._current_color)
            
            if font_obj["font"]:
                metrics = self.font_manager.get_metrics(self._current_font)
                if line_height is None:
                    line_height = metrics.height
                
                lines = text.split("\n")
                for i, line in enumerate(lines):
                    self._draw.text(
                        (x, y + i * line_height),
                        line,
                        font=font_obj["font"],
                        fill=color
                    )
        except Exception:
            pass
    
    def draw_image(self, x: float, y: float, image: object, 
                   width: float = None, height: float = None):
        """Draw image"""
        if self._image is None or image is None:
            return
        
        try:
            from PIL import Image
            
            if isinstance(image, Image.Image):
                if width is not None and height is not None:
                    img = image.resize((int(width), int(height)), Image.Resampling.LANCZOS)
                else:
                    img = image
                
                self._image.paste(img, (int(x), int(y)))
        except Exception:
            pass
    
    def get_image(self):
        """Get canvas image"""
        return self._image
    
    def save(self, filepath: str, format: str = "PNG"):
        """Save canvas to file"""
        if self._image is None:
            return False
        
        try:
            self._image.save(filepath, format=format)
            return True
        except Exception:
            return False
    
    def get_size(self) -> Tuple[int, int]:
        """Get canvas size"""
        return (self.width, self.height)