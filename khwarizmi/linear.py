"""Linear class and specific linear types defined with its methods and attributes."""

import matplotlib.pyplot as plt

from enum import Enum, auto
from expression import  Expression
from equations import Equation
from exc import (InvalidFormError, LinearSolutionError,
                           RedundantConversionError, UnableToDefineFormError, UnsuitableSlopeInterceptForm, InfinitelySolutionsError)
from misc import if_assign, num

class LinearForms(Enum):
    Standard = "Standard Form"
    SlopeIntercept = "Slope-Intercept"
    PointSlope = "Point-Slope"

class Linear(Equation):
    """Base class for all linear equations."""

    def __init__(self, equation):

        Equation.__init__(self, equation)
        self.form = self.get_form()
        self.x_coefficient = self.get_x_coefficient()
        self.y_coefficient = self.get_y_coefficient()
        self.slope = self.get_slope()
        self.y_intercept = num(self.solve_for("x", 0))

    def get_x_coefficient(self):
        """Returns whatever number is multiplying the x variable on this equation as a string."""

        side = if_assign(self.form is LinearForms.Standard, self.equation, self.sol_side)

        if side[0] == '-':
            coefficient = if_assign(side[1].isdigit(), self.get_number(1, side), "1")
            return '-' + coefficient
        if side[0].isdigit():
            coefficient = self.get_number(0, side)
        else:
            coefficient = 1

        return coefficient

    def get_y_coefficient(self):
        """Returns whatever number is multiplying the y variable on this equation"""

        eqtn, index = self.equation, self.equation.index('x') + 2

        if self.form == LinearForms.Standard:
            coefficient = if_assign(eqtn[index].isdigit(), self.get_number(index, eqtn), "1")

            if eqtn[index - 1] == '-':
                coefficient = '-' + coefficient
        else:
            if eqtn[0] == '-':
                coefficient = if_assign(eqtn[1].isdigit(), self.get_number(1, eqtn), "1")
                coefficient = '-' + coefficient
            else:
                coefficient = if_assign(eqtn[0].isdigit(), self.get_number(0, eqtn), "1")

        return coefficient

    def express_as(self, form):
        """Expresses the equation in the form passed as an argument
        and returns an instance of that form's class as the new expression.

        Valid forms are , Standard and .
        Keyword arguments:

        form (str): the form the equation will be converted to"""

        if self.form == LinearForms.SlopeIntercept:
            return SlopeIntercept(self.equation).express_as(form)
        if self.form == LinearForms.Standard:
            return Standard(self.equation).express_as(form)
        if self.form == LinearForms.PointSlope:
            return PointSlope(self.equation).express_as(form)

        return None

    def get_slope(self):
        """Returns the slope of this linear equation."""

        a_points, b_points = self.get_point(1), self.get_point(2)
        return num((a_points[1] - b_points[1]) / (a_points[0] - b_points[0]))

    def get_form(self):
        """ Returns the form of this linear equation."""

        if "x" in self.inc_side and "y" in self.inc_side:
            return LinearForms.Standard
        if self.equation[self.equal_index - 1] == "y":
            return LinearForms.SlopeIntercept
        if self.inc_side[0] == "y" and self.equation[self.equal_index - 1].isdigit():
            return LinearForms.PointSlope

        raise UnableToDefineFormError(self.equation)

    def points(self, a, b):
        """Returns the points formed by all values of x between a and b.

            Keyword Arguments:

            a (int): initial value of the iteration.
            b (int): last value of the iteration.
            """

        if type(a) == float or type(b) == float:
            a, b = int(round(a) - 1), int(round(b) + 1)

        solutions = []
        for i in range(a, b + 1):
            solutions.append(tuple((i, self.solve_for("x", i))))

        return solutions

    def get_point(self, x_value):
        """Returns the point formed when x is equal to x_value.

        Keyword arguments:

        x_value (int): the value of x the equation will be evaluated with to return
        the point."""

        return tuple((x_value, self.solve_for("x", x_value)))

    def graph(self, points, y_label="", x_label=""):
        """Graphs the line formed by points.

        Keyword arguments:

        points (list of tuples): the points that define the line.

        y_label (str): label to describe the y axis (optional)

        x_label (str): label to describe the x axis (optional)"""

        x, y = [], []

        x.extend((points[0][0], points[-1][0]))
        y.extend((points[0][1], points[-1][1]))

        plt.plot(x, y)
        plt.ylabel(y_label)
        plt.xlabel(x_label)

        plt.show()

    def solve(self, show=False):
        """Overwritten solve() method inherited from Equation class
        to raise error if used on Linear class."""

        raise LinearSolutionError()

    def sort(self, for_variable):
        """Sorts this equation depending on its type to be solved
        for the variable argument.

        Keyword arguments:

        for_variable (str): the variable to sort the equation for."""

        if self.form is LinearForms.PointSlope:
            return PointSlope(self.equation).sort(for_variable)
        if self.form is LinearForms.SlopeIntercept:
            return SlopeIntercept(self.equation).sort(for_variable)

        return Standard(self.equation).sort(for_variable)

    def show_sorted(self, variable, value, sol_side):
        """Shows the side pass as parameter sorted for the equation variable.

        Keyword arguments:

        variable (str): the variable to show the equation sorted for.

        value (int): the value that will replace the variable we are sorting for.

        sol_side: the side of the equation that was sorted (the solution side)."""

        if variable is self.variables[0]:
            inc = self.variables[1]
        else:
            inc = self.variables[0]

        print(inc + "=" + sol_side.replace(variable, value))

    def solve_for(self, variable, value, show=False):
        """Solves the equation after changing variable into value.

        Keyword Arguments:

        variable (str): the variable to be replaced by a value.
        value (int): the value to replace the variable by.
        (optional) show (bool) : print the sorted equation."""

        eqtn, value = self.equation, str(value)
        sol_side = self.sort(variable)

        if eqtn[eqtn.find(variable) - 1] == "(" and self.form is not LinearForms.PointSlope:
            eqtn = eqtn.replace("(" + variable, "*(" + variable)
            sol_side = eqtn[eqtn.find("=") + 1:]

        if show is True:
            self.show_sorted(variable, value, sol_side)

        return num(eval(sol_side.replace(variable, value)))


