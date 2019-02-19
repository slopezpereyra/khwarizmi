"""Polynomial expressions and its operations."""

from expression import Expression
from terms_ops import TermOperations
from exc import InvalidOperationError
from misc import if_assign, isanumber


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
        self.degree = powers[0]
        return powers

    def get_primary_coefficient(self):
        """Returns the primary coefficient of this polynomial."""

        term = self.terms_by_degree[self.degree]
        return self.get_number(0, term)

    def get_non_coefficient_term(self):

        return next((term for term in self.terms if isanumber(term)), "0")

    def reorder_terms(self):

        """Reorders the terms of the polynomial; higher degrees first."""

        ordered_terms = []

        for degree in self.degrees:
            ordered_terms.append(self.terms_by_degree[degree])

        expression = "+".join(ordered_terms)
        return Expression.beautify(expression)

    def get_terms_by_degree(self):

        """Returns a dictionary where each term is paired to a degree key."""

        terms_by_degree = {}

        for term in self.terms:
            terms_by_degree[TermOperations.getpower(term)] = term

        return terms_by_degree

    def evaluate(self, x):
        pol = self.polynomial.replace('x', '*(' + str(x) + ')')
        return eval(pol)


class PolynomialOperation:

    """Class holding static methods involving polynomial operations."""

    @staticmethod
    def addition(p, q, name=None):
        """Performs addition of polynomials p and q."""

        if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
            raise InvalidOperationError(p, q)

        result = ""
        longer_polynomial = if_assign(len(p.degrees) >= len(q.degrees), p, q)

        for degree in longer_polynomial.terms_by_degree:
            try:
                term_of_p = p.terms_by_degree[degree] + '**' + degree
                term_of_q = q.terms_by_degree[degree] + '**' + degree
                result += TermOperations.add(term_of_p, term_of_q) + '+'

            except KeyError:
                result_term = p.terms_by_degree[degree] + '**' + degree
                if not result_term.startswith('-'):
                    result_term = '+' + result_term
                result += result_term + '+'

        if result.endswith('+'):
            result = result[:-1]

        return Polynomial(Expression.beautify(result), name)

    @staticmethod
    def product(p, q, name=None):
        """Takes the product of polynomials p and q."""

        if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
            raise InvalidOperationError(p, q)

        result = []

        for term_of_p in p.terms:
            for term_of_q in q.terms:
                result.append(TermOperations.multiply(term_of_p, term_of_q))

        result = '+'.join(result)
        return Polynomial(Expression.beautify(result), name)

