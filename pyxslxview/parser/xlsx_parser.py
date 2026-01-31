"""
XLSX file parser
"""

import zipfile
import xml.etree.ElementTree as ET

from ..core.document import Document
from ..core.workbook import Workbook
from ..core.worksheet import Worksheet
from ..core.cell import Cell
from ..core.styles import CellStyle
from ..core.alignment import Alignment
from .shared_strings import SharedStringsParser
from .styles import StylesParser


class XLSXParser:
    """XLSX file parser"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.shared_strings_parser = SharedStringsParser()
        self.styles_parser = StylesParser()
        self.namespace = {
            'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
    
    def parse(self) -> Document:
        """Parse XLSX file"""
        with zipfile.ZipFile(self.filepath, 'r') as zf:
            doc = Document(self.filepath)
            
            doc.shared_strings = self.shared_strings_parser.parse(zf)
            doc.styles = self.styles_parser.parse(zf)
            
            doc.workbook = self._parse_workbook(zf)
            self._parse_worksheets(zf, doc)
            
            return doc
    
    def _parse_workbook(self, zf: zipfile.ZipFile) -> Workbook:
        """Parse workbook"""
        workbook = Workbook()
        
        try:
            with zf.open("xl/workbook.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                sheets = root.findall(".//ns:sheets/ns:sheet", self.namespace)
                for sheet in sheets:
                    name = sheet.get("name", f"Sheet{len(workbook.worksheets) + 1}")
                    ws = Worksheet(name=name, workbook=workbook)
                    ws.sheet_id = sheet.get("sheetId")
                    ws.r_id = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                    workbook.worksheets.append(ws)
                
        except KeyError:
            pass
        
        return workbook
    
    def _parse_worksheets(self, zf: zipfile.ZipFile, doc: Document):
        """Parse worksheets"""
        try:
            with zf.open("xl/workbook.xml") as f:
                ET.parse(f)
                
                rels = self._parse_relationships(zf)
                
                for ws in doc.workbook.worksheets:
                    if hasattr(ws, 'r_id') and ws.r_id in rels:
                        target = rels[ws.r_id]
                        self._parse_worksheet_data(zf, target, ws, doc)
        
        except KeyError:
            pass
    
    def _parse_relationships(self, zf: zipfile.ZipFile) -> dict:
        """Parse relationships"""
        rels = {}
        
        try:
            with zf.open("xl/_rels/workbook.xml.rels") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                for rel in root.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
                    rel_id = rel.get("Id")
                    target = rel.get("Target")
                    rels[rel_id] = target
                
        except KeyError:
            pass
        
        return rels
    
    def _parse_worksheet_data(self, zf: zipfile.ZipFile, target: str, worksheet: Worksheet, doc: Document):
        """Parse worksheet data"""
        try:
            with zf.open(f"xl/{target}") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                sheet_data = root.find(".//ns:sheetData", self.namespace)
                
                if sheet_data is not None:
                    for row_elem in sheet_data.findall(".//ns:row", self.namespace):
                        
                        for cell_elem in row_elem.findall(".//ns:c", self.namespace):
                            cell_ref = cell_elem.get("r", "")
                            row, col = self._parse_cell_reference(cell_ref)
                            
                            cell = worksheet.cell(row, col)
                            
                            v_elem = cell_elem.find(".//ns:v", self.namespace)
                            if v_elem is not None and v_elem.text:
                                value = v_elem.text
                                
                                if value.startswith("0"):
                                    try:
                                        idx = int(value)
                                        value = doc.shared_strings[idx]
                                    except (ValueError, IndexError):
                                        pass
                                
                                cell.value = value
                                
                                t_elem = cell_elem.get("t", "s")
                                if t_elem == "s":
                                    try:
                                        style_idx = int(v_elem.text)
                                        if 0 <= style_idx < len(doc.styles.cell_formats):
                                            cell.style = doc.styles.cell_formats[style_idx]
                                    except (ValueError, IndexError):
                                        pass
        except KeyError:
            pass
    
    def _parse_cell_reference(self, ref: str):
        """Parse cell reference (e.g., 'A1') to row, col"""
        col_str = ""
        row_str = ""
        
        for char in ref:
            if char.isalpha():
                col_str += char
            elif char.isdigit():
                row_str += char
        
        col = 0
        for char in col_str:
            col = col * 26 + (ord(char.upper()) - ord('A') + 1)
        
        row = int(row_str)
        return (row, col)