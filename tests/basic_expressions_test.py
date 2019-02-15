import unittest
import sys
import os
sys.path.append(os.path.abspath('../khwarizmi'))
from expression import Expression

class BasicExpressionsTest(unittest.TestCase):

	def setUp(self):

		self.a_expression = Expression("2x + 4y - 22 = -10x")
		self.b_expression = Expression("1/2x - 3/4y * 5 - 2 = 0")
		self.c_expression = Expression("2x**2 - 4z = x/z")
		self.d_expression = Expression("-x + y = -z")

	def test_variables(self):
		self.assertEqual(self.a_expression.variables, ['x', 'y'])
		self.assertEqual(self.b_expression.variables, ['x', 'y'])
		self.assertEqual(self.c_expression.variables, ['x', 'z'])
		self.assertEqual(self.d_expression.variables, ['x', 'y', 'z'])

	def test_terms(self):
		self.assertEqual(self.a_expression.terms, ['2x', '4y', '-22', '-10x'])
		self.assertEqual(self.b_expression.terms, ['1/2x', '-3/4y*5', '-2', '0'])
		self.assertEqual(self.c_expression.terms, ['2x**2', '-4z', 'x/z'])
		self.assertEqual(self.d_expression.terms, ['-x', 'y', '-z'])

	def test_coefficients(self):
		self.assertEqual(self.a_expression.coefficients, ['2', '4', '-10'])
		self.assertEqual(self.b_expression.coefficients, ['1/2', '-3/4'])
		self.assertEqual(self.c_expression.coefficients, ['2', '-4', '1'])
		self.assertEqual(self.d_expression.coefficients, ['-1', '1', '-1'])


if __name__ == '__main__':
	unittest.main()
