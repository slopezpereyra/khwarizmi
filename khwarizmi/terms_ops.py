"""Base class for algebraic operations."""

from misc import if_assign, num, isanumber
from exc import NonAlgebraicOperationError, InvalidOperationError
from expression import Expression


class TermOperations:
    """Defines operations between algebraic terms.
    This class is not ment to have instances, but is a placeholder
    for static methods to be used on terms constructed on classes
    deriving from Expression (see expression.py)."""

    @staticmethod
    def ispowered(a):
        """Returns true if a is being elevated by an exponent."""

        return True if '**' in a else False

    @staticmethod
    def getpower(a):
        """Returns exponent of term a."""

        if TermOperations.ispowered(a):
            return num(a[a.find('**') + 2:])
        elif not isanumber(a):
            return 1
        return 0

    @staticmethod
    def isnegative(a):
        """True if a is negative, false otherwise."""

        if a.count('-') != 0 and a.count('-') % 2 != 0:
            return True
        return False

    @staticmethod
    def commonvars(a, b):

        a, b = Expression(a), Expression(b)
        common_vars = []

        for var in a.variables:
            if var in b.variables:
                common_vars.append(var)

        return common_vars

    @staticmethod
    def add(a, b):
        """Returns the expression resultant of adding terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        if isanumber(a.expression) or isanumber(b.expression):
            raise NonAlgebraicOperationError

        if len(a.terms) > 1 or len(b.terms) > 1:
            raise InvalidOperationError(a, b)

        if TermOperations.getpower(a.expression) is not TermOperations.getpower(b.expression) or a.variables != b.variables:
            operator = if_assign(b.expression.startswith('-'), '', '+')
            return Expression.beautify(a.expression + operator + b.expression)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(int(a_coefficient) + int(b_coefficient))
        result = if_assign(result == '1', "", result)
        result = if_assign(result == '-1', "-", result)

        result += "".join(a.variables) + '**' + str(TermOperations.getpower(a.expression))
        if result.endswith('**1'):
            result = result.replace('**1', '')
        return Expression.beautify(result)

    @staticmethod
    def substract(a, b):
        """Returns the expression resultant of substracting terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        if isanumber(a.expression) or isanumber(b.expression):
            raise NonAlgebraicOperationError

        if len(a.terms) > 1 or len(b.terms) > 1:
            raise InvalidOperationError(a, b)

        if TermOperations.getpower(a.expression) is not TermOperations.getpower(b.expression) or a.variables != b.variables:
            result = a.expression + '-' + b.expression
            return Expression.beautify(result)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(int(a_coefficient) - int(b_coefficient))
        result = if_assign(result == '1', "", result)
        result = if_assign(result == '-1', "-", result)

        result += "".join(a.variables) + '**' + TermOperations.getpower(a.expression)
        return Expression.beautify(result)

    @staticmethod
    def multiply(a, b):
        """Multiplies terms a and b."""

        a = Expression(a, no_vars_intended=True)
        b = Expression(b, no_vars_intended=True)

        variables = set(a.variables + b.variables)
        power = '**' + str(int(TermOperations.getpower(a.expression)) + int(TermOperations.getpower(b.expression)))
        power = if_assign(power == '1', '', power)

        if power == '0':
            return "".join(variables)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(int(a_coefficient) * int(b_coefficient)) + "".join(variables) + power
        return Expression.beautify(result)

    @staticmethod
    def divide(a, b):
        a = Expression(a)
        b = Expression(b)

        variables = set(a.variables + b.variables)
        power = '**' + str(int(TermOperations.getpower(a.expression)) - int(TermOperations.getpower(b.expression)))
        power = if_assign(power == '**1', '', power)

        if power == '**0':
            return "/".join(variables)

        a_coefficient = a.get_number(0)
        b_coefficient = b.get_number(0)

        result = str(num(int(a_coefficient) / int(b_coefficient))) + "/".join(variables)
        result = if_assign(power != '', '(' + result + ')' + power, result)
        return Expression.beautify(result)


A = '4xz'
B = '4xz'

