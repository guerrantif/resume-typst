# Simple CV Build System - Always rebuilds

SRC := build/cv.typ

.PHONY: all academic industry short clean help dev watch pdf-academic pdf-industry pdf-short png-academic png-industry png-short

# Build all variants
all: academic industry short

# Build specific variants (PDF + PNG)
academic: pdf-academic png-academic
industry: pdf-industry png-industry  
short: pdf-short png-short

# PDF targets
pdf-academic:
	@mkdir -p out/pdf
	@echo "Building academic PDF..."
	typst compile $(SRC) out/pdf/cv-academic.pdf --root . --input variant=academic --format pdf --pdf-standard a-2b

pdf-industry:
	@mkdir -p out/pdf
	@echo "Building industry PDF..."
	typst compile $(SRC) out/pdf/cv-industry.pdf --root . --input variant=industry --format pdf --pdf-standard a-2b

pdf-short:
	@mkdir -p out/pdf
	@echo "Building short PDF..."
	typst compile $(SRC) out/pdf/cv-short.pdf --root . --input variant=short --format pdf --pdf-standard a-2b

# PNG targets (with page numbering)
png-academic:
	@mkdir -p out/png
	@echo "Building academic PNG..."
	typst compile $(SRC) "out/png/cv-academic-{p}.png" --root . --input variant=academic --format png --ppi 300

png-industry:
	@mkdir -p out/png
	@echo "Building industry PNG..."
	typst compile $(SRC) "out/png/cv-industry-{p}.png" --root . --input variant=industry --format png --ppi 300

png-short:
	@mkdir -p out/png
	@echo "Building short PNG..."
	typst compile $(SRC) "out/png/cv-short-{p}.png" --root . --input variant=short --format png --ppi 300

# Development commands
dev:
	@echo "Building development version (academic PDF)..."
	typst compile $(SRC) --root . --input variant=academic --format pdf

watch:
	@echo "Starting watch mode (academic variant)..."
	typst watch $(SRC) --root . --input variant=academic

# Clean outputs
clean:
	@echo "Cleaning up generated files..."
	@rm -rf out/
	@rm -rf build/*.pdf

# Help
help:
	@echo "Build Commands:"
	@echo ""
	@echo "Build specific variants"
	@echo "  make academic      # Full academic CV (all sections, complete details)"
	@echo "  make industry      # Industry-focused CV (filtered publications, practical emphasis)"
	@echo "  make short         # Ultra-compact CV (2 positions, 2 degrees, 3 papers, no details)"
	@echo ""
	@echo "Build all variants"
	@echo "  make all           # Generate PDF and PNG for all three variants"
	@echo ""
	@echo "Development workflow"
	@echo "  make dev           # Quick compile for testing (defaults to academic PDF)"
	@echo "  make watch         # Live reload during development (academic variant)"
	@echo "  make clean         # Remove all generated outputs"
	@echo ""
	@echo "Individual formats"
	@echo "  make pdf-academic  # Build only academic PDF"
	@echo "  make png-academic  # Build only academic PNG"