"""
Image output
"""

from ..core.worksheet import Worksheet
from ..graphics.canvas import Rectangle, Canvas
from ..renderer.cell_renderer import CellRenderer
from ..renderer.base import RenderContext
from ..layout.calculator import LayoutCalculator


class ImageOutput:
    """Image output renderer"""
    
    def __init__(self, scale: float = 1.0, dpi: int = 96):
        self.scale = scale
        self.dpi = dpi
    
    def render(self, worksheet: Worksheet, filepath: str, 
               format: str = "PNG") -> bool:
        """Render worksheet to image file"""
        calculator = LayoutCalculator(worksheet)
        width, height = calculator.calculate_worksheet_size()
        
        canvas_width = int(width * self.scale)
        canvas_height = int(height * self.scale)
        
        canvas = Canvas(canvas_width, canvas_height)
        canvas.create()
        
        self._render_worksheet(worksheet, canvas, calculator)
        
        return canvas.save(filepath, format)
    
    def render_page(self, worksheet: Worksheet, page, filepath: str,
                    format: str = "PNG") -> bool:
        """Render single page to image file"""
        canvas_width = int(page.width * self.scale)
        canvas_height = int(page.height * self.scale)
        
        canvas = Canvas(canvas_width, canvas_height)
        canvas.create()
        
        self._render_page(worksheet, page, canvas)
        
        return canvas.save(filepath, format)
    
    def _render_worksheet(self, worksheet: Worksheet, canvas: Canvas, 
                          calculator: LayoutCalculator):
        """Render entire worksheet"""
        cell_renderer = CellRenderer(canvas)
        
        for (row, col), cell in worksheet.cells.items():
            if cell.is_merged() and not cell.is_merged_parent():
                continue
            
            rect = calculator.get_cell_rect(row, col)
            scaled_rect = Rectangle(
                rect.x * self.scale,
                rect.y * self.scale,
                rect.width * self.scale,
                rect.height * self.scale
            )
            
            context = RenderContext(
                cell=cell,
                rect=scaled_rect,
                scale=self.scale,
                worksheet=worksheet
            )
            
            cell_renderer.render(context)
    
    def _render_page(self, worksheet: Worksheet, page, canvas: Canvas):
        """Render single page"""
        cell_renderer = CellRenderer(canvas)
        
        for row in range(page.row_start, page.row_end + 1):
            for col in range(page.col_start, page.col_end + 1):
                if (row, col) not in worksheet.cells:
                    continue
                
                cell = worksheet.cells[(row, col)]
                
                if cell.is_merged() and not cell.is_merged_parent():
                    continue
                
                from ..layout.calculator import LayoutCalculator
                calculator = LayoutCalculator(worksheet)
                rect = calculator.get_cell_rect(row, col)
                
                scaled_rect = Rectangle(
                    (rect.x - page.x_offset) * self.scale,
                    (rect.y - page.y_offset) * self.scale,
                    rect.width * self.scale,
                    rect.height * self.scale
                )
                
                context = RenderContext(
                    cell=cell,
                    rect=scaled_rect,
                    scale=self.scale,
                    worksheet=worksheet,
                    page_number=page.page_number
                )
                
                cell_renderer.render(context)
    
    def get_image(self, worksheet: Worksheet):
        """Get image object"""
        calculator = LayoutCalculator(worksheet)
        width, height = calculator.calculate_worksheet_size()
        
        canvas_width = int(width * self.scale)
        canvas_height = int(height * self.scale)
        
        canvas = Canvas(canvas_width, canvas_height)
        canvas.create()
        
        self._render_worksheet(worksheet, canvas, calculator)
        
        return canvas.get_image()