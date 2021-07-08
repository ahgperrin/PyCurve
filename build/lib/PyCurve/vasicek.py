from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from PyCurve.simulation import Simulation

plt.style.use("bmh")


class Vasicek:

    def __init__(self, alpha: float, beta: float, sigma: float, rt: float, time: float, delta_time: float) -> None:
        self._alpha = alpha
        self._beta = beta
        self._sigma = sigma
        self._rt = rt
        self._dt = delta_time
        self._steps = int(time / delta_time)

    def get_attr(self, attr: str) -> Union[float,int]:
        return self.__getattribute__(attr)

    def _sigma_part(self, n: int) -> float:
        return self.get_attr("_sigma") * np.sqrt(self.get_attr("_dt")) * np.random.normal(size=n)

    def _mu_dt(self, rt: np.ndarray) -> float:
        return self.get_attr("_alpha") * (self.get_attr("_beta") - rt) * self.get_attr("_dt")

    def simulate_paths(self, n: int) -> np.array:
        simulation = np.zeros(shape=(self.get_attr("_steps"), n))
        simulation[0, :] = -0.004
        for i in range(1, self.get_attr("_steps"), 1):
            dr = self._mu_dt(simulation[i - 1, :]) + self._sigma_part(n)
            simulation[i, :] = simulation[i - 1, :] + dr
        return Simulation(simulation,self.get_attr("_dt"))
