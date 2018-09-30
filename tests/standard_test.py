from khwarizmi import linear, exc
import unittest

class SlopeInterceptTest(unittest.TestCase):

    def setUp(self):
        self.linear_1 = linear.Standard('-2x - y = 3')
        self.linear_2 = linear.Standard('-5x - 2y = 10')
        self.linear_3 = linear.Standard('5x + y = -15')
        self.linear_4 = linear.Standard('-x + y = 5')

    def test_equation(self):
        self.assertEqual(self.linear_1.equation, '-2x-y=3')
        self.assertEqual(self.linear_2.equation, '-5x-2y=10')
        self.assertEqual(self.linear_3.equation, '5x+y=-15')
        self.assertEqual(self.linear_4.equation, '-x+y=5')

    def test_form(self):
        self.assertEqual(self.linear_1.form, 'Standard Form')
        self.assertEqual(self.linear_2.form, 'Standard Form')
        self.assertEqual(self.linear_3.form, 'Standard Form')
        self.assertEqual(self.linear_4.form, 'Standard Form')

    def test_x_mult(self):
        self.assertEqual(self.linear_1.x_mult, '-2')
        self.assertEqual(self.linear_2.x_mult, '-5')
        self.assertEqual(self.linear_3.x_mult, '5')
        self.assertEqual(self.linear_4.x_mult, '-1')

    def test_y_mult(self):
        self.assertEqual(self.linear_1.y_mult, '-1')
        self.assertEqual(self.linear_2.y_mult, '-2')
        self.assertEqual(self.linear_3.y_mult, '1')
        self.assertEqual(self.linear_4.y_mult, '1')

    def test_slope(self):
        self.assertEqual(self.linear_1.slope, -2)
        self.assertEqual(self.linear_2.slope, -2.5)
        self.assertEqual(self.linear_3.slope, -5)
        self.assertEqual(self.linear_4.slope, 1)

    def test_y_intercept(self):
        self.assertEqual(self.linear_1.y_intercept, -3)
        self.assertEqual(self.linear_2.y_intercept, -5)
        self.assertEqual(self.linear_3.y_intercept, -15)
        self.assertEqual(self.linear_4.y_intercept, 5)

    def test_points(self):
        self.assertEqual(self.linear_1.points(-1, 0), [(-1, -1), (0, -3)])
        self.assertEqual(self.linear_2.points(1, 2), [(1, -7.5), (2, -10)])
        self.assertEqual(self.linear_3.points(1, 2), [(1, -20), (2, -25)])
        self.assertEqual(self.linear_4.points(2, 3), [(2, 7), (3, 8)])

    def test_get_point(self):
        self.assertEqual(self.linear_1.get_point(5), (5, -13))
        self.assertEqual(self.linear_2.get_point(1.25), (1.25, -8.125))
        self.assertEqual(self.linear_3.get_point(5), (5, -40))
        self.assertEqual(self.linear_4.get_point(-10), (-10, -5))

    def test_solve(self):
        with self.assertRaises(exc.LinearSolutionError):
            self.assertEqual(self.linear_1.solve())
            self.assertEqual(self.linear_2.solve())
            self.assertEqual(self.linear_3.solve())
            self.assertEqual(self.linear_4.solve())

    def test_sort_for_x(self):
        self.assertEqual(self.linear_1.sort('x'), '(3+2*x)/-1')
        self.assertEqual(self.linear_2.sort('x'), '(10+5*x)/-2')
        self.assertEqual(self.linear_3.sort('x'), '(-15-5*x)/1')
        self.assertEqual(self.linear_4.sort('x'), '(5+1*x)/1')

    def test_sort_for_y(self):
        self.assertEqual(self.linear_1.sort('y'), '(3+1*y)/-2')
        self.assertEqual(self.linear_2.sort('y'), '(10+2*y)/-5')
        self.assertEqual(self.linear_3.sort('y'), '(-15-1*y)/5')
        self.assertEqual(self.linear_4.sort('y'), '(5-1*y)/-1')

    def test_expressing_as_slope_intercept(self):
        self.assertEqual(self.linear_1.express_as('Slope-Intercept').equation, 'y=-2x-3')
        self.assertEqual(self.linear_2.express_as('Slope-Intercept').equation, 'y=-2.5x-5')
        self.assertEqual(self.linear_3.express_as('Slope-Intercept').equation, 'y=-5x-15')
        self.assertEqual(self.linear_4.express_as('Slope-Intercept').equation, 'y=1x+5')

    def test_expressing_as_point_slope(self):
        self.assertEqual(self.linear_1.express_as('Point-Slope').equation, 'y+7=-2(x-2)')
        self.assertEqual(self.linear_2.express_as('Point-Slope').equation, 'y+10=-2.5(x-2)')
        self.assertEqual(self.linear_3.express_as('Point-Slope').equation, 'y+25=-5(x-2)')
        self.assertEqual(self.linear_4.express_as('Point-Slope').equation, 'y-7=1(x-2)')

    def test_solving_for_x(self):
        self.assertEqual(self.linear_1.solve_for('x', 3), -9)
        self.assertEqual(self.linear_2.solve_for('x', 9), -27.5)
        self.assertEqual(self.linear_3.solve_for('x', -4), 5)
        self.assertEqual(self.linear_4.solve_for('x', -0.5), 4.5)

    def test_solving_for_y(self):
        self.assertEqual(self.linear_1.solve_for('y', 3), -3)
        self.assertEqual(self.linear_2.solve_for('y', 9), -5.6)
        self.assertEqual(self.linear_3.solve_for('y', -4), -2.2)
        self.assertEqual(self.linear_4.solve_for('y', 5.5), 0.5)

    def test_solving_for_x_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as('Slope-Intercept').solve_for('x', 3), -9)
        self.assertEqual(self.linear_2.express_as('Slope-Intercept').solve_for('x', 9), -27.5)
        self.assertEqual(self.linear_3.express_as('Slope-Intercept').solve_for('x', -4), 5)
        self.assertEqual(self.linear_4.express_as('Slope-Intercept').solve_for('x', -0.5), 4.5)

    def test_solving_for_y_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as('Point-Slope').solve_for('y', 3), -3)
        self.assertEqual(self.linear_2.express_as('Point-Slope').solve_for('y', 9), -5.6)
        self.assertEqual(self.linear_3.express_as('Point-Slope').solve_for('y', -4), -2.2)
        self.assertEqual(self.linear_4.express_as('Point-Slope').solve_for('y', 5.5), 0.5)


if __name__ == '__main__':
    unittest.main()