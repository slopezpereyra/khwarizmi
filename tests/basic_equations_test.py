from khwarizmi import equations
from khwarizmi.exc import NoEqualityError
import unittest

# 0.22 seconds to run.

class BasicEquationsTest(unittest.TestCase):

    def setUp(self):
        self.equation_1 = equations.Equation('-3x = -6 * 5')
        self.equation_2 = equations.Equation('8x - 2x = 9 + 3x + 5')
        self.equation_3 = equations.Equation('2x + 2x = 5x + 5')
        self.equation_4 = equations.Equation('4x = 24 / 2')

    def test_sorting_equation(self):
        self.assertEqual(self.equation_1.sort_equation(), '(-6*5)/-3')
        self.assertEqual(self.equation_2.sort_equation(), '(9+5)/3')
        self.assertEqual(self.equation_3.sort_equation(), '(+5)/-1')
        self.assertEqual(self.equation_4.sort_equation(), '(24/2)/4')

    def test_solution(self):
        self.assertEqual(self.equation_1.solve(), 10)
        self.assertEqual(self.equation_2.solve(), 4.666666666666667)
        self.assertEqual(self.equation_3.solve(), -5)
        self.assertEqual(self.equation_4.solve(), 3)

    def test_inc_multipplier(self):
        self.assertEqual(self.equation_1.inc_multiplier, "-3")
        self.assertEqual(self.equation_2.inc_multiplier, "8")
        self.assertEqual(self.equation_3.inc_multiplier, "2")
        self.assertEqual(self.equation_4.inc_multiplier, "4")



if __name__ == '__main__':
    unittest.main()