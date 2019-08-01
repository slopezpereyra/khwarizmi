import unittest
import sys
import os
sys.path.append(os.path.abspath('../khwarizmi'))
from polynomials import Polynomial, PolynomialOperation

# 0.001 sec

class PolynomialsTest(unittest.TestCase):

    def setUp(self):
        self.a_polynomial = Polynomial("2x**4 + 4x**3 - 5x**2 - 9")
        self.b_polynomial = Polynomial("2a**2 + 4a**4 - 2")
        self.c_polynomial = Polynomial("1/2z**4 - 1/2")
        self.d_polynomial = Polynomial("4x**5 + x**4 - 2x**3 + 3")

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
        self.assertEqual(self.b_polynomial.non_coefficient_term, '-2')
        self.assertEqual(self.c_polynomial.non_coefficient_term, '-1/2')

    def test_terms_by_degree(self):
        dic_a = {4: '2x**4', 3: '4x**3', 2: '-5x**2', 0: '-9'}
        dic_b = {4: '4a**4', 2: '2a**2', 0: '-2'}
        dic_c = {4: '1/2z**4', 0: '-1/2'}

        self.assertDictEqual(self.a_polynomial.terms_by_degree, dic_a)
        self.assertDictEqual(self.b_polynomial.terms_by_degree, dic_b)
        self.assertDictEqual(self.c_polynomial.terms_by_degree, dic_c)

    def test_primary_coefficient(self):
        self.assertEqual(self.a_polynomial.primary_coefficient, '2')
        self.assertEqual(self.b_polynomial.primary_coefficient, '4')
        self.assertEqual(self.c_polynomial.primary_coefficient, '1/2')

    def test_polynomial_addition(self):
        p, q = self.a_polynomial, self.d_polynomial
        self.assertEqual(PolynomialOperation.addition(p, q).__str__(), "4x**5+3x**4+2x**3-5x**2-6")

    def test_polynomial_multiplication(self):
        p, q = self.a_polynomial, self.b_polynomial
        self.assertEqual(PolynomialOperation.product(p, q).__str__(), "8x**9+18x**8-20x**7-13x**6-26x**5-3x**4+30x**3-15x**2-27")



if __name__ == '__main__':
    unittest.main()
