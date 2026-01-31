"""
Formula renderer
"""

from .base import BaseRenderer, RenderContext
from ..core.color import Color


class FormulaRenderer(BaseRenderer):
    """Formula renderer"""
    
    def __init__(self, canvas):
        super().__init__(canvas)
        self.color_manager = canvas.color_manager
    
    def render(self, context: RenderContext):
        """Render formula"""
        cell = context.cell
        
        if not cell.formula:
            return
        
        style = cell.style
        alignment = style.alignment
        
        font = style.font
        color = Color.get_red()
        
        self.canvas.set_font(font)
        self.canvas.set_text_color(color)
        
        text = cell.formula
        
        x = self._calculate_x_position(context, text, alignment)
        y = self._calculate_y_position(context, alignment)
        
        self.canvas.draw_text(x, y, text)
    
    def _calculate_x_position(self, context: RenderContext, text: str, 
                              alignment) -> float:
        """Calculate x position"""
        rect = context.rect
        font = context.cell.style.font
        
        text_width, _ = self.canvas.font_manager.measure_text(font, text)
        
        if alignment.horizontal == "left":
            return rect.x + 2
        elif alignment.horizontal == "center":
            return rect.center_x - text_width / 2
        elif alignment.horizontal == "right":
            return rect.right - text_width - 2
        else:
            return rect.x + 2
    
    def _calculate_y_position(self, context: RenderContext, alignment) -> float:
        """Calculate y position"""
        rect = context.rect
        font = context.cell.style.font
        
        _, text_height = self.canvas.font_manager.measure_text(font, "M")
        
        if alignment.vertical == "top":
            return rect.y + 2
        elif alignment.vertical == "center":
            return rect.center_y - text_height / 2
        elif alignment.vertical == "bottom":
            return rect.bottom - text_height - 2
        else:
            return rect.bottom - text_height - 2