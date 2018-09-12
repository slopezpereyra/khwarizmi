import equations

class Linear (equations.Equation):

    def __init__(self, equation):

        super().__init__(equation)
        self.equation = equation.replace(" ", "")
        self.get_all_incognitos()
        self.equal_index = self.equation.index("=")

        self.indexed_incognitos = {self.incognitos[0]: self.equation.index(self.incognitos[0]),
                                   self.incognitos[1]: self.equation.index(self.incognitos[1])}

        self.form = self.get_equation_form()
        self.slope = self.get_slope()
        self.y_intercept = self.get_y_intercept(self.equation)

    def get_all_incognitos (self):
        """ """

        index = 0
        for symbol in self.equation:

            if symbol.isalpha() and symbol not in self.incognitos:
                self.incognitos.append(symbol)



    def get_slope (self):

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
            replaced_solution_side = self.solution_side.replace("(x", "*(0")

        else:
            replaced_solution_side = self.solution_side.replace("x", "*0")

        return eval(replaced_solution_side)


    def get_equation_form (self):

        if self.equation[0] == "y" and self.equation[1] == "=":

            return "Slope-Intercept Form"

        if self.incognito_side[0] == "y" and self.equation[self.equal_index - 1].isdigit():
            return "Point-Slope Form"

    def points(self, count):
        """Returns range number of points which are solution for this equation."""

        solutions = []

        for i in range(1, count + 1):

            equation = self.solution_side
            if self.equation[self.indexed_incognitos["x"] - 1] == "(":
                equation = equation.replace("(x", "*(" + str(i))
            else:
                equation = equation.replace("x", "*" + str(i))
            solutions.append(tuple((i, eval(equation))))

        return solutions

    def get_point(self, x_value):

        # Confusing, uh? Returns, as a tuple, the x_value and the y_value that results
        # of that x_value.

        if self.equation[self.indexed_incognitos["x"] - 1] == "(":
            return(tuple((x_value, eval(self.solution_side.replace("(x", "*(" + str(x_value))))))

        return(tuple((x_value, eval(self.solution_side.replace("x", "*" + str(x_value))))))





LINEAR = Linear ("y = 3x - 9")
print(LINEAR.form)
print(LINEAR.points(10))
print(LINEAR.get_point(10))
print(LINEAR.slope)

