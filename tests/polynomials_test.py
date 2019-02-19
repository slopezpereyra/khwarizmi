import unittest
import sys
import os
sys.path.append(os.path.abspath('../khwarizmi'))
from polynomials import Polynomial

class PolynomialsTest(unittest.TestCase):

    def setUp(self):
        self.a_polynomial = Polynomial("2x**4 + 4x**3 - 5x**2 - 9")
        self.b_polynomial = Polynomial("2a**2 + 4a**4 - 2")
        self.c_polynomial = Polynomial("1/2z**4 - 1/2")

    def test_polynomial_expression(self):
        self.assertEqual(self.a_polynomial.polynomial, '2x**4+4x**3-5x**2-9')
        self.assertEqual(self.b_polynomial.polynomial, '4a**4+2a**2-2')
        self.assertEqual(self.c_polynomial.polynomial, '1/2z**4-1/2')

    def test_indeterminates(self):
        self.assertEqual(self.a_polynomial.indeterminates, ['x'])
        self.assertEqual(self.b_polynomial.indeterminates, ['a'])
        self.assertEqual(self.c_polynomial.indeterminates, ['z'])

    def test_degrees(self):
        self.assertEqual(self.a_polynomial.degrees, [4, 3, 2, 0])
        self.assertEqual(self.b_polynomial.degrees, [4, 2, 0])
        self.assertEqual(self.c_polynomial.degrees, [4, 0])

    def test_degree(self):
        self.assertEqual(self.a_polynomial.degree, 4)
        self.assertEqual(self.b_polynomial.degree, 4)
        self.assertEqual(self.c_polynomial.degree, 4)

    def test_non_coefficient_term(self):
        self.assertEqual(self.a_polynomial.non_coefficient_term, '-9')

if __name__ == '__main__':
    unittest.main()
