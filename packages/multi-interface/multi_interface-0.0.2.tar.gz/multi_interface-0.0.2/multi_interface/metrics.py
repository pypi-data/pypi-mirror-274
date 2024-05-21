import numpy as np


class Metrics:
    @classmethod
    def calculate_mse(cls, m1, m2):
        return np.linalg.norm(m1 - m2, 2) / m1.shape[0] / m1.shape[1]

    @classmethod
    def calculate_kl(cls, m):
        return np.linalg.norm(m - m.mean(), 1)/ m.shape[0] / m.shape[1]

    @classmethod
    def calculate_range(cls, m):
        return m.min(), m.max()


