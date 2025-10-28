#!/bin/bash
# Quick test script to verify the system works without Docker

set -e  # Exit on error

echo "==================================="
echo "Quick Test - LaTeX Problem Generator"
echo "==================================="
echo ""

# Check Python
echo "1. Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "   ERROR: python3 not found"
    exit 1
fi
echo "   ✓ Python found: $(python3 --version)"

# Check Jinja2
echo ""
echo "2. Checking Jinja2..."
if ! python3 -c "import jinja2" 2>/dev/null; then
    echo "   WARNING: jinja2 not installed"
    echo "   Install with: pip3 install jinja2"
    exit 1
fi
echo "   ✓ Jinja2 installed"

# Generate TeX files
echo ""
echo "3. Generating TeX files..."
python3 src/generate.py --seed 12345 --num-problems 5
echo "   ✓ TeX files generated"

# Check if files exist
echo ""
echo "4. Verifying output files..."
if [ ! -f "output/problems.tex" ]; then
    echo "   ERROR: output/problems.tex not found"
    exit 1
fi
if [ ! -f "output/answers.tex" ]; then
    echo "   ERROR: output/answers.tex not found"
    exit 1
fi
echo "   ✓ problems.tex exists ($(wc -l < output/problems.tex) lines)"
echo "   ✓ answers.tex exists ($(wc -l < output/answers.tex) lines)"

# Check LuaLaTeX (optional)
echo ""
echo "5. Checking LuaLaTeX..."
if command -v lualatex &> /dev/null; then
    echo "   ✓ LuaLaTeX found"
    echo ""
    echo "   You can compile PDFs with:"
    echo "   make build"
else
    echo "   ⚠ LuaLaTeX not found"
    echo ""
    echo "   To compile PDFs, either:"
    echo "   - Install TeX Live: sudo apt-get install texlive-full"
    echo "   - Use Docker: make docker-build"
fi

echo ""
echo "==================================="
echo "Quick test completed successfully!"
echo "==================================="
