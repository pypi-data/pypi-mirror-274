import logging
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from pydra.tasks.nireports.reportlets.nuisance import (
    confoundplot,
    plot_carpet,
    spikesplot,
)
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class fMRIPlot:
    """Generates the fMRI Summary Plot."""

    __slots__ = (
        "timeseries",
        "segments",
        "tr",
        "confounds",
        "spikes",
        "nskip",
        "sort_carpet",
        "paired_carpet",
    )

    def __init__(
        self,
        timeseries,
        segments,
        confounds=None,
        conf_file=None,
        tr=None,
        usecols=None,
        units=None,
        vlines=None,
        spikes_files=None,
        nskip=0,
        sort_carpet=True,
        paired_carpet=False,
    ):

        self.timeseries = timeseries
        self.segments = segments
        self.tr = tr
        self.nskip = nskip
        self.sort_carpet = sort_carpet
        self.paired_carpet = paired_carpet
        if units is None:
            units = {}
        if vlines is None:
            vlines = {}
        self.confounds = {}
        if confounds is None and conf_file:
            confounds = pd.read_csv(
                conf_file, sep=r"[\t\s]+", usecols=usecols, index_col=False
            )
        if confounds is not None:
            for name in confounds.columns:
                self.confounds[name] = {
                    "values": confounds[[name]].values.squeeze().tolist(),
                    "units": units.get(name),
                    "cutoff": vlines.get(name),
                }
        self.spikes = []
        if spikes_files:
            for sp_file in spikes_files:
                self.spikes.append((np.loadtxt(sp_file), None, False))

    def plot(self, figure=None):
        """Main plotter"""
        import seaborn as sns

        sns.set_style("whitegrid")
        sns.set_context("paper", font_scale=0.8)
        if figure is None:
            figure = plt.gcf()
        nconfounds = len(self.confounds)
        nspikes = len(self.spikes)
        nrows = 1 + nconfounds + nspikes
        # Create grid
        grid = GridSpec(
            nrows, 1, wspace=0.0, hspace=0.05, height_ratios=[1] * (nrows - 1) + [5]
        )
        grid_id = 0
        for tsz, name, iszs in self.spikes:
            spikesplot(
                tsz, title=name, outer_gs=grid[grid_id], tr=self.tr, zscored=iszs
            )
            grid_id += 1
        if self.confounds:
            from seaborn import color_palette

            palette = color_palette("husl", nconfounds)
        for i, (name, kwargs) in enumerate(self.confounds.items()):
            tseries = kwargs.pop("values")
            confoundplot(
                tseries,
                grid[grid_id],
                tr=self.tr,
                color=palette[i],
                name=name,
                **kwargs
            )
            grid_id += 1
        plot_carpet(
            self.timeseries,
            segments=self.segments,
            subplot=grid[-1],
            tr=self.tr,
            sort_rows=self.sort_carpet,
            drop_trs=self.nskip,
            cmap="paired" if self.paired_carpet else None,
        )
        return figure
