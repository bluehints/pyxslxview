"""
Unit conversion utilities
"""


class Units:
    """Unit conversion utilities"""
    
    POINTS_PER_INCH = 72.0
    POINTS_PER_CM = 28.35
    POINTS_PER_MM = 2.835
    PIXELS_PER_POINT = 1.333
    
    @staticmethod
    def inches_to_points(inches: float) -> float:
        """Convert inches to points"""
        return inches * Units.POINTS_PER_INCH
    
    @staticmethod
    def points_to_inches(points: float) -> float:
        """Convert points to inches"""
        return points / Units.POINTS_PER_INCH
    
    @staticmethod
    def cm_to_points(cm: float) -> float:
        """Convert centimeters to points"""
        return cm * Units.POINTS_PER_CM
    
    @staticmethod
    def points_to_cm(points: float) -> float:
        """Convert points to centimeters"""
        return points / Units.POINTS_PER_CM
    
    @staticmethod
    def mm_to_points(mm: float) -> float:
        """Convert millimeters to points"""
        return mm * Units.POINTS_PER_MM
    
    @staticmethod
    def points_to_mm(points: float) -> float:
        """Convert points to millimeters"""
        return points / Units.POINTS_PER_MM
    
    @staticmethod
    def pixels_to_points(pixels: float, dpi: int = 96) -> float:
        """Convert pixels to points"""
        return pixels / dpi * Units.POINTS_PER_INCH
    
    @staticmethod
    def points_to_pixels(points: float, dpi: int = 96) -> float:
        """Convert points to pixels"""
        return points * dpi / Units.POINTS_PER_INCH
    
    @staticmethod
    def twips_to_points(twips: float) -> float:
        """Convert twips to points (1 twip = 1/20 point)"""
        return twips / 20.0
    
    @staticmethod
    def points_to_twips(points: float) -> float:
        """Convert points to twips"""
        return points * 20.0
    
    @staticmethod
    def excel_column_width_to_pixels(width: float) -> float:
        """Convert Excel column width to pixels"""
        return (width * 7.0 + 0.5) * Units.PIXELS_PER_POINT
    
    @staticmethod
    def pixels_to_excel_column_width(pixels: float) -> float:
        """Convert pixels to Excel column width"""
        return (pixels / Units.PIXELS_PER_POINT - 0.5) / 7.0
    
    @staticmethod
    def excel_row_height_to_points(height: float) -> float:
        """Convert Excel row height to points"""
        return height
    
    @staticmethod
    def points_to_excel_row_height(points: float) -> float:
        """Convert points to Excel row height"""
        return points