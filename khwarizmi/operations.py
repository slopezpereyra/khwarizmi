"""Base class for algebraic operations."""

from khwarizmi.misc import is_number, if_assign
from khwarizmi.exc import NonAlgebraicOperationError, InvalidOperationError
from khwarizmi.expression import  Expression


class Term:
	"""Defines operations between to algebraic terms."""

	@staticmethod
	def ispowered(a):

		return True if '**' in a else False

	@staticmethod
	def getpower(a):
		"""Returns exponent of term a."""

		if Term.ispowered(a):
			return a[a.find('**') + 2:]
		return 1

	@staticmethod
	def isnegative(a):
		"""True if a is negative, false otherwise."""

		if a.count('-') != 0 and a.count('-') % 2 != 0:
			return True
		return False

	@staticmethod
	def add(a, b):
		"""Returns the expression resultant of adding terms a and b."""

		a = Expression(a)
		b = Expression(b)

		if is_number(a.expression) or is_number(b.expression):
			raise NonAlgebraicOperationError

		if len(a.terms) > 1 or len(b.terms) > 1:
			raise InvalidOperationError(a, b)

		if Term.getpower(a.expression) is not Term.getpower(b.expression) or a.variables != b.variables:
			operator = if_assign(b.expression.startswith('-'), '', '+')
			return a.expression + operator + b.expression

		a_coefficient = a.get_number(0)
		b_coefficient = b.get_number(0)

		result = str(int(a_coefficient) + int(b_coefficient))
		result = if_assign(result == '1', "", result)
		result = if_assign(result == '-1', "-", result)

		return result + "".join(a.variables) + '**' + Term.getpower(a.expression)

	@staticmethod
	def substract(a, b):
		"""Returns the expression resultant of substracting terms a and b."""

		a = Expression(a)
		b = Expression(b)

		if is_number(a.expression) or is_number(b.expression):
			raise NonAlgebraicOperationError

		if len(a.terms) > 1 or len(b.terms) > 1:
			raise InvalidOperationError(a, b)

		if Term.getpower(a.expression) is not Term.getpower(b.expression) or a.variables != b.variables:
			result = a.expression + '-' + b.expression
			return result

		a_coefficient = a.get_number(0)
		b_coefficient = b.get_number(0)

		result = str(int(a_coefficient) - int(b_coefficient))
		result = if_assign(result == '1', "", result)
		result = if_assign(result == '-1', "-", result)

		return result + "".join(a.variables) + '**' + Term.getpower(a.expression)

	@staticmethod
	def multiply(a, b):

		a = Expression(a)
		b = Expression(b)

		variables = set(a.variables + b.variables)
		power = str(int(Term.getpower(a.expression)) + int(Term.getpower(b.expression)))
		power = if_assign(power == '1', '', power)

		if power == '0':
			return "".join(variables)

		a_coefficient = a.get_number(0)
		b_coefficient = b.get_number(0)

		result = str(int(a_coefficient) * int(b_coefficient)) + "".join(variables) + '**' + power
		return result


# print(Term.add("4xz**3", "-5x**3"))
# print(Term.substract('4x**3', '-5x**4'))

print(Term.multiply("4xz**4", "3x**2"))