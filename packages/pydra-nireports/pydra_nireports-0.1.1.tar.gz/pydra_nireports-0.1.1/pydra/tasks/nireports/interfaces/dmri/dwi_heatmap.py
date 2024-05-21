import attrs
from fileformats.generic import File
import logging
import nibabel as nb
from pydra.tasks.nireports.nipype_ports.utils.filemanip import fname_presuffix
from pydra.tasks.nireports.reportlets.modality.dwi import plot_heatmap
import numpy as np
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def DWIHeatmap(
    in_file: File,
    scalarmap: File,
    mask_file: File,
    b_indices: dict,
    threshold: float,
    subsample: int,
    sigma: float,
    colormap: str,
    scalarmap_label: str,
    bins: ty.Any,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.dmri.dwi_heatmap import DWIHeatmap

    """
    gtable = b_indices
    threshold = None if (threshold is attrs.NOTHING) else threshold
    subsample = None if (subsample is attrs.NOTHING) else subsample
    sigma = None if (sigma is attrs.NOTHING) else sigma
    scalarmap_label = None if (scalarmap_label is attrs.NOTHING) else scalarmap_label

    out_figure = plot_heatmap(
        nb.load(in_file).get_fdata(dtype="float32"),
        list(gtable.values()),
        list(gtable.keys()),
        np.abs(np.asanyarray(nb.load(mask_file).dataobj) - 1) < 1e-3,
        nb.load(scalarmap).get_fdata(dtype="float32"),
        scalar_label=scalarmap_label,
        imax=threshold,
        sub_size=subsample,
        sigma=sigma,
        cmap=colormap,
        bins=bins,
    )

    out_file = fname_presuffix(
        in_file,
        newpath=os.getcwd(),
        suffix="heatmap.svg",
        use_ext=False,
    )

    out_figure.savefig(out_file, format="svg", dpi=300)

    return out_file


# Nipype methods converted into functions
