"""Template files for CV projects."""

from pathlib import Path
def get_template_files() -> dict[str, str | bytes]:
    """Return all template files as a dictionary."""
    
    # Get the package directory - templates are co-located with code
    package_dir = Path(__file__).parent
    
    # Template files to copy from the package (included via MANIFEST.in)
    files_to_copy = [
        "build/cv.typ", "lib/template.typ", "lib/config.typ", "lib/data.typ",
        "lib/renderers.typ", "lib/components.typ", "lib/styles.typ",
        "data/config.yaml", "data/personal.yaml", "Makefile", ".gitignore",
        "data/variants/academic.yaml", "data/variants/industry.yaml", "data/variants/short.yaml",
        "data/sections/experience.yaml", "data/sections/education.yaml", "data/sections/publication.yaml",
        "data/sections/awards.yaml", "data/sections/memberships.yaml", "data/sections/reviewer.yaml",
        "data/sections/skills.yaml", "data/sections/supervision.yaml", "data/sections/talks.yaml",
        "data/sections/teaching.yaml",
    ]
    
    template_files = {}
    for file_path in files_to_copy:
        source_file = package_dir / file_path
        if source_file.exists():
            template_files[file_path] = source_file.read_text(encoding='utf-8')
    
    # Add a README for the generated project
    template_files["README.md"] = get_project_readme()
    
    return template_files


def get_project_readme() -> str:
    """Generate README for new CV projects."""
    return """# My Professional CV

This CV was generated using the `typst-cv` CLI tool.

## Quick Start

```bash
# Build academic variant
typst-cv build academic

# Build all variants  
typst-cv build --all

# Watch for changes
typst-cv build academic --watch
```

## Customization

Edit your CV content in the `data/` directory:

- `data/config.yaml` - Global styling and configuration
- `data/sections/*.yaml` - Your CV content (experience, education, etc.)
- `data/variants/*.yaml` - Variant-specific overrides

## Building

Available variants:
- **academic**: Full academic CV with all publications
- **industry**: Industry-focused with selected publications  
- **short**: Compact 1-2 page version

```bash
typst-cv build academic     # Academic variant
typst-cv build industry     # Industry variant
typst-cv build short        # Short variant
typst-cv build --all        # All variants
```

## Output

Built files are saved to `out/`:
- `out/pdf/` - PDF versions
- `out/png/` - PNG versions (if requested)

## More Info

For more details, see the [typst-cv documentation](https://github.com/filippoguerranti/typst-cv).
"""