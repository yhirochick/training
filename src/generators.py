"""
Problem generators for middle school math worksheets.
"""
import random
from fractions import Fraction


class LinearEquationGenerator:
    """Generator for linear equations (中1 一次方程式)."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate(self, num_problems: int = 5) -> list:
        """Generate linear equations of the form ax + b = c."""
        problems = []

        for _ in range(num_problems):
            # Generate random coefficients
            a = self.rng.randint(2, 10)
            b = self.rng.randint(-20, 20)
            c = self.rng.randint(-20, 20)

            # Ensure b != 0 to avoid trivial ax = c
            while b == 0:
                b = self.rng.randint(-20, 20)

            # Calculate solution: x = (c - b) / a
            solution = Fraction(c - b, a)

            # Format equation
            if b > 0:
                equation = f"{a}x + {b} = {c}"
            else:
                equation = f"{a}x - {abs(b)} = {c}"

            # Format solution
            if solution.denominator == 1:
                solution_str = str(solution.numerator)
            else:
                solution_str = f"\\frac{{{solution.numerator}}}{{{solution.denominator}}}"

            problems.append({
                'equation': equation,
                'solution': solution_str
            })

        return problems


class ProportionalFunctionGenerator:
    """Generator for proportional function problems (中1 比例)."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate(self, num_problems: int = 5) -> list:
        """Generate proportional function problems from x-y value tables."""
        problems = []

        for _ in range(num_problems):
            # Random proportionality constant
            a = self.rng.randint(-10, 10)
            while a == 0:
                a = self.rng.randint(-10, 10)

            # Generate three x values
            x_values = []
            for _ in range(3):
                x = self.rng.randint(-5, 5)
                while x == 0 or x in x_values:
                    x = self.rng.randint(-5, 5)
                x_values.append(x)

            # Sort x values in ascending order (left to right in table)
            x_values.sort()

            # Calculate corresponding y values
            y_values = [a * x for x in x_values]

            # Format solution
            if a == 1:
                solution = "x"
            elif a == -1:
                solution = "-x"
            else:
                solution = f"{a}x"

            problems.append({
                'x_values': x_values,
                'y_values': y_values,
                'solution': solution
            })

        return problems


class ProportionalFunctionFromConditionGenerator:
    """Generator for proportional function problems from conditions (中1 比例 - 条件から式を求める)."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate(self, num_problems: int = 5) -> list:
        """Generate proportional function problems from conditions like 'y is proportional to x, when x=2, y=6'."""
        problems = []

        for _ in range(num_problems):
            # Random proportionality constant
            a = self.rng.randint(-10, 10)
            while a == 0:
                a = self.rng.randint(-10, 10)

            # Generate a random x value (not 0)
            x_value = self.rng.randint(-10, 10)
            while x_value == 0:
                x_value = self.rng.randint(-10, 10)

            # Calculate corresponding y value
            y_value = a * x_value

            # Format condition text
            condition = f"x={x_value}のときy={y_value}"

            # Format solution
            if a == 1:
                solution = "x"
            elif a == -1:
                solution = "-x"
            else:
                solution = f"{a}x"

            problems.append({
                'condition': condition,
                'x_value': x_value,
                'y_value': y_value,
                'solution': solution
            })

        return problems


class SimultaneousEquationGenerator:
    """Generator for simultaneous equations (中2 連立方程式)."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate(self, num_problems: int = 5) -> list:
        """Generate systems of two linear equations."""
        problems = []

        for _ in range(num_problems):
            # Generate integer solutions
            x_sol = self.rng.randint(-10, 10)
            y_sol = self.rng.randint(-10, 10)

            # Generate first equation: a1*x + b1*y = c1
            a1 = self.rng.randint(1, 5)
            b1 = self.rng.randint(1, 5)
            c1 = a1 * x_sol + b1 * y_sol

            # Generate second equation: a2*x + b2*y = c2
            a2 = self.rng.randint(1, 5)
            b2 = self.rng.randint(1, 5)
            # Ensure equations are independent (not parallel)
            while a1 * b2 == a2 * b1:
                a2 = self.rng.randint(1, 5)
                b2 = self.rng.randint(1, 5)

            c2 = a2 * x_sol + b2 * y_sol

            # Format equations
            eq1 = self._format_equation(a1, b1, c1)
            eq2 = self._format_equation(a2, b2, c2)

            problems.append({
                'eq1': eq1,
                'eq2': eq2,
                'solution_x': x_sol,
                'solution_y': y_sol
            })

        return problems

    def _format_equation(self, a: int, b: int, c: int) -> str:
        """Format equation ax + by = c."""
        parts = []

        # x term
        if a == 1:
            parts.append("x")
        elif a == -1:
            parts.append("-x")
        else:
            parts.append(f"{a}x")

        # y term
        if b > 0:
            if b == 1:
                parts.append("+ y")
            else:
                parts.append(f"+ {b}y")
        else:
            if b == -1:
                parts.append("- y")
            else:
                parts.append(f"- {abs(b)}y")

        # constant
        equation = " ".join(parts) + f" = {c}"

        return equation
