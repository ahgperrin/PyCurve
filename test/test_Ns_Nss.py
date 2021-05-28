import unittest

from src.curve import Curve
from src.nelson_siegel import NelsonSiegel
from src.svensson_nelson_siegel import NelsonSiegelAugmented


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

    def test_ns_constructor(self)->None:
        self.assertEqual(self.ns.get_attr("beta0"), 1)
        self.assertEqual(self.ns.get_attr("beta1"), 2)
        self.assertEqual(self.ns.get_attr("beta2"), 3)
        self.assertEqual(self.ns.get_attr("tau"), 4)
        self.assertEqual(self.ns.get_attr("attr_list"), ["beta0", "beta1", "beta2", "tau"])

    def test_ns_setter(self)->None:
        self.ns.set_attr("beta0", 6)
        self.ns.set_attr("beta1", 5)
        self.ns.set_attr("beta2", 4)
        self.ns.set_attr("tau", 2)

        self.assertEqual(self.ns.get_attr("beta0"), 6)
        self.assertEqual(self.ns.get_attr("beta1"), 5)
        self.assertEqual(self.ns.get_attr("beta2"), 4)
        self.assertEqual(self.ns.get_attr("tau"), 2)

    def test_ns_attr_strike(self)->None:
        self.assertRaises(AttributeError, lambda: self.ns.set_attr("beta0", -1))
        self.assertRaises(AttributeError, lambda: self.ns.set_attr("tau", -1))

    def test_nss_constructor(self)->None:
        self.assertEqual(self.nss.get_attr("beta0"), 1)
        self.assertEqual(self.nss.get_attr("beta1"), 2)
        self.assertEqual(self.nss.get_attr("beta2"), 3)
        self.assertEqual(self.nss.get_attr("beta3"), 4)
        self.assertEqual(self.nss.get_attr("tau"), 5)
        self.assertEqual(self.nss.get_attr("tau2"), 6)
        self.assertEqual(self.nss.get_attr("attr_list"), ["beta0", "beta1", "beta2", "beta3", "tau", "tau2"])

    def test_nss_setter(self)->None:
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

    def test_nss_attr_strike(self)->None:
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("beta0", -1))
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("tau", -1))
        self.assertRaises(AttributeError, lambda: self.nss.set_attr("tau2", -1))

    def test_ns_calibration(self)->None:
        self.assertRaises(ValueError, lambda: self.ns.calibrate(1))
        self.res_ns = self.ns.calibrate(self.curve_1)
        self.assertEqual(self.res_ns.x[0], 0.44121845796127146)
        self.assertEqual(self.res_ns.x[1], -1.0420528066723032)
        self.assertEqual(self.res_ns.x[2], 1.6042117376081295)
        self.assertEqual(self.res_ns.x[3], 4.757459370801262)
        self.assertEqual(self.res_ns.fun, 0.0004361538923576626)
        self.assertEqual(self.res_ns.nit, 19)

    def test_nss_calibration(self)->None:
        self.assertRaises(ValueError, lambda: self.nss.calibrate(1))
        self.res_nss = self.nss.calibrate(self.curve_1)
        self.assertEqual(self.res_nss.x[0], 0.4317673238443175)
        self.assertEqual(self.res_nss.x[1], -1.043896871285076)
        self.assertEqual(self.res_nss.x[2], 5.6796728449553795)
        self.assertEqual(self.res_nss.x[3], -3.972010693898574)
        self.assertEqual(self.res_nss.x[4], 4.070897553608448)
        self.assertEqual(self.res_nss.x[5], 3.8033723280403975)
        self.assertEqual(self.res_nss.fun, 8.494051924053917e-05)
        self.assertEqual(self.res_nss.nit, 147)

    def test_nss_rate(self)->None:
        self.nss.calibrate(self.curve_1)
        self.assertAlmostEqual(self.nss.rate(1), -0.673195667196413, 10)
        self.assertAlmostEqual(self.nss.rate(20), 0.32765049508711156594, 10)
        self.assertAlmostEqual(self.nss.rate(30), 0.41648832622344749292, 10)
        self.assertAlmostEqual(self.nss.forward_rate(30, 40), 0.4698397053600250028, 10)

    def test_ns_rate(self)->None:
        self.ns.calibrate(self.curve_1)
        self.assertAlmostEqual(self.ns.rate(1), -0.6765621734520236092, 10)
        self.assertAlmostEqual(self.ns.rate(20), 0.3249196408508820863, 10)
        self.assertAlmostEqual(self.ns.rate(30), 0.42084917599682446888, 10)
        self.assertAlmostEqual(self.ns.forward_rate(30, 40), 0.48935917386055295962, 10)

    def test_nss_df(self)->None:
        self.nss.calibrate(self.curve_1)
        self.assertAlmostEqual(self.nss.df_t(1), 1.006777583067515285, 10)
        self.assertAlmostEqual(self.nss.df_t(20), 0.9366711881807507148, 10)
        self.assertAlmostEqual(self.nss.df_t(30), 0.88277314591438881626, 10)

    def test_ns_df(self)->None:
        self.ns.calibrate(self.curve_1)
        self.assertAlmostEqual(self.ns.df_t(1), 1.0068117071685892162, 10)
        self.assertAlmostEqual(self.ns.df_t(20), 0.9371812457122977514, 10)
        self.assertAlmostEqual(self.ns.df_t(30), 0.88162381744194171017, 10)


if __name__ == '__main__':
    unittest.main()