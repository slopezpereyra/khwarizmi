"""Defines an equation class and its functions."""

from khwarizmi.exc import NoEqualityError, NoVariableError
from khwarizmi.misc import num, if_assign

OPERATORS = ["-", "+", "/", "*"]
excused_symbols = ["/", "."]


class Equation (object):

    """Base class for all specific equation types.

    Attributes:

    equation = the equation passed as parameter with all the spaces removed.
    sol_side = the solution side of the equation.
    inc_side = the incognito side of the equation.
    incognitos = a list of all incognitos on this equation (for linear equations and others).
    incognito = the specific incognito of this equation.
    incognito_index = the index or rather position of the incognito on this equation.
    mult_length = the length of the incognito multiplier.
    inc_multiplier = the number that multiplies the incognito.
    inc_mult_index = the index or rather position of the number that multiplies the incognito.

    """

    def __init__(self, equation):
        self.equation = equation.replace(" ", "")
        self.sol_side = ""
        self.inc_side = ""
        self.get_sides()
        self.incognitos = self.get_all_incognitos()
        self.incognito = self.return_incognito()
        self.incognito_index = self.equation.index(self.incognito)
        self.mult_length = 0
        self.inc_multiplier = self.return_inc_multiplier()
        self.inc_mult_index = self.incognito_index - self.mult_length

    def __str__(self):
        """String representation of the equation."""

        str = self.equation
        return str

    def return_incognito(self):
        """Returns the incognito of the equation; this is, any
        character of the equation string that is not a number and rather
        a letter. E.g. the letter x or y."""

        index = 0

        for character in self.equation:

            if character.isalpha() is True:

                if character not in self.incognitos:
                    self.incognitos.append(character)

                return character

            index += 1

        raise NoVariableError(self.equation)

    def get_all_incognitos(self):
        """Adds every incognito of the equation
        to the incognitos attribute (list)."""

        index, incs = 0, []
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in incs:
                incs.append(symbol)

        return incs

    def return_inc_multiplier(self, inc_index=None, side=None):
        """Returns the incognito multiplier; i.e.  the number that multiplies the
        variable (if any)."""

        number = ""
        parser = 1

        index = self.incognito_index if inc_index is None else inc_index
        inc_side = self.inc_side if side is None else side

        # While there is a previous character and this character is a digit
        try:
            while parser <= index and (inc_side[index - parser].isdigit() or inc_side[index - parser] in excused_symbols):
                number = self.inc_side[self.incognito_index - parser] + number
                parser += 1

            self.mult_length = len(number)
            return number

        except IndexError:
            return number

    def get_sides(self):
        """Assigns to the inc_side and the sol_side attributes sliced
        parts of the equation; the part the incognito is in, and the part the result
        is in. The equation is sliced to the left and to the right of the equal sign.
        """

        try:
            equal_sign = self.equation.index("=")
            self.inc_side = self.equation[0:equal_sign]
            self.sol_side = self.equation[equal_sign + 1:]

        except ValueError:
            raise NoEqualityError(self.equation)

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

        expression = expression.replace('/+', '/')

        return expression

    def get_operator(self, number_pos, full_number):
        """Returns the operator to be used on a specific number to clear it
        from the side of the equation it is in. For example, for the equation
        2x+5=15, taking the number 5, it would return the - (minus) operator,
        for we have to substract five to each side to clear +5. The equation
        would then be 2x=15-5 .

        Keyword Arguments:

        number_pos: the position in the equation of the number whose operator to
        check.
        full_number: the full number (not individual symbol) to be checked."""

        character = self.inc_side[number_pos]

        if number_pos > 0 and character not in OPERATORS:
            if full_number == self.inc_multiplier:
                if self.inc_side[self.inc_mult_index - 1] == '-':
                    return "/-"
                return "/"
            elif self.inc_side[number_pos - 1] == "+":
                return "-"
            else:
                return "+"

        elif full_number == self.inc_multiplier:
            return "/"

        else:
            return "-"

    def format_parenthesis(self):
        """Formats parenthesis positions if required"""

        if self.inc_multiplier is not "":

            op_index = self.sol_side.index("/")
            symbols_until_end = if_assign(self.sol_side[op_index + 1] == '-', 2, 1)
            high_operation = self.sol_side[op_index: op_index + self.mult_length + symbols_until_end]
            self.sol_side = "(" + self.sol_side.replace(high_operation, "") + ")" + high_operation

    def get_number(self, number, index, side=None):
        """Get's all the numbers that form a full number and returns the full
        number.

        Keyword Arguments:

        number -- first number to which append following numbers
        index -- index of the number being initially parsed, which is number
        side -- side of the equation to parse (by default it parses the whole
        equation)"""

        side = side if side is not None else self.equation

        parser = 1

        if len(side) > index + parser:
            if side[index + 1] == "=":
                return number

            while side[index + parser].isdigit() or side[index + parser] in excused_symbols:
                number += side[index + parser]

                if index + parser + 1 < len(side):
                    parser += 1
                else:
                    return number

            return number

        return number

    def sort_equation(self, get_unknown_side=False):
        """Sorts the equation, which is a very highschool, wrongly phrased
        way of saying that clears the incognito side by substracting all
        positive numbers, adding all negative numbers, dividing all multipliers
        and multiplying all divisors, doing the same operations on the solution
        side. """

        index = 0

        while len(self.inc_side) > 1:
            symbol = self.inc_side[index]
            try:
                if symbol.isdigit():

                    # Get the symbol (the full number) and its index.

                    symbol = self.get_number(symbol, index, self.inc_side)
                    previous_symbol = self.inc_side[index - 1]
                    operator = self.get_operator(index, symbol)

                    # Pass the number from the incognito side of the equation to
                    # the solution side, with the proper operator...

                    self.sol_side += operator + symbol
                    self.inc_side = self.inc_side.replace(
                        symbol, "", 1)
                    if previous_symbol in OPERATORS:
                        # If there's an operator before this symbol, erase it.

                        self.inc_side = self.inc_side.replace(
                            previous_symbol, "", 1)
                    continue

                index += 1

            except IndexError:

                index = 0

        # Format the solution side of the equation so that multiplications
        # and divisiones are made over the whole expression and not a single
        # number, using parenthesis.
        # E.g., 25x-10 = 5--> x = (5+10)/25
        self.format_parenthesis()
        if get_unknown_side is True:
            return self.sol_side

        return self.inc_side + " = " + self.sol_side

    def solve(self, show=False):
        """Evaluates  the algebraic expression.
        If show is True, displays a step by step explanation."""

        self.sort_equation()

        if show is True:

            print("Equation\n" + self.equation + "\n")
            print("Sorted:\n" + self.inc_side + " = " + self.sol_side + "\n")
            print("Solved:\n" + self.incognito +
                  " = " + str(eval(self.sol_side)) + "\n")

        return num(eval(self.sol_side))


