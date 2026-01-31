"""
PDF output
"""

from ..core.worksheet import Worksheet
from ..layout.calculator import LayoutCalculator
from ..layout.paginator import Paginator


class PDFOutput:
    """PDF output renderer"""
    
    def __init__(self, scale: float = 1.0):
        self.scale = scale
    
    def render(self, worksheet: Worksheet, filepath: str) -> bool:
        """Render worksheet to PDF file"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas as pdf_canvas
            
            paginator = Paginator(worksheet)
            pages = paginator.paginate()
            
            c = pdf_canvas.Canvas(filepath, pagesize=A4)
            
            for page in pages:
                self._render_page(worksheet, page, c)
                c.showPage()
            
            c.save()
            return True
            
        except Exception:
            return False
    
    def _render_page(self, worksheet: Worksheet, page, pdf_canvas):
        """Render single page to PDF"""
        margin = 36
        pdf_canvas._pagesize[0] - 2 * margin
        pdf_canvas._pagesize[1] - 2 * margin
        
        calculator = LayoutCalculator(worksheet)
        
        for row in range(page.row_start, page.row_end + 1):
            for col in range(page.col_start, page.col_end + 1):
                if (row, col) not in worksheet.cells:
                    continue
                
                cell = worksheet.cells[(row, col)]
                
                if cell.is_merged() and not cell.is_merged_parent():
                    continue
                
                rect = calculator.get_cell_rect(row, col)
                
                x = margin + (rect.x - page.x_offset) * self.scale
                y = pdf_canvas._pagesize[1] - margin - (rect.y - page.y_offset + rect.height) * self.scale
                width = rect.width * self.scale
                height = rect.height * self.scale
                
                self._draw_cell_to_pdf(cell, x, y, width, height, pdf_canvas)
    
    def _draw_cell_to_pdf(self, cell, x: float, y: float, 
                          width: float, height: float, pdf_canvas):
        """Draw cell to PDF canvas"""
        self._draw_cell_background(cell, x, y, width, height, pdf_canvas)
        self._draw_cell_border(cell, x, y, width, height, pdf_canvas)
        self._draw_cell_text(cell, x, y, width, height, pdf_canvas)
    
    def _draw_cell_background(self, cell, x: float, y: float,
                              width: float, height: float, pdf_canvas):
        """Draw cell background"""
        fill = cell.style.fill
        
        if fill and fill.fill_type == "solid":
            pdf_canvas.setFillColorRGB(
                fill.fg_color.red / 255,
                fill.fg_color.green / 255,
                fill.fg_color.blue / 255
            )
            pdf_canvas.rect(x, y, width, height, fill=1, stroke=0)
    
    def _draw_cell_border(self, cell, x: float, y: float,
                           width: float, height: float, pdf_canvas):
        """Draw cell border"""
        border = cell.style.border
        
        if not border or not border.has_any_border():
            return
        
        line_widths = {
            "thin": 0.5,
            "medium": 1.0,
            "thick": 2.0,
            "hair": 0.25,
        }
        
        def draw_line(x1, y1, x2, y2, side_border):
            if side_border.is_visible():
                pdf_canvas.setStrokeColorRGB(
                    side_border.color.red / 255,
                    side_border.color.green / 255,
                    side_border.color.blue / 255
                )
                pdf_canvas.setLineWidth(line_widths.get(side_border.style, 0.5))
                pdf_canvas.line(x1, y1, x2, y2)
        
        draw_line(x, y, x + width, y, border.top)
        draw_line(x + width, y, x + width, y + height, border.right)
        draw_line(x + width, y + height, x, y + height, border.bottom)
        draw_line(x, y + height, x, y, border.left)
    
    def _draw_cell_text(self, cell, x: float, y: float,
                         width: float, height: float, pdf_canvas):
        """Draw cell text"""
        if not cell.value or cell.data_type == "blank":
            return
        
        font = cell.style.font
        alignment = cell.style.alignment
        
        pdf_canvas.setFont(font.name, font.size)
        pdf_canvas.setFillColorRGB(
            font.color.red / 255,
            font.color.green / 255,
            font.color.blue / 255
        )
        
        text = str(cell.value)
        text_width = pdf_canvas.stringWidth(text, font.name, font.size)
        
        text_x = self._calculate_text_x(x, width, text_width, alignment.horizontal)
        text_y = self._calculate_text_y(y, height, font.size, alignment.vertical)
        
        pdf_canvas.drawString(text_x, text_y, text)
    
    def _calculate_text_x(self, x: float, width: float, text_width: float,
                           horizontal: str) -> float:
        """Calculate text x position"""
        if horizontal == "center":
            return x + (width - text_width) / 2
        elif horizontal == "right":
            return x + width - text_width - 2
        else:
            return x + 2
    
    def _calculate_text_y(self, y: float, height: float, font_size: float,
                           vertical: str) -> float:
        """Calculate text y position"""
        if vertical == "center":
            return y + (height - font_size) / 2
        elif vertical == "top":
            return y + height - font_size - 2
        else:
            return y + 2