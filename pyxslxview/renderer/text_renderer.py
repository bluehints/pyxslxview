"""
Text renderer
"""

from .base import BaseRenderer, RenderContext
from ..core.alignment import Alignment, HorizontalAlign, VerticalAlign


class TextRenderer(BaseRenderer):
    """Text renderer"""
    
    def __init__(self, canvas):
        super().__init__(canvas)
        self.font_manager = canvas.font_manager
        self.color_manager = canvas.color_manager
    
    def render(self, context: RenderContext):
        """Render text"""
        cell = context.cell
        
        if not cell.value or cell.data_type == "blank":
            return
        
        style = cell.style
        alignment = style.alignment
        
        font = style.font
        color = font.color
        
        if color.auto:
            fill_color = style.fill.fg_color
            color = self.color_manager.get_contrast_color(fill_color)
        
        self.canvas.set_font(font)
        self.canvas.set_text_color(color)
        
        text = str(cell.value)
        
        if alignment.wrap_text:
            self._draw_wrapped_text(context, text, alignment)
        else:
            self._draw_single_line_text(context, text, alignment)
    
    def _draw_single_line_text(self, context: RenderContext, text: str, alignment: Alignment):
        """Draw single line text"""
        rect = context.rect
        font = context.cell.style.font
        
        text_width, text_height = self.font_manager.measure_text(font, text)
        
        x = self._calculate_x_position(rect, text_width, alignment.horizontal)
        y = self._calculate_y_position(rect, text_height, alignment.vertical)
        
        self.canvas.draw_text(x, y, text)
    
    def _draw_wrapped_text(self, context: RenderContext, text: str, alignment: Alignment):
        """Draw wrapped text"""
        rect = context.rect
        font = context.cell.style.font
        
        lines = self._wrap_text(text, rect.width, font)
        
        text_width, text_height = self.font_manager.measure_text(font, "M")
        line_height = text_height * 1.2
        
        x = self._calculate_x_position(rect, rect.width, alignment.horizontal)
        y = self._calculate_y_position(rect, len(lines) * line_height, alignment.vertical)
        
        self.canvas.draw_multiline_text(x, y, "\n".join(lines), line_height)
    
    def _wrap_text(self, text: str, max_width: float, font) -> list:
        """Wrap text to fit within max width"""
        lines = []
        words = text.split()
        
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width, _ = self.font_manager.measure_text(font, test_line)
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _calculate_x_position(self, rect, text_width: float, 
                              horizontal: HorizontalAlign) -> float:
        """Calculate x position based on horizontal alignment"""
        if horizontal == "left":
            return rect.x + 2
        elif horizontal == "center":
            return rect.center_x - text_width / 2
        elif horizontal == "right":
            return rect.right - text_width - 2
        elif horizontal == "fill":
            return rect.x
        elif horizontal == "justify":
            return rect.x
        elif horizontal == "centerContinuous":
            return rect.center_x - text_width / 2
        elif horizontal == "distributed":
            return rect.x
        else:
            return rect.x + 2
    
    def _calculate_y_position(self, rect, text_height: float, 
                              vertical: VerticalAlign) -> float:
        """Calculate y position based on vertical alignment"""
        if vertical == "top":
            return rect.y + 2
        elif vertical == "center":
            return rect.center_y - text_height / 2
        elif vertical == "bottom":
            return rect.bottom - text_height - 2
        elif vertical == "justify":
            return rect.y
        elif vertical == "distributed":
            return rect.y
        else:
            return rect.bottom - text_height - 2