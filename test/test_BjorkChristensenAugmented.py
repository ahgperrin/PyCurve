import unittest

from PyCurve.bjork_christensen_augmented import BjorkChristensenAugmented
from PyCurve.curve import Curve


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
        self.bjork_christensen = BjorkChristensenAugmented(1, 2, 3, 4, 5, 6)

    def test_bjk_constructor(self) -> None:
        self.assertEqual(self.bjork_christensen.get_attr("beta0"), 1)
        self.assertEqual(self.bjork_christensen.get_attr("beta1"), 2)
        self.assertEqual(self.bjork_christensen.get_attr("beta2"), 3)
        self.assertEqual(self.bjork_christensen.get_attr("beta3"), 4)
        self.assertEqual(self.bjork_christensen.get_attr("beta4"), 5)
        self.assertEqual(self.bjork_christensen.get_attr("tau"), 6)
        self.assertEqual(self.bjork_christensen.get_attr("attr_list"),
                         ["beta0", "beta1", "beta2", "beta3", "beta4", "tau"])

    def test_bjk_setter(self) -> None:
        self.bjork_christensen.set_attr("beta0", 6)
        self.bjork_christensen.set_attr("beta1", 5)
        self.bjork_christensen.set_attr("beta2", 4)
        self.bjork_christensen.set_attr("beta3", 3)
        self.bjork_christensen.set_attr("beta4", 2)
        self.bjork_christensen.set_attr("tau", 1)

        self.assertEqual(self.bjork_christensen.get_attr("beta0"), 6)
        self.assertEqual(self.bjork_christensen.get_attr("beta1"), 5)
        self.assertEqual(self.bjork_christensen.get_attr("beta2"), 4)
        self.assertEqual(self.bjork_christensen.get_attr("beta3"), 3)
        self.assertEqual(self.bjork_christensen.get_attr("beta4"), 2)
        self.assertEqual(self.bjork_christensen.get_attr("tau"), 1)

    def test_bjork_christensen_attr_strike(self) -> None:
        self.assertRaises(AttributeError, lambda: self.bjork_christensen.set_attr("beta0", -1))
        self.assertRaises(AttributeError, lambda: self.bjork_christensen.set_attr("tau", -1))

    def test_bjork_christensen_calibration(self) -> None:
        self.assertRaises(ValueError, lambda: self.bjork_christensen.calibrate(1))
        self.res_bjork_christensen = self.bjork_christensen.calibrate(self.curve_1)
        self.assertEqual(self.res_bjork_christensen.x[0], 1.6086026450303779)
        self.assertEqual(self.res_bjork_christensen.x[1], -0.13920910952860865)
        self.assertEqual(self.res_bjork_christensen.x[2], -1.9649335181673264)
        self.assertEqual(self.res_bjork_christensen.x[3], -3.095914509002693)
        self.assertEqual(self.res_bjork_christensen.x[4], -0.24710283790219)
        self.assertEqual(self.res_bjork_christensen.x[5], 3.3869504759346336)
        self.assertEqual(self.res_bjork_christensen.fun, 0.00013909793572569192)
        self.assertEqual(self.res_bjork_christensen.nit, 47)

    def test_bjork_christensen_rate(self) -> None:
        self.bjork_christensen.calibrate(self.curve_1)
        self.assertAlmostEqual(self.bjork_christensen.rate(1), -0.67627832663938393213, 10)
        self.assertAlmostEqual(self.bjork_christensen.rate(20), 0.33039622991859094614, 10)
        self.assertAlmostEqual(self.bjork_christensen.rate(30), 0.40729027000210230784, 10)
        self.assertAlmostEqual(self.bjork_christensen.forward_rate(30, 40), 0.16858548353284021696, 10)

    def test_nss_df(self) -> None:
        self.bjork_christensen.calibrate(self.curve_1)
        self.assertAlmostEqual(self.bjork_christensen.df_t(1), 1.0068088299073549722, 10)
        self.assertAlmostEqual(self.bjork_christensen.df_t(20), 0.9361586451691218605, 10)
        self.assertAlmostEqual(self.bjork_christensen.df_t(30), 0.8852024292336747718, 10)
        self.assertAlmostEqual(self.bjork_christensen.cdf_t(1), 1.0067857025220037777, 10)
        self.assertAlmostEqual(self.bjork_christensen.cdf_t(20), 0.9360566826197276989, 10)
        self.assertAlmostEqual(self.bjork_christensen.cdf_t(30), 0.8849827895489620966, 10)


if __name__ == '__main__':
    unittest.main()
