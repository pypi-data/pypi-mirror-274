from abc import ABCMeta, abstractmethod
import numpy as np
from math import factorial
from scipy.signal.windows import tukey
from scipy.fftpack import fft2, ifft2


class Bnd(metaclass=ABCMeta):
    def __init__(self, vgg, bnds, rhos, observation_plane, longrkm, longckm):
        self.vgg = vgg
        self.bnds = bnds
        self.rhos = rhos
        self.observation_plane = observation_plane
        self.longrkm, self.longckm = longrkm, longckm

    @abstractmethod
    def downward(self, t):
        pass


class ParkerI(Bnd):
    def __init__(self, vgg, bnds, rhos, observation_plane, longrkm, longckm, wh, alpha, target_layer=2, target_depth=0):
        super(ParkerI, self).__init__(vgg, bnds, rhos, observation_plane, longrkm, longckm)
        self.K = max(self.rhos.keys())
        self.G = 6.67
        self.wh = wh
        self.alpha = alpha
        self.target_layer = target_layer
        self.target_depth = target_depth
        self.omga = self.__initial__omga__()
        self.filter = self.__initial__filter__()
        # temp
        self.temp = {}

    def __initial__omga__(self):
        nrow, ncol = [item.shape for item in self.bnds.values()][0]
        omga = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                i_changed = i if i <= nrow / 2 else i - nrow
                j_changed = j if j <= ncol / 2 else j - ncol
                omga[i, j] = np.sqrt(i_changed ** 2 / self.longrkm ** 2 + j_changed ** 2 / self.longckm ** 2) * 2 * np.pi
        return omga

    def __initial__filter__(self):
        wh = self.omga.max() * self.wh
        nrow, ncol = self.vgg.shape
        filter = np.ones((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                if self.omga[i, j] > wh:
                    swh = self.omga[i, j] / wh
                    filter[i, j] = swh ** (1 - self.alpha) - (1 - self.alpha) * np.log(swh) * swh ** (1 - self.alpha)
        return filter

    @classmethod
    def twkey(cls, layer, truncate=0.1):
        nrow, ncol = layer.shape
        twk = np.array([item1 * item2 for item1 in tukey(nrow, truncate) for item2 in tukey(ncol, truncate)]).reshape(
            (nrow, ncol))
        return twk * layer

    def bnd_k_n(self, k, n, truncate=0.1):
        name = '%d-%d' % (k, n)
        if self.temp.get(name) is None:
            bnd = self.bnds.get(k)
            bnd_twkey = self.twkey(bnd, truncate=truncate)
            bnd_twkey_n = bnd_twkey ** n
            bnd_fourier = fft2(bnd_twkey_n)
            self.temp[name] = bnd_fourier
        else:
            bnd_fourier = self.temp.get(name)
        return bnd_fourier

    def vgg_fft(self, truncate=0.1):
        name = 'vgg-ft'
        if self.temp.get(name) is None:
            vgg_ft = fft2(self.twkey(self.vgg, truncate=truncate))
            self.temp[name] = vgg_ft
        else:
            vgg_ft = self.temp.get(name)
        return vgg_ft

    def once_downward(self, target_bnd, t, truncate=0.1):
        self.bnds[self.target_layer] = target_bnd
        fft = -self.vgg_fft(truncate=truncate) / 2 / np.pi / self.G / \
              (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1]) / np.exp(-self.omga * self.observation_plane)
        for k in range(self.K):
            if k != self.target_layer:
                fft = fft - (self.rhos[k] - self.rhos[k+1]) / (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1])\
                      * self.bnd_k_n(k, n=1, truncate=truncate)
        fft2 = 0
        for k in range(self.K):
            factor_kj = (self.rhos[k] - self.rhos[k+1]) / (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1])
            for n in range(2, t + 1):
                fft2 = fft2 + factor_kj * self.omga ** (n - 1) / factorial(n) * self.bnd_k_n(k, n=n, truncate=truncate)
        fft3 = fft - fft2
        fft3[0, 0] = 0
        return ifft2(fft3 * self.filter).real + self.target_depth

    def downward(self, t=10, truncate=0.1):
        target_bnd = self.once_downward(target_bnd=0, t=1, truncate=truncate)
        if t == 1:
            return target_bnd
        else:
            for n in range(2, t+1):
                target_bnd = self.once_downward(target_bnd=target_bnd, t=n, truncate=truncate)
            return target_bnd


class ChaoI(Bnd):
    def __init__(self, vgg, bnds, rhos, observation_plane, longrkm, longckm, wh, alpha, target_layer=2, target_depth=0):
        super(ChaoI, self).__init__(vgg, bnds, rhos, observation_plane, longrkm, longckm)
        self.K = max(self.rhos.keys())
        self.G = 6.67
        self.wh = wh
        self.alpha = alpha
        self.target_layer = target_layer
        self.target_depth = target_depth
        self.omga = self.__initial__omga__()
        self.filter = self.__initial__filter__()
        self.ave_depth = self.__initial__ave_depth__()
        # temp
        self.temp = {}

    def __initial__omga__(self):
        nrow, ncol = [item.shape for item in self.bnds.values()][0]
        omga = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                i_changed = i if i <= nrow / 2 else i - nrow
                j_changed = j if j <= ncol / 2 else j - ncol
                omga[i, j] = np.sqrt(i_changed ** 2 / self.longrkm ** 2 + j_changed ** 2 / self.longckm ** 2) * 2 * np.pi
        return omga

    def __initial__filter__(self):
        wh = self.omga.max() * self.wh
        nrow, ncol = self.vgg.shape
        filter = np.ones((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                if self.omga[i, j] > wh:
                    swh = self.omga[i, j] / wh
                    filter[i, j] = swh ** (1 - self.alpha) - (1 - self.alpha) * np.log(swh) * swh ** (1 - self.alpha)
        return filter

    def __initial__ave_depth__(self):
        ave_depth = {key: value.mean() for key, value in self.bnds.items()}
        ave_depth[self.target_layer] = self.target_depth
        return ave_depth

    @classmethod
    def twkey(cls, layer, truncate=0.1):
        nrow, ncol = layer.shape
        twk = np.array([item1 * item2 for item1 in tukey(nrow, truncate) for item2 in tukey(ncol, truncate)]).reshape(
            (nrow, ncol))
        return twk * layer

    def bnd_k_n(self, k, n, truncate=0.1):
        name = '%d-%d' % (k, n)
        if self.temp.get(name) is None:
            bnd = self.bnds.get(k)
            bnd_twkey = self.twkey(bnd - self.ave_depth[k], truncate=truncate)
            bnd_twkey_n = bnd_twkey ** n
            bnd_fourier = fft2(bnd_twkey_n)
            self.temp[name] = bnd_fourier
        else:
            bnd_fourier = self.temp.get(name)
        return bnd_fourier

    def vgg_fft(self, truncate=0.1):
        name = 'vgg-ft'
        if self.temp.get(name) is None:
            vgg_ft = fft2(self.twkey(self.vgg, truncate=truncate))
            self.temp[name] = vgg_ft
        else:
            vgg_ft = self.temp.get(name)
        return vgg_ft

    def once_downward(self, target_bnd, t, truncate=0.1):
        self.bnds[self.target_layer] = target_bnd
        fft = -self.vgg_fft(truncate=truncate) / 2 / np.pi / self.G / \
              (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1]) / \
              np.exp(-self.omga * (self.observation_plane - self.target_depth))
        for k in range(self.K):
            if k != self.target_layer:
                fft = fft - (self.rhos[k] - self.rhos[k+1]) / (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1])\
                      * self.bnd_k_n(k, n=1, truncate=truncate) * np.exp(self.omga * (self.ave_depth[k] - self.target_depth))
        fft2 = 0
        for k in range(self.K):
            factor_kj = (self.rhos[k] - self.rhos[k+1]) / (self.rhos[self.target_layer] - self.rhos[self.target_layer + 1]) * \
                        np.exp(self.omga * (self.ave_depth[k] - self.target_depth))
            for n in range(2, t + 1):
                fft2 = fft2 + factor_kj * self.omga ** (n - 1) / factorial(n) * self.bnd_k_n(k, n=n, truncate=truncate)
        fft3 = fft - fft2
        fft3[0, 0] = 0
        return ifft2(fft3 * self.filter).real + self.target_depth

    def downward(self, t=10, truncate=0.1):
        target_bnd = self.once_downward(target_bnd=0, t=1, truncate=truncate)
        if t == 1:
            return target_bnd
        else:
            for n in range(2, t+1):
                target_bnd = self.once_downward(target_bnd=target_bnd, t=n, truncate=truncate)
            return target_bnd


