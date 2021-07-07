import unittest

from PyCurve.vasicek import Vasicek
from PyCurve.linear import LinearCurve


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.vasicek = Vasicek(1, 0.04, 0, -0.004, 1, 1 / 365)
        self.vasicek_2 = Vasicek(1, 0.07, 0, 0.015, 1, 1 / 365)
        self.vasicek_sig = Vasicek(1, 0.07, 0.01, 0.015, 1, 1 / 365)

    def test_constructor(self) -> None:
        self.assertEqual(self.vasicek.get_attr("_alpha"), 1)
        self.assertEqual(self.vasicek.get_attr("_beta"), 0.04)
        self.assertEqual(self.vasicek.get_attr("_sigma"), 0)
        self.assertEqual(self.vasicek.get_attr("_rt"), -0.004)
        self.assertEqual(self.vasicek.get_attr("_dt"), 0.0027397260273972603)
        self.assertEqual(self.vasicek.get_attr("_steps"), 365)

        self.assertEqual(self.vasicek_sig.get_attr("_alpha"), 1)
        self.assertEqual(self.vasicek_sig.get_attr("_beta"), 0.07)
        self.assertEqual(self.vasicek_sig.get_attr("_sigma"), 0.01)
        self.assertEqual(self.vasicek_sig.get_attr("_rt"), 0.015)
        self.assertEqual(self.vasicek_sig.get_attr("_dt"), 0.0027397260273972603)
        self.assertEqual(self.vasicek_sig.get_attr("_steps"), 365)

    def test_simulation_no_sigma(self) -> None:
        simulation = self.vasicek.simulate_paths(15)
        self.assertAlmostEqual(simulation.get_sim[0].mean(), -0.004, 3)
        self.assertAlmostEqual(simulation.get_sim[364].mean(), 0.02379, 3)
        simulation_2 = self.vasicek_2.simulate_paths(15)
        self.assertAlmostEqual(simulation_2.get_sim[0].mean(), -0.004, 3)
        self.assertAlmostEqual(simulation_2.get_sim[364].mean(), 0.04274, 3)

    def test_simulation_sigma(self) -> None:
        simulation = self.vasicek_sig.simulate_paths(2000)
        self.assertAlmostEqual(simulation.get_sim[0].mean(), -0.004, 3)
        self.assertAlmostEqual(simulation.get_sim[364].mean(), 0.042768498574009446, 3)
        linear = LinearCurve(simulation.yield_curve())
        self.assertAlmostEqual(float(linear.d_rate(0.2)), 0.00285333, 3)
        self.assertAlmostEqual(float(linear.d_rate(0.5)), 0.01184294, 3)
        self.assertAlmostEqual(float(linear.d_rate(0.9)), 0.02146702, 3)


if __name__ == '__main__':
    unittest.main()
