"""
Shared strings parser
"""

import zipfile
import xml.etree.ElementTree as ET
from typing import List, Optional


class SharedStringsParser:
    """Parser for shared strings table"""
    
    def __init__(self):
        self.strings: List[str] = []
    
    def parse(self, zf: zipfile.ZipFile) -> List[str]:
        """Parse shared strings from XLSX file"""
        try:
            with zf.open("xl/sharedStrings.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                namespace = {
                    'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
                }
                
                for si in root.findall(".//ns:si", namespace):
                    text_parts = []
                    
                    for t in si.findall(".//ns:t", namespace):
                        if t.text:
                            text_parts.append(t.text)
                    
                    self.strings.append("".join(text_parts))
                
                return self.strings
                
        except KeyError:
            return []
    
    def get_string(self, index: int) -> Optional[str]:
        """Get shared string by index"""
        if 0 <= index < len(self.strings):
            return self.strings[index]
        return None