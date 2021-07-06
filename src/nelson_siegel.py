from typing import Any

import numpy as np
from scipy.optimize import minimize

from src._actuarial_implementation import discrete_df
from src.curve import Curve


class NelsonSiegel:
    def __init__(self, beta0: float, beta1: float, beta2: float, tau: float):
        self.beta0: float = self._is_positive_attr(beta0)
        self.beta1: float = beta1
        self.beta2: float = beta2
        self.tau: float = self._is_positive_attr(tau)
        self.attr_list: list = ["beta0", "beta1", "beta2", "tau"]

    @staticmethod
    def _is_valid_curve(curve: Any) -> Curve:
        """Check if an attribute is an instance of Curve"""
        if not (isinstance(curve, Curve)):
            raise ValueError("Curve parameter must be an instance of Curve")
        return curve

    @staticmethod
    def _is_positive_attr(attr):
        if attr < 0:
            raise AttributeError("Beta0 and tau, must be positive")
        return attr

    def get_attr(self, attr):
        return self.__getattribute__(attr)

    def set_attr(self, attr, x):
        if attr in (["beta0", "tau"]):
            self.__setattr__(attr, self._is_positive_attr(x))
        self.__setattr__(attr, x)

    def _print_model(self):
        print("Nelson Siegel Model")
        print(28 * "=")
        for attr in self.attr_list:
            print(attr + " =", self.get_attr(attr))
        print(28 * "_")

    @staticmethod
    def _calibration_func(x, curve):
        ns = NelsonSiegel(x[0], x[1], x[2], x[3])
        curve_estim = np.ones(len(curve.get_time))
        for i in range(len(curve.get_time)):
            curve_estim[i] = ns.rate(curve.get_time[i])
        sqr_error_sum = ((curve_estim - curve.get_rate) ** 2).sum()
        return sqr_error_sum

    def _print_fitting(self, res):
        self._print_model()
        print(28 * "=")
        print("Calibration Results")
        print(28 * "=")
        print(res.message)
        print("Mean Squared Error", res.fun)
        print("Number of Iterations", res.nit)
        print(28 * "_")

    def calibrate(self, curve):
        self._is_valid_curve(curve)
        x0 = np.array([1, 0, 0, 1])
        boundaries = ((1e-6, np.inf), (-30, 30), (-30, 30), (1e-6, 30))
        calibration_result = minimize(self._calibration_func, x0, method='L-BFGS-B', args=curve, bounds=boundaries)
        i = 0
        for attr in self.attr_list:
            self.set_attr(attr, calibration_result.x[i])
            i += 1
        self._print_fitting(calibration_result)
        return calibration_result

    def rate(self, t):
        first_coefficient = np.array(self.beta1 * np.exp(-np.array(t, np.float128) / self.tau))
        second_coefficient = np.array(
            self.beta2 * (-np.array(t, np.float128) / self.tau) * np.exp(-np.array(t, np.float128) / self.tau))
        return self.beta0 + first_coefficient + second_coefficient

    def df_t(self, t):
        return discrete_df(self.rate(t), t)

    def forward_rate(self, t_1, t_2):
        return ((self.rate(t_2) * t_2) - (self.rate(t_1) * t_1)) / (t_2 - t_1)
