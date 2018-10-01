from khwarizmi import linear, exc
import unittest

# 0.21 seconds to run

class SlopeInterceptTest(unittest.TestCase):

    def setUp(self):
        self.linear_1 = linear.SlopeIntercept('y = 2x + 5')
        self.linear_2 = linear.SlopeIntercept('-y = -12x - 2')
        self.linear_3 = linear.SlopeIntercept('y = 1/2x + 1/4')
        self.linear_4 = linear.SlopeIntercept('y = -3x - 1/2')

    def test_equation(self):
        self.assertEqual(self.linear_1.equation, 'y=2x+5')
        self.assertEqual(self.linear_2.equation, '-y=-12x-2')
        self.assertEqual(self.linear_3.equation, 'y=1/2x+1/4')

    def test_unsuitable_equations(self):
        with self.assertRaises(exc.UnsuitableSlopeInterceptForm):
            linear.Linear('2y = 2x + 5')
            linear.Linear('y = 2 (x + 5)')

    def test_form(self):
        self.assertEqual(self.linear_1.form, 'Slope-Intercept Form')
        self.assertEqual(self.linear_2.form, 'Slope-Intercept Form')
        self.assertEqual(self.linear_3.form, 'Slope-Intercept Form')
        self.assertEqual(self.linear_4.form, 'Slope-Intercept Form')

    def test_x_mult(self):
        self.assertEqual(self.linear_1.x_mult, '2')
        self.assertEqual(self.linear_2.x_mult, '-12')
        self.assertEqual(self.linear_3.x_mult, '1/2')
        self.assertEqual(self.linear_4.x_mult, '-3')

    def test_y_mult(self):
        self.assertEqual(self.linear_1.y_mult, '1')
        self.assertEqual(self.linear_2.y_mult, '-1')
        self.assertEqual(self.linear_3.y_mult, '1')
        self.assertEqual(self.linear_4.y_mult, '1')

    def test_slope(self):
        self.assertEqual(self.linear_1.slope, 2)
        self.assertEqual(self.linear_2.slope, 12)
        self.assertEqual(self.linear_3.slope, 0.5)
        self.assertEqual(self.linear_4.slope, -3)

    def test_y_intercept(self):
        self.assertEqual(self.linear_1.y_intercept, 5)
        self.assertEqual(self.linear_2.y_intercept, 2)
        self.assertEqual(self.linear_3.y_intercept, 0.25)
        self.assertEqual(self.linear_4.y_intercept, -0.5)

    def test_points(self):
        self.assertEqual(self.linear_1.points(-1, 0), [(-1, 3), (0, 5)])
        self.assertEqual(self.linear_2.points(1, 2), [(1, 14), (2, 26)])
        self.assertEqual(self.linear_3.points(1, 2), [(1, 0.75), (2, 1.25)])
        self.assertEqual(self.linear_4.points(2, 3), [(2, -6.5), (3, -9.5)])

    def test_get_point(self):
        self.assertEqual(self.linear_1.get_point(5), (5, 15))
        self.assertEqual(self.linear_2.get_point(1.25), (1.25, 17))
        self.assertEqual(self.linear_3.get_point(5), (5, 2.75))
        self.assertEqual(self.linear_4.get_point(-10), (-10, 29.5))

    def test_solve(self):
        with self.assertRaises(exc.LinearSolutionError):
            self.linear_1.solve()
            self.linear_2.solve()
            self.linear_3.solve()
            self.linear_4.solve()

    def test_sort_for_x(self):
        self.assertEqual(self.linear_1.sort('x'), '(2*x+5)/1')
        self.assertEqual(self.linear_2.sort('x'), '(-12*x-2)/-1')
        self.assertEqual(self.linear_3.sort('x'), '(1/2*x+1/4)/1')
        self.assertEqual(self.linear_4.sort('x'), '(-3*x-1/2)/1')

    def test_sort_for_y(self):
        self.assertEqual(self.linear_1.sort('y'), '(1*y-5)/2')
        self.assertEqual(self.linear_2.sort('y'), '(-1*y+2)/-12')
        self.assertEqual(self.linear_3.sort('y'), '(1*y-0.25)/0.5')
        self.assertEqual(self.linear_4.sort('y'), '(1*y+0.5)/-3')

    def test_expressing_as_standard(self):
        self.assertEqual(self.linear_1.express_as('Standard').equation, '-2x+y=5')
        self.assertEqual(self.linear_2.express_as('Standard').equation, '-12x+y=2')
        self.assertEqual(self.linear_3.express_as('Standard').equation, '-0.5x+y=0.25')
        self.assertEqual(self.linear_4.express_as('Standard').equation, '3x+y=-0.5')

    def test_expressing_as_point_slope(self):
        self.assertEqual(self.linear_1.express_as('Point-Slope').equation, 'y-9=2(x-2)')
        self.assertEqual(self.linear_2.express_as('Point-Slope').equation, 'y-26=12(x-2)')
        self.assertEqual(self.linear_3.express_as('Point-Slope').equation, 'y-1.25=0.5(x-2)')
        self.assertEqual(self.linear_4.express_as('Point-Slope').equation, 'y+6.5=-3(x-2)')

    def test_solving_for_x(self):
        self.assertEqual(self.linear_1.solve_for('x', 3), 11)
        self.assertEqual(self.linear_2.solve_for('x', 9), 110)
        self.assertEqual(self.linear_3.solve_for('x', -4), -1.75)
        self.assertEqual(self.linear_4.solve_for('x', -0.5), 1)

    def test_solving_for_y(self):
        self.assertEqual(self.linear_1.solve_for('y', 3), -1)
        self.assertEqual(self.linear_2.solve_for('y', 9), 0.5833333333333334)
        self.assertEqual(self.linear_3.solve_for('y', -4), -8.5)
        self.assertEqual(self.linear_4.solve_for('y', 5.5), -2)

    def test_solving_for_x_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as('Standard').solve_for('x', 3), 11)
        self.assertEqual(self.linear_2.express_as('Standard').solve_for('x', 9), 110)
        self.assertEqual(self.linear_3.express_as('Standard').solve_for('x', -4), -1.75)
        self.assertEqual(self.linear_4.express_as('Standard').solve_for('x', -0.5), 1)

    def test_solving_for_y_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as('Point-Slope').solve_for('y', 3), -1)
        self.assertEqual(self.linear_2.express_as('Point-Slope').solve_for('y', 9), 0.5833333333333334)
        self.assertEqual(self.linear_3.express_as('Point-Slope').solve_for('y', -4), -8.5)
        self.assertEqual(self.linear_4.express_as('Point-Slope').solve_for('y', 5.5), -2)

if __name__ == '__main__':
    unittest.main()