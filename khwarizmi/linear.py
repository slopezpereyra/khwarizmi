from exceptions import (InvalidFormError, LinearSolutionError,
                        RedundantConversionError)

import equations
from lib.mathlib import num


class Linear (equations.Equation):

    def __init__(self, equation):
        super().__init__(equation)
        self.get_all_incognitos()
        self.equal_index = self.equation.index("=")
        self.indexed_incognitos = {self.incognitos[0]:
                                   self.equation.index(self.incognitos[0]),
                                   self.incognitos[1]:
                                   self.equation.index(self.incognitos[1])}
        self.form = self.get_form()
        self.slope = self.get_slope()
        self.y_intercept = self.get_y_intercept(self.equation)

    def get_all_incognitos(self):
        """Adds every incognito of the equation
        to the incognitos attribute (list)."""

        index = 0
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in self.incognitos:
                self.incognitos.append(symbol)

    def get_slope(self):
        """Returns the slope of this linear equation."""

        a_points, b_points = self.get_point(1), self.get_point(2)
        print("A POINT, B POINT ", a_points, b_points)
        return (a_points[1] - b_points[1]) / (a_points[0] - b_points[0])

    def get_y_intercept(self, expression):

        if self.form == "Standard Form":
            return self.solve_for("x", 0)

        if self.equation[self.indexed_incognitos["x"] - 1] == "(":
            replaced_sol_side = self.sol_side.replace("(x", "*(0")

        else:

            replaced_sol_side = self.sol_side.replace("x", "*0")

        return eval(replaced_sol_side)

    def get_form(self):
        if "x" in self.inc_side and "y" in self.inc_side:
            return "Standard Form"
        if self.equation[self.equal_index - 1] == "y":
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
            solutions.append(tuple((i, self.solve_for("x", i))))

        return solutions

    def get_point(self, x_value):
        """Returns the point formed when x is equal to x_value.

        Keyword arguments:

        x_value : the value of x the equation will be evaluated with to return
        the point."""

        # Confusing, uh? Returns, as a tuple, the value of x and the resulting
        # value of y.

        return(tuple((x_value, self.solve_for("x", x_value))))

    def solve(self):
        raise LinearSolutionError()

    def sort(self, for_variable):

        if self.form == "Point-Slope Form":

            return self.sort_for_pl_form(for_variable)

        elif self.form == "Slope-Intercept Form":
            return SlopeIntercept(self.equation).sort(for_variable)

        else:
            std = Standard(self.equation)
            return std.sort(for_variable)

    def show_sorted(self, variable, value):

        if variable is self.incognitos[0]:
            inc = self.incognitos[1]
        else:
            inc = self.incognitos[0]

        print(inc + "=" + self.sol_side.replace(variable, value))

    def solve_for(self, variable, value, show=False):
        """Solves the equation after changing variable into value.

        Keyword Arguments:

        variable : the variable to be replaced by a value.
        value : the value to replace the variable by.
        (optional) show : print the sorted equation."""

        eqtn, indexed_inc = self.equation, self.indexed_incognitos
        value = str(value)

        sol_side = self.sort(variable)

        if eqtn[eqtn.find(variable) - 1] == "(" and self.form != "Point-Slope Form":
            eqtn = eqtn.replace("(" + variable, "*(" + variable)
            sol_side = eqtn[eqtn.find("=") + 1:]

        if show is True:
            self.show_sorted(variable, value)

        return eval(sol_side.replace(variable, value))


class SlopeIntercept(Linear):

    def __init__(self, equation):
        self.equation = equation
        super().__init__(equation)

    def __str__(self):
        return self.equation

    def sort(self, for_variable):
        """Sorts a Slope-Intercept Form linear equation
        to be solved for a given variable."""

        eqtn = self.equation
        sol_side = self.sol_side

        y_mult = "1"

        if eqtn[0].isdigit():
            y_mult = self.get_full_number(eqtn[0], 0)

        if for_variable == 'x':
            sol_side = "(" + sol_side + ")/" + y_mult
            sol_side = sol_side.replace(
                for_variable, "*" + for_variable)
            return sol_side

        y_index = self.indexed_incognitos["y"]
        x_index = self.indexed_incognitos["x"]

        if eqtn[x_index - 1] == "(":
            b_index = sol_side.find("+") + 1
            b = self.get_full_number(
                sol_side[b_index], b_index, sol_side)

            sol_side = "(y" + "-" + self.slope + \
                "*" + b + ")/" + self.slope
            return sol_side

        sol_side = "(" + y_mult + "*y-" + \
            str(self.y_intercept) + ")/" + str(self.slope)
        return sol_side


