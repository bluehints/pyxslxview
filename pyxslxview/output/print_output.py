"""
Print output
"""

from typing import Optional, List
from ..core.worksheet import Worksheet
from ..layout.paginator import Paginator, Page
from .image_output import ImageOutput


class PrintOutput:
    """Print output renderer"""
    
    def __init__(self, scale: float = 1.0, dpi: int = 300):
        self.scale = scale
        self.dpi = dpi
    
    def render(self, worksheet: Worksheet) -> List[bytes]:
        """Render worksheet to print-ready images"""
        paginator = Paginator(worksheet)
        pages = paginator.paginate()
        
        page_images = []
        
        for page in pages:
            image_data = self._render_page(worksheet, page)
            if image_data:
                page_images.append(image_data)
        
        return page_images
    
    def _render_page(self, worksheet: Worksheet, page: Page) -> Optional[bytes]:
        """Render single page to image bytes"""
        try:
            from io import BytesIO
            
            image_output = ImageOutput(scale=self.scale, dpi=self.dpi)
            
            temp_file = BytesIO()
            success = image_output.render_page(worksheet, page, temp_file, "PNG")
            
            if success:
                temp_file.seek(0)
                return temp_file.read()
            
            return None
            
        except Exception:
            return None
    
    def print_pages(self, worksheet: Worksheet, printer_name: str = None):
        """Print worksheet pages"""
        try:
            import subprocess
            import tempfile
            import os
            
            page_images = self.render(worksheet)
            
            for i, image_data in enumerate(page_images):
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                    f.write(image_data)
                    temp_path = f.name
                
                try:
                    if printer_name:
                        subprocess.run(["lpr", "-P", printer_name, temp_path], check=True)
                    else:
                        subprocess.run(["lpr", temp_path], check=True)
                finally:
                    os.unlink(temp_path)
            
            return True
            
        except Exception:
            return False
    
    def get_page_count(self, worksheet: Worksheet) -> int:
        """Get number of pages"""
        paginator = Paginator(worksheet)
        pages = paginator.paginate()
        return len(pages)
    
    def preview_pages(self, worksheet: Worksheet):
        """Preview pages (returns list of image objects)"""
        paginator = Paginator(worksheet)
        pages = paginator.paginate()
        
        previews = []
        
        for page in pages:
            image_output = ImageOutput(scale=0.5, dpi=96)
            image = image_output.get_image(worksheet)
            if image:
                previews.append(image)
        
        return previews