"""Defines an equation class and its functions."""

import copy

from expression import Expression
from exc import NoEqualityError, NoVariableError
from misc import num, if_assign, isanumber, frac_to_num
from polynomials import Polynomial

OPERATORS = ["-", "+", "/", "*", '=']
excused_symbols = ["/", "."]


class Equation(Expression):
	"""Base class for all expressions of the form a = b of one variable"""

	def __init__(self, equation):

		Expression.__init__(self, equation)
		self.equation = self.expression
		self.var = self.variables[0]
		self.equal_index = self.equation.find("=")
		self.lhs = ""
		self.rhs = ""
		self.get_sides()

	def __str__(self):
		"""String representation of the equation."""

		return self.equation

	def get_sides(self):
		"""Assigns to the inc_side and the sol_side attributes their correspondent
		parts of the equation; the part the variable is in, and the part the result
		is in. The equation is sliced to the left and to the right of the equal sign.
		"""

		try:
			equal_sign = self.equation.index("=")
			self.lhs = self.equation[0:equal_sign]
			self.rhs = self.equation[equal_sign + 1:]

		except ValueError:
			raise NoEqualityError(self.equation)

	def solve(self, debug=False):
		"""Returns the solution of the equation as integer or float, depending on what
		the solution is."""

		rhs_no_var_terms = [num(term) for term in Expression(self.rhs, no_vars_intended=True).get_terms() if isanumber(term)]
		lhs_no_var_terms = [num(term) for term in Expression(self.lhs, no_vars_intended=True).get_terms() if isanumber(term)]

		rhs_var_terms = [term for term in Expression(self.rhs, no_vars_intended=True).get_terms() if any(var in term for var in self.variables)]
		lhs_var_terms = [term for term in Expression(self.lhs, no_vars_intended=True).get_terms() if any(var in term for var in self.variables)]

		polynomial = '+'.join(lhs_var_terms) + '-' + '+'.join(rhs_var_terms)
		polynomial = if_assign(polynomial.endswith('-'), polynomial[:-1], polynomial)

		lhs = Polynomial(polynomial)
		coefficient = self.get_number(0, lhs.polynomial)
		result = sum(rhs_no_var_terms) - sum(lhs_no_var_terms)

		if debug:
			print(lhs, '=', result, '-->', str(result) + '/(' + coefficient + ')')

		if coefficient is '0':
			if result == 0:
				return "All real numbers are solutions."
			return "No solutions."

		return num(str((eval(str(result) + '/(' + coefficient + ')'))))


EQ = Equation("-3x = -6 * 5")
print(EQ.solve(True))
