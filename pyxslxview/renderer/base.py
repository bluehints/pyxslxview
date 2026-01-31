"""
Base renderer
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..core.cell import Cell
from ..core.worksheet import Worksheet
from ..graphics.canvas import Rectangle


@dataclass
class RenderContext:
    """Render context"""
    
    cell: Cell
    rect: Rectangle
    scale: float = 1.0
    worksheet: Optional[Worksheet] = None
    page_number: Optional[int] = None
    total_pages: Optional[int] = None
    
    @property
    def x(self) -> float:
        return self.rect.x
    
    @property
    def y(self) -> float:
        return self.rect.y
    
    @property
    def width(self) -> float:
        return self.rect.width
    
    @property
    def height(self) -> float:
        return self.rect.height


class BaseRenderer(ABC):
    """Base renderer class"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.scale = 1.0
    
    @abstractmethod
    def render(self, context: RenderContext):
        """Render"""
        pass
    
    def set_scale(self, scale: float):
        """Set rendering scale"""
        self.scale = scale