class SlopeIntercept(Linear):
    """Class for linear equations of  form."""

    def __init__(self, equation):
        self.equation = equation
        Linear.__init__(self, equation)
        self.warn_if_unsuitable()

    def __str__(self):
        return self.equation

    def warn_if_unsuitable(self):
        """Raises an error on initialization if equation is not fit."""

        if self.equation[self.equation.find('x') - 1] == "(":
            raise UnsuitableSlopeInterceptForm(self.equation)
        if any(char.isdigit() for char in self.inc_side):
            raise UnsuitableSlopeInterceptForm(self.equation)

    def sort_for_x(self):
        """Sorts equation for x."""

        eqtn, sol_side, y_coefficient = self.equation, self.sol_side, self.y_coefficient
        x_index = eqtn.index('x')

        # Set the solution side
        sol_side = "(" + sol_side + ")/" + y_coefficient
        # Add a * symbol before the x if there's a number before it.
        sol_side = if_assign(eqtn[x_index - 1].isdigit(), sol_side.replace('x', '*x'), sol_side)
        # Beautify the solution side.
        sol_side = Expression.beautify(sol_side)

        return sol_side

    def sort_for_y(self):
        """Sorts equation for y."""

        eqtn, sol_side = self.equation, self.sol_side
        x_index = eqtn.index('x')
        operator = if_assign(eqtn[x_index + 1] == '-', '+', '-')
        slope_sign = if_assign(eqtn[0] == '-', '-', '')

        sol_side = "(" + self.y_coefficient + "*y" + operator + \
                str(self.y_intercept).replace('-', '') + ")/" + slope_sign + str(self.slope)
        sol_side = Expression.beautify(sol_side)

        return sol_side


    def sort(self, for_variable):
        """Sorts a  Form linear equation
        to be solved for a given variable.

        Keyword arguments:

        variable(str) : the variable this equation will be sorted to solve for."""

        # Sorts everything to solve for x.
        if for_variable == 'x':
            return self.sort_for_x()

        # Sorts everything to solve for y.
        return self.sort_for_y()

    def express_as(self, form):
        """Expresses the equation in the form passed as an argument
        and returns an instance of that form's class as the new expression.

        Valid forms are , Standard and .
        Keyword arguments:

        form (str): the form the equation will be converted to"""

        # Required and convenient variables definition.

        slope, y_intercept = str(self.slope), str(self.y_intercept)

        if not isinstance(form, LinearForms):
            raise InvalidFormError(self.equation.form, form)
        if form == self.form:
            raise RedundantConversionError(self.form, form)

        # Express in Standard Form.
        if form is LinearForms.Standard:

            slope = slope.replace('-', '')
            x_op = if_assign(self.slope < 0, '', '-')

            # 'y' will always be positive, for negative multipliers of it will
            # be distributed. Hence why '+' is the operator before 'y'.

            rewritten = x_op + slope + "x" + '+' + "y" + "=" + y_intercept
            rewritten = Expression.beautify(rewritten)

            return Standard(rewritten)

        # Express in  form.
        if form is LinearForms.PointSlope:

            points = self.get_point(2)
            x_point, y_point = str(points[0]), str(points[1])

            rewritten = "y-" + y_point + "=" + slope + "(x-" + x_point + ")"
            rewritten = Expression.beautify(rewritten)

            return PointSlope(rewritten)

        raise InvalidFormError(form)


class Standard(Linear):
    """Class for linear equations of Standard Form."""

    def __init__(self, equation):
        Linear.__init__(self, equation)

    def __str__(self):
        return self.equation

    def sort(self, for_variable):
        """Sorts a Standard Form linear equation
        to be solved for a given variable.

        Keyword arguments:

        variable (str): the variable this equation will be sorted to solve for."""

        # Required and convenient variables definition.

        eqtn = self.equation
        c_pos, a, b = eqtn.find("=") + 1, self.x_coefficient, self.y_coefficient
        c = self.get_number(c_pos, eqtn)
        den = if_assign(for_variable == 'y', a, b)
        mult = if_assign(for_variable == 'y', b, a)

        if eqtn[eqtn.index(for_variable) - len(str(mult)) - 1] == "-":
            operator = "+"
        else:
            operator = "-"

        # Expressing

        sol_side = "(" + c + operator + mult + "*" + for_variable + ")" + "/" + den
        sol_side = Expression.beautify(sol_side)

        return sol_side

    def express_as(self, form):
        """Expresses the equation in the form passed as an argument
        and returns an instance of that form's class as the new expression.

        Valid forms are , Standard and .
        Keyword arguments:

        form (str): the form the equation will be converted to"""

        slope = str(self.slope)

        if not isinstance(form, LinearForms):
            raise InvalidFormError(form)
        if form is self.form:
            raise RedundantConversionError(self.form, form)

        if form is LinearForms.PointSlope:

            points = self.get_point(2)
            x_point, y_point = str(points[0]), str(points[1])
            rewritten = "y-" + y_point + "=" + slope + "(x-" + x_point + ")"

            rewritten = Expression.beautify(rewritten)
            return PointSlope(rewritten)

        if form == LinearForms.SlopeIntercept:
            operator = "+" if self.y_intercept > 0 else ""
            rewritten = "y=" + slope + "x" + operator + str(self.y_intercept)

            rewritten = Expression.beautify(rewritten)
            return SlopeIntercept(rewritten)

        raise InvalidFormError(form)


