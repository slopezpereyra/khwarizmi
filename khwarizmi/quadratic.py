import math

from khwarizmi import equations
from khwarizmi.exc import NegativeSquareError


class Quadratic(equations.Equation):

    def __init__(self, equation):
        self.equation = equation.replace(" ", "")
        self.symbols = self.return_quadratic_elements()
        self.formulated = self.formulate()
        self.plus_solution = 0
        self.minus_solution = 0
        self.get_solutions()

    def __str__(self):

        return self.formulated

    def return_quadratic_elements(self):
        """Returns a dictionary with the elements of the quadratic equation
        with their indexes. For the quadratic equation

        ax**2 + bx**2 + c = 0

        elements are a, first x, b, second x and c."""

        symbols = {"a": 1, "b": 1, "c": 1}
        equation = self.equation

        if equation[0].isdigit():
            a = self.get_number(equation[0], 0, equation)
            symbols["a"] = float(a)

        # Returns the first symbol after the first plus sign.
        b_index = equation.find("+") + 1

        if equation[b_index].isdigit():
            b = self.get_number(equation[b_index], b_index, equation)
            symbols["b"] = float(b)

        # Returns the first symbol after the second plus sign.
        c_index = equation.find("+", b_index + 1) + 1

        if equation[c_index].isdigit():
            c = self.get_number(equation[c_index], c_index, equation)
            symbols["c"] = float(c)

        return symbols

    def formulate(self):
        """Returns the quadratic equation expressed on the quadratic formula

        x = -b + - (square root of b - 4ac) / 2a"""

        sqr, roof, psms = "\u221A", "\u0305", "\u00b1"
        s = self.symbols

        # Converts floats into integers when decimal part is equal to .0,
        # to make str representation of the class more pretty.

        for key in s:
            str_key = str(s[key])
            if str_key[1:] == ".0":
                s[key] = int(s.get(key))

        formulated = ("(-" + str(s.get("b")) + psms + sqr + str(s.get("b")) + roof +
                      "*" + roof + "*" + roof + "2" + roof + "-" + roof + "4" + roof
                      + "*" + roof + str(s.get("a")) + roof +
                      "*" + roof + str(s.get("c")) + roof + ")/2*" + str(s.get("a")))

        return formulated

    def get_solutions(self):

        s = self.symbols

        print(s.get("b"), s.get("a"), s.get("c"))

        try:
            square = math.sqrt(s.get("b") ** 2 - 4 * s.get("a") * s.get("c"))
        except ValueError:
            raise NegativeSquareError

        plus_solution = eval(
            "(-" + str(s.get("b")) + "+" + str(int(square)) + ")")

        minus_solution = eval(
            "(-" + str(s.get("b")) + "-" + str(int(square)) + ")")

        denominator = 2 * s.get("a")

        self.plus_solution = plus_solution / denominator
        self.minus_solution = minus_solution / denominator

    def solve(self):

        self.get_solutions()
