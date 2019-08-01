import unittest
import sys
import os
import equations
from exc import NoEqualityError, NoVariableError, NoVariableError

# 0.002 seconds to run.


class BasicEquationsTest(unittest.TestCase):

    def setUp(self):
        self.equation_1 = equations.Equation('-3x = -6 * 5')
        self.equation_2 = equations.Equation('8x - 2x = 9 + 3x + 5')
        self.equation_3 = equations.Equation('2x + 2x = 5x + 5')
        self.equation_4 = equations.Equation('4x = 24 / 2')
        self.equation_5 = equations.Equation('22y - 20y + 5 = -12 + 6 + 4y')

    def test_solution(self):
        self.assertEqual(self.equation_1.solve(), 10)
        self.assertEqual(self.equation_2.solve(), 4.666666666666667)
        self.assertEqual(self.equation_3.solve(), -5)
        self.assertEqual(self.equation_4.solve(), 3)
        self.assertEqual(self.equation_5.solve(), 5.5)

    def test_errors(self):
        with self.assertRaises(NoEqualityError):
            self.equation_a = equations.Equation('2y + 9 -2')
        with self.assertRaises(NoVariableError):
            self.equation_b = equations.Equation('2 + 5 = -2')


if __name__ == '__main__':
    unittest.main()
