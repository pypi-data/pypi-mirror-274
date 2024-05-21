from .modality import fMRIPlot, plot_heatmap
from .mosaic import (
    plot_mosaic,
    plot_segmentation,
    plot_slice,
    plot_slice_tern,
    plot_spikes,
)
from .nuisance import (
    _ward_to_linkage,
    confoundplot,
    confounds_correlation_plot,
    plot_carpet,
    spikesplot,
)
from .utils import _bbox, _get_limits, get_parula
from .xca import compcor_variance_plot
