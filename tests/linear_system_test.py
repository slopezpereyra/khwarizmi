from khwarizmi import linear
from khwarizmi.exc import InfinitelySolutionsError
import unittest

# 0.22 seconds to run.

class LinearSystemTest(unittest.TestCase):

    def setUp(self):
        self.linear_1 = linear.PointSlope('y - 4 = 5(x - 2')
        self.linear_2 = linear.SlopeIntercept('y = 2x + 5')
        self.system_1 = linear.LinearSystem(self.linear_1, self.linear_2)
        self.linear_3 = linear.Standard('3x + y = 2')
        self.linear_4 = linear.Standard('3x + y = 5')
        self.system_2 = linear.LinearSystem(self.linear_3, self.linear_4)
        self.linear_5 = linear.SlopeIntercept('y = 2x - 6')
        self.linear_6 = linear.PointSlope('y - 2 = 2(x - 4)')
        self.system_3 = linear.LinearSystem(self.linear_5, self.linear_6)

    def test_number_of_solutions(self):
        self.assertEqual(self.system_1.solutions, 'One solution')
        self.assertEqual(self.system_2.solutions, 'No solutions')
        self.assertEqual(self.system_3.solutions, 'Infinitely many solutions')

    def test_solution(self):
        self.assertEqual(self.system_1.solve(), (3.6666666666666665, 12.333333333333332))
        self.assertEqual(self.system_2.solve(), None)
        with self.assertRaises(InfinitelySolutionsError):
            self.system_3.solve()

    def test_if_is_compatible(self):
        self.assertEqual(self.system_1.compatible, True)
        self.assertEqual(self.system_2.compatible, False)
        self.assertEqual(self.system_3.compatible, True)

if __name__ == '__main__':
    unittest.main()