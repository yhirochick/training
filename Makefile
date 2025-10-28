.PHONY: build clean docker-build docker-clean help

# Default seed for reproducibility
SEED ?= 12345

help:
	@echo "Available targets:"
	@echo "  make build          - Generate all PDFs (problems + answers)"
	@echo "  make clean          - Remove generated files"
	@echo "  make docker-build   - Build Docker image and generate PDFs inside container"
	@echo "  make docker-clean   - Clean inside Docker container"
	@echo ""
	@echo "Options:"
	@echo "  SEED=<number>       - Set random seed (default: 12345)"
	@echo ""
	@echo "Example: make build SEED=54321"

# Build all PDFs locally (requires environment)
build:
	python3 src/generate.py --seed $(SEED)
	lualatex -output-directory=output output/problems.tex
	lualatex -output-directory=output output/problems.tex
	lualatex -output-directory=output output/answers.tex
	lualatex -output-directory=output output/answers.tex
	@echo "PDFs generated in output/ directory"

# Build using Docker
docker-build:
	docker compose run --rm latex-builder make build SEED=$(SEED)

# Clean generated files locally
clean:
	rm -rf output/*.tex output/*.pdf output/*.aux output/*.log output/*.out

# Clean using Docker
docker-clean:
	docker compose run --rm latex-builder make clean
