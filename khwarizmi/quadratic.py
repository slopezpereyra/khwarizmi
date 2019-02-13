import math

from equations import Equation
from polynomials import Polynomial
from exc import NegativeSquareError
from enum import Enum, auto
from misc import num
from matplotlib import pyplot as plt

class RootTypes(Enum):

    DistinctRealRoots = auto()
    IdenticRealRoots = auto()
    ComplexConjugateRoots = auto()


class Quadratic(Polynomial):

    def __init__(self, polynomial):
        Polynomial.__init__(self, polynomial)
        self.discriminant = self.get_discriminant()
        self._root_type = None
        self.roots_nature = self.get_roots_nature()
        #self.roots = self.find_roots()

    def getabc(self):
        """Returns a tuple containing the values of a, b and c variables of Bhaskara's formula"""
        print(self.terms)
        return (self.get_number(0, self.terms[0]), self.get_number(0, self.terms[1]), self.terms[2])

    def get_discriminant(self):
        """Returns the discriminant an evaluated number; this means it will not return the discriminants
        form but its already simplified value."""

        abc = self.getabc()
        a, b, c = abc[0], abc[1], abc[2]

        disc = b + "**2-4*" + a + "*" + c
        return eval(disc)

    def get_roots_nature(self):
        """Returns a string defining this quadratic's roots
        nature; i.e, is it complex, real, distinct or identic."""

        if self.discriminant > 0:
            self._root_type = RootTypes.DistinctRealRoots
            return 'Two real distinct roots'
        if self.discriminant == 0:
            self._root_type = RootTypes.IdenticRealRoots
            return 'Two undistinct real roots'
        self._root_type = RootTypes.ComplexConjugateRoots
        return 'Two complex conjugate roots'

    def bhaskarize(self):
        """Returns a string representation of this quadratic's roots.
        It returns a string and not an int/float because complex roots
        can only be represented as strings (since Python can't
        evaluate complex numbers."""

        disc = self.discriminant
        abc = self.getabc()
        a, b, c = abc[0], abc [1], abc [2]
        den = eval("2*" + a)

        simple = ''

        simple = '(-' + b + ' +/- i(' + str(disc) +')**½) /' + str(den)
        if self._root_type != RootTypes.ComplexConjugateRoots:
            simple = simple.replace('i', '')
        return simple

    def get_roots(self):

        if self._root_type == RootTypes.ComplexConjugateRoots:
            return self.bhaskarize()

        bhask = self.bhaskarize().replace('½', '0.5')

        if self._root_type == RootTypes.IdenticRealRoots:
            return eval(bhask.replace('+/-', '+'))

        roots = []
        roots.append(eval(bhask.replace('+/-', '+')))
        roots.append (eval(bhask.replace('+/-', '-')))

        return roots

    def graph (self, domain_range):

        x_coors = []
        y_coors = []

        for x in range(-domain_range, domain_range):
            x_coors.append(x)
            y_coors.append(self.evaluate(x))
            print("INSPECT ", x, " ", self.evaluate(x))

        print(x_coors)
        print(y_coors)

        plt.plot(x_coors)
        plt.plot(y_coors)
        plt.show()


QUA = Quadratic("-2x**2 + 2x + 5")
print("FIRSTLY ", QUA.terms, " AND ", QUA.getabc())
print("\n")
print(QUA.polynomial)
print(QUA.discriminant)
print(QUA.roots_nature)
print(QUA.bhaskarize())
print(QUA.get_roots())
print(QUA.graph(10))
