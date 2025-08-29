# Typst CV Template

A modular CV template built with Typst featuring YAML-based data management and configurable output variants.

## Features

- **Modular data structure** - Separate content from presentation using YAML files
- **Multiple variants** - Generate academic, industry, or short CVs from the same data
- **Configurable formatting** - Control styling, publication formats, and section filtering through variant configs
- **Publication management** - Automatic author name bolding, citation links, and variant-specific filtering
- **Easy compilation** - Simple Makefile commands for all variants

## Requirements

- [Typst](https://github.com/typst/typst) (latest version)
- FontAwesome package (`@preview/fontawesome:0.6.0`)
- Datify package (`@preview/datify:0.1.4`)

## Quick Start

```bash
# Clone and build academic CV
git clone <repo-url>
cd resume-typst
make academic

# Build all variants
make all

# Development with auto-reload
make watch
```

## Project Structure

```
├── build/
│   └── cv.typ              # Main template file
├── data/
│   ├── config.yaml         # Global styling configuration
│   ├── personal.yaml       # Contact information
│   ├── sections/           # Modular content sections
│   │   ├── experience.yaml
│   │   ├── education.yaml
│   │   ├── publication.yaml
│   │   └── ...
│   └── variants/           # Output variant configurations
│       ├── academic.yaml
│       ├── industry.yaml
│       └── short.yaml
├── lib/                    # Template components
└── out/                    # Generated PDFs
```

## Usage

### Build Commands

```bash
make academic    # Full academic CV
make industry    # Industry-focused CV with filtered publications
make short       # Condensed 1-2 page version
make all         # Build all variants
make clean       # Remove generated PDFs
```

### Customization

**Edit your data:**
```bash
# Update personal information
vim data/personal.yaml

# Add publications, experience, etc.
vim data/sections/publication.yaml
```

**Modify variants:**
```bash
# Change which sections appear in industry CV
vim data/variants/industry.yaml

# Adjust styling and formatting
vim data/config.yaml
```

### Variant Differences

- **Academic**: Complete CV with all sections, full author lists, paper links
- **Industry**: Filtered publications (max 5), abbreviated author names, no links
- **Short**: Essential sections only for quick applications

## Data Format

Each section uses structured YAML. Example publication:

```yaml
papers:
  - title: "Your Paper Title"
    authors: ["Your Name", "Co-author"]
    year: 2024
    venue: "Conference Name"
    link: "https://..."
```

The template automatically bolds your name in author lists and applies variant-specific formatting.

## Configuration

**Global settings** (`data/config.yaml`):
- Typography (fonts, sizes)
- Layout (margins, spacing)
- Colors and styling

**Variant settings** (`data/variants/*.yaml`):
- Section ordering
- Publication filtering
- Formatting options

## Advanced Features

- **Publication filtering**: Prefer first-author papers, limit entry count
- **Variant-aware formatting**: Brief vs full author lists, link inclusion
- **Flexible data structure**: Easy to add new sections or modify existing ones
- **Watch mode**: Auto-recompile during development

## Troubleshooting

**Compilation errors**: Ensure all YAML files have valid syntax and required fields.

**Missing sections**: Check that section names in variant configs match data files.

**Font issues**: Verify required packages are installed or modify font settings in config.yaml.

## License

MIT License - see LICENSE file for details.