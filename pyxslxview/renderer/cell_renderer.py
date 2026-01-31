"""
Cell renderer
"""

from .base import BaseRenderer, RenderContext
from .background_renderer import BackgroundRenderer
from .border_renderer import BorderRenderer
from .text_renderer import TextRenderer
from .formula_renderer import FormulaRenderer


class CellRenderer(BaseRenderer):
    """Cell renderer"""
    
    def __init__(self, canvas):
        super().__init__(canvas)
        self.background_renderer = BackgroundRenderer(canvas)
        self.border_renderer = BorderRenderer(canvas)
        self.text_renderer = TextRenderer(canvas)
        self.formula_renderer = FormulaRenderer(canvas)
    
    def render(self, context: RenderContext):
        """Render cell"""
        cell = context.cell
        
        if cell.is_merged() and not cell.is_merged_parent():
            return
        
        self.background_renderer.render(context)
        self.border_renderer.render(context)
        
        if cell.data_type == "formula":
            self.formula_renderer.render(context)
        elif cell.value is not None and cell.data_type != "blank":
            self.text_renderer.render(context)