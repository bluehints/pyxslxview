"""
Tests for pyxslxview
"""

import pytest
from pyxslxview.core import Color, Font, Alignment, Border, Fill, CellStyle
from pyxslxview.utils import Units, Helpers, Cache


class TestColor:
    """Test Color class"""
    
    def test_color_creation(self):
        """Test color creation"""
        color = Color(red=255, green=0, blue=0)
        assert color.red == 255
        assert color.green == 0
        assert color.blue == 0
        assert color.alpha == 255
    
    def test_color_from_hex(self):
        """Test color from hex string"""
        color = Color.from_hex("#FF0000")
        assert color.red == 255
        assert color.green == 0
        assert color.blue == 0
    
    def test_color_from_rgb(self):
        """Test color from RGB values"""
        color = Color.from_rgb(0, 255, 0)
        assert color.red == 0
        assert color.green == 255
        assert color.blue == 0
    
    def test_color_hex_property(self):
        """Test color hex property"""
        color = Color(red=255, green=128, blue=64)
        assert color.hex == "#ff8040"
    
    def test_color_presets(self):
        """Test color presets"""
        assert Color.black().rgb == (0, 0, 0)
        assert Color.white().rgb == (255, 255, 255)
        assert Color.get_red().rgb == (255, 0, 0)
        assert Color.get_green().rgb == (0, 255, 0)
        assert Color.get_blue().rgb == (0, 0, 255)


class TestFont:
    """Test Font class"""
    
    def test_font_creation(self):
        """Test font creation"""
        font = Font(name="Arial", size=12, bold=True)
        assert font.name == "Arial"
        assert font.size == 12.0
        assert font.bold is True
        assert font.italic is False


class TestAlignment:
    """Test Alignment class"""
    
    def test_alignment_creation(self):
        """Test alignment creation"""
        alignment = Alignment(horizontal="center", vertical="middle", wrap_text=True)
        assert alignment.horizontal == "center"
        assert alignment.vertical == "middle"
        assert alignment.wrap_text is True


class TestBorder:
    """Test Border class"""
    
    def test_border_creation(self):
        """Test border creation"""
        border = Border()
        assert border.left.style == "none"
        assert border.right.style == "none"
        assert border.top.style == "none"
        assert border.bottom.style == "none"
    
    def test_border_visibility(self):
        """Test border visibility"""
        from pyxslxview.core.border import SideBorder
        border = Border(
            left=SideBorder(style="thin", color=Color.get_red()),
            right=SideBorder(style="medium", color=Color.get_blue())
        )
        assert border.has_any_border() is True
        assert border.left.is_visible() is True
        assert border.right.is_visible() is True


class TestFill:
    """Test Fill class"""
    
    def test_fill_solid(self):
        """Test solid fill"""
        fill = Fill(fill_type="solid", fg_color=Color.get_red())
        assert fill.fill_type == "solid"
        assert fill.fg_color.rgb == Color.get_red().rgb
    
    def test_fill_solid_method(self):
        """Test solid fill method"""
        fill = Fill.solid(Color.get_blue())
        assert fill.fill_type == "solid"
        assert fill.fg_color.rgb == Color.get_blue().rgb


class TestCellStyle:
    """Test CellStyle class"""
    
    def test_cell_style_creation(self):
        """Test cell style creation"""
        style = CellStyle()
        assert style.font.name == "Calibri"
        assert style.alignment.horizontal == "left"
        assert style.alignment.vertical == "bottom"


class TestUnits:
    """Test Units class"""
    
    def test_inches_to_points(self):
        """Test inches to points conversion"""
        assert Units.inches_to_points(1.0) == 72.0
        assert Units.inches_to_points(2.0) == 144.0
    
    def test_points_to_inches(self):
        """Test points to inches conversion"""
        assert Units.points_to_inches(72.0) == 1.0
        assert Units.points_to_inches(144.0) == 2.0
    
    def test_cm_to_points(self):
        """Test centimeters to points conversion"""
        result = Units.cm_to_points(1.0)
        assert abs(result - 28.35) < 0.1
    
    def test_pixels_to_points(self):
        """Test pixels to points conversion"""
        result = Units.pixels_to_points(96, dpi=96)
        assert abs(result - 72.0) < 0.1


class TestHelpers:
    """Test Helpers class"""
    
    def test_parse_cell_reference(self):
        """Test cell reference parsing"""
        row, col = Helpers.parse_cell_reference("A1")
        assert row == 1
        assert col == 1
        
        row, col = Helpers.parse_cell_reference("B10")
        assert row == 10
        assert col == 2
    
    def test_tuple_to_cell_reference(self):
        """Test tuple to cell reference"""
        ref = Helpers.tuple_to_cell_reference(1, 1)
        assert ref == "A1"
        
        ref = Helpers.tuple_to_cell_reference(10, 2)
        assert ref == "B10"
    
    def test_parse_range_reference(self):
        """Test range reference parsing"""
        row1, col1, row2, col2 = Helpers.parse_range_reference("A1:B10")
        assert row1 == 1
        assert col1 == 1
        assert row2 == 10
        assert col2 == 2
    
    def test_get_column_letter(self):
        """Test get column letter"""
        assert Helpers.get_column_letter(1) == "A"
        assert Helpers.get_column_letter(26) == "Z"
        assert Helpers.get_column_letter(27) == "AA"
    
    def test_get_column_number(self):
        """Test get column number"""
        assert Helpers.get_column_number("A") == 1
        assert Helpers.get_column_number("Z") == 26
        assert Helpers.get_column_number("AA") == 27
    
    def test_clamp(self):
        """Test clamp function"""
        assert Helpers.clamp(5, 0, 10) == 5
        assert Helpers.clamp(-5, 0, 10) == 0
        assert Helpers.clamp(15, 0, 10) == 10
    
    def test_lerp(self):
        """Test linear interpolation"""
        assert Helpers.lerp(0, 10, 0.5) == 5.0
        assert Helpers.lerp(0, 100, 0.25) == 25.0


class TestCache:
    """Test Cache class"""
    
    def test_cache_set_get(self):
        """Test cache set and get"""
        cache = Cache(max_size=10)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_cache_remove(self):
        """Test cache remove"""
        cache = Cache(max_size=10)
        cache.set("key1", "value1")
        cache.remove("key1")
        assert cache.get("key1") is None
    
    def test_cache_clear(self):
        """Test cache clear"""
        cache = Cache(max_size=10)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.size() == 0
    
    def test_cache_size(self):
        """Test cache size"""
        cache = Cache(max_size=10)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.size() == 2


class TestCell:
    """Test Cell class"""
    
    def test_cell_creation(self):
        """Test cell creation"""
        from pyxslxview.core.workbook import Workbook
        from pyxslxview.core.worksheet import Worksheet
        from pyxslxview.core.cell import Cell
        
        workbook = Workbook()
        worksheet = Worksheet(name="Sheet1", workbook=workbook)
        cell = Cell(row=1, col=1, worksheet=worksheet, value="Test")
        
        assert cell.row == 1
        assert cell.col == 1
        assert cell.value == "Test"
        assert cell.data_type == "string"
    
    def test_cell_coordinate(self):
        """Test cell coordinate"""
        from pyxslxview.core.workbook import Workbook
        from pyxslxview.core.worksheet import Worksheet
        from pyxslxview.core.cell import Cell
        
        workbook = Workbook()
        worksheet = Worksheet(name="Sheet1", workbook=workbook)
        cell = Cell(row=1, col=1, worksheet=worksheet)
        
        assert cell.coordinate == "A1"
        
        cell = Cell(row=10, col=26, worksheet=worksheet)
        assert cell.coordinate == "Z10"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])