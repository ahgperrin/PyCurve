import unittest

import numpy as np
from PyCurve.simulation import Simulation


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = Simulation(np.array([[1, 1, 1, 1], [2, 2, 2, 2], [2, 2, 2, 2]]), 0.5)
        self.sim_2 = Simulation(np.array([[1, 1, 1, 1], [1.5, 1.5, 1.5, 1.5], [3.5, 3.5, 3.5, 3.5]]), 1.5)

    def test_getter(self) -> None:
        self.assertTrue((self.sim.get_sim == np.array([[1, 1, 1, 1], [2, 2, 2, 2], [2, 2, 2, 2]])).all())
        self.assertEqual(self.sim.get_nb_sim, 4)
        self.assertEqual(self.sim.get_dt, 0.5)
        self.assertEqual(self.sim.get_steps, 3)

        self.assertTrue((self.sim_2.get_sim == np.array([[1, 1, 1, 1],
                                                         [1.5, 1.5, 1.5, 1.5], [3.5, 3.5, 3.5, 3.5]])).all())
        self.assertEqual(self.sim_2.get_nb_sim, 4)
        self.assertEqual(self.sim_2.get_dt, 1.5)
        self.assertEqual(self.sim_2.get_steps, 3)

    def test_curve_computation(self) -> None:
        curve_1 = self.sim.yield_curve()
        self.assertTrue(np.array_equal(curve_1.get_time, np.array([0.5, 1., 1.5]), equal_nan=False))
        self.assertTrue(np.array_equal(np.round(curve_1.get_rate, 8), np.array([1.71828183, 3.48168907, 4.29449005]),
                                       equal_nan=False))
        curve_2 = self.sim_2.yield_curve()
        print(curve_2.get_rate)
        self.assertTrue(np.array_equal(curve_2.get_time, np.array([1.5, 3., 4.5]), equal_nan=False))
        self.assertTrue(np.array_equal(np.round(curve_2.get_rate, 8), np.array([1.71828183, 2.49034296, 6.3890561]),
                                       equal_nan=False))

    def test_df_computation(self) -> None:
        discount_1 = self.sim.discount_factor()
        self.assertTrue(
            np.array_equal(np.round(discount_1, 6), np.round(np.array([[0.60653066, 0.60653066, 0.60653066, 0.60653066],
                                                                       [0.22313016, 0.22313016, 0.22313016, 0.22313016],
                                                                       [0.082085, 0.082085, 0.082085, 0.082085]]), 6),
                           equal_nan=False))
        discount_2 = self.sim_2.discount_factor()
        self.assertTrue(
            np.array_equal(np.round(discount_2, 7),
                           np.round(np.array([[2.23130160e-01, 2.23130160e-01, 2.23130160e-01, 2.23130160e-01],
                                              [2.35177459e-02, 2.35177459e-02, 2.35177459e-02, 2.35177459e-02],
                                              [1.23409804e-04, 1.23409804e-04, 1.23409804e-04, 1.23409804e-04]]), 7),
                           equal_nan=False))


if __name__ == '__main__':
    unittest.main()
