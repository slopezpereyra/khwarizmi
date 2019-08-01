import unittest
import os
import sys
sys.path.append(os.path.abspath('../khwarizmi'))
from quadratic import Quadratic

# 0.003 sec

class QuadraticTest(unittest.TestCase):

    def setUp(self):
        self.first_quadratic = Quadratic('2x**2 + 3x + 5')
        self.sec_quadratic = Quadratic('3x**2')
        self.third_quadratic = Quadratic('-4x**2 - 2x + 2')

    def test_discriminant(self):
        self.assertEqual(self.first_quadratic.discriminant, -31)
        self.assertEqual(self.sec_quadratic.discriminant, 0)
        self.assertEqual(self.third_quadratic.discriminant, 36)

    def test_roots_type(self):
        self.assertEqual(self.first_quadratic.roots_type, 'Complex conjugate roots')
        self.assertEqual(self.sec_quadratic.roots_type, 'Identical real roots')
        self.assertEqual(self.third_quadratic.roots_type, 'Distinct real roots')

    def test_roots(self):
        self.assertEqual(self.first_quadratic.roots, ['(-3 +/- i(31**½)) / 4'])
        self.assertEqual(self.sec_quadratic.roots, [0])
        self.assertEqual(self.third_quadratic.roots, [-1, 0.5])

    def test_vertex(self):
        self.assertEqual(self.first_quadratic.vertex, (-0.75, 3.875))
        self.assertEqual(self.sec_quadratic.vertex, (0, 0))
        self.assertEqual(self.third_quadratic.vertex, (-0.25, 2.25))

    def test_axis_of_simmetry(self):
        self.assertEqual(self.first_quadratic.axis_of_simmetry, 'x = -0.75')
        self.assertEqual(self.sec_quadratic.axis_of_simmetry, 'x = 0')
        self.assertEqual(self.third_quadratic.axis_of_simmetry, 'x = -0.25')

    def test_is_ascendant(self):
        self.assertTrue(self.first_quadratic.isascendant)
        self.assertTrue(self.sec_quadratic.isascendant)
        self.assertFalse(self.third_quadratic.isascendant)



if __name__ == '__main__':
    unittest.main()
