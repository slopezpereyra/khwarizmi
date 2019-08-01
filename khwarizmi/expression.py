"""Basic expressions"""

from misc import if_assign, isanumber, frac_to_num
from exc import NoVariableError
import copy

SEPARATORS = ['+', '-', '=', '*', "(", ")"]
excused_symbols = ["/", "."]


class Expression:
    """Base class for every algebraic expression of any form."""

    def __init__(self, expression, no_vars_intended=False):
        self.no_vars_intended = no_vars_intended
        self.expression = expression.replace(' ', '')
        print(self.expression)
        self.variables = self.get_variables()
        self.unknown = self.variables[0] if len(self.variables) > 0 else None
        self.terms = self.get_terms()
        self.coefficients = self.get_coefficients()

    def __str__(self):
        return self.expression

    def get_variables(self):
        """Returns a list of all variables on the expression."""

        index, incs = 0, []
        for symbol in self.expression:

            if symbol.isalpha() and symbol not in incs:
                incs.append(symbol)

        if len(incs) is 0 and self.no_vars_intended is False:
            raise NoVariableError(self.expression)

        return incs

    def get_number(self, index, expression=None, catch_variable=False, catch_term=False, frac_to_number=False):
        """Given an expression (str) returns the number that starts at index.
        It may or may not catch full terms and variables. If no expression is given
        then self.expression is imparted by default."""

        expression = self.expression if expression is None else expression
        separators = copy.copy(SEPARATORS)
        starts_with_minus = False

        # Profilactic measure
        if catch_term is True and catch_variable is False:
            catch_variable = True

        if catch_variable is False:
            separators.extend(self.variables)
        if catch_term is True:
            separators.remove('*')

        expression = expression[index:]
        if expression.startswith('-'):
            starts_with_minus = True
            expression = expression[1:]

        if any(x in separators for x in expression):
            # If there actually are any separators on the expression...
            separator = next((x for x in expression if x in separators))
            pos = expression.find(separator)
            if expression[0:pos] is "" and isanumber(expression[0:pos+1]):
                number = expression[0:pos+1]
            else:
                number = expression[0:pos]
        else:
            number = expression

        if frac_to_number:
            number = frac_to_num(number)

        if expression[0].isalpha() and number == '':
            return '1' if starts_with_minus is False else '-1'

        return number if starts_with_minus is False else '-' + number

    def get_terms(self, side=None):
        """Returns a list of all terms of an expression.
        self.equation is imparted by default."""

        side = self.expression if side is None else side
        index, terms = 0, []

        while index < len(side):
            term = self.get_number(index, side, catch_term=True)
            if len(term) > 0:
                terms.append(term)
            index += len(term) if len(term) > 0 else 1
        return terms

    def get_coefficients(self):
        """Returns every coefficient on this expression."""

        coefficients = []

        for term in self.terms:
            if any(char.isalpha() for char in term):
                coefficient = self.get_number(0, term)
                coefficient = if_assign(coefficient is '', '1', coefficient)
                coefficient = if_assign(coefficient is '-', '-1', coefficient)
                coefficients.append(coefficient)

        return coefficients

    @staticmethod
    def beautify(expression):
        """Beautifies a mathematical expression, turning '--' into '+',
            '+*' into '*', etc., increasing or even allowing any readibility."""

        expression = expression.replace('--', '+')
        expression = expression.replace('*+', '*')
        if expression[0] == '+':
            expression = expression.replace('+', '', 1)
        expression = expression.replace('+-', '-')
        expression = expression.replace('=+', '=')
        expression = expression.replace('/+', '/')
        neutral_power = expression.find('**1')
        if neutral_power != -1 and not expression[neutral_power + 1].isdigit():
            expression.replace('**1', '', neutral_power)
        if expression.endswith('+'):
            expression = expression[:-1]

        return expression

