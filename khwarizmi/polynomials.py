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
        self.terms_by_degree = self.get_terms_by_degree()
        self.degrees = sorted(list(self.terms_by_degree.keys()), reverse=True)
        self.degree = self.degrees[0]
        self.indeterminates = self.variables
        self.non_coefficient_term = self.get_non_coefficient_term()
        self.primary_coefficient = self.get_primary_coefficient()
        self.polynomial = self.simplify()
        self.polynomial = self.reorder_terms()

    def __str__(self):

        if self.name is not None and self.name is not '':
            return self.name + " = " + self.polynomial
        return self.polynomial

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

    def simplify(self):
        """Simplify terms of same degree into single term."""

        polynomial = ""
        for k, v in self.terms_by_degree.items():
            polynomial += v + "+"

        return Expression.beautify(polynomial)

    def get_terms_by_degree(self):
        """Returns a dictionary where each term is paired to a degree key."""

        terms_by_degree = {}

        for term in self.terms:
            exponent = TermOperations.getpower(term)

            if exponent in terms_by_degree:
               simplified_term = TermOperations.add(term, terms_by_degree[exponent])
               terms_by_degree[exponent] = simplified_term

            else:
                terms_by_degree[TermOperations.getpower(term)] = term

        return terms_by_degree

    def evaluate(self, x):
        pol = self.polynomial.replace('x', '*(' + str(x) + ')')
        if pol.startswith('*'):
            pol = pol[1:]
        return eval(pol)


class PolynomialOperation:
    """Class holding static methods involving polynomial operations."""

    @staticmethod
    def _find_matching_term(e, p):
        """Given an exponent e, returns the term of polynomial p that has same
        degree of e."""

        if TermOperations.getpower(e) in p.terms_by_degree:
            return p.terms_by_degree[TermOperations.getpower(e)]
        else:
            return None

    @staticmethod
    def addition(p, q, name=None):
        """Performs addition between polynomials p and q."""

        if not isinstance(p, Polynomial) or not isinstance(q, Polynomial):
            raise InvalidOperationError(p, q)

        result = ""
        alr_added = []

        for term in p.terms:
            if term in alr_added:
                continue
            match = PolynomialOperation._find_matching_term(term, q)
            if match is not None and match not in alr_added:
                result += str(TermOperations.add(term, match, non_algebraic=True)) + '+'
                alr_added.extend([term, match])
                continue
            result += term + '+'
            alr_added.append(term)

        for term in q.terms:
            if PolynomialOperation._find_matching_term(term, p) is None:
                result += term + '+'

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

#print(PolynomialOperation.product(P, Q))
