import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-dark")


class Vasicek:

    def __init__(self, alpha: float, beta: float, sigma: float, rt: float, time: float, steps: int) -> None:
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma
        self.rt = rt
        self.dt = time / steps
        self._steps = steps

    def _sigma_part(self) -> float:
        """Generate a unique sigma dWt value"""
        return self.sigma * np.sqrt(self.dt) * np.random.normal()

    def _mu_dt(self, rt) -> float:
        """Generate a unique  mean reverting vasicek value"""
        return self.alpha * (self.beta - rt) * self.dt

    def simulate_paths(self, n: int) -> np.array:
        """Simulate Vasicek paths"""
        simulation = np.zeros((self._steps, n))
        simulation[0] = self.rt
        for j in range(0, n, 1):
            for i in range(1, self._steps, 1):
                simulation[i, j] = simulation[i - 1, j] + self._mu_dt(simulation[i - 1, j]) + self._sigma_part()
        return simulation

    def yield_curve(self, simul: np.array) -> np.array:
        """Given a simulation return an array of rate"""
        curve = np.zeros(self._steps)
        curve[0] = self.rt
        for i in range(1, self._steps):
            curve[i] = np.mean(simul[i])
        return curve

    def discount_factor(self, simul: np.array) -> np.array:
        """Given a simulation return an array of discount factor"""
        discount = self.yield_curve(simul)
        for i in range(self._steps):
            discount[i] = np.exp(-discount[i] * i * self.dt)
        return discount

    def plot_paths(self, simul: np.array) -> None:
        """Create a vizualisation of the Vasicek Stochastic Process"""
        fig, ax = plt.subplots(1)
        fig.suptitle(
            "Vasicek Simulated Paths \n(Alpha: " + str(self.alpha) + " /Beta: " + str(self.beta) + " /Sigma: " + str(
                self.sigma) + ")")
        ax.set_xlabel('Time, t')
        ax.set_ylabel('Simulated Asset Price')
        ax.plot(simul)
        plt.show()
