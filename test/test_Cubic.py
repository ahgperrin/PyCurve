import unittest
from PyCurve.curve import Curve
from PyCurve.cubic import CubicCurve

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.curve_1 = Curve([0.25, 0.5, 0.75, 1., 2., 3., 4., 5., 6.,
                              7., 8., 9., 10., 11., 12., 13., 14., 15.,
                              16., 17., 18., 19., 20., 21., 22., 23., 24.,
                              25., 26., 27., 28., 29., 30.],
                             [-0.63171, -0.650322, -0.664493, -0.674608, -0.681294,
                              -0.647593, -0.587828, -0.51251, -0.429238, -0.343399,
                              -0.258716, -0.177665, -0.101804, -0.032016, 0.031297,
                              0.088074, 0.138485, 0.182851, 0.221585, 0.25515, 0.284028,
                              0.308697, 0.32962, 0.347231, 0.361935, 0.374099, 0.38406,
                              0.392117, 0.398536, 0.403555, 0.407379, 0.410192, 0.412151])
        self.cub_curve = CubicCurve(self.curve_1)

    def test_rate(self)->None:
        self.assertAlmostEqual(self.cub_curve.d_rate(0.30), -0.63580618, 6)
        self.assertAlmostEqual(self.cub_curve.d_rate(3), -0.647593, 6)
        self.assertAlmostEqual(self.cub_curve.d_rate(10), -0.101804, 6)
        self.assertAlmostEqual(self.cub_curve.forward(10, 20), 0.761044, 6)

    def test_df(self)->None:
        self.assertAlmostEqual(self.cub_curve.df_t(0.30),  1.0019153400191672, 10)
        self.assertAlmostEqual(self.cub_curve.df_t(3), 1.0196821584930882, 10)
        self.assertAlmostEqual(self.cub_curve.df_t(10), 1.0102376351919737, 10)

    def test_curve(self)->None:
        self.curve_2 = self.cub_curve.create_curve([0,5,10,15,20])
        self.assertEqual(self.curve_2.get_time, self.curve_2.get_time)
        self.assertEqual(self.curve_2.get_rate[0], self.cub_curve.d_rate(self.curve_2.get_time[0]))
        self.assertEqual(self.curve_2.get_rate[2], self.cub_curve.d_rate(self.curve_2.get_time[2]))
        self.assertEqual(self.curve_2.get_rate[4], self.cub_curve.d_rate(self.curve_2.get_time[4]))


if __name__ == '__main__':
    unittest.main()
