"""Defines an equation class and its functions."""

operators = ["-", "+", "/", "*"]

class Equation :

    def __init__ (self, equation):
        # equation
        self.equation = equation.replace(" ", "")
        # sides of the equation
        self.solution_side = ""
        self.incognito_side = ""
        self.get_sides()
        # incognito
        self.incognito = self.return_incognito(self.equation)
        self.incognito_index = self.equation.index(self.incognito)
        self.dyn_incognito_index = self.equation.index(self.incognito)
        # incognito multiplier
        self.multiplier_length = 0
        self.inc_multiplier = self.return_inc_multiplier()
        self.dyn_inc_mult_index = self.incognito_index - self.multiplier_length
        self.inc_mult_index = self.incognito_index - self.multiplier_length
        # sorted and solved equation
        self.sorted_equation = self.sort_equation()
        self.solution = self.solve()

    def __str__(self) :

        str = self.equation
        return str


    def update_dynamic_data (self):

        self.return_incognito(self.incognito_side)
        self.dyn_inc_mult_index = self.dyn_incognito_index - 1


    def return_incognito(self, expression) :
        """Returns the incognito of the equation; this is, any
        character of the equation string that is not a number and rather
        a letter. E.g. the letter x or y."""

        index = 0

        for character in expression:

            if character.isalpha() is True:

                self.dyn_incognito_index = index
                return character

            index += 1

        print ("There's no incognito to be cleared on this equation!")

    def return_inc_multiplier (self):

        number = ""
        parser = 1

        while self.incognito_side [self.incognito_index - parser].isdigit() and parser <= self.incognito_index:
            number = self.incognito_side[self.incognito_index - parser] + number
            parser += 1

        self.multiplier_length = len(number)
        return number

    def get_sides(self):

        try:
            equal_sign = self.equation.index("=")
            self.incognito_side = self.equation[0:equal_sign]
            self.solution_side = self.equation[equal_sign + 1:]

        except ValueError:
            print("There isn't an equality defined on the passed equation.")

    def get_operator (self, number_pos, full_number):
        """Returns True if number is positive; otherwise returns False."""

        character = self.incognito_side[number_pos]

        if number_pos > 0 and character not in operators:
            if full_number == self.inc_multiplier:
                return "/"
            elif self.incognito_side[number_pos - 1] == "+":
                return "-"
            else:
                return "+"

        elif full_number == self.inc_multiplier:
            return "/"

        else:
            return "-"

    def format_parenthesis (self) :
        """Formats parenthesis positions if required"""

        high_operator = self.solution_side.index("/")
        high_operation = self.solution_side[high_operator: high_operator + self.multiplier_length + 1]

        # high operation = all characters from the operator / to the last cipher of the number.
        # If operation is x = 50/25-70, high operation is "/25".

        self.solution_side = "(" + self.solution_side.replace(high_operation, "") + ")" + high_operation

    def get_full_number(self, number, index, parser=1):
        """Get's all the numbers that form a full number and returns the full
        numbers.

        Keyword Arguments:

        number -- first number to which append following numbers
        index -- index of the number being initially parsed, which is number"""

        if len(self.incognito_side) > index + parser - 1:

            while self.incognito_side[index + parser].isdigit():

                number += self.incognito_side[index + parser]

                if index + parser + 1 < len(self.incognito_side):
                    print ("O K")
                    parser += 1
                else:
                    return number

        return number

    def sort_equation (self) :
        """Sorts the equation, which is a very highschool, wrongly phrased
        way of saying that clears the incognito side by substracting all
        positive numbers, adding all negative numbers, dividing all multipliers
        and multiplying all divisors, doing the same operations on the solution
        side. """

        index = 0

        while len(self.incognito_side) > 1:
            symbol = self.incognito_side[index]
            try:
                if symbol.isdigit():

                    # Get the symbol (the full number) and its index.
                    symbol = self.get_full_number(symbol, index)
                    previous_symbol = self.incognito_side[index - 1] # THIS IS OKAY SANTIAGO STOP BREAKING IT!
                    operator = self.get_operator(index, symbol)

                    # Pass the number from the incognito side of the equation to
                    # the solution side, with the proper operator...

                    self.solution_side += operator + symbol
                    self.incognito_side = self.incognito_side.replace(symbol, "", 1)

                    if previous_symbol in operators:
                        # If there's an operator before this symbol, erase it.

                        self.incognito_side = self.incognito_side.replace(previous_symbol, "", 1)

                    self.update_dynamic_data()

                    continue

                index += 1

            except IndexError:

                index = 0;

        self.format_parenthesis()
        return self.incognito_side + " = " + self.solution_side

    def solve (self) :
        """Evaluates  the algebraic expression."""

        return self.incognito + " = " + str(eval(self.solution_side))
