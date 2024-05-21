from abc import ABCMeta, abstractmethod
from scipy.fftpack import fft2, ifft2
import numpy as np
from math import factorial


class Vgg(metaclass=ABCMeta):
    def __init__(self, bnds, rhos, observation_plane, longrkm, longckm):
        self.bnds = bnds
        self.rhos = rhos
        self.observation_plane = observation_plane
        self.longrkm, self.longckm = longrkm, longckm

    @abstractmethod
    def forward(self, t):
        pass


class Parker(Vgg):
    def __init__(self, bnds, rhos, observation_plane, longrkm, longckm):
        super(Parker, self).__init__(bnds=bnds, rhos=rhos, observation_plane=observation_plane, longrkm=longrkm, longckm=longckm)
        self.omga = self.__initial__omga__()
        self.K = max(self.bnds.keys())
        self.G = 6.67

    def __initial__omga__(self):
        nrow, ncol = self.bnds[0].shape
        omga = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                i_changed = i if i <= nrow / 2 else i - nrow
                j_changed = j if j <= ncol / 2 else j - ncol
                omga[i, j] = np.sqrt(i_changed ** 2 / self.longrkm ** 2 + j_changed ** 2 / self.longckm ** 2) * 2 * np.pi
        return omga

    def forward(self, t):
        fft_all = 0
        for k in range(self.K):
            factor_k = (self.rhos[k] - self.rhos[k+1]) * np.exp(-self.omga * self.observation_plane)
            fft_k = 0
            for n in range(1, t+1):
                fft_k = fft_k + self.omga ** (n - 1) / factorial(n) * fft2(self.bnds[k] ** n)
            fft_all = fft_all + factor_k * fft_k
        transformed_fft_all = -2 * np.pi * self.G * fft_all
        vgg = ifft2(transformed_fft_all).real
        return vgg


class Chao(Vgg):
    def __init__(self, bnds, rhos, observation_plane, longrkm, longckm):
        super(Chao, self).__init__(bnds=bnds, rhos=rhos, observation_plane=observation_plane, longrkm=longrkm,
                                     longckm=longckm)
        self.omga = self.__initial__omga__()
        self.ave_depth = self.__initial_ave_depth__()
        self.K = max(self.bnds.keys())
        self.G = 6.67

    def __initial__omga__(self):
        nrow, ncol = self.bnds[0].shape
        omga = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                i_changed = i if i <= nrow / 2 else i - nrow
                j_changed = j if j <= ncol / 2 else j - ncol
                omga[i, j] = np.sqrt(
                    i_changed ** 2 / self.longrkm ** 2 + j_changed ** 2 / self.longckm ** 2) * 2 * np.pi
        return omga

    def __initial_ave_depth__(self):
        ave_depth = {key: value.mean() for key, value in self.bnds.items()}
        return ave_depth

    def forward(self, t):
        fft_all = 0
        for k in range(self.K):
            factor_k = (self.rhos[k] - self.rhos[k + 1]) * np.exp(-self.omga * (self.observation_plane - self.ave_depth[k]))
            fft_k = 0
            for n in range(1, t + 1):
                fft_k = fft_k + self.omga ** (n - 1) / factorial(n) * fft2((self.bnds[k] - self.ave_depth[k]) ** n)
            fft_all = fft_all + factor_k * fft_k
        transformed_fft_all = -2 * np.pi * self.G * fft_all
        return ifft2(transformed_fft_all).real
