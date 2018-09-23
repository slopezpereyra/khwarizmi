from exceptions import (InvalidFormError, LinearSolutionError,
                        RedundantConversionError)

import equations
from equations import operators
from lib.misc import cond_assign, num


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
        self.multipliers = self.return_multipliers()
        self.slope = self.get_slope()
        self.y_intercept = self.solve_for("x", 0)

    def get_all_incognitos(self):
        """Adds every incognito of the equation
        to the incognitos attribute (list)."""

        index = 0
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in self.incognitos:
                self.incognitos.append(symbol)

    def return_multipliers(self):

        if self.form == "Slope-Intercept Form":
            return SlopeIntercept(self.equation).return_multipliers()
        elif self.form == "Standard Form":
            return Standard(self.equation).return_multipliers()

    def get_slope(self):
        """Returns the slope of this linear equation."""

        a_points, b_points = self.get_point(1), self.get_point(2)
        return (a_points[1] - b_points[1]) / (a_points[0] - b_points[0])

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

    def show_sorted(self, variable, value, sol_side):

        if variable is self.incognitos[0]:
            inc = self.incognitos[1]
        else:
            inc = self.incognitos[0]

        print(inc + "=" + sol_side.replace(variable, value))

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
            self.show_sorted(variable, value, sol_side)

        return eval(sol_side.replace(variable, value))


class SlopeIntercept(Linear):

    def __init__(self, equation):
        self.equation = equation
        super().__init__(equation)

    def __str__(self):
        return self.equation

    def return_multipliers(self):

        index, eqtn = self.equal_index + 1, self.equation
        x_mult = cond_assign(
            eqtn[index + 1].isdigit(), self.get_number(eqtn[index + 1], index + 1), "1")
        y_mult = cond_assign(
            eqtn[0].isdigit(), self.get_number(eqtn[0], 0), "1")

        return {"x": x_mult, "y": y_mult}

    def sort(self, for_variable):
        """Sorts a Slope-Intercept Form linear equation
        to be solved for a given variable."""

        eqtn = self.equation
        sol_side = self.sol_side

        y_mult = cond_assign(
            eqtn[0].isdigit(), self.get_number(eqtn[0], 0), "1")

        # Sorts everything to solve for x.
        if for_variable == 'x':
            sol_side = "(" + sol_side + ")/" + y_mult
            sol_side = sol_side.replace(
                for_variable, "*" + for_variable)

            return sol_side

        # Sorts everything to solve for y.
        y_index = self.indexed_incognitos["y"]
        x_index = self.indexed_incognitos["x"]

        if eqtn[x_index - 1] == "(":

            b_index = sol_side.find("+") + 1
            b = self.get_number(sol_side[b_index], b_index, sol_side)

            sol_side = "(y" + "-" + self.slope + "*" + b + ")/" + self.slope
            return sol_side

        sol_side = "(" + y_mult + "*y-" + \
            str(self.y_intercept) + ")/" + str(self.slope)

        return sol_side

    def express_as(self, form):

        eqtn, slope, mults = self.equation, str(self.slope), self.multipliers
        forms = ["Slope-Intercept", "Point-Slope", "Standard"]
        if form not in forms:
            raise InvalidFormError(form, forms)
        if form in self.form:
            raise RedundantConversionError(form)

        if form == "Standard":

            slope = slope.replace('-', '')
            y_op = cond_assign(eqtn[0] == '-', '-', '+')
            y_mult = cond_assign(mults['y'] == '1', '', mults['y'])
            x_op = cond_assign(self.slope < 0, '', '-')

            rewritten = x_op + slope + "x" + \
                y_op + y_mult + "y" + "=" + str(self.y_intercept)

            return Standard(rewritten)

        elif form == "Point-Slope":
            points = self.get_point(2)
            x_point, y_point = str(points[0]), str(points[1])

            rewritten = "y-" + y_point + "=" + \
                slope + "(x-" + x_point + ")"

            return PointSlope(rewritten)


