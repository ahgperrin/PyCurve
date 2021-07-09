from PyCurve.curve import Curve
from PyCurve.actuarial_implementation import *
from scipy.interpolate import CubicSpline, PPoly
from typing import Any, Union, Iterable


class CubicCurve:
    def __init__(self, curve: Curve) -> None:
        self._curve = self._is_valid_curve(curve)
        self._func_rate: PPoly = CubicSpline(self._curve.get_time, self._curve.get_rate)

    @staticmethod
    def _is_valid_curve(attr: Any) -> Curve:
        """Check if an attribute is an instance of Curve"""
        assert (isinstance(attr, Curve)), "You need to Instance with a Curve"
        return attr

    def d_rate(self, t: Union[np.ndarray, Iterable, int, float]) -> Union[np.ndarray, Iterable, int, float]:
        """Given a maturity return a d_rate"""
        return self._func_rate(t)

    def df_t(self, t: Union[np.ndarray, Iterable, int, float]) -> Union[np.ndarray, Iterable, int, float]:
        """Given a maturity return a discount factor"""
        return discrete_df(self.d_rate(t), t)

    def forward(self, t_1: Union[np.ndarray, Iterable, int, float],
                t_2: Union[np.ndarray, Iterable, int, float]) -> Union[np.ndarray, Iterable, int, float]:
        """Given two times return the forward d_rate between t_1/t_2"""
        return ((self.d_rate(t_2) * t_2) - (self.d_rate(t_1) * t_1)) / (t_2 - t_1)

    def create_curve(self, t_array: Union[np.ndarray, Iterable, int, float]) -> Curve:
        """Given an array of time create a new curve"""
        return Curve(t_array, self.d_rate(t_array))
