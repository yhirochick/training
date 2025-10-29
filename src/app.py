#!/usr/bin/env python3
"""
Flask web application for math worksheet PDF generation.
"""
import os
import random
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from jinja2 import Environment, FileSystemLoader

from generators import (
    LinearEquationGenerator,
    ProportionalFunctionGenerator,
    SimultaneousEquationGenerator
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = PROJECT_ROOT / 'templates'
OUTPUT_DIR = PROJECT_ROOT / 'output'

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_tex_files(seed, num_problems, output_dir):
    """Generate TeX files for problems and answers."""
    # Set random seed
    rng = random.Random(seed)

    # Initialize generators
    linear_gen = LinearEquationGenerator(rng)
    proportional_gen = ProportionalFunctionGenerator(rng)
    simultaneous_gen = SimultaneousEquationGenerator(rng)

    # Generate problems
    linear_equations = linear_gen.generate(num_problems)
    proportional_functions = proportional_gen.generate(num_problems)
    simultaneous_equations = simultaneous_gen.generate(num_problems)

    # Prepare template data
    template_data = {
        'seed': seed,
        'linear_equations': linear_equations,
        'proportional_functions': proportional_functions,
        'simultaneous_equations': simultaneous_equations
    }

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Render problems template
    problems_template = env.get_template('problems.tex.j2')
    problems_tex = problems_template.render(**template_data)
    problems_path = output_dir / 'problems.tex'
    with open(problems_path, 'w', encoding='utf-8') as f:
        f.write(problems_tex)

    # Render answers template
    answers_template = env.get_template('answers.tex.j2')
    answers_tex = answers_template.render(**template_data)
    answers_path = output_dir / 'answers.tex'
    with open(answers_path, 'w', encoding='utf-8') as f:
        f.write(answers_tex)

    return problems_path, answers_path


def compile_tex_to_pdf(tex_path, output_dir):
    """Compile TeX file to PDF using LuaLaTeX."""
    # Run lualatex twice for proper references
    for _ in range(2):
        result = subprocess.run(
            ['lualatex', '-output-directory', str(output_dir), str(tex_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")

    # Return PDF path
    pdf_path = output_dir / f"{tex_path.stem}.pdf"
    return pdf_path


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate PDFs based on form input."""
    try:
        # Get parameters from form
        seed = int(request.form.get('seed', 12345))
        num_problems = int(request.form.get('num_problems', 5))
        pdf_type = request.form.get('pdf_type', 'both')  # 'problems', 'answers', or 'both'

        # Validate parameters
        if not (1 <= num_problems <= 20):
            return jsonify({'error': 'Number of problems must be between 1 and 20'}), 400

        # Create temporary directory for this generation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Generate TeX files
            problems_tex, answers_tex = generate_tex_files(seed, num_problems, temp_path)

            # Compile to PDF
            pdf_files = []
            if pdf_type in ['problems', 'both']:
                problems_pdf = compile_tex_to_pdf(problems_tex, temp_path)
                pdf_files.append(('problems', problems_pdf))

            if pdf_type in ['answers', 'both']:
                answers_pdf = compile_tex_to_pdf(answers_tex, temp_path)
                pdf_files.append(('answers', answers_pdf))

            # Copy PDFs to output directory
            result_files = []
            for name, pdf_path in pdf_files:
                output_path = OUTPUT_DIR / f"{name}_seed{seed}.pdf"
                with open(pdf_path, 'rb') as src, open(output_path, 'wb') as dst:
                    dst.write(src.read())
                result_files.append({
                    'name': name,
                    'filename': output_path.name,
                    'url': f"/download/{output_path.name}"
                })

            return jsonify({
                'success': True,
                'seed': seed,
                'num_problems': num_problems,
                'files': result_files
            })

    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except RuntimeError as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/download/<filename>')
def download(filename):
    """Download a generated PDF file."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
