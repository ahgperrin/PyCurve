from typing import Any
from PyCurve.curve import Curve
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-dark')


class Simulation:
    def __init__(self, simulated_paths: np.ndarray, dt: float) -> None:
        self._sim = self._is_valid_attr(simulated_paths)
        self._dt = dt

    @property
    def get_sim(self) -> np.ndarray:
        return self.__getattribute__("_sim")

    @property
    def get_nb_sim(self) -> int:
        return self.__getattribute__("_sim").shape[1]

    @property
    def get_steps(self) -> int:
        return self.__getattribute__("_sim").shape[0]

    @property
    def get_dt(self) -> float:
        return self.__getattribute__("_dt")

    @staticmethod
    def _is_valid_attr(attr: Any) -> np.ndarray:
        assert isinstance(attr, np.ndarray), "Class Constructor takes only numpy arrays or list as arguments"
        return attr

    def yield_curve(self) -> np.array:
        discount_factor: np.ndarray = self.discount_factor()
        yield_curve = np.mean(discount_factor, axis=1) ** (-1 / np.full(self.get_steps, self.get_dt).cumsum()) - 1
        return Curve(np.full(self.get_steps, self.get_dt).cumsum(),yield_curve)

    def discount_factor(self) -> np.array:
        rieman_sum: np.ndarray = np.zeros(shape=self.get_sim.shape)
        discount_factor: np.ndarray = np.zeros(shape=self.get_sim.shape)
        for sim in range(self.get_nb_sim):
            rieman_sum[:, sim] = np.cumsum(self.get_sim[:, sim]) * self.get_dt
            discount_factor[:, sim] = np.exp(-rieman_sum[:, sim])
        return discount_factor

    def plot_discount_curve(self, average: bool = False) ->None:
        discount_factor: np.ndarray = self.discount_factor()
        t: np.ndarray = np.full(self.get_steps, self.get_dt).cumsum()
        fig, ax = plt.subplots(1)
        fig.canvas.set_window_title('Discount Factor')
        fig.suptitle("Discount Factor")
        ax.set_xlabel('Time, t')
        ax.set_ylabel('Simulated Discount Factor')
        if average:
            ax.plot(t, np.mean(discount_factor, axis=1),c="navy")
        else:
            ax.plot(t, discount_factor)

    def plot_simulation(self) -> None:
        t: np.ndarray = np.full(self.get_steps, self.get_dt).cumsum()
        fig, ax = plt.subplots(1)
        fig.suptitle("Simulated Paths")
        fig.canvas.set_window_title('Simulated Paths')
        ax.set_xlabel('Time, t')
        ax.set_ylabel('Simulated Yield')
        ax.plot(t, self.get_sim,lw=0.5)
        plt.show()

    def plot_yield_curve(self) -> None:
        t: np.ndarray = np.full(self.get_steps, self.get_dt).cumsum()
        curve : Curve = self.yield_curve()
        fig, ax = plt.subplots(1)
        fig.suptitle("Simulated Yield Curve")
        fig.canvas.set_window_title('Simulated Yield Curve')
        ax.set_xlabel('Time, t')
        ax.set_ylabel('Simulated Yield')
        ax.plot(t, self.get_sim, lw=0.5)
        ax.plot(curve.get_time, curve.get_rate , label="Yield Curve", lw=2,c="darkred")
        plt.legend()
        plt.show()

    def plot_model(self) -> None:
        t: np.ndarray = np.full(self.get_steps, self.get_dt).cumsum()
        curve: Curve = self.yield_curve()
        fig = plt.figure(figsize=(12.5, 8))
        fig.suptitle("Simulated Model")
        fig.canvas.set_window_title('Simulated Model')
        ax1 = fig.add_subplot(212)
        ax1.set_xlabel('Time, t')
        ax1.set_ylabel('Yield')
        ax1.plot(t, self.get_sim, lw=0.5)
        ax2 = fig.add_subplot(221)
        ax2.set_xlabel('Time, t')
        ax2.set_ylabel('Discount factor')
        ax2.plot(t, np.mean(self.discount_factor(), axis=1), lw=2,c="navy")
        ax3 = fig.add_subplot(222)
        ax3.set_xlabel('Time, t')
        ax3.set_ylabel('Yield')
        ax3.plot(curve.get_time,curve.get_rate ,lw=2,c="darkred")
        plt.show()