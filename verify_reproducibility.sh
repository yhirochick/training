#!/bin/bash
# Script to verify that the same seed produces identical TeX files

SEED=12345

echo "=== Reproducibility Verification ==="
echo "Testing with seed: $SEED"
echo ""

# Generate first time
echo "Generating files (attempt 1)..."
python3 src/generate.py --seed $SEED --num-problems 5 > /dev/null 2>&1
cp output/problems.tex output/problems_test1.tex
cp output/answers.tex output/answers_test1.tex

# Generate second time
echo "Generating files (attempt 2)..."
python3 src/generate.py --seed $SEED --num-problems 5 > /dev/null 2>&1
cp output/problems.tex output/problems_test2.tex
cp output/answers.tex output/answers_test2.tex

# Compare
echo ""
echo "Comparing outputs..."

if diff -q output/problems_test1.tex output/problems_test2.tex > /dev/null; then
    echo "✓ problems.tex: IDENTICAL"
else
    echo "✗ problems.tex: DIFFERENT"
fi

if diff -q output/answers_test1.tex output/answers_test2.tex > /dev/null; then
    echo "✓ answers.tex: IDENTICAL"
else
    echo "✗ answers.tex: DIFFERENT"
fi

# Cleanup
rm output/problems_test1.tex output/problems_test2.tex
rm output/answers_test1.tex output/answers_test2.tex

echo ""
echo "Reproducibility test complete!"
