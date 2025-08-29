# CV Build System

.PHONY: all academic industry short clean help

# Default target
all: academic industry short

# Build specific variants using parameters
academic:
	typst compile build/cv.typ out/cv-academic.pdf --root . --input variant=academic

industry:
	typst compile build/cv.typ out/cv-industry.pdf --root . --input variant=industry

short:
	typst compile build/cv.typ out/cv-short.pdf --root . --input variant=short

# Clean build artifacts
clean:
	rm -f out/*.pdf

# Development - quick compile for testing (defaults to academic)
dev:
	typst compile build/cv.typ --root .

# Watch mode for development
watch:
	typst watch build/cv.typ --root . --input variant=academic

# Help
help:
	@echo "Available targets:"
	@echo "  all        - Build all CV variants"
	@echo "  academic   - Build academic CV"
	@echo "  industry   - Build industry CV"  
	@echo "  short      - Build short CV"
	@echo "  clean      - Remove PDF files"
	@echo "  dev        - Quick compile for testing"
	@echo "  watch      - Watch mode for development"
	@echo "  help       - Show this help"