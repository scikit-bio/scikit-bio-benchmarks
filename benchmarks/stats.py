""""Benchmarks on skbio.stats"""

from skbio.stats.distance import randdm, permanova

import numpy as np

class DistanceSuite:

    def setup(self):
        dm_size = 6000
        self.dm = randdm(dm_size, random_fn=42)
        rng = np.random.default_rng(seed=42)
        self.groups = rng.integers(2, size=dm_size)

    def time_permanova(self):
        return permanova(self.dm, self.groups)
