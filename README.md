# pyxslxview

High-fidelity XLSX file preview library for Python.

## Features

- High-fidelity XLSX file rendering
- Support for cell styles (fonts, colors, borders, fills)
- Support for formula calculation and display
- Support for charts, images, and other objects
- Support for merged cells
- Support for conditional formatting
- Support for data bars, color scales, icon sets
- Support for print layout and pagination preview
- Cross-platform support (Windows, Linux, macOS)

## Installation

```bash
pip install pyxslxview
```

## Quick Start

```python
from pyxslxview import Document

# Load an XLSX file
doc = Document("example.xlsx")

# Get the first worksheet
worksheet = doc.workbook.worksheets[0]

# Render to image
from pyxslxview.output import ImageOutput
output = ImageOutput()
output.render(worksheet, "output.png")
```

## Documentation

See the [docs](docs/) directory for detailed documentation.

## License

MIT License