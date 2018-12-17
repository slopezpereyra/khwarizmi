"""Polynomial expressions and its operations."""

from khwarizmi.expression import Expression
from khwarizmi.operations import TermOperations
from khwarizmi.exc import InvalidOperationError
from khwarizmi.misc import if_assign, is_number


class Polynomial(Expression):

	"""Base class for all polynomial expressions."""

	def __init__(self, polynomial, name=None):
		Expression.__init__(self, polynomial)
		self.polynomial = polynomial
		self.name = name
		self.indeterminates = self.variables
		self.degree = None
		self.degrees = self.get_degrees()
		self.non_coefficient_term = self.get_non_coefficient_term()
		self.terms_by_degree = self.get_terms_by_degree()
		self.primary_coefficient = self.get_primary_coefficient()
		self.polynomial = self.reorder_terms()

	def __str__(self):
		if self.name is not None and self.name is not '':
			return self.name + " = " + self.polynomial
		return self.polynomial

	def get_degrees(self):

		"""Returns all degrees of all terms of this polynomial."""

		powers = []

		for term in self.terms:
			powers.append(int(TermOperations.getpower(term)))

		powers = sorted(powers, reverse=True)
		self.degree = str(powers[0])
		return list(map(str, powers))

	def get_primary_coefficient(self):
		"""Returns the primary coefficient of this polynomial."""

		term = self.terms_by_degree[self.degree]
		return self.get_number(0, term)

	def get_non_coefficient_term(self):

		return next((term for term in self.terms if is_number(term)), "0")

	def reorder_terms(self):

		"""Reorders the terms of the polynomial; higher degrees first."""

		ordered_terms = []

		for degree in self.degrees:
			ordered_terms.append(self.terms_by_degree[degree] + '**' + degree)

		expression = "+".join(ordered_terms)
		return Expression.beautify(expression)

	def get_terms_by_degree(self):

		"""Returns a dictionary where each term is paired to a degree key."""

		terms_by_degree = {}

		for degree in self.degrees:
			term = next(term for term in self.terms if '**' + degree in term)
			terms_by_degree[degree] = term[0:term.find('**')]

		if any('**' not in term for term in self.terms):
			terms_by_degree["1"] = next((term for term in self.terms if '**' not in term), None)

		return terms_by_degree


class PolynomialOperation:

	"""Class holding static methods involving polynomial operations."""

	@staticmethod
	def addition(p, q):
		"""Performs addition of polynomials p and q."""

		if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
			raise InvalidOperationError(p, q)

		result = ""
		longer_polynomial = if_assign(len(p.degrees) >= len(q.degrees), p, q)

		for degree in longer_polynomial.terms_by_degree:
			try:
				p_term, q_term = p.terms_by_degree[degree] + '**' + degree, q.terms_by_degree[degree] + '**' + degree
				result += TermOperations.add(p_term, q_term) + '+'

			except KeyError:
				result_term = p.terms_by_degree[degree] + '**' + degree
				if not result_term.startswith('-'):
					result_term = '+' + result_term
				result += result_term + '+'

		if result.endswith('+'):
			result = result[:-1]

		return Expression.beautify(result)

	@staticmethod
	def product(p, q, name=None):
		"""Finds the product of polynomials p and q."""

		if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
			raise InvalidOperationError(p, q)

		result = []

		for p_term in p.terms:
			for q_term in q.terms:
				result.append(TermOperations.multiply(p_term, q_term))

		result = '+'.join(result)
		return Polynomial(Expression.beautify(result), name)

# Error. When multiplying 3 by 6x**5 it returns 18x**6. No x, no exponent addition!


Px = Polynomial("2x**3 - x**2", "P(x)")
Qx = Polynomial("6x**5 + 3x**9", "Q(x)")

Fx = PolynomialOperation.product(Px, Qx, "F(x)")
print(Fx.terms_by_degree)
print(Fx.degrees)
print(Fx)
print(Fx.primary_coefficient)
