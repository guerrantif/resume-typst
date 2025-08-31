# resumyst ✨

**Conjure the perfect CV with Typst magic** - transform YAML data into professional documents.

|Academic|Industry|Short|
|:-:|:-:|:-:|
|![academic CV](out/png/cv-academic-1.png)|![industry CV](out/png/cv-industry-1.png)|![short CV](out/png/cv-short-1.png)|

A modern, hybrid CV generation system that combines the power of Typst templating with Python CLI convenience. Generate multiple CV variants from a single data source with intelligent filtering and beautiful typography.

## Features

- **🎯 Multiple Variants**: Academic, industry, and ultra-compact formats
- **🧙 Interactive Wizard**: Guided project setup for beginners
- **⚡ Live Preview**: Real-time server with auto-reload
- **✅ Smart Validation**: Helpful error messages and data checking
- **📝 Interactive Editor**: Menu-driven content editing
- **🎨 Intelligent Filtering**: `exclude_from` flags for precise control
- **🚀 Zero Config**: Works out of the box, customize when needed
- **📱 Modern Output**: PDF and PNG generation

## Installation

```bash
pip install resumyst
```

**Prerequisites**: Install [Typst](https://typst.app/docs/installation/) first.

## Quick Start

### Interactive Mode

```bash
# Create a new CV project with guided setup
resumyst init my-cv
cd my-cv

# Interactive content editing
resumyst edit

# Live preview with auto-reload
resumyst serve

# Build specific variant
resumyst build academic
```

### Direct Mode

```bash
# Initialize with minimal setup
resumyst init my-cv --quick
cd my-cv

# Build all variants
resumyst build --all

# Validate data before building
resumyst validate
```

### Make Commands (Traditional workflow)

```bash
make academic    # Full academic CV
make industry    # Industry-focused CV  
make short       # Ultra-compact CV
make all         # Build all variants
make watch       # Live development mode
make clean       # Remove generated files
```

## Architecture Overview

### Single Source of Truth → Template System → Multiple Outputs**

```txt
data/               Template Layer        Output
├── personal.yaml   ┌─────────────────┐   ├── academic.pdf
├── config.yaml  ───┤ Typst Templates ├───┼── industry.pdf
├── sections/    ───┤  + Smart Filter ├───┼── short.pdf
└── variants/    ───┤     System      ├───└── *.png
                    └─────────────────┘
```

### Core Design Principles

- **Configuration Hierarchy**: Base config + variant overrides = final config
- **Smart Filtering**: `exclude_from` flags for precise content control
- **Template Modularity**: Separate concerns across focused files
- **Hybrid Architecture**: Python CLI + direct Typst access

## Project Structure

```bash
my-cv/
├── build/
│   └── cv.typ              # 17-line build coordinator
├── data/
│   ├── config.yaml         # Typography, colors, layout
│   ├── personal.yaml       # Contact information
│   ├── sections/           # Content modules
│   │   ├── experience.yaml
│   │   ├── education.yaml
│   │   ├── publication.yaml
│   │   ├── awards.yaml
│   │   ├── skills.yaml
│   │   └── ...
│   └── variants/           # Variant-specific settings
│       ├── academic.yaml   # Complete academic CV
│       ├── industry.yaml   # Industry-focused
│       └── short.yaml      # Ultra-compact
├── lib/                    # Template system
│   ├── template.typ        # Main template logic
│   ├── config.typ          # Configuration merging
│   ├── data.typ           # Data loading & filtering
│   ├── components.typ      # Reusable UI components
│   ├── renderers.typ       # Section renderers
│   └── styles.typ          # Typography utilities
└── out/                    # Generated PDFs and PNGs
```

## CLI Commands

### Project Management

```bash
resumyst init <project>     # Create new CV project
resumyst init --quick       # Skip interactive wizard
resumyst clean              # Remove generated files
```

### Development Workflow

```bash
resumyst build <variant>    # Build specific variant
resumyst build --all        # Build all variants
resumyst build --no-png     # Skip PNG generation
resumyst build --no-validate # Skip validation
resumyst validate           # Check data integrity
resumyst serve              # Live preview server
resumyst serve --port 8080  # Custom port
resumyst edit               # Interactive content editor
```

## Intelligent Filtering System

### The `exclude_from` Flag

Control exactly where each item appears using simple flags:

```yaml
# data/sections/publication.yaml
papers:
  - title: "Advanced Research Methods"
    authors: ["Alice Wonderland", "Eve Explorer"]
    year: 2024
    venue: "Conference on Marginally Useful Algorithms (CMUA)"
    # No exclude_from = appears in ALL variants
    
  - title: "Specialized Academic Methods"
    authors: ["Alice Wonderland", "Grace Hopper-Like"]
    year: 2023
    venue: "International Journal of Unimportant Thoughts (IJUT)"
    exclude_from: ["industry", "short"]  # Academic only
    
  - title: "Foundational Techniques"
    authors: ["Alice Wonderland", "Oscar Algorithm"]  
    year: 2020
    venue: "Proceedings of Dubious Research Excellence (PDRE)"
    exclude_from: ["short"]  # Skip in ultra-compact
```

### Smart Sorting Logic

- **Publications**: Year priority + first-author boost
- **Experience**: Most recent positions first
- **Education**: Most recent degrees first

## Variant Comparison

| Feature | Academic | Industry | Short |
|---------|----------|----------|--------|
| **Target** | Complete record | Practical focus | Ultra-compact |
| **Publications** | All papers | Max 5, filtered | Max 3, recent |
| **Experience** | All positions | All positions | Max 2, recent |
| **Education** | All degrees | All degrees | Max 2, recent |
| **Details** | Full bullets | Full bullets | **Hidden** |
| **Links** | ✅ Paper links | ❌ Clean | ❌ Print-ready |
| **Author Lists** | Complete | "et al." format | "et al." format |
| **Spacing** | Standard | Standard | **40% tighter** |
| **Use Case** | Academic jobs | Industry roles | Networking events |

## Data Format Examples

### Personal Information

```yaml
# data/personal.yaml
name:
  full: "Dr. Alice Wonderland"
  variants: ["Alice Wonderland", "A. Wonderland", "Wonderland, A."]

contact:
  email: "alice.wonderland@university.eu"
  website: "https://example.com/~alicewonderland" 
  location: "Berlin, Germany"
```

### Publications

```yaml
# data/sections/publication.yaml
papers:
  - id: "paper_2024"
    title: "Novel Methods for Data Analysis and Processing"
    authors: ["Alice Wonderland", "Bob Builder", "Charlie Chocolate"]
    year: 2024
    venue: "International Conference on Negligible Research (ICNR)"
    link: "https://example.com/paper1"
    # Appears in all variants (no exclude_from)
    
  - id: "niche_paper"
    title: "Advanced Techniques for Specialized Applications"
    authors: ["Alice Wonderland", "Max Planck-ish"]
    year: 2023
    venue: "Journal of Questionable AI Advances (JQAIA)"
    link: "https://example.com/paper2"
    exclude_from: ["industry", "short"]  # Academic only
```

### Experience

```yaml
# data/sections/experience.yaml
positions:
  - id: "current_position"
    position: "Research Scientist" 
    company: "Tech Company"
    start_date: "2023-01"
    end_date: "present"
    location: "Berlin, Germany"
    details:
      - "Led team developing novel AI architectures"
      - "Published 5 papers in top-tier conferences"
      - "Mentored 3 junior researchers"
```

## Configuration System

### Hierarchy: Base + Variant = Final Config

```yaml
# data/config.yaml (base typography and styling)
typography:
  font_size: 11pt
  heading_color: rgb(0, 0, 128)
  spacing: 1.2em

# data/variants/short.yaml (variant-specific overrides)
formatting:
  compact_spacing: true      # 40% reduced spacing
  hide_details: true         # Remove bullet points  
  include_paper_links: false # Clean, print-ready

filters:
  publications:
    max_entries: 3           # Only top 3 papers
  experience: 
    max_entries: 2           # Only 2 most recent
```

## Advanced Features

### Live Preview Server

```bash
resumyst serve
# → Opens http://localhost:8000
# → Auto-reloads on file changes
# → Serves PDFs with proper headers
# → File watcher monitors data/ directory
```

### Interactive Editor

```bash
resumyst edit
# → Menu-driven interface for editing CV content
# → Built-in validation with helpful error messages
# → Rich terminal UI with color and formatting
```

### Validation System

```bash
resumyst validate
# → Comprehensive YAML structure validation
# → Checks required fields and data types
# → Helpful error messages with file locations
# → Validates all sections and configurations
```

## Template System Details

### Clean Architecture

- **`template.typ`**: Main template combining section renderers
- **`data.typ`**: Data loading with intelligent filtering
- **`config.typ`**: Simple configuration merging
- **`renderers.typ`**: Section-specific rendering logic
- **`components.typ`**: Reusable UI elements
- **`styles.typ`**: Typography and formatting utilities

### Section Configuration

```typst
// Single source of truth in template.typ
let sections_config = (
  awards: ("Awards & Scholarships", render-awards),
  education: ("Education", render-education), 
  experience: ("Experience", render-experience),
  publication: ("Publications", render-publications),
  // ... other sections
)
```

## Python CLI Architecture

Built with modern Python practices:

- **Click**: Command-line interface framework
- **Rich**: Beautiful terminal output and progress indicators
- **PyYAML**: Configuration and data file parsing
- **Watchdog**: File system monitoring for live reload
- **Type Hints**: Full type safety with Python 3.10+ syntax

### Key Components

- **`cli.py`**: Main command interface
- **`wizard.py`**: Interactive project setup
- **`validator.py`**: Comprehensive data validation
- **`server.py`**: Live preview HTTP server
- **`editor.py`**: Interactive content editing

## Troubleshooting

### Build Errors

```bash
# Check YAML syntax
resumyst validate

# Detailed error output
resumyst build academic --no-validate 2>&1 | head -20

# Test Typst directly
typst compile build/cv.typ --input variant=academic
```

### Common Issues

**Empty sections**:

- Check `exclude_from` flags aren't too restrictive
- Verify section names match between data and config files

**Missing content**:

- Ensure required fields are present (run `resumyst validate`)
- Check variant filter settings (max_entries, date ranges)

**Styling problems**:

- Confirm Typst packages are installed (`@preview/fontawesome`, `@preview/datify`)
- Verify config.yaml syntax with a YAML validator

**Server issues**:

- Check port availability (default 8000)
- Ensure file permissions allow reading data/ directory

## Extending the System

### Adding New Sections

1. Create YAML data file in `data/sections/new_section.yaml`
2. Add renderer function to `lib/renderers.typ`
3. Register in `sections_config` dictionary in `lib/template.typ`
4. Add to section order in variant configs

### Custom Variants

1. Create new variant file in `data/variants/custom.yaml`
2. Define filtering rules and formatting options
3. Build with `resumyst build custom`

### Template Customization

- Modify `lib/styles.typ` for typography changes
- Edit `lib/components.typ` for UI elements
- Customize `lib/renderers.typ` for section-specific formatting

## Development

### Running from Source

```bash
git clone https://github.com/guerrantif/resumyst.git
cd resumyst
pip install -e .
resumyst --help
```

### Project Standards

- **Python 3.10+**: Modern type hints with built-in union syntax
- **Type Safety**: Full type annotations throughout
- **Rich Output**: Colored terminal interfaces with progress indicators
- **Error Handling**: Comprehensive validation with helpful messages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Test all variants: `make all` 
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using [Typst](https://typst.app/) and modern Python**
