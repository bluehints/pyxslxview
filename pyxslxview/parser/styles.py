"""
Styles parser
"""

import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List

from ..core.font import Font
from ..core.border import Border, SideBorder
from ..core.fill import Fill, GradientFill, GradientStop
from ..core.color import Color


@dataclass
class Styles:
    """Parsed styles"""
    
    fonts: List[Font] = None
    fills: List[Fill] = None
    borders: List[Border] = None
    cell_styles: List[dict] = None
    cell_formats: List[dict] = None
    
    def __post_init__(self):
        if self.fonts is None:
            self.fonts = [Font()]
        if self.fills is None:
            self.fills = [Fill(), Fill()]
        if self.borders is None:
            self.borders = [Border()]
        if self.cell_styles is None:
            self.cell_styles = []
        if self.cell_formats is None:
            self.cell_formats = []


class StylesParser:
    """Parser for styles"""
    
    def __init__(self):
        self.namespace = {
            'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
        }
    
    def parse(self, zf: zipfile.ZipFile) -> Styles:
        """Parse styles from XLSX file"""
        styles = Styles()
        
        try:
            with zf.open("xl/styles.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                fonts_elem = root.find(".//ns:fonts", self.namespace)
                if fonts_elem is not None:
                    for font_elem in fonts_elem.findall(".//ns:font", self.namespace):
                        font = Font()
                        
                        bold_elem = font_elem.find(".//ns:b", self.namespace)
                        if bold_elem is not None:
                            font.bold = bold_elem.get("val", "0") == "1"
                        
                        italic_elem = font_elem.find(".//ns:i", self.namespace)
                        if italic_elem is not None:
                            font.italic = italic_elem.get("val", "0") == "1"
                        
                        size_elem = font_elem.find(".//ns:sz", self.namespace)
                        if size_elem is not None:
                            font.size = float(size_elem.get("val", "11"))
                        
                        color_elem = font_elem.find(".//ns:color", self.namespace)
                        if color_elem is not None:
                            rgb = color_elem.get("rgb")
                            if rgb:
                                font.color = Color.from_hex(rgb)
                        
                        name_elem = font_elem.find(".//ns:name", self.namespace)
                        if name_elem is not None:
                            font.name = name_elem.get("val", "Calibri")
                        
                        styles.fonts.append(font)
                
                fills_elem = root.find(".//ns:fills", self.namespace)
                if fills_elem is not None:
                    for fill_elem in fills_elem.findall(".//ns:fill", self.namespace):
                        fill = Fill()
                        
                        pattern_fill_elem = fill_elem.find(".//ns:patternFill", self.namespace)
                        if pattern_fill_elem is not None:
                            fill.fill_type = "pattern"
                            fill.pattern_type = pattern_fill_elem.get("patternType", "none")
                            
                            fg_color_elem = pattern_fill_elem.find(".//ns:fgColor", self.namespace)
                            if fg_color_elem is not None:
                                rgb = fg_color_elem.get("rgb")
                                if rgb:
                                    fill.fg_color = Color.from_hex(rgb)
                            
                            bg_color_elem = pattern_fill_elem.find(".//ns:bgColor", self.namespace)
                            if bg_color_elem is not None:
                                rgb = bg_color_elem.get("rgb")
                                if rgb:
                                    fill.bg_color = Color.from_hex(rgb)
                        
                        styles.fills.append(fill)
                
                borders_elem = root.find(".//ns:borders", self.namespace)
                if borders_elem is not None:
                    for border_elem in borders_elem.findall(".//ns:border", self.namespace):
                        border = Border()
                        
                        for side in ['left', 'right', 'top', 'bottom']:
                            side_elem = border_elem.find(f".//ns:{side}", self.namespace)
                            if side_elem is not None:
                                side_border = SideBorder()
                                side_border.style = side_elem.get("style", "none")
                                
                                color_elem = side_elem.find(".//ns:color", self.namespace)
                                if color_elem is not None:
                                    rgb = color_elem.get("rgb")
                                    if rgb:
                                        side_border.color = Color.from_hex(rgb)
                                
                                setattr(border, side, side_border)
                        
                        styles.borders.append(border)
                
                cell_xfs = root.find(".//ns:cellXfs", self.namespace)
                if cell_xfs is not None:
                    for xf in cell_xfs.findall(".//ns:xf", self.namespace):
                        cell_format = {}
                        
                        font_id = xf.get("fontId")
                        if font_id is not None:
                            idx = int(font_id)
                            if 0 <= idx < len(styles.fonts):
                                cell_format['font'] = styles.fonts[idx]
                        
                        fill_id = xf.get("fillId")
                        if fill_id is not None:
                            idx = int(fill_id)
                            if 0 <= idx < len(styles.fills):
                                cell_format['fill'] = styles.fills[idx]
                        
                        border_id = xf.get("borderId")
                        if border_id is not None:
                            idx = int(border_id)
                            if 0 <= idx < len(styles.borders):
                                cell_format['border'] = styles.borders[idx]
                        
                        styles.cell_formats.append(cell_format)
                
        except KeyError:
            pass
        
        return styles