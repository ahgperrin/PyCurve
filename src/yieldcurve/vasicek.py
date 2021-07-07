import numpy as np
import matplotlib.pyplot as plt
from src.yieldcurve.curve import Curve,Simulation

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
        return Simulation(simulation,self.dt)
