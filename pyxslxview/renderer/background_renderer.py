"""
Background renderer
"""

from .base import BaseRenderer, RenderContext
from ..core.fill import Fill
from ..core.color import Color


class BackgroundRenderer(BaseRenderer):
    """Background renderer"""
    
    def render(self, context: RenderContext):
        """Render background"""
        cell = context.cell
        fill = cell.style.fill
        
        if not fill or fill.fill_type == "none":
            return
        
        rect = context.rect
        
        if fill.fill_type == "solid":
            self._draw_solid_fill(rect, fill.fg_color)
        elif fill.fill_type == "gradient":
            self._draw_gradient_fill(rect, fill)
        elif fill.fill_type == "pattern":
            self._draw_pattern_fill(rect, fill)
    
    def _draw_solid_fill(self, rect, color: Color):
        """Draw solid fill"""
        self.canvas.set_fill_color(color)
        self.canvas.fill_rect(rect)
    
    def _draw_gradient_fill(self, rect, fill: Fill):
        """Draw gradient fill"""
        if not fill.gradient or not fill.gradient.stops:
            return
        
        gradient = fill.gradient
        
        if gradient.gradient_type == "linear":
            self._draw_linear_gradient(rect, gradient)
        else:
            self._draw_radial_gradient(rect, gradient)
    
    def _draw_linear_gradient(self, rect, gradient):
        """Draw linear gradient"""
        stops = sorted(gradient.stops, key=lambda s: s.position)
        
        if len(stops) < 2:
            return
        
        height = rect.height
        
        for i in range(len(stops) - 1):
            stop1 = stops[i]
            stop2 = stops[i + 1]
            
            y1 = rect.y + stop1.position * height
            y2 = rect.y + stop2.position * height
            
            from ..graphics.canvas import Rectangle
            sub_rect = Rectangle(rect.x, y1, rect.width, y2 - y1)
            
            self.canvas.set_fill_color(stop1.color)
            self.canvas.fill_rect(sub_rect)
    
    def _draw_radial_gradient(self, rect, gradient):
        """Draw radial gradient"""
        stops = sorted(gradient.stops, key=lambda s: s.position)
        
        if not stops:
            return
        
        center_x = rect.center_x
        center_y = rect.center_y
        max_radius = min(rect.width, rect.height) / 2
        
        for stop in reversed(stops):
            radius = stop.position * max_radius
            
            from ..graphics.canvas import Rectangle
            sub_rect = Rectangle(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )
            
            self.canvas.set_fill_color(stop.color)
            self.canvas.fill_rect(sub_rect)
    
    def _draw_pattern_fill(self, rect, fill: Fill):
        """Draw pattern fill"""
        self.canvas.set_fill_color(fill.bg_color)
        self.canvas.fill_rect(rect)
        
        if fill.pattern_type == "none":
            return
        
        self._draw_pattern(rect, fill)
    
    def _draw_pattern(self, rect, fill: Fill):
        """Draw pattern"""
        pattern_size = 8
        fg_color = fill.fg_color
        
        for y in range(int(rect.y), int(rect.y + rect.height), pattern_size):
            for x in range(int(rect.x), int(rect.x + rect.width), pattern_size):
                self._draw_pattern_cell(x, y, pattern_size, fill.pattern_type, fg_color)
    
    def _draw_pattern_cell(self, x: int, y: int, size: int, pattern_type: str, color: Color):
        """Draw pattern cell"""
        from ..graphics.canvas import Rectangle
        
        if pattern_type == "darkHorizontal":
            rect = Rectangle(x, y + size // 2, size, size // 2)
            self.canvas.set_fill_color(color)
            self.canvas.fill_rect(rect)
        elif pattern_type == "darkVertical":
            rect = Rectangle(x + size // 2, y, size // 2, size)
            self.canvas.set_fill_color(color)
            self.canvas.fill_rect(rect)
        elif pattern_type == "darkDown":
            for i in range(size):
                self.canvas.draw_line(x + i, y, x + i, y + i + 1)
        elif pattern_type == "darkUp":
            for i in range(size):
                self.canvas.draw_line(x + i, y + size, x + i, y + size - i - 1)
        elif pattern_type == "darkGrid":
            rect = Rectangle(x + size // 2, y, size // 2, size)
            self.canvas.set_fill_color(color)
            self.canvas.fill_rect(rect)
            rect = Rectangle(x, y + size // 2, size, size // 2)
            self.canvas.fill_rect(rect)
        elif pattern_type == "darkTrellis":
            for i in range(0, size, 2):
                self.canvas.draw_line(x + i, y, x + i, y + size)
                self.canvas.draw_line(x, y + i, x + size, y + i)