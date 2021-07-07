import unittest
from PyCurve.curve import Curve
import numpy as np


class TestCurve(unittest.TestCase):
    def setUp(self) -> None:
        self.curve_1 = Curve([0, 0, 0, 0], [0, 0, 0, 0])
        self.curve_2 = Curve(np.array([0, 0, 0, 0]), np.array([0, 0, 0, 0]))

    def test_getter(self) -> None:
        self.assertEqual(self.curve_1.get_time, [0, 0, 0, 0])
        self.assertEqual(self.curve_1.get_rate, [0, 0, 0, 0])
        self.assertTrue((self.curve_2.get_time == np.array([0, 0, 0, 0])).all())
        self.assertTrue((self.curve_2.get_rate == np.array([0, 0, 0, 0])).all())

    def test_setter(self) -> None:
        self.curve_1.set_time([0, 1, 2, 3])
        self.curve_1.set_rate([3, 2, 1, 0])
        self.assertEqual(self.curve_1.get_time, [0, 1, 2, 3])
        self.assertEqual(self.curve_1.get_rate, [3, 2, 1, 0])

        self.curve_2.set_time(np.array([0, 1, 2, 3]))
        self.curve_2.set_rate(np.array([3, 2, 1, 0]))
        self.assertTrue((self.curve_2.get_time == np.array([0, 1, 2, 3])).all())
        self.assertTrue((self.curve_2.get_rate == np.array([3, 2, 1, 0])).all())


if __name__ == '__main__':
    unittest.main()
