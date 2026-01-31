"""
Conditional format renderer
"""

from .base import BaseRenderer, RenderContext
from ..core.color import Color
from typing import List


class ConditionalFormatRenderer(BaseRenderer):
    """Conditional format renderer"""
    
    def render(self, context: RenderContext):
        """Render conditional format"""
        cell = context.cell
        cond_formats = cell.worksheet.get_conditional_formats(cell.row, cell.col)
        
        for cf in cond_formats:
            if cf.type == "data_bar":
                self._render_data_bar(context, cf)
            elif cf.type == "color_scale":
                self._render_color_scale(context, cf)
            elif cf.type == "icon_set":
                self._render_icon_set(context, cf)
    
    def _render_data_bar(self, context: RenderContext, cf):
        """Render data bar"""
        value = context.cell.value
        
        if not isinstance(value, (int, float)):
            return
        
        min_val = cf.min_value
        max_val = cf.max_value
        
        if max_val == min_val:
            ratio = 1.0
        else:
            ratio = (value - min_val) / (max_val - min_val)
        
        ratio = max(0.0, min(1.0, ratio))
        
        rect = context.rect
        bar_width = rect.width * ratio
        bar_height = rect.height * 0.5
        bar_y = rect.center_y - bar_height / 2
        
        from ..graphics.canvas import Rectangle
        bar_rect = Rectangle(rect.x, bar_y, bar_width, bar_height)
        
        self.canvas.set_fill_color(cf.color)
        self.canvas.fill_rect(bar_rect)
    
    def _render_color_scale(self, context: RenderContext, cf):
        """Render color scale"""
        value = context.cell.value
        
        if not isinstance(value, (int, float)):
            return
        
        stops = sorted(cf.stops, key=lambda s: s.value)
        
        if len(stops) < 2:
            return
        
        min_val = stops[0].value
        max_val = stops[-1].value
        
        if max_val == min_val:
            color = stops[0].color
        else:
            ratio = (value - min_val) / (max_val - min_val)
            ratio = max(0.0, min(1.0, ratio))
            
            color = self._interpolate_color(stops, ratio)
        
        self.canvas.set_fill_color(color)
        self.canvas.fill_rect(context.rect)
    
    def _interpolate_color(self, stops: List, ratio: float) -> Color:
        """Interpolate color based on ratio"""
        for i in range(len(stops) - 1):
            stop1 = stops[i]
            stop2 = stops[i + 1]
            
            if ratio >= stop1.position and ratio <= stop2.position:
                local_ratio = (ratio - stop1.position) / (stop2.position - stop1.position)
                
                r = int(stop1.color.red * (1 - local_ratio) + stop2.color.red * local_ratio)
                g = int(stop1.color.green * (1 - local_ratio) + stop2.color.green * local_ratio)
                b = int(stop1.color.blue * (1 - local_ratio) + stop2.color.blue * local_ratio)
                
                return Color(red=r, green=g, blue=b)
        
        return stops[-1].color
    
    def _render_icon_set(self, context: RenderContext, cf):
        """Render icon set"""
        value = context.cell.value
        
        if not isinstance(value, (int, float)):
            return
        
        icon = self._get_icon_for_value(value, cf)
        
        if icon:
            rect = context.rect
            icon_size = min(rect.width, rect.height) * 0.6
            icon_x = rect.center_x - icon_size / 2
            icon_y = rect.center_y - icon_size / 2
            
            self._draw_icon(icon, icon_x, icon_y, icon_size)
    
    def _get_icon_for_value(self, value: float, cf):
        """Get icon for value"""
        thresholds = sorted(cf.icons, key=lambda i: i.threshold)
        
        for icon in thresholds:
            if value >= icon.threshold:
                return icon.symbol
        
        return None
    
    def _draw_icon(self, symbol: str, x: float, y: float, size: float):
        """Draw icon symbol"""
        font = self.canvas._current_font
        self.canvas.set_font(font)
        self.canvas.draw_text(x, y, symbol)