"""Basic expressions"""

from khwarizmi.misc import if_assign
import copy

excused_symbols = ["/", "."]


class Expression:

	def __init__(self, expression):
		self.expression = expression.replace(' ', '')
		self.variables = self.get_variables()
		self.unknown = self.variables[0]
		self.coefficients = self.get_coefficients()
		self.terms = self.get_terms()

	def get_variables(self):
		"""Adds every unknown of the equation
		to the unknowns attribute (list)."""

		index, incs = 0, []
		for symbol in self.expression:

			if symbol.isalpha() and symbol not in incs:
				incs.append(symbol)

		return incs

	def get_number(self, number, index, side=None, catch_negatives=False, catch_variable=False):
		"""Returns the set of symbols that form a full number.

		Keyword Arguments:

		number -- first number to which append following numbers
		index -- index of the number being initially parsed, which is number
		side -- side of the equation to parse (by default it parses the whole
		equation)"""

		side = side if side is not None else self.expression
		catcher = copy.copy(excused_symbols)
		parser = 1

		if catch_negatives is True:
			catcher.append('-')
		if catch_variable is True:
			catcher.append(self.unknown)

		if len(side) > index + parser:
			if side[index + 1] == "=" and side[index].isdigit():
				return number

			while side[index + parser].isdigit() or side[index + parser] in catcher:
				number += side[index + parser]

				if index + parser + 1 < len(side):
					parser += 1
				else:
					return number

			return number

		if number.isdigit():
			return number
		return None

	def get_terms(self, side=None):
		"""Returns a list of all terms of this equation."""

		side = self.expression if side is None else side
		index, terms = 0, []

		while index < len(side):

			term = self.get_number(side[index], index, catch_variable=True)
			terms.append(term)

			try:
				index += len(term)
				index = if_assign(side[index] == '-', index, index + 1)
			except (TypeError, IndexError):
				index += 1

		return terms

	def get_coefficient(self, unknown_index=None, side=None):
		"""Returns the unknown's coefficient; i.e.  the number that multiplies the
		unknown (if any)."""

		number, parser = "", 1
		catcher = copy.copy(excused_symbols)
		catcher.append('-')

		index = self.unknown_index if unknown_index is None else unknown_index
		side = self.inc_side if side is None else side

		# While there is a previous character and this character is a digit
		try:
			while parser <= index and (side[index - parser].isdigit() or side[index - parser] in catcher):
				number = side[index - parser] + number
				if side[index - parser] == '-':
					break
				parser += 1

			self.coefficient_length = len(number)
			return number

		except IndexError:
			return number

	def get_coefficients(self, first_index=0):

		previous_index = first_index
		unknowns = []

		for variable in self.variables:
			for number in range(1, self.expression.count(variable) + 1):
				cur_index = self.expression.find(variable, previous_index + 1)
				unknowns.append(self.get_coefficient(cur_index, self.expression))
				previous_index = cur_index
			previous_index = 0

		return unknowns

	@staticmethod
	def beautify(expression):
		"""Beautifies a mathematical expression, turning '--' into '+',
		'+*' into '*', etc."""

		if '--' in expression:
			expression = expression.replace('--', '+')

		if '*+' in expression:
			expression = expression.replace('*+', '*')

		if expression[0] == '+':
			expression = expression.replace('+', '', 1)

		if '+-' in expression:
			expression = expression.replace('+-', '-')

		if '=+' in expression:
			expression = expression.replace('=+', '=')

		expression = expression.replace('/+', '/')

		return expression


EXPR = Expression("2x - 5z + 9q + 7 + 4")
print(EXPR.expression)
print(EXPR.variables)
print(EXPR.coefficients)