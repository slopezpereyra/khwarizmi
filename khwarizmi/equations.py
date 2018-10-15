"""Defines an equation class and its functions."""

import copy

from khwarizmi.exc import NoEqualityError, NoVariableError
from khwarizmi.misc import num, if_assign

OPERATORS = ["-", "+", "/", "*", '=']
excused_symbols = ["/", "."]


class Equation(object):
    """Base class for all specific equation types."""

    def __init__(self, equation):

        self.equation = equation.replace(' ', '')
        self.sol_side = ""
        self.inc_side = ""
        self.get_sides()
        self.unknowns = self.get_all_unknowns()
        self.unknown = self.return_unknown()
        self.unknown_index = self.equation.index(self.unknown)
        self.coefficient_length = 0
        self.coefficient = self.return_inc_multiplier()
        self.coefficient_index = self.unknown_index - self.coefficient_length
        self.terms = self.get_terms()

    def __str__(self):
        """String representation of the equation."""

        return self.equation

    def return_unknown(self):
        """Returns the unknown of the equation; this is, any
        character of the equation string that is not a number and rather
        a letter. E.g. the letter x or y."""

        for character in self.equation:
            if character.isalpha() is True:
                return character

        raise NoVariableError(self.equation)

    def get_all_unknowns(self):
        """Adds every unknown of the equation
        to the unknowns attribute (list)."""

        index, incs = 0, []
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in incs:
                incs.append(symbol)

        return incs

    def return_inc_multiplier(self, unknown_index=None, side=None):
        """Returns the unknown multiplier; i.e.  the number that multiplies the
        variable (if any)."""

        number, parser = "", 1
        catcher = copy.copy(excused_symbols)
        catcher.append('-')

        index = self.unknown_index if unknown_index is None else unknown_index
        side = self.inc_side if side is None else side

        # While there is a previous character and this character is a digit
        try:
            while parser <= index and (side[index - parser].isdigit() or side[index - parser] in catcher):
                number = side[index - parser] + number
                if side[index - parser] == '-':
                    break
                parser += 1

            self.coefficient_length = len(number)
            return number

        except IndexError:
            return number

    def get_sides(self):
        """Assigns to the inc_side and the sol_side attributes sliced
        parts of the equation; the part the unknown is in, and the part the result
        is in. The equation is sliced to the left and to the right of the equal sign.
        """

        try:
            equal_sign = self.equation.index("=")
            self.inc_side = self.equation[0:equal_sign]
            self.sol_side = self.equation[equal_sign + 1:]

        except ValueError:
            raise NoEqualityError(self.equation)

    def get_terms(self, side=None):

        side = self.equation if side is None else side
        index, terms = 0, []

        while index < len(side):

            term = self.get_number(side[index], index, catch_variable=True)
            terms.append(term)

            try:
                index += len(term)
                index = if_assign(side[index] == '-', index, index + 1)
            except (TypeError, IndexError):
                index += 1

        return terms

    @staticmethod
    def beautify(expression):
        """Beautifies a mathematical expression, turning '--' into '+',
        '+*' into '*', etc."""

        if '--' in expression:
            expression = expression.replace('--', '+')

        if '*+' in expression:
            expression = expression.replace('*+', '*')

        if expression[0] == '+':
            expression = expression.replace('+', '', 1)

        if '+-' in expression:
            expression = expression.replace('+-', '-')

        if '=+' in expression:
            expression = expression.replace('=+', '=')

        expression = expression.replace('/+', '/')

        return expression

    def get_number(self, number, index, side=None, catch_negatives=False, catch_variable=False):
        """Returns the set of symbols that form a full number.

        Keyword Arguments:

        number -- first number to which append following numbers
        index -- index of the number being initially parsed, which is number
        side -- side of the equation to parse (by default it parses the whole
        equation)"""

        side = side if side is not None else self.equation
        catcher = copy.copy(excused_symbols)
        parser = 1

        if catch_negatives is True:
            catcher.append('-')
        if catch_variable is True:
            catcher.append(self.unknown)

        if len(side) > index + parser:
            if side[index + 1] == "=" and side[index].isdigit():
                return number

            while side[index + parser].isdigit() or side[index + parser] in catcher:
                number += side[index + parser]

                if index + parser + 1 < len(side):
                    parser += 1
                else:
                    return number

            return number

        if number.isdigit():
            return number
        return None

    def get_all_unknown_multipliers(self, first_index):

        if self.equation.count(self.unknown) > 1:
            previous_index = first_index
            unknowns = []
            for number in range(1, self.equation.count(self.unknown) + 1):
                cur_index = self.equation.find(self.unknown, previous_index + 1)
                unknowns.append(self.return_inc_multiplier(cur_index, self.equation))
                previous_index = cur_index

            return unknowns

        return []

    def simplify_equation(self):
        """Simplifies the equation by evaluating all coefficients of the variable to one single
        coefficient."""

        first_index = self.equation.find(self.unknown)
        first_coefficient = self.return_inc_multiplier(first_index)
        sol_side, counter, left_hand_terms = self.sol_side, 0, self.get_terms(self.inc_side)

        unknowns = self.get_all_unknown_multipliers(first_index)
        unknowns.insert(0, first_coefficient)

        if len(unknowns) > 2:
            unknowns.pop()

        for number in unknowns:

            index = sol_side.find(number + self.unknown)
            replacement = if_assign(sol_side[index - 1] in OPERATORS, sol_side[index - 1] + number, number)
            sol_side = sol_side.replace(replacement + self.unknown, '')

            if number + self.unknown in self.sol_side:
                unknowns[counter] = if_assign(unknowns[counter].startswith('-'), number.replace('-', ''), '-' + number)

            counter += 1

        for term in left_hand_terms:
            if self.unknown not in term:
                sol_side += '-' + term

        try:
            unknowns = list(map(num, unknowns))
            unknown = str(sum(unknowns))
        except ValueError:
            unknown = ''

        simplified = self.beautify(unknown + self.unknown + '=' + sol_side)
        return simplified

    def sort(self, show=False):
        """Sorts the equation, which is a very highschool, wrongly phrased
        way of saying that clears the unknown side by substracting all
        positive numbers, adding all negative numbers, dividing all multipliers
        and multiplying all divisors, doing the same operations on the solution
        side. """

        index = 0

        # Local variables for the local, simplified version of the equation
        # (not equal to self.equation).

        equation = self.simplify_equation()
        equal_sign = equation.index("=")
        inc_side, sol_side = equation[0:equal_sign], equation[equal_sign + 1:]
        symbol = self.get_number(inc_side[0], index, inc_side, catch_negatives=True)

        if symbol is None:
            symbol = if_assign(equation[0] == '-', '-1', '1')

        inc_side = inc_side.replace(symbol, "", 1)
        sol_side = '(' + sol_side + ')/' + symbol

        if show is True:

            string = """Equation \n{}\n\nSimplified\n{}\n\nSorted\n{}\n\nSolved \n{}""".format(
                self.equation, equation, inc_side + '=' + sol_side,
                self.unknown + '=' + str(num(eval(sol_side))) + '\n')

            print(string)

        return sol_side

    def solve(self, show=False):
        """Evaluates the algebraic expression.
        If show is True, displays a step by step explanation."""

        return num(eval(self.sort(show=show)))

