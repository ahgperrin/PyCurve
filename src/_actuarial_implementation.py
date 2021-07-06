import numpy as np


def discrete_df(r, t):
    return 1 / ((1 + r/100) ** t)


def continuous_df(r, t):
    return np.exp(-r/100 * t)


def discrete_rate(df, t):
    return ((1 / df) ** (1 / t)) - 1


def continuous_rate(df, t):
    return np.log(1 / df) ** t