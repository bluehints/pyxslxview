# pyxslxview

High-fidelity XLSX file preview library for Python.

## Features

- High-fidelity rendering of XLSX files
- Support for cell styles, fonts, colors, borders, and fills
- Multiple output formats: Image (PNG, JPEG), PDF, Print
- Comprehensive cell merging and conditional formatting support
- Pagination for large worksheets
- Easy-to-use API

## Installation

```bash
pip install pyxslxview
```

For PDF output support:

```bash
pip install pyxslxview[pdf]
```

## Quick Start

```python
from pyxslxview import Document
from pyxslxview.output import ImageOutput

# Load an XLSX file
doc = Document("example.xlsx")

# Render to image
output = ImageOutput(scale=2.0, dpi=96)
output.render(doc.active_sheet, "output.png")
```

## Usage

### Loading Documents

```python
from pyxslxview import Document

# Load from file
doc = Document("workbook.xlsx")

# Access workbook and worksheets
workbook = doc.workbook
worksheet = workbook.active_sheet

# Iterate through worksheets
for sheet in workbook.worksheets:
    print(sheet.name)
```

### Working with Cells

```python
# Get cell by reference
cell = worksheet.cell("A1")

# Get cell by row and column (1-indexed)
cell = worksheet.cell(1, 1)

# Access cell properties
print(cell.value)
print(cell.data_type)
print(cell.coordinate)

# Modify cell value
cell.value = "Hello, World!"
```

### Cell Styles

```python
from pyxslxview.core import Color, Font, Alignment, Border, Fill

# Set font
cell.style.font = Font(
    name="Arial",
    size=14,
    bold=True,
    italic=False,
    color=Color.red()
)

# Set alignment
cell.style.alignment = Alignment(
    horizontal="center",
    vertical="center",
    wrap_text=True
)

# Set border
cell.style.border = Border(
    left=SideBorder(style="thin", color=Color.black()),
    right=SideBorder(style="thin", color=Color.black()),
    top=SideBorder(style="thin", color=Color.black()),
    bottom=SideBorder(style="thin", color=Color.black())
)

# Set fill
cell.style.fill = Fill.solid(Color.get_blue())
```

### Merged Cells

```python
# Merge cells
worksheet.merge_cells("A1:B2")

# Check if cell is merged
cell = worksheet.cell("A1")
if cell.is_merged():
    print("Cell is part of a merged range")
```

### Output Formats

#### Image Output

```python
from pyxslxview.output import ImageOutput

output = ImageOutput(scale=2.0, dpi=96)

# Render entire worksheet
output.render(worksheet, "output.png")

# Render single page
from pyxslxview.layout import Paginator
paginator = Paginator(worksheet)
pages = paginator.paginate()
output.render_page(worksheet, pages[0], "page1.png")
```

#### PDF Output

```python
from pyxslxview.output import PDFOutput

output = PDFOutput(scale=1.0)
output.render(worksheet, "output.pdf")
```

#### Print Output

```python
from pyxslxview.output import PrintOutput

output = PrintOutput(scale=1.0, dpi=300)

# Get page count
page_count = output.get_page_count(worksheet)
print(f"Total pages: {page_count}")

# Print pages
output.print_pages(worksheet, printer_name="MyPrinter")

# Preview pages
previews = output.preview_pages(worksheet)
```

## Development

### Running Tests

```bash
pytest pyxslxview/tests/
```

### Code Quality

```bash
# Linting
flake8 pyxslxview/

# Type checking
mypy pyxslxview/

# Formatting
black pyxslxview/
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.