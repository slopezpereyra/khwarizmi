"""Basic expressions"""

from misc import if_assign, isanumber
from exc import NoVariableError
import copy

SEPARATORS = ['+', '-', '=', '*', "(", ")"]
excused_symbols = ["/", "."]


class Expression:
    """Base class for every algebraic expression of any form."""

    def __init__(self, expression, no_vars_intended=False):
        self.no_vars_intended = no_vars_intended
        self.expression = expression.replace(' ', '')
        self.variables = self.get_variables()
        self.unknown = self.variables[0] if len(self.variables) > 0 else None
        self.terms = self.get_terms()
        self.coefficients = self.get_coefficients()

    def get_variables(self):
        """Adds every variable of the equation
        to the variables attribute (list)."""

        index, incs = 0, []
        for symbol in self.expression:

            if symbol.isalpha() and symbol not in incs:
                incs.append(symbol)

        if len(incs) is 0 and self.no_vars_intended is False:
            raise NoVariableError(self.expression)

        return incs

    def get_number(self, index, expression=None, catch_variable=False, catch_term=False):
        """Returns the number that starts at index on expression.
        It may or may not catch full terms and variables."""

        expression = self.expression if expression is None else expression
        separators = copy.copy(SEPARATORS)
        is_negative = False

        if catch_term is True and catch_variable is False:
            catch_variable = True

        if catch_variable is False:
            separators.extend(self.variables)
        if catch_term is True:
            separators.remove('*')

        expression = expression[index:]
        if expression.startswith('-'):
            is_negative = True
            expression = expression[1:]

        if any(x in separators for x in expression):
            separator = next((x for x in expression if x in separators))
            pos = expression.find(separator)
            if expression[0:pos] is "" and isanumber(expression[0:pos+1]):
                number = expression[0:pos+1]
            else:
                number = expression[0:pos]
        else:
            number = expression

        if expression[0].isalpha() and number == '':
            return '1' if is_negative is False else '-1'

        return number if is_negative is False else '-' + number

    def get_terms(self, side=None):
        """Returns a list of all terms of this equation."""

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
            '+*' into '*', etc."""

        expression = expression.replace('--', '+')
        expression = expression.replace('*+', '*')
        if expression[0] == '+':
            expression = expression.replace('+', '', 1)
        expression = expression.replace('+-', '-')
        expression = expression.replace('=+', '=')
        expression = expression.replace('/+', '/')
        expression = expression.replace('**1', '')

        return expression