class Standard (Linear):
    def __init__(self, equation):
        super().__init__(equation)
        print("INIT ", self.slope)

    def __str__(self):
        return self.equation

    def sort(self, for_variable):

        eqtn = self.equation
        sol_side = self.sol_side

        if eqtn[0].isdigit():
            a = self.get_full_number(eqtn[0], 0, eqtn)
        elif eqtn[1].isdigit():
            a = self.get_full_number(eqtn[1], 1, eqtn)

        if eqtn[eqtn.find("x") + 2].isdigit():
            b = self.get_full_number(
                eqtn[eqtn.find("x") + 2], eqtn.find("x") + 2, eqtn)

        if eqtn[eqtn.find("=") + 1].isdigit():
            c = self.get_full_number(
                eqtn[eqtn.find("=") + 1], eqtn.find("=") + 1, eqtn)

        if for_variable == "y":
            denominator = a
            mult = b
        elif for_variable == "x":
            denominator = b
            mult = a

        if eqtn[self.indexed_incognitos[for_variable] - len(mult) - 1] == "-":
            op = "+"
        else:
            op = "-"

        sol_side = "(" + c + op + mult + "*" + \
            for_variable + ")" + "/" + denominator

        return sol_side

    def express_as(self, form):
        """Returns an equivalent expression of the equation in the form
        passed as parameter.

        Keyword arguments:

        (str) form: the form into which convert this equation."""

        eqtn, slope = self.equation, str(self.slope)
        print("SLOPE IS ", slope)

        forms = ["Slope-Intercept", "Point-Slope", "Standard"]

        if form not in forms:
            raise InvalidFormError(form, forms)
        if form in self.form:
            raise RedundantConversionError(form)

        if form == "Point-Slope":
            points = self.get_point(2)
            x_point, y_point = str(points[0]), str(points[1])

            rewritten = "y-" + y_point + "=" + \
                slope + "(x-" + x_point + ")"

            return PointSlope(rewritten)

        elif form == "Slope-Intercept":
            op = "-" if eqtn[eqtn.find("=") + 1] == "-" else "+"

            rewritten = "y=" + slope + "x" + op + str(self.y_intercept)

            return SlopeIntercept(rewritten)


class PointSlope (Linear):
    def __init__(self, equation):
        super().__init__(equation)

    def __str__(self):
        return self.equation

    def sort(self, for_variable):
        """Sorts a Point-Slope Formed linear equation
        to be solved for a given variable."""

        eqtn, y_index = self.equation, self.indexed_incognitos["y"]
        sol_side = self.sol_side
        x_index, slope_pos = self.indexed_incognitos["x"], self.equal_index + 1

        y_point = self.get_full_number(eqtn[y_index + 2], y_index + 2, eqtn)
        slope = self.get_full_number(eqtn[slope_pos], slope_pos, eqtn)
        x_point = self.get_full_number(eqtn[x_index + 2], x_index + 2, eqtn)

        if for_variable == 'y':

            sol_side = "(y" + eqtn[y_index + 1] + \
                y_point + "+" + slope + "*" + x_point + ")/" + slope

        elif for_variable == 'x':
            if eqtn[y_index + 1] == "-":
                first_op = "+"
            elif eqtn[y_index + 1] == "+":
                first_op = "-"

            second_op = eqtn[x_index + 1]

            sol_side = slope + \
                "*(x" + second_op + x_point + ")" + first_op + y_point

            return sol_side


LINEAR = Standard("5x + 2y = 3")
POINT = LINEAR.express_as("Slope-Intercept")

print("\nLINEAR = ", LINEAR)
print("POINT = ", POINT, "\n")


#print(LINEAR.solve_for("x", 3, True))
#print(POINT.solve_for("x", 3, True))
