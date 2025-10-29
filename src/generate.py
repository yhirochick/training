#!/usr/bin/env python3
"""
Main script to generate math worksheet PDFs.
"""
import argparse
import random
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from generators import (
    LinearEquationGenerator,
    ProportionalFunctionGenerator,
    ProportionalFunctionFromConditionGenerator,
    SimultaneousEquationGenerator
)


def main():
    parser = argparse.ArgumentParser(
        description='Generate math worksheets and answer keys as LaTeX files'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=12345,
        help='Random seed for reproducibility (default: 12345)'
    )
    parser.add_argument(
        '--num-problems',
        type=int,
        default=5,
        help='Number of problems per section (default: 5)'
    )
    args = parser.parse_args()

    # Set random seed
    rng = random.Random(args.seed)
    print(f"Generating problems with seed: {args.seed}")

    # Initialize generators
    linear_gen = LinearEquationGenerator(rng)
    proportional_gen = ProportionalFunctionGenerator(rng)
    proportional_condition_gen = ProportionalFunctionFromConditionGenerator(rng)
    simultaneous_gen = SimultaneousEquationGenerator(rng)

    # Generate problems
    linear_equations = linear_gen.generate(args.num_problems)
    proportional_functions = proportional_gen.generate(args.num_problems)
    proportional_conditions = proportional_condition_gen.generate(args.num_problems)
    simultaneous_equations = simultaneous_gen.generate(args.num_problems)

    # Prepare template data
    template_data = {
        'seed': args.seed,
        'linear_equations': linear_equations,
        'proportional_functions': proportional_functions,
        'proportional_conditions': proportional_conditions,
        'simultaneous_equations': simultaneous_equations
    }

    # Set up Jinja2 environment
    project_root = Path(__file__).parent.parent
    template_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Render problems template
    problems_template = env.get_template('problems.tex.j2')
    problems_tex = problems_template.render(**template_data)
    problems_path = output_dir / 'problems.tex'
    with open(problems_path, 'w', encoding='utf-8') as f:
        f.write(problems_tex)
    print(f"Generated: {problems_path}")

    # Render answers template
    answers_template = env.get_template('answers.tex.j2')
    answers_tex = answers_template.render(**template_data)
    answers_path = output_dir / 'answers.tex'
    with open(answers_path, 'w', encoding='utf-8') as f:
        f.write(answers_tex)
    print(f"Generated: {answers_path}")

    print("\nTeX files generated successfully!")
    print("Run 'make build' or 'make docker-build' to compile PDFs.")


if __name__ == '__main__':
    main()
