"""Defines an equation class and its functions."""

import copy

from expression import Expression
from exc import NoEqualityError, NoVariableError
from misc import num, if_assign, isanumber

OPERATORS = ["-", "+", "/", "*", '=']
excused_symbols = ["/", "."]


class Equation(Expression):
	"""Base class for all expressions of the form a = b."""

	def __init__(self, equation):

		Expression.__init__(self, equation)
		self.equation = self.expression
		self.equal_index = self.equation.find("=")
		self.sol_side = ""
		self.inc_side = ""
		self.get_sides()
		self.unknown_index = self.equation.index(self.unknown)
		self.coefficient_length = 0
		self.coefficient = self.get_coefficient()

	def __str__(self):
		"""String representation of the equation."""

		return self.equation

	def get_unknown(self):
		"""Returns the unknown of the equation; this is, any
		character of the equation string that is not a number and rather
		a letter. E.g. the letter x or y."""

		for character in self.expression:
			if character.isalpha() is True:
				return character

		raise NoVariableError(self.expression)

	def get_sides(self):
		"""Assigns to the inc_side and the sol_side attributes sliced
		parts of the equation; the part the unknown is in, and the part the result
		is in. The equation is sliced to the left and to the right of the equal sign.
		"""

		try:
			equal_sign = self.equation.index("=")
			self.inc_side = self.equation[0:equal_sign]
			self.sol_side = self.equation[equal_sign + 1:]

		except ValueError:
			raise NoEqualityError(self.equation)

	def simplify_equation(self):
		"""Simplifies the equation by evaluating all coefficients of the equation to one single
		coefficient."""

		sol_side, counter, left_hand_terms = self.sol_side, 0, self.get_terms(self.inc_side)

		unknowns = self.get_coefficients()
		# For each number in unknowns, check if its found on the solution side;
		# if it is, pass it to the equation side with opposite sign.
		for number in unknowns:
			index = sol_side.find(number + self.unknown)

			if index == -1:
				counter += 1
				continue

			replacement = if_assign(sol_side[index - 1] in OPERATORS, sol_side[index - 1] + number, number)
			sol_side = sol_side.replace(replacement + self.unknown, '')
			# If this number is on the solution side
			if number + self.unknown in self.sol_side:
				unknowns[counter] = if_assign(unknowns[counter].startswith('-'), number.replace('-', ''), '-' + number)

			counter += 1

		for term in left_hand_terms:
			if self.unknown not in term:
				sol_side += '-' + term

		try:
			unknowns = list(map(num, unknowns))
			unknown = str(sum(unknowns))
		except ValueError:
			unknown = ''

		simplified = self.beautify(unknown + self.unknown + '=' + sol_side)
		return simplified

	def get_coefficient(self):
		"""Returns this equation's coefficient."""

		equation = self.simplify_equation()
		return self.get_number(0, equation)

	def sort(self, show=False):
		"""Sorts the equation, which is a very highschool, wrongly phrased
		way of saying that clears the unknown side by substracting all
		positive numbers, adding all negative numbers, dividing all multipliers
		and multiplying all divisors, doing the same operations on the solution
		side. """

		index = 0

		# Local variables for the local, simplified version of the equation
		# (not equal to self.equation).

		equation = self.simplify_equation()
		equal_sign = equation.index("=")
		inc_side, sol_side = equation[0:equal_sign], equation[equal_sign + 1:]
		symbol = self.coefficient

		if not isanumber(symbol):
			symbol = if_assign(equation[0] == '-', '-1', '1')

		inc_side = inc_side.replace(symbol, "", 1)
		sol_side = '(' + sol_side + ')/' + symbol

		if show is True:

			string = """Equation \n{}\n\nSimplified\n{}\n\nSorted\n{}\n\nSolved \n{}""".format(
				self.equation, equation, inc_side + '=' + sol_side,
				self.unknown + '=' + str(num(eval(sol_side))) + '\n')

			print(string)

		return sol_side

	def solve(self, show=False):
		"""Evaluates the algebraic expression.
		If show is True, displays a step by step explanation."""

		return num(eval(self.sort(show=show)))


