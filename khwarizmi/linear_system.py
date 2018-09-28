from khwarizmi import equations, linear


class LinearSystem():

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def iscompatible(self):
        """Returns true if there's any value of x that equally satisfies
        both equations."""

        return True if self.first.slope != self.second.slope else False

    def solutions(self):
        """ Returns the number of solutions for this system
        of equations"""

        if self.iscompatible() is True:
            if self.first.points(1, 2) == self.second.points(1, 2):
                return 'Infinitely many solutions'
            else:
                return 'One solution'
        else:
            return 'No solutions'

    def get_solution(self):
        """Returns the solution of this system of equations."""

        if self.solutions() == 'One solution':
            return self.solve()

    def solve(self):

        if self.first.form != 'Slope-Intercept Form':
            self.first = self.first.express_as('Slope-Intercept')

        if self.second.form != 'Slope-Intercept Form':
            self.second = self.second.express_as('Slope-Intercept')

        second_mults = self.second.return_multipliers()
        first_mults = self.first.return_multipliers()

        x_total = first_mults['x'] - second_mults['x']
        first_original = self.first.equation

        first.equation = first.equation.replace(str(first_mults['x']), str(x_total))
        second.equation = second.equation.replace(str(second_mults['x']) + 'x', '')
        first.get_sides()
        second.get_sides()

        eqtn = self.first.sol_side + '=' + self.second.sol_side

        eqtn = equations.Equation(eqtn)
        x = eqtn.solve()
        y = linear.Linear(first_original).solve_for('x', x)

        return (x, y)


first = linear.Linear('y = -2x + 5')
second = linear.Linear('y = -5x + 3')

system = LinearSystem(first, second)
print(system.get_solution())
