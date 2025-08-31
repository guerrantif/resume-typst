# resumyst

Generate professional CVs from YAML data using Typst templates.

> **Alpha Software**: This project is in early development. Features may change and bugs are expected. Always review generated CVs before submitting them.

|Academic|Industry|Short|
|:-:|:-:|:-:|
|![academic CV](out/png/cv-academic-1.png)|![industry CV](out/png/cv-industry-1.png)|![short CV](out/png/cv-short-1.png)|

A modern CV generation system that combines Typst templating with Python CLI convenience. Generate multiple CV variants from a single YAML data source.

## Features

- Multiple variants: Academic, industry, and compact formats
- Interactive project setup wizard
- Live preview server with auto-reload
- Data validation with helpful error messages
- Interactive content editor
- Intelligent filtering with `exclude_from` flags
- PDF and PNG output formats

## Installation

```bash
pip install resumyst
```

Typst will be automatically installed when first needed, or you can install it manually beforehand from [typst.app](https://typst.app/docs/installation/).

## Quick Start

### Interactive Setup

```bash
# Create new CV project
resumyst init my-cv
cd my-cv

# Edit your data
resumyst edit

# Live preview
resumyst serve

# Build CV
resumyst build academic
```

### Direct Usage

```bash
# Skip wizard, use defaults
resumyst init my-cv --quick

# Build specific variant
resumyst build industry

# Build all variants
resumyst build --all

# Watch for changes
resumyst build academic --watch
```

## Project Structure

```
my-cv/
├── data/
│   ├── config.yaml          # Global styling
│   ├── personal.yaml        # Contact info
│   ├── sections/             # CV content
│   │   ├── experience.yaml
│   │   ├── education.yaml
│   │   └── ...
│   └── variants/             # Variant settings
│       ├── academic.yaml
│       ├── industry.yaml
│       └── short.yaml
├── typst/                    # Template files
└── out/                      # Generated outputs
    ├── pdf/
    └── png/
```

## CV Variants

**Academic** - Complete CV with all publications, teaching, and academic activities
**Industry** - Professional focus with selected publications and practical experience
**Short** - Compact 1-2 page version for quick applications

Control what appears in each variant using `exclude_from` flags in your YAML files:

```yaml
# This entry appears in all variants
- title: "Important Publication"
  year: 2024

# This entry is excluded from short variant
- title: "Minor Publication"
  year: 2023
  exclude_from: ["short"]
```

## Commands

- `resumyst init [name]` - Create new CV project
- `resumyst edit` - Interactive content editor
- `resumyst build [variant]` - Build CV (academic/industry/short)
- `resumyst serve` - Start live preview server
- `resumyst validate` - Validate YAML data
- `resumyst clean` - Remove build outputs

## Configuration

Edit `data/config.yaml` to customize typography, spacing, colors, and formatting:

```yaml
typography:
  fonts:
    text: "Libertinus Serif"
  sizes:
    body: 11.2pt

colors:
  link: "#0645ad"

formatting:
  date_format: "MMM YYYY"
  show_location: true
```

## Template Customization

Modify Typst template files in the `typst/` directory:
- `typst/styles.typ` - Typography and layout
- `typst/components.typ` - UI elements
- `typst/renderers.typ` - Section formatting

## Auto-Installation

Resumyst automatically installs Typst using platform-appropriate package managers:

- **Windows**: winget, Cargo
- **macOS**: Homebrew, Cargo  
- **Linux**: Cargo (APT/Snap require manual installation for security)

Disable auto-installation: `resumyst build academic --no-auto-install`

## Development

```bash
git clone https://github.com/guerrantif/resumyst.git
cd resumyst
pip install -e .
resumyst --help
```

## Requirements

- Python 3.10+
- Typst (auto-installed)

## License

MIT License - see LICENSE file for details.