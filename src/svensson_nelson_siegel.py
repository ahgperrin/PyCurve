from typing import Any

from src._actuarial_implementation import discrete_df, continuous_df
from src.curve import Curve
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

plt.style.use("bmh")
np.seterr(divide='ignore', invalid='ignore')


class NelsonSiegelAugmented:

    def __init__(self, beta0: float, beta1: float, beta2: float, beta3: float, tau: float, tau2: float) -> None:
        self.beta0: float = self._is_positive_attr(beta0)
        self.beta1: float = beta1
        self.beta2: float = beta2
        self.beta3: float = beta3
        self.tau: float = self._is_positive_attr(tau)
        self.tau2: float = self._is_positive_attr(tau2)
        self.attr_list: list = ["beta0", "beta1", "beta2", "beta3", "tau", "tau2"]

    @staticmethod
    def _is_valid_curve(curve: Any) -> Curve:
        """Check if an attribute is an instance of Curve"""
        if not (isinstance(curve, Curve)):
            raise ValueError("Curve parameter must be an instance of Curve")
        return curve

    @staticmethod
    def _is_positive_attr(attr: float) -> float:
        """Check attribute is positive"""
        if attr < 0:
            raise AttributeError("Beta0, tau and tau2, must be positive")
        return attr

    def get_attr(self, attr: str) -> float:
        return self.__getattribute__(attr)

    def set_attr(self, attr: str, x: float) -> None:
        if attr in (["beta0", "tau", "tau2"]):
            self.__setattr__(attr, self._is_positive_attr(x))
        self.__setattr__(attr, x)

    def _print_model(self) -> None:
        print("Augmented Nelson Siegel Model")
        print(28 * "=")
        for attr in self.attr_list:
            print(attr + " =", self.get_attr(attr))
        print(28 * "_")

    @staticmethod
    def _calibration_func(x: list, curve: Curve) -> float:
        ns = NelsonSiegelAugmented(x[0], x[1], x[2], x[3], x[4], x[5])
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
        x0 = np.array([1, 0, 0, 0, 1, 1])
        boundaries = ((1e-6, np.inf), (-30, 30), (-30, 30), (-30, 30), (1e-6, 30), (1e-6, 30))
        calibration_result = minimize(self._calibration_func, x0, method='L-BFGS-B', args=curve, bounds=boundaries)
        i = 0
        for attr in self.attr_list:
            self.set_attr(attr, calibration_result.x[i])
            i += 1
        self._print_fitting(calibration_result)
        return calibration_result

    def _time_decay(self, t):
        return self.beta1 * (np.array(((1 - np.exp(-np.array(t, np.float128) / self.tau)) /
                                       (np.array(t, np.float128) / self.tau))))

    def _hump(self, t):
        return self.beta2 * np.subtract(np.array(((1 - np.exp(-np.array(t, np.float128) / self.tau)) /
                                                  (np.array(t, np.float128) / self.tau))),
                                        np.array(np.exp(-np.array(t, np.float128) / self.tau)))

    def _second_hump(self, t):
        return self.beta3 * np.subtract(np.array(((1 - np.exp(-np.array(t, np.float128) / self.tau2)) /
                                                  (np.array(t, np.float128) / self.tau2))),
                                        np.array(np.exp(-np.array(t, np.float128) / self.tau2)))

    def rate(self, t):
        first_coefficient = self._time_decay(t)
        second_coefficient = self._hump(t)
        third_coefficient = self._second_hump(t)
        return self.beta0 + first_coefficient + second_coefficient + third_coefficient

    def plot_model_params(self):
        t = np.linspace(0.0, 50, 1000)
        b0 = np.ones(1000) * self.beta0
        fig = plt.figure(figsize=(12.5, 8))
        fig.suptitle("Nelson Siegel Parameters")
        ax1 = fig.add_subplot(212)
        ax1.plot(t, self.rate(t))
        ax1.set_xlabel('t, years')
        ax1.set_ylabel('Yield')
        ax1.set_title('Nelson Siegel Svensson Model')
        ax2 = fig.add_subplot(241)
        ax2.plot(t, b0)
        ax2.set_ylabel('Yield')
        ax2.set_title('Long Term Rate')
        ax3 = fig.add_subplot(242)
        ax3.plot(t, self._time_decay(t))
        ax3.set_title('Time Decay Part')
        ax4 = fig.add_subplot(243)
        ax4.plot(t, self._hump(t))
        ax4.set_title('Hump Part')
        ax5 = fig.add_subplot(244)
        ax5.plot(t, self._second_hump(t))
        ax5.set_title('Second Hump Part')
        plt.show()

    def plot_model(self):
        t = np.linspace(0.001, 50, 1000)
        b0 = np.ones(1000) * self.beta0
        fig = plt.figure()
        fig.suptitle("Nelson Siegel Svensson BreakDown")
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('t, years')
        ax.set_ylabel('Yield')
        ax.plot(t, self.rate(t), label="Full Model")
        ax.plot(t, b0, label="Long Term Rate")
        ax.plot(t, self._hump(t), label="Hump")
        ax.plot(t, self._time_decay(t), label="Time Decay")
        ax.plot(t, self._second_hump(t), label="Second Hump")
        plt.legend()
        plt.show()

    def df_t(self, t):
        return discrete_df(self.rate(t), t)

    def cdf_t(self, t):
        return continuous_df(self.rate(t), t)

    def forward_rate(self, t_1, t_2):
        return ((self.rate(t_2) * t_2) - (self.rate(t_1) * t_1)) / (t_2 - t_1)