class PointSlope(Linear):
    """Class for all linear equations of  form."""

    def __init__(self, equation):
        Linear.__init__(self, equation)

    def __str__(self):
        return self.equation

    def sort_for_x(self):
        """Sorts equation for x."""

        eqtn, y_index = self.equation, self.equation.index('y')
        x_index = eqtn.index('x')
        y_point = self.get_number(y_index + 2, eqtn)
        x_point = self.get_number(x_index + 2, eqtn)

        slope_pos = self.equal_index + 1

        # Gets the slope instead of using self.slope because this method is called
        # before defining (and to define) the slope attribute.

        slope = self.get_number(slope_pos, eqtn)

        first_op = if_assign(eqtn[y_index + 1] == '-', '+', '-')
        second_op = eqtn[x_index + 1]

        sol_side = slope + "*(x" + second_op + x_point + ")" + first_op + y_point
        sol_side = Expression.beautify(sol_side)

        return sol_side

    def sort_for_y(self):
        """Sorts equation for y."""

        # Required and convenient variables definition.
        eqtn, y_index = self.equation, self.equation.index('y')
        x_index = eqtn.index('x')
        y_point = self.get_number(y_index + 2, eqtn)
        x_point = self.get_number(x_index + 2, eqtn)
        x_point_op = if_assign(eqtn[x_index + 1] == '-', '-', '+')

        # Expression
        sol_side = "(y" + eqtn[y_index + 1] + y_point + "-" + str(self.slope) + \
                "*" + x_point_op + x_point + ")/" + str(self.slope)

        sol_side = Expression.beautify(sol_side)
        return sol_side

    def sort(self, for_variable):
        """Sorts a  Form linear equation
        to be solved for a given variable.

        Keyword arguments:

        variable (str): the variable this equation will be sorted to solve for."""

        if for_variable == 'y':
            return self.sort_for_y()
        if for_variable == 'x':
            return self.sort_for_x()
        return None

    def express_as(self, form):
        """Expresses the equation in the form passed as an argument
        and returns an instance of that form's class as the new expression.

        Valid forms are , Standard and .
        Keyword arguments:

        form (str): the form the equation will be converted to"""

        eqtn, slope = self.equation, str(self.slope)

        if not isinstance(form, LinearForms):
            raise InvalidFormError(form)

        if form is self.form:
            raise RedundantConversionError(self.form, form)

        if form is LinearForms.SlopeIntercept:
            operator = if_assign(self.y_intercept < 0, '', '+')
            rewritten = 'y=' + slope + "x" + operator + str(self.y_intercept)

            if '--' in rewritten:
                rewritten = rewritten.replace('--', '+')

            return SlopeIntercept(rewritten)

        if form is LinearForms.Standard:
            operator = if_assign(eqtn[0] == '-', '-', '+')
            y_coefficient = if_assign(self.y_coefficient == '1', '', self.y_coefficient)

            rewritten = '-' + self.x_coefficient + 'x' + operator + \
                    y_coefficient + 'y' + '=' + str(self.y_intercept)

            rewritten = Expression.beautify(rewritten)

            return Standard(rewritten)

        raise InvalidFormError(form)


class LinearSystem:
    """This class defines the Linear System object to work with
    systems of equations."""

    def __init__(self, first_equation, second_equation):
        self.linear_1 = self.convert(first_equation)
        self.linear_2 = self.convert(second_equation)

    def is_compatible(self):
        """Returns true if there's any value of x that equally satisfies
        both equations."""

        if self.linear_1.slope != self.linear_2.slope:
            return True
        elif self.linear_2.y_intercept == self.linear_1.y_intercept:
            return True

        return False

    def get_number_of_solutions(self):
        """ Returns the number of solutions for this system
        of equations"""

        if self.is_compatible() is True:
            if self.linear_1.points(1, 2) == self.linear_2.points(1, 2):
                return 'Infinitely many solutions'

            return 'One solution'

        return 'No solutions'

    def convert(self, linear):
        """Converts a linear equation to Slope-Intercept  if under other form."""
        try:
            return linear.express_as(LinearForms.SlopeIntercept)
        except RedundantConversionError:
            return linear

    def solve(self):
        """Returns the solution to this system of equation."""

        if self.is_compatible() is False:
            return None
        if self.get_number_of_solutions() == 'Infinitely many solutions':
            raise InfinitelySolutionsError

        x_coefficient = str(num(self.linear_2.x_coefficient) - num(self.linear_1.x_coefficient))
        x_coefficient = '' if x_coefficient == '1' else x_coefficient
        equation = x_coefficient + 'x' + '=' + str(self.linear_1.y_intercept) + '-' + str(self.linear_2.y_intercept)

        x_value = Equation(equation).solve()

        return self.linear_1.get_point(x_value)

    def graph(self):

        solution_point = self.solve()
        x_solution, y_solution = solution_point[0], solution_point[1]

        first_line = self.linear_1.points(x_solution - 3, x_solution + 3)
        second_line = self.linear_2.points(x_solution - 3, x_solution + 3)

        first_x, first_y, second_x, second_y = [], [], [], []

        first_x.extend((first_line[0][0], first_line[-1][0]))
        first_y.extend((first_line[0][1], first_line[-1][1]))

        second_x.extend((second_line[0][0], second_line[-1][0]))
        second_y.extend((second_line[0][1], second_line[-1][1]))

        plt.plot(first_x, first_y)
        plt.plot(second_x, second_y)

        plt.ylabel("Y = " + str(y_solution))
        plt.xlabel("X = " + str(x_solution))

        plt.show()

    compatible = property(is_compatible)
    solutions = property(get_number_of_solutions)

