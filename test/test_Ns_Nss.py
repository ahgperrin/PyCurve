import unittest

from src.PyCurve.curve import Curve
from src.PyCurve.nelson_siegel import NelsonSiegel
from src.PyCurve.svensson_nelson_siegel import NelsonSiegelAugmented


class Test_ns_nss(unittest.TestCase):
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
        self.nss = NelsonSiegelAugmented(1, 2, 3, 4, 5, 6)
        self.ns = NelsonSiegel(1, 2, 3, 4)

    def test_ns_constructor(self) -> None:
        self.assertEqual(self.ns.get_attr("beta0"), 1)
        self.assertEqual(self.ns.get_attr("beta1"), 2)
        self.assertEqual(self.ns.get_attr("beta2"), 3)
        self.assertEqual(self.ns.get_attr("tau"), 4)
        self.assertEqual(self.ns.get_attr("attr_list"), ["beta0", "beta1", "beta2", "tau"])

    def test_ns_setter(self) -> None:
        self.ns.set_attr("beta0", 6)
        self.ns.set_attr("beta1", 5)
        self.ns.set_attr("beta2", 4)
        self.ns.set_attr("tau", 2)

        self.assertEqual(self.ns.get_attr("beta0"), 6)
        self.assertEqual(self.ns.get_attr("beta1"), 5)
        self.assertEqual(self.ns.get_attr("beta2"), 4)
        self.assertEqual(self.ns.get_attr("tau"), 2)

    def test_ns_attr_strike(self) -> None:
        self.assertRaises(AttributeError, lambda: self.ns.set_attr("beta0", -1))
        self.assertRaises(AttributeError, lambda: self.ns.set_attr("tau", -1))

    def test_nss_constructor(self) -> None:
        self.assertEqual(self.nss.get_attr("beta0"), 1)
        self.assertEqual(self.nss.get_attr("beta1"), 2)
        self.assertEqual(self.nss.get_attr("beta2"), 3)
        self.assertEqual(self.nss.get_attr("beta3"), 4)
        self.assertEqual(self.nss.get_attr("tau"), 5)
        self.assertEqual(self.nss.get_attr("tau2"), 6)
        self.assertEqual(self.nss.get_attr("attr_list"), ["beta0", "beta1", "beta2", "beta3", "tau", "tau2"])

    def test_nss_setter(self) -> None:
        self.nss.set_attr("beta0", 6)
        self.nss.set_attr("beta1", 5)
        self.nss.set_attr("beta2", 4)
        self.nss.set_attr("beta3", 3)
        self.nss.set_attr("tau", 2)
        self.nss.set_attr("tau2", 1)
        self.assertEqual(self.nss.get_attr("beta0"), 6)
        self.assertEqual(self.nss.get_attr("beta1"), 5)
        self.assertEqual(self.nss.get_attr("beta2"), 4)
        self.assertEqual(self.nss.get_attr("beta3"), 3)
        self.assertEqual(self.nss.get_attr("tau"), 2)
        self.assertEqual(self.nss.get_attr("tau2"), 1)

    def test_nss_attr_strike(self) -> None:
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("beta0", -1))
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("tau", -1))
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("tau2", -1))

    def test_ns_calibration(self) -> None:
        self.assertRaises(ValueError, lambda: self.ns.calibrate(1))
        self.res_ns = self.ns.calibrate(self.curve_1)
        self.assertEqual(self.res_ns.x[0], 0.7591072778783439)
        self.assertEqual(self.res_ns.x[1], -1.3260856584993546)
        self.assertEqual(self.res_ns.x[2], -2.30884199679111)
        self.assertEqual(self.res_ns.x[3], 2.4967046326924147)
        self.assertEqual(self.res_ns.fun, 0.01320690898431798)
        self.assertEqual(self.res_ns.nit, 22)

    def test_nss_calibration(self) -> None:
        self.assertRaises(ValueError, lambda: self.nss.calibrate(1))
        self.res_nss = self.nss.calibrate(self.curve_1)
        self.assertEqual(self.res_nss.x[0], 0.7591047678885469)
        self.assertEqual(self.res_nss.x[1], -1.3260829741760174)
        self.assertEqual(self.res_nss.x[2], -1.3574664081884185)
        self.assertEqual(self.res_nss.x[3], -0.9513767860626137)
        self.assertEqual(self.res_nss.x[4], 2.496692288666087)
        self.assertEqual(self.res_nss.x[5], 2.4966928037670777)
        self.assertEqual(self.res_nss.fun, 0.013206908995289438)
        self.assertEqual(self.res_nss.nit, 37)

    def test_nss_rate(self) -> None:
        self.nss.calibrate(self.curve_1)
        self.assertAlmostEqual(self.nss.rate(1), -0.6892160964115264675, 10)
        self.assertAlmostEqual(self.nss.rate(20), 0.3062571184311050645, 10)
        self.assertAlmostEqual(self.nss.rate(30), 0.45661080539385167975, 10)
        self.assertAlmostEqual(self.nss.forward_rate(30, 40), 0.75905851040282940203, 10)

    def test_ns_rate(self) -> None:
        self.ns.calibrate(self.curve_1)
        self.assertAlmostEqual(self.ns.rate(1), -0.68921534129209782287, 10)
        self.assertAlmostEqual(self.ns.rate(20), 0.30625725996129391995, 10)
        self.assertAlmostEqual(self.ns.rate(30), 0.45661171324789959496, 10)
        self.assertAlmostEqual(self.ns.forward_rate(30, 40), 0.75906101770412713473, 10)

    def test_nss_df(self) -> None:
        self.nss.calibrate(self.curve_1)
        self.assertAlmostEqual(self.nss.df_t(1), 1.0069399925095810551, 10)
        self.assertAlmostEqual(self.nss.df_t(20), 0.9406747695226624711, 10)
        self.assertAlmostEqual(self.nss.df_t(30), 0.87225675881522176205, 10)
        self.assertAlmostEqual(self.nss.cdf_t(1), 1.0069159665647441921, 10)
        self.assertAlmostEqual(self.nss.cdf_t(20), 0.9405867242630298321, 10)
        self.assertAlmostEqual(self.nss.cdf_t(30), 0.87198483906456019884, 10)

    def test_ns_df(self) -> None:
        self.ns.calibrate(self.curve_1)
        self.assertAlmostEqual(self.ns.df_t(1), 1.0069399848532126206, 10)
        self.assertAlmostEqual(self.ns.df_t(20), 0.94067474297718491294, 10)
        self.assertAlmostEqual(self.ns.df_t(30), 0.8722565223305238475, 10)
        self.assertAlmostEqual(self.ns.cdf_t(1), 1.0069159589613261271, 10)
        self.assertAlmostEqual(self.ns.cdf_t(20), 0.9405866976387468649, 10)
        self.assertAlmostEqual(self.ns.cdf_t(30), 0.8719846015741027802, 10)


if __name__ == '__main__':
    unittest.main()
