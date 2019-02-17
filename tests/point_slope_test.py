import sys
import os
sys.path.append(os.path.abspath('../khwarizmi'))
import linear, exc
import unittest

# 0.22 seconds to run.

class PointSlopeTest(unittest.TestCase):

    def setUp(self):
        self.linear_1 = linear.PointSlope('y - 4 = 2(x - 2)')
        self.linear_2 = linear.PointSlope('y + 2 = -3(x - 6)')
        self.linear_3 = linear.PointSlope('y - 1/2 = 10(x + 2)')
        self.linear_4 = linear.PointSlope('y - 10 = 1/2(x + 1/4)')

    def test_error_raising_on_unsuitable_equation(self):
        with self.assertRaises(exc.UnableToDefineFormError):
            linear.PointSlope('2y - 2 = 2(x - 5)')
            linear.PointSlope('-2y - 2 = 2(x - 5)')

    def test_equation(self):
        self.assertEqual(self.linear_1.equation, 'y-4=2(x-2)')
        self.assertEqual(self.linear_2.equation, 'y+2=-3(x-6)')
        self.assertEqual(self.linear_3.equation, 'y-1/2=10(x+2)')
        self.assertEqual(self.linear_4.equation, 'y-10=1/2(x+1/4)')

    def test_form(self):
        self.assertEqual(self.linear_1.form, linear.LinearForms.PointSlope)
        self.assertEqual(self.linear_2.form, linear.LinearForms.PointSlope)
        self.assertEqual(self.linear_3.form, linear.LinearForms.PointSlope)
        self.assertEqual(self.linear_4.form, linear.LinearForms.PointSlope)

    def test_x_mult(self):
        self.assertEqual(self.linear_1.x_coefficient, '2')
        self.assertEqual(self.linear_2.x_coefficient, '-3')
        self.assertEqual(self.linear_3.x_coefficient, '10')
        self.assertEqual(self.linear_4.x_coefficient, '1/2')

    def test_y_mult(self):
        self.assertEqual(self.linear_1.y_coefficient, '1')
        self.assertEqual(self.linear_2.y_coefficient, '1')
        self.assertEqual(self.linear_3.y_coefficient, '1')
        self.assertEqual(self.linear_4.y_coefficient, '1')

    def test_slope(self):
        self.assertEqual(self.linear_1.slope, 2)
        self.assertEqual(self.linear_2.slope, -3)
        self.assertEqual(self.linear_3.slope, 10)
        self.assertEqual(self.linear_4.slope, 0.5)

    def test_y_intercept(self):
        self.assertEqual(self.linear_1.y_intercept, -0)
        self.assertEqual(self.linear_2.y_intercept, 16)
        self.assertEqual(self.linear_3.y_intercept, 20.5)
        self.assertEqual(self.linear_4.y_intercept, 10.125)

    def test_points(self):
        self.assertEqual(self.linear_1.points(-1, 0), [(-1, -2), (0, 0)])
        self.assertEqual(self.linear_2.points(-5, -3), [(-5, 31), (-4, 28), (-3, 25)])
        self.assertEqual(self.linear_3.points(1, 2), [(1, 30.5), (2, 40.5)])
        self.assertEqual(self.linear_4.points(1, 2), [(1, 10.625), (2, 11.125)])

    def test_get_point(self):
        self.assertEqual(self.linear_1.get_point(5), (5, 10))
        self.assertEqual(self.linear_2.get_point(-5), (-5, 31))
        self.assertEqual(self.linear_3.get_point(1.25), (1.25, 33))
        self.assertEqual(self.linear_4.get_point(5), (5, 12.625))

    def test_solve(self):
        with self.assertRaises(exc.LinearSolutionError):
            self.linear_1.solve()
            self.linear_2.solve()
            self.linear_3.solve()
            self.linear_4.solve()

    def test_sort_for_x(self):
        self.assertEqual(self.linear_1.sort('x'), '2*(x-2)+4')
        self.assertEqual(self.linear_2.sort('x'), '-3*(x-6)-2')
        self.assertEqual(self.linear_3.sort('x'), '10*(x+2)+1/2')
        self.assertEqual(self.linear_4.sort('x'), '1/2*(x+1/4)+10')

    def test_sort_for_y(self):
        self.assertEqual(self.linear_1.sort('y'), '(y-4-2*-2)/2')
        self.assertEqual(self.linear_2.sort('y'), '(y+2+3*-6)/-3')
        self.assertEqual(self.linear_3.sort('y'), '(y-1/2-10*2)/10')
        self.assertEqual(self.linear_4.sort('y'), '(y-10-0.5*1/4)/0.5')

    def test_expressing_as_standard(self):
        self.assertEqual(self.linear_1.express_as(linear.LinearForms.Standard).equation, '-2x+y=0')
        self.assertEqual(self.linear_2.express_as(linear.LinearForms.Standard).equation, '3x+y=16')
        self.assertEqual(self.linear_3.express_as(linear.LinearForms.Standard).equation, '-10x+y=20.5')
        self.assertEqual(self.linear_4.express_as(linear.LinearForms.Standard).equation, '-1/2x+y=10.125')

    def test_expressing_as_slope_intercept(self):
        self.assertEqual(self.linear_1.express_as(linear.LinearForms.SlopeIntercept).equation, 'y=2x+0')
        self.assertEqual(self.linear_2.express_as(linear.LinearForms.SlopeIntercept).equation, 'y=-3x+16')
        self.assertEqual(self.linear_3.express_as(linear.LinearForms.SlopeIntercept).equation, 'y=10x+20.5')
        self.assertEqual(self.linear_4.express_as(linear.LinearForms.SlopeIntercept).equation, 'y=0.5x+10.125')

    def test_solving_for_x(self):
        self.assertEqual(self.linear_1.solve_for('x', 3), 6)
        self.assertEqual(self.linear_2.solve_for('x', 9), -11)
        self.assertEqual(self.linear_3.solve_for('x', -4), -19.5)
        self.assertEqual(self.linear_4.solve_for('x', 0.5), 10.375)

    def test_solving_for_y(self):
        self.assertEqual(self.linear_1.solve_for('y', 3), 1.5)
        self.assertEqual(self.linear_2.solve_for('y', 9), 2.3333333333333335)
        self.assertEqual(self.linear_3.solve_for('y', -4), -2.45)
        self.assertEqual(self.linear_4.solve_for('y', 0.5), -19.25)

    def test_solving_for_x_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as(linear.LinearForms.Standard).solve_for('x', 3), 6)
        self.assertEqual(self.linear_2.express_as(linear.LinearForms.Standard).solve_for('x', 9), -11)
        self.assertEqual(self.linear_3.express_as(linear.LinearForms.Standard).solve_for('x', -4), -19.5)
        self.assertEqual(self.linear_4.express_as(linear.LinearForms.Standard).solve_for('x', 0.5), 10.375)

    def test_solving_for_y_on_reexpression(self):
        self.assertEqual(self.linear_1.express_as(linear.LinearForms.SlopeIntercept).solve_for('y', 3), 1.5)
        self.assertEqual(self.linear_2.express_as(linear.LinearForms.SlopeIntercept).solve_for('y', 9), 2.3333333333333335)
        self.assertEqual(self.linear_3.express_as(linear.LinearForms.SlopeIntercept).solve_for('y', -4), -2.45)
        self.assertEqual(self.linear_4.express_as(linear.LinearForms.SlopeIntercept).solve_for('y', 0.5), -19.25)


if __name__ == '__main__':
    unittest.main()
