"""Defines an equation class and its functions."""


operators = ["-", "+", "/", "*"]

class Equation :

    def __init__ (self, equation):

        self.equation = equation
        self.incognito_index = 0
        self.incognito = self.return_incognito()
        self.solution_side = ""
        self.incognito_side = ""
        self.get_sides()
        self.sorted_equation = self.sort_equation()

    def __str__(self) :

        str = self.equation
        return str



    def return_incognito(self) :
        """Returns the incognito of the equation; this is, any
        character of the equation string that is not a number and rather
        a letter. E.g. the letter x or y."""

        index = 0

        for character in self.equation:

            if character.isalpha() is True:

                self.incognito_index = index
                return character

            index += 1

        print ("There's no incognito to be cleared on this equation!")

    def return_inc_mult (self) :
        """Returns the incognito multiplier if any. This is,
        the number that multiplies the incognito. For example,
        if we have 2x + 1 = 5, inc_mul is 2."""

        if self.equation[self.incognito_index] != "":
            return self.equation[self.incognito_index - 1]

    def get_sides(self):

        try:
            equal_sign = self.equation.index("=")
            self.incognito_side = self.equation[0:equal_sign]
            self.solution_side = self.equation[equal_sign + 1:]

        except ValueError:
            print("There isn't an equality defined on the passed equation.")

    def is_positive (self, number_pos):
        """Returns True if number is positive; otherwise returns False."""

        if number_pos > 0:

            print("LOOK HERE ", self.incognito_side[number_pos - 2:number_pos])

            if "-" not in self.incognito_side[number_pos - 2:number_pos]:
                # if there's not a substraction symbol two places before this number.
                return True
            else:
                return False

    def sort_equation (self) :
        """Sorts the equation, which is a very highschool, wrongly phrased
        way of saying that clears the incognito side by substracting all
        positive numbers, adding all negative numbers, dividing all multipliers
        and multiplying all divisors, doing the same operations on the solution
        side. """

        index = 0

        while len(self.incognito_side) > 1:

            try:
                if self.incognito_side[index].isdigit():

                    print(self.incognito_side[index])

                    is_positive = self.is_positive(index)

                    if is_positive is True:
                        operator = "-"
                    else:
                        operator = "+"

                    self.solution_side += operator + self.incognito_side[index]
                    self.incognito_side = self.incognito_side.replace(self.incognito_side[index], "", 1)

                    if self.incognito_side[index - 2] in operators:

                        self.incognito_side = self.incognito_side.replace(self.incognito_side[index - 2], "", 1)

                    continue

                elif self.incognito_side[index] == " ":
                    self.incognito_side = self.incognito_side.replace(self.incognito_side[index], "", 1)

                index += 1

            except IndexError:

                index = 0;

        return self.incognito_side + " = " + self.solution_side


EQUATION = Equation("2x+5=9")
print("EQUATION IS ", EQUATION)
print("INCOGNITO IS ", EQUATION.incognito)
print("MULTIPLIER INDEX IS ", EQUATION.incognito_index  )
print("SOLUTION SIDE ", EQUATION.solution_side)
print("INCOGNITO SIDE ", EQUATION.incognito_side)
print("SORTED ", EQUATION.sorted_equation)
