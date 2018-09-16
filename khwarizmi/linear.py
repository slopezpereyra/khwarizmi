from exceptions import LinearSolutionError

import equations


class Linear (equations.Equation):

    def __init__(self, equation):
        super().__init__(equation)
        self.get_all_incognitos()
        self.equal_index = self.equation.index("=")

        self.indexed_incognitos = {self.incognitos[0]:
                                   self.equation.index(self.incognitos[0]),
                                   self.incognitos[1]:
                                   self.equation.index(self.incognitos[1])}

        self.form = self.get_equation_form()
        self.slope = self.get_slope()
        self.y_intercept = self.get_y_intercept(self.equation)

    def get_all_incognitos(self):
        """ """

        index = 0
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in self.incognitos:
                self.incognitos.append(symbol)

    def get_slope(self):

        x_index = self.indexed_incognitos.get("x")

        if self.equation[x_index - 1].isdigit() is False:
            return 1

        parser = 2
        slope = self.equation[x_index - 1]

        while self.equation[x_index - parser].isdigit() or self.equation[x_index - parser] == "/":
            slope = self.equation[x_index - parser] + slope
            parser += 1

        return slope

    def get_y_intercept(self, expression):

        if self.equation[self.indexed_incognitos["x"] - 1] == "(":
            replaced_sol_side = self.sol_side.replace("(x", "*(0")

        else:
            replaced_sol_side = self.sol_side.replace("x", "*0")

        return eval(replaced_sol_side)

    def get_equation_form(self):

        if self.equation[0] == "y" and self.equation[1] == "=":
            return "Slope-Intercept Form"

        if self.inc_side[0] == "y" and self.equation[self.equal_index - 1].isdigit():
            return "Point-Slope Form"

    def points(self, a, b):
        """Returns the points formed by all values of x between a and b.

        Keyword Arguments:

        a: initial value of the iteration.
        b: last value of the iteration.
        """

        solutions = []

        for i in range(a, b + 1):

            equation = self.sol_side
            if self.equation[self.indexed_incognitos["x"] - 1] == "(":
                equation = equation.replace("(x", "*(" + str(i))
            else:
                equation = equation.replace("x", "*" + str(i))
            solutions.append(tuple((i, eval(equation))))

        return solutions

    def get_point(self, x_value):
        """Returns the point formed when x is equal to x_value.

        Keyword arguments:

        x_value : the value of x the equation will be evaluated with to return
        the point."""

        # Confusing, uh? Returns, as a tuple, the x_value and the y_value that
        # results of that x_value.

        if self.equation[self.indexed_incognitos["x"] - 1] == "(":
            return(tuple((x_value, eval(self.sol_side.replace(
                "(x", "*(" + str(x_value))))))

        return(tuple((x_value, eval(self.sol_side.replace(
                                    "x", "*" + str(x_value))))))

    def solve(self):
        raise LinearSolutionError()

    def sort_for_pl_form(self, for_variable):
        """Sorts a Point-Slope Formed linear equation
        to be solved for a given variable."""

        equation = self.equation

        y_index = self.indexed_incognitos["y"]

        y_point = self.get_full_number(
            equation[y_index + 2], y_index + 2, equation)

        x_index = self.indexed_incognitos["x"]

        slope = self.get_full_number(
            equation[self.equal_index + 1], self.equal_index + 1, equation)

        x_point = self.get_full_number(
            equation[x_index + 2], x_index + 2, equation)

        if for_variable == 'y':

            self.sol_side = "(y" + equation[y_index + 1] + y_point + "+" + slope + \
                "*" + x_point + ")/" + slope

        elif for_variable == 'x':

            if equation[y_index + 1] == "-":
                first_op = "+"
            elif equation[y_index + 1] == "+":
                first_op = "-"

            second_op = equation[x_index + 1]

            self.sol_side = slope + "*x" + second_op + \
                slope + "*" + x_point + first_op + y_point

            return "y = " + self.sol_side

    def sort_for_si_form(self, for_variable):
        """Sorts a Slope-Intercept Form linear equation
        to be solved for a given variable."""

        equation = self.equation

        y_index = self.indexed_incognitos["y"]
        x_index = self.indexed_incognitos["x"]

        slope = self.get_full_number(
            equation[self.equal_index + 1], self.equal_index + 1, equation)

        if for_variable == "y":

            print("(y-" + str(self.y_intercept) + ")/" + slope)
            self.sol_side = "(y-" + str(self.y_intercept) + ")/" + slope

        else:

            return self.sort_equation()

    def sort_linear_equation(self, for_variable):

        if self.form == "Point-Slope Form":

            return self.sort_for_pl_form(for_variable)

        else:

            return self.sort_for_si_form(for_variable)

    def solve_for(self, variable, value, show=False):
        """Solves the equation after changing variable into value.

        Keyword Arguments:

        variable : the variable to be replaced by a value.
        value : the value to replace the variable by.
        (optional) show : print the sorted equation."""

        value = str(value)
        self.sort_linear_equation(variable)

        if show is True:

            if variable is self.incognitos[0]:
                inc = self.incognitos[1]
            else:
                inc = self.incognitos[0]

            if self.equation[self.indexed_incognitos[variable] - 1].isdigit():
                print(inc + "=" + self.sol_side.replace(variable, "*" + value))
            else:
                print(inc + "=" + self.sol_side.replace(variable, value))

        if variable == "x":
            self.sol_side.replace("(", "*(")

            if self.indexed_incognitos[variable] > 0:

                if self.equation[self.indexed_incognitos[variable] - 1].isdigit():

                    return eval(self.sol_side.replace(variable, "*" + value))

        return eval(self.sol_side.replace(variable, value))


LINEAR = Linear("y = 5x - 3")
LINEAR2 = Linear("y - 9 = 5 (x + 3)")


print(LINEAR.form)
print(LINEAR2.form)
print(LINEAR.solve_for("x", 3, True))
print("\n---\n")
print(LINEAR2.solve_for("y", 1.03486, True))
print(LINEAR.solve_for("x", "5"))
print(LINEAR2.solve_for("x", "5"))
