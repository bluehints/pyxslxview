"""
Formula parser
"""

import re
from typing import Optional, List


class FormulaParser:
    """Parser for Excel formulas"""
    
    FUNCTION_PATTERN = re.compile(r"[A-Z_][A-Z0-9_.]*\(")
    CELL_REF_PATTERN = re.compile(r"\$?[A-Z]+\$?\d+")
    RANGE_REF_PATTERN = re.compile(r"\$?[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+")
    
    def __init__(self):
        self.functions = self._get_builtin_functions()
    
    def _get_builtin_functions(self) -> set:
        """Get built-in Excel functions"""
        return {
            "SUM", "AVERAGE", "COUNT", "MAX", "MIN", "IF", "VLOOKUP", "HLOOKUP",
            "INDEX", "MATCH", "CONCATENATE", "LEFT", "RIGHT", "MID", "LEN",
            "TRIM", "UPPER", "LOWER", "PROPER", "VALUE", "TEXT", "DATE",
            "TODAY", "NOW", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND",
            "ROUND", "ROUNDUP", "ROUNDDOWN", "INT", "ABS", "SQRT", "POWER",
            "LOG", "LN", "EXP", "SIN", "COS", "TAN", "PI", "RAND", "RANDBETWEEN",
            "AND", "OR", "NOT", "ISERROR", "ISBLANK", "ISNUMBER", "ISTEXT",
            "CHOOSE", "OFFSET", "INDIRECT", "ADDRESS", "COLUMN", "ROW",
            "COUNTA", "COUNTBLANK", "COUNTIF", "SUMIF", "AVERAGEIF",
        }
    
    def parse(self, formula: str) -> dict:
        """Parse formula and extract components"""
        if not formula or not formula.startswith("="):
            return {"valid": False, "error": "Formula must start with '='"}
        
        formula_body = formula[1:]
        
        result = {
            "valid": True,
            "original": formula,
            "body": formula_body,
            "functions": self._extract_functions(formula_body),
            "cell_references": self._extract_cell_references(formula_body),
            "range_references": self._extract_range_references(formula_body),
            "operators": self._extract_operators(formula_body),
        }
        
        return result
    
    def _extract_functions(self, formula: str) -> List[str]:
        """Extract function names from formula"""
        matches = self.FUNCTION_PATTERN.findall(formula)
        return list(set(matches))
    
    def _extract_cell_references(self, formula: str) -> List[str]:
        """Extract cell references from formula"""
        matches = self.CELL_REF_PATTERN.findall(formula)
        return list(set(matches))
    
    def _extract_range_references(self, formula: str) -> List[str]:
        """Extract range references from formula"""
        matches = self.RANGE_REF_PATTERN.findall(formula)
        return list(set(matches))
    
    def _extract_operators(self, formula: str) -> List[str]:
        """Extract operators from formula"""
        operators = []
        for char in formula:
            if char in ['+', '-', '*', '/', '^', '&', '=', '<', '>', '<=', '>=', '<>']:
                operators.append(char)
        return list(set(operators))
    
    def evaluate(self, formula: str, context: dict = None) -> Optional[object]:
        """Evaluate formula (simplified implementation)"""
        if context is None:
            context = {}
        
        parsed = self.parse(formula)
        if not parsed["valid"]:
            return None
        
        try:
            return eval(parsed["body"], {"__builtins__": {}}, context)
        except Exception:
            return None