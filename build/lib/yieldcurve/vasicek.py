import numpy as np
import matplotlib.pyplot as plt
from src.yieldcurve.curve import Curve

plt.style.use("bmh")


class Vasicek:

    def __init__(self, alpha: float, beta: float, sigma: float, rt: float, time: float, steps: int) -> None:
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma
        self.rt = rt
        self.dt = time / steps
        self.steps = steps

    def _sigma_part(self, n: int) -> float:
        return self.sigma * np.sqrt(self.dt) * np.random.normal(size=n)

    def _mu_dt(self, rt: np.ndarray) -> float:
        return self.alpha * (self.beta - rt) * self.dt

    def simulate_paths(self, n: int) -> np.array:
        simulation = np.zeros(shape=(self.steps, n))
        simulation[0, :] = -0.004
        for i in range(1, self.steps, 1):
            dr = self.alpha * (self.beta - simulation[i - 1, :]) * self.dt + self._sigma_part(n)
            simulation[i, :] = simulation[i - 1, :] + dr
        return simulation

    def yield_curve(self, simulation: np.ndarray) -> np.array:
        yield_curve = np.zeros(shape=self.steps)
        discount_factor = self.discount_factor(simulation)
        t = np.zeros(shape=self.steps)
        for df in range(1, test.steps):
            yield_curve[df] = np.mean(discount_factor[df]) ** (-1 / (self.dt * df)) - 1
            t[df] = df
        yield_curve[0] = np.nan
        return yield_curve

    @staticmethod
    def discount_factor(simulation: np.ndarray) -> np.array:
        rieman_sum = np.zeros(shape=simulation.shape)
        discount_factor = np.zeros(shape=simulation.shape)
        for sim in range(simulation.shape[1]):
            rieman_sum[:, sim] = np.cumsum(simulation[:, sim]) * test.dt
            discount_factor[:, sim] = np.exp(-rieman_sum[:, sim])
        return discount_factor

    def plot_paths(self, simulation: np.array) -> None:
        fig, ax = plt.subplots(1)
        fig.suptitle(
            "Vasicek Simulated Paths \n(Alpha: " + str(self.alpha) + " /Beta: " + str(self.beta) + " /Sigma: " + str(
                self.sigma) + ")")
        ax.set_xlabel('Time, t')
        ax.set_ylabel('Simulated Asset Price')
        ax.plot(simulation)
        plt.show()


test = Vasicek(1, 0.04, 0.006, -0.004, 1, 365)
