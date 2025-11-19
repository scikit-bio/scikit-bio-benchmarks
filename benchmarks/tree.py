"""Benchmarks on skbio.tree"""

from skbio.stats.distance import randdm
from skbio.tree import nj

from asv_runner.benchmarks.mark import SkipNotImplemented

class Tree:
    def setup(self):
        size = 250
        self.dm = randdm(size)

        # bme and gme aren't available in all versions of skbio being benchmarked.
        # Need to make sure that an ImportError doesn't occur otherwise none of the benchmarks
        # here will run.
        try:
            from skbio.tree import bme
            self.bme = bme
            self.bme_available = True
        except ImportError:
            self.bme = None
            self.bme_available = False

        try:
            from skbio.tree import gme
            self.gme = gme
            self.gme_available = True
        except ImportError:
            self.gme = None
            self.gme_available = False

    def time_nj(self):
        return nj(self.dm)

    def time_bme(self):
        if not self.bme_available:
            raise SkipNotImplemented("bme not available")
        return self.bme(self.dm)

    def time_gme(self):
        if not self.gme_available:
            raise SkipNotImplemented("gme not available")
        return self.gme(self.dm)
