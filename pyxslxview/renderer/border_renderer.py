"""
Border renderer
"""

from .base import BaseRenderer, RenderContext
from ..core.border import BorderStyle


class BorderRenderer(BaseRenderer):
    """Border renderer"""
    
    def render(self, context: RenderContext):
        """Render border"""
        cell = context.cell
        border = cell.style.border
        
        if not border or not border.has_any_border():
            return
        
        rect = context.rect
        
        if border.left.is_visible():
            self._draw_border_line(
                rect.left, rect.top,
                rect.left, rect.bottom,
                border.left
            )
        
        if border.right.is_visible():
            self._draw_border_line(
                rect.right, rect.top,
                rect.right, rect.bottom,
                border.right
            )
        
        if border.top.is_visible():
            self._draw_border_line(
                rect.left, rect.top,
                rect.right, rect.top,
                border.top
            )
        
        if border.bottom.is_visible():
            self._draw_border_line(
                rect.left, rect.bottom,
                rect.right, rect.bottom,
                border.bottom
            )
        
        if border.diagonal.is_visible():
            if border.diagonal_up:
                self._draw_border_line(
                    rect.left, rect.bottom,
                    rect.right, rect.top,
                    border.diagonal
                )
            if border.diagonal_down:
                self._draw_border_line(
                    rect.left, rect.top,
                    rect.right, rect.bottom,
                    border.diagonal
                )
    
    def _draw_border_line(self, x1: float, y1: float, x2: float, y2: float,
                         border_style):
        """Draw border line"""
        self.canvas.set_line_color(border_style.color)
        self.canvas.set_line_width(self._get_border_width(border_style.style))
        self.canvas.set_line_style(border_style.style)
        
        if border_style.style in ["dashed", "mediumDashed"]:
            self._draw_dashed_line(x1, y1, x2, y2)
        elif border_style.style in ["dotted", "hair"]:
            self._draw_dotted_line(x1, y1, x2, y2)
        elif border_style.style in ["double"]:
            self._draw_double_line(x1, y1, x2, y2)
        elif border_style.style in ["dashDot", "mediumDashDot"]:
            self._draw_dash_dot_line(x1, y1, x2, y2)
        elif border_style.style in ["dashDotDot", "mediumDashDotDot"]:
            self._draw_dash_dot_dot_line(x1, y1, x2, y2)
        else:
            self.canvas.draw_line(x1, y1, x2, y2)
    
    def _get_border_width(self, style: BorderStyle) -> float:
        """Get border width"""
        widths = {
            "none": 0,
            "thin": 1.0,
            "medium": 2.0,
            "thick": 3.0,
            "hair": 0.5,
            "dashed": 1.0,
            "dotted": 1.0,
            "double": 3.0,
            "mediumDashed": 2.0,
            "dashDot": 1.0,
            "mediumDashDot": 2.0,
            "dashDotDot": 1.0,
            "mediumDashDotDot": 2.0,
            "slantDashDot": 2.0,
        }
        return widths.get(style, 1.0)
    
    def _draw_dashed_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw dashed line"""
        dash_length = 5
        gap_length = 3
        
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        current = 0
        while current < length:
            end = min(current + dash_length, length)
            self.canvas.draw_line(
                x1 + dx * current,
                y1 + dy * current,
                x1 + dx * end,
                y1 + dy * end
            )
            current = end + gap_length
    
    def _draw_dotted_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw dotted line"""
        dot_spacing = 3
        
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        current = 0
        while current < length:
            self.canvas.draw_line(
                x1 + dx * current,
                y1 + dy * current,
                x1 + dx * current + 0.5,
                y1 + dy * current + 0.5
            )
            current += dot_spacing
    
    def _draw_double_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw double line"""
        offset = 1.0
        
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        nx = -dy
        ny = dx
        
        self.canvas.draw_line(
            x1 + nx * offset,
            y1 + ny * offset,
            x2 + nx * offset,
            y2 + ny * offset
        )
        self.canvas.draw_line(
            x1 - nx * offset,
            y1 - ny * offset,
            x2 - nx * offset,
            y2 - ny * offset
        )
    
    def _draw_dash_dot_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw dash-dot line"""
        dash_length = 5
        dot_length = 2
        gap_length = 2
        
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        current = 0
        while current < length:
            end = min(current + dash_length, length)
            self.canvas.draw_line(
                x1 + dx * current,
                y1 + dy * current,
                x1 + dx * end,
                y1 + dy * end
            )
            current = end + gap_length
            
            if current < length:
                end = min(current + dot_length, length)
                self.canvas.draw_line(
                    x1 + dx * current,
                    y1 + dy * current,
                    x1 + dx * end,
                    y1 + dy * end
                )
                current = end + gap_length
    
    def _draw_dash_dot_dot_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw dash-dot-dot line"""
        dash_length = 5
        dot_length = 2
        gap_length = 2
        
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return
        
        dx = (x2 - x1) / length
        dy = (y2 - y1) / length
        
        current = 0
        while current < length:
            end = min(current + dash_length, length)
            self.canvas.draw_line(
                x1 + dx * current,
                y1 + dy * current,
                x1 + dx * end,
                y1 + dy * end
            )
            current = end + gap_length
            
            for _ in range(2):
                if current < length:
                    end = min(current + dot_length, length)
                    self.canvas.draw_line(
                        x1 + dx * current,
                        y1 + dy * current,
                        x1 + dx * end,
                        y1 + dy * end
                    )
                    current = end + gap_length