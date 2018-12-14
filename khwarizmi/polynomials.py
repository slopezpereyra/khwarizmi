"""Polynomial expressions and its operations."""

from khwarizmi.expression import Expression
from khwarizmi.exc import InvalidOperationError
from khwarizmi.misc import if_assign


class Polynomial(Expression):
	"""Base class for all polynomial expressions."""

	def __init__(self, polynomial, name=None):
		Expression.__init__(self, polynomial)
		self.polynomial = polynomial
		self.name = name
		self.indeterminates = self.variables
		self.degrees = self.get_degrees()
		self.degree = max(self.degrees)
		self.primary_coefficient = self.get_primary_coefficient()
		self.non_coefficient_term = self.get_non_coefficient_term()
		self.polynomial = self.reorder_terms()
		self.terms_by_degree = self.get_terms_by_degree()

	def __str__(self):
		if self.name is not None and self.name is not '':
			return self.name + " = " + self.polynomial
		return self.polynomial

	def get_degrees(self):
		"""Returns all degrees of all terms of this polynomial."""
		last_power_index = 0
		power_count = self.polynomial.count("**")
		powers = []

		for power in range(0, power_count):
			index = self.polynomial.find("**", last_power_index)
			powers.append(self.polynomial[index + 2])
			last_power_index = index + 2

		return sorted(powers, reverse=True)

	def get_primary_coefficient(self):
		"""Returns the primary coefficient of this polynomial."""

		counter = 0
		for coefficient in self.coefficients:
			if self.terms[counter].startswith(coefficient) and self.terms[counter].endswith("**" + self.degree):
				return coefficient
			counter += 1

	def get_non_coefficient_term(self):
		for term in self.terms:
			if any(char.isalpha() for char in term):
				continue
			return term

		return 0

	def reorder_terms(self):
		"""Reorders the terms of the polynomial; higher degrees first."""

		reordered = ""
		for degree in self.degrees:
			for term in self.terms:
				if "**" + degree in term:
					if not term.startswith('-'):
						term = '+' + term
					reordered += term
					break

		non_coefficient = if_assign(self.non_coefficient_term.startswith('-'), self.non_coefficient_term, '+' + self.non_coefficient_term)
		reordered += non_coefficient
		if reordered.startswith('+'):
			reordered = reordered.replace("+", '', 1)

		return Expression.beautify(reordered)

	def get_terms_by_degree(self):

		terms_by_degree = {}

		for degree in self.degrees:
			for term in self.terms:
				if "**" + degree in term:
					index = term.find('*')
					term_without_exponent = term[0:index]
					terms_by_degree[degree] = term_without_exponent
					break

		terms_by_degree["1"] = next(term for term in self.terms if '**' not in term)

		return terms_by_degree


class PolynomialOperation:
	"""Class holding static methods involving polynomial operations."""

	def __init__(self, p, q):
		self.p = p
		self.q = q

	@staticmethod
	def addition(p, q, name):
		"""Performs the addition of two polynomials."""

		if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
			raise InvalidOperationError(p, q)

		result = ""

		longer_polynomial = if_assign(len(p.degrees) >= len (q.degrees), p, q)

		for degree in longer_polynomial.terms_by_degree:
			try:
				p_term_variable = next((char for char in p.terms_by_degree[degree] if char.isalpha()), 'x')
				q_term_variable = next((char for char in q.terms_by_degree[degree] if char.isalpha()), 'x')

				p_power_index = p.terms_by_degree[degree].find(p_term_variable)
				q_power_index = q.terms_by_degree[degree].find(q_term_variable)

				p_power_index = if_assign(p_power_index is -1, len(p.terms_by_degree[degree]), p_power_index)
				q_power_index = if_assign(q_power_index is -1, len(q.terms_by_degree[degree]), q_power_index)

				p_all_variables = p.terms_by_degree[degree][p_power_index:]
				q_all_variables = q.terms_by_degree[degree][q_power_index:]

				if p_all_variables != q_all_variables:
					# Get this working
					raise KeyError

				p_term, q_term = p.terms_by_degree[degree][0:p_power_index], q.terms_by_degree[degree][0:q_power_index]
				result_term = str(int(p_term) + int(q_term)) + p_all_variables + '**' + degree
				if not result_term.startswith('-'):
					result_term = '+' + result_term
				result += result_term

			except KeyError:
				print("Here!")
				result_term = p.terms_by_degree[degree] + '**' + degree
				if not result_term.startswith('-'):
					result_term = '+' + result_term
				result += result_term

		if result.startswith('+'):
			result = result.replace('+', '', 1)
			result = result.replace('**1', '')

		return Polynomial(result, name)


Px = Polynomial("2x**3 - 5x**2 - 3x**4 + 7x**5 - 2 + 6x**9", "P(x)")
Qx = Polynomial("3x**3 - 4x**2 + 6x**5 + 5 + 3x**9", "Q(x)")

print(Px.terms_by_degree)

print(Px)
print(Qx)

RESULT = PolynomialOperation.addition(Px, Qx, 'F(x)')
print(RESULT)