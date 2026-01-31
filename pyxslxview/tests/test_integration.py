"""
Integration tests for pyxslxview
"""

import pytest
from pyxslxview import Document
from pyxslxview.output import ImageOutput, PDFOutput


class TestDocumentLoading:
    """Test document loading"""
    
    def test_document_creation(self):
        """Test document creation"""
        doc = Document()
        assert doc.filepath is None
        assert doc.workbook is None
    
    def test_workbook_creation(self):
        """Test workbook creation"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        assert workbook.worksheets == []
        assert workbook.active_sheet_index == 0
    
    def test_worksheet_creation(self):
        """Test worksheet creation"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        assert worksheet.name == "Sheet1"
        assert len(workbook.worksheets) == 1


class TestCellOperations:
    """Test cell operations"""
    
    def test_cell_value_assignment(self):
        """Test cell value assignment"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.value = "Hello"
        
        assert cell.value == "Hello"
        assert cell.data_type == "string"
    
    def test_cell_number_value(self):
        """Test cell number value"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.value = 42.5
        
        assert cell.value == 42.5
        assert cell.data_type == "number"
    
    def test_cell_boolean_value(self):
        """Test cell boolean value"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.value = True
        
        assert cell.value is True
        assert cell.data_type == "boolean"
    
    def test_cell_formula_value(self):
        """Test cell formula value"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.value = "=SUM(A1:A10)"
        
        assert cell.formula == "=SUM(A1:A10)"
        assert cell.data_type == "formula"


class TestCellStyles:
    """Test cell styles"""
    
    def test_cell_font_style(self):
        """Test cell font style"""
        from pyxslxview.core import Workbook, Color, Font
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.style.font = Font(name="Arial", size=14, bold=True, color=Color.red())
        
        assert cell.style.font.name == "Arial"
        assert cell.style.font.size == 14.0
        assert cell.style.font.bold is True
        assert cell.style.font.color.rgb == Color.red().rgb
    
    def test_cell_alignment_style(self):
        """Test cell alignment style"""
        from pyxslxview.core import Workbook, Alignment
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.style.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        assert cell.style.alignment.horizontal == "center"
        assert cell.style.alignment.vertical == "center"
        assert cell.style.alignment.wrap_text is True
    
    def test_cell_border_style(self):
        """Test cell border style"""
        from pyxslxview.core import Workbook, Border, SideBorder, Color
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.style.border = Border(
            left=SideBorder(style="thin", color=Color.black()),
            right=SideBorder(style="thin", color=Color.black()),
            top=SideBorder(style="thin", color=Color.black()),
            bottom=SideBorder(style="thin", color=Color.black())
        )
        
        assert cell.style.border.has_any_border() is True
    
    def test_cell_fill_style(self):
        """Test cell fill style"""
        from pyxslxview.core import Workbook, Fill, Color
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        cell = worksheet.cell(1, 1)
        cell.style.fill = Fill.solid(Color.get_blue())
        
        assert cell.style.fill.fill_type == "solid"
        assert cell.style.fill.fg_color.rgb == Color.get_blue().rgb


class TestMergedCells:
    """Test merged cells"""
    
    def test_merge_cells(self):
        """Test cell merging"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        worksheet.merge_cells("A1:B2")
        
        assert len(worksheet.merged_cells) == 1
        assert worksheet.merged_cells[0].min_row == 1
        assert worksheet.merged_cells[0].max_row == 2
        assert worksheet.merged_cells[0].min_col == 1
        assert worksheet.merged_cells[0].max_col == 2
    
    def test_cell_is_merged(self):
        """Test cell is merged check"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        worksheet.merge_cells("A1:B2")
        
        cell_a1 = worksheet.cell(1, 1)
        cell_b2 = worksheet.cell(2, 2)
        
        assert cell_a1.is_merged() is True
        assert cell_b2.is_merged() is True
        assert cell_a1.is_merged_parent() is True
        assert cell_b2.is_merged_parent() is False


class TestWorksheetDimensions:
    """Test worksheet dimensions"""
    
    def test_worksheet_dimensions(self):
        """Test worksheet dimensions calculation"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        for row in range(1, 11):
            for col in range(1, 6):
                cell = worksheet.cell(row, col)
                cell.value = f"Cell {row}-{col}"
        
        assert worksheet.max_row == 10
        assert worksheet.max_col == 5


class TestRowColumnOperations:
    """Test row and column operations"""
    
    def test_row_height(self):
        """Test row height"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        row = worksheet.get_row(1)
        row.height = 25.0
        
        assert worksheet.rows[1].height == 25.0
    
    def test_column_width(self):
        """Test column width"""
        from pyxslxview.core import Workbook
        workbook = Workbook()
        worksheet = workbook.add_worksheet("Sheet1")
        
        col = worksheet.get_column(1)
        col.width = 15.0
        
        assert worksheet.columns[1].width == 15.0


class TestImageOutput:
    """Test image output"""
    
    def test_image_output_creation(self):
        """Test image output creation"""
        output = ImageOutput(scale=1.0, dpi=96)
        assert output.scale == 1.0
        assert output.dpi == 96


class TestPDFOutput:
    """Test PDF output"""
    
    def test_pdf_output_creation(self):
        """Test PDF output creation"""
        output = PDFOutput(scale=1.0)
        assert output.scale == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])