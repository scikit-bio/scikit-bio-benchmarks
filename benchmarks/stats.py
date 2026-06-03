"""Benchmarks on skbio.stats"""

import numpy as np
import pandas as pd

from skbio.stats.distance import randdm, permanova, anosim, permdisp, mantel
from skbio.stats.ordination import pcoa, cca, rda, pcoa_biplot
from skbio.stats.composition import alr, clr, ilr, multi_replace, dirmult_ttest, ancom
from skbio.stats import subsample_counts


class Distance:
    def setup(self):
        # asv times out if the size is too large, adjust as necessary
        size = 500
        self.dm = randdm(size)
        self.dm2 = randdm(size)
        rng = np.random.default_rng(seed=42)
        self.groups = rng.integers(2, size=size)

    def time_permanova(self):
        return permanova(self.dm, self.groups)

    def time_anosim(self):
        return anosim(self.dm, self.groups)

    def time_permdisp(self):
        return permdisp(self.dm, self.groups)

    def time_mantel(self):
        return mantel(self.dm, self.dm2)


class Ordination:
    def setup(self):
        # size = number of samples
        size = 500
        self.ids = [f"s{i}" for i in range(size)]
        self.dm = randdm(size, ids=self.ids)
        # use Pandas for compatibility across skbio versions
        self.y = pd.DataFrame(data=np.random.rand(size, 1000), index=self.ids)
        self.x = pd.DataFrame(data=np.random.rand(size, 5), index=self.ids)
        self.res = pcoa(self.dm)

    def time_pcoa(self):
        return pcoa(self.dm)

    def time_cca(self):
        return cca(self.y, self.x)

    def time_rda(self):
        return rda(self.y, self.x)

    # old versions of pcoa_biplot fail
    def _disabled_time_pcoa_biplot(self):
        return pcoa_biplot(self.res, self.x)


class Composition:
    def setup(self):
        size = 500
        n_feats = 50
        self.mat = np.random.rand(size, n_feats)
        self.df = pd.DataFrame(data=self.mat)
        # make a random matrix with some zeros in it
        self.mat_z = self.mat * (self.mat > 0.2)
        rng = np.random.default_rng(seed=42)
        self.groups = pd.Series(data=rng.integers(2, size=size).astype(str))

    def time_clr(self):
        return clr(self.mat)

    def time_alr(self):
        return alr(self.mat)

    def time_ilr(self):
        return ilr(self.mat)

    def time_multi_replace(self):
        return multi_replace(self.mat_z)

    def time_ancom(self):
        return ancom(self.df, self.groups)
    # give ancom 2 minutes before timing out (default is 60s)
    time_ancom.timeout = 120.0

    def time_dirmult_ttest(self):
        return dirmult_ttest(self.df, self.groups, treatment="0", reference="1")
    # give dirmult_ttest 2 minutes before timing out (default is 60s)
    time_dirmult_ttest.timeout = 120.0


class Subsample:
    def setup(self):
        size = 1000
        self.counts = np.random.default_rng().integers(low=0, high=100, size=size)

    def time_subsample_counts(self):
        return subsample_counts(self.counts, 100)
