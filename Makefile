# CV Build System

SRC := build/cv.typ

.PHONY: all academic industry short clean dev watch help force

# Force rebuild
force: ;

# Pattern rules

# PDF
out/pdf/cv-%.pdf: $(SRC) | force
	@mkdir -p $(dir $@)
	typst compile $(SRC) $@ --root . --input variant=$* --format pdf --pdf-standard a-2b

# PNG
out/png/cv-%-{p}.png: $(SRC) | force
	@mkdir -p $(dir $@)
	typst compile $(SRC) $@ --root . --input variant=$* --format png --ppi 300

# Convenience targets
academic: out/pdf/cv-academic.pdf out/png/cv-academic-{p}.png
industry: out/pdf/cv-industry.pdf out/png/cv-industry-{p}.png
short:    out/pdf/cv-short.pdf out/png/cv-short-{p}.png

# Default target builds all variants
all: academic industry short

# Clean
clean:
	rm -f out/*/*

# Quick compile for testing (defaults to academic/pdf)
dev:
	typst compile $(SRC) --root .

# Watch mode
watch:
	typst watch $(SRC) --root . --input variant=academic

# Help
help:
	@echo "Usage:"
	@echo "  make all                  # build all CV variants in PDF and PNG"
	@echo "  make academic             # build academic variant PDF and PNG"
	@echo "  make academic format=png  # build academic PNG (optional single run)"
	@echo "  make clean                # remove all outputs"