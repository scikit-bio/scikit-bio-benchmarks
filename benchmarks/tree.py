"""Benchmarks on skbio.tree"""

from skbio.stats.distance import randdm
from skbio.tree import nj
from asv_runner.benchmarks.mark import skip_benchmark_if


class Tree:
    def setup(self):
        size = 500
        self.dm = randdm(size)

        # bme and gme aren't available in all versions of skbio being benchmarked.
        # Need to make sure that an ImportError doesn't occur otherwise none of the benchmarks
        # here will run.
        bme_available = True
        self.bme = None
        try:
            from skbio.tree import bme
            self.bme = bme
        except ImportError:
            self.bme_available = False

        gme_available = True
        self.gme = None
        try:
            from skbio.tree import gme
            self.gme = gme
        except ImportError:
            self.gme_available = False

    def time_nj(self):
        return nj(self.dm)

    @skip_benchmark_if(not bme_available)
    def time_bme(self):
        return self.bme(self.dm)

    @skip_benchmark_if(not gme_available)
    def time_gme(self):
        return self.gme(self.dm)