class Standard (Linear):
    def __init__(self, equation):
        super().__init__(equation)

    def __str__(self):
        return self.equation

    def return_multipliers(self):

        eqtn, index = self.equation, self.equation.find("x") + 2

        x_mult = cond_assign(
            eqtn[0].isdigit(), self.get_number(eqtn[0], 0), "1")
        y_mult = cond_assign(eqtn[index].isdigit(),
                             self.get_number(eqtn[index], index), "1")

        return {"x": x_mult, "y": y_mult}

    def sort(self, for_variable):

        eqtn = self.equation
        sol_side = self.sol_side

        c_pos = eqtn.find("=") + 1
        a, b = self.multipliers["x"], self.multipliers["y"]

        c = self.get_number(eqtn[c_pos], c_pos)

        den = cond_assign(for_variable == 'y', a, b)
        mult = cond_assign(for_variable == 'y', b, a)

        if eqtn[self.indexed_incognitos[for_variable] - len(mult) - 1] == "-":
            op = "+"
        else:
            op = "-"

        sol_side = "(" + c + op + mult + "*" + for_variable + ")" + "/" + den
        return sol_side

    def express_as(self, form):
        """Returns an equivalent expression of the equation in the form
        passed as parameter.

        Keyword arguments:

        (str) form: the form into which convert this equation."""

        eqtn, slope = self.equation, str(self.slope)
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

    def return_multipliers(self):

        eqtn, index = self.equation, self.equal_index + 1

        if eqtn[index] in operators:
            x_mult = cond_assign(
                eqtn[index + 1].isdigit(), self.get_number(eqtn[index + 1], index + 1), "1")
        elif eqtn[index].isdigit():
            x_mult = cond_assign(eqtn[index].isdigit(
            ), self.get_number(eqtn[index], index), "1")

        y_mult = cond_assign(eqtn[0].isdigit(),
                             self.get_number(eqtn[0], 0), "1")

        return {"x": x_mult, "y": y_mult}

    def sort(self, for_variable):
        """Sorts a Point-Slope Formed linear equation
        to be solved for a given variable."""

        eqtn, y_index = self.equation, self.indexed_incognitos["y"]
        sol_side = self.sol_side
        x_index, slope_pos = self.indexed_incognitos["x"], self.equal_index + 1

        y_point = self.get_number(eqtn[y_index + 2], y_index + 2, eqtn)
        slope = self.get_number(eqtn[slope_pos], slope_pos, eqtn)
        x_point = self.get_number(eqtn[x_index + 2], x_index + 2, eqtn)

        if for_variable == 'y':

            sol_side = "(y" + eqtn[y_index + 1] + \
                y_point + "+" + slope + "*" + x_point + ")/" + slope

            return sol_side

        elif for_variable == 'x':

            first_op = cond_assign(eqtn[y_index + 1] == '-', '+', '-')
            second_op = eqtn[x_index + 1]

            sol_side = slope + \
                "*(x" + second_op + x_point + ")" + first_op + y_point

            return sol_side

    def express_as(self, form):
        """Express this equation in the form passed as an argument.

        Keyword arguments:

        form : form on which to express the equation."""

        eqtn, slope = self.equation, str(self.slope)
        forms = ["Slope-Intercept", "Point-Slope", "Standard"]

        if form not in forms:
            raise InvalidFormError(form, forms)
        if form in self.form:
            raise RedundantConversionError(form)

        if form == 'Slope-Intercept':

            op = cond_assign(self.y_intercept < 0, '-', '+')
            rewritten = 'y=' + slope + "x" + op + str(self.y_intercept)

            return SlopeIntercept(rewritten)

        elif form == 'Standard':

            op = cond_assign(eqtn[0] == '-', '-', '+')
            y_mult = cond_assign(
                self.multipliers['y'] == '1', '', self.multipliers['y'])

            rewritten = self.multipliers['x'] + 'x' + op + \
                y_mult + 'y' + '=' + str(self.y_intercept)

            return Standard(rewritten)


a = SlopeIntercept("y = 5x - 3")
b = PointSlope("y - 9 = 5 (x + 3)")
c = Standard("2x + 5y = 9")
a_point_slope = a.express_as("Point-Slope")
print(a_point_slope)
