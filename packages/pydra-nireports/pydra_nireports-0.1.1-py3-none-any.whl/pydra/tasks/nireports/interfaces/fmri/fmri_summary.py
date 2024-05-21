import attrs
from fileformats.generic import File
import logging
import nibabel as nb
from pydra.tasks.nireports.nipype_ports.utils.filemanip import fname_presuffix
from pydra.tasks.nireports.reportlets.modality.func import fMRIPlot
from pydra.tasks.nireports.tools.timeseries import (
    cifti_timeseries,
    get_tr,
    nifti_timeseries,
)
import numpy as np
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def FMRISummary(
    in_func: File,
    in_spikes_bg: File,
    fd: File,
    dvars: File,
    outliers: File,
    in_segm: File,
    tr: ty.Any,
    fd_thres: float,
    drop_trs: int,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.fmri.fmri_summary import FMRISummary

    """
    import pandas as pd

    out_file = fname_presuffix(
        in_func,
        suffix="_fmriplot.svg",
        use_ext=False,
        newpath=os.getcwd(),
    )

    dataframe = (
        pd.DataFrame(
            {
                "outliers": np.loadtxt(outliers, usecols=[0]).tolist(),
                # Pick non-standardize dvars (col 1)
                # First timepoint is NaN (difference)
                "DVARS": [np.nan] + np.loadtxt(dvars, skiprows=1, usecols=[1]).tolist(),
                # First timepoint is zero (reference volume)
                "FD": [0.0] + np.loadtxt(fd, skiprows=1, usecols=[0]).tolist(),
            }
        )
        if (
            (outliers is not attrs.NOTHING)
            and (dvars is not attrs.NOTHING)
            and (fd is not attrs.NOTHING)
        )
        else None
    )

    input_data = nb.load(in_func)
    seg_file = in_segm if (in_segm is not attrs.NOTHING) else None
    dataset, segments = (
        cifti_timeseries(input_data)
        if isinstance(input_data, nb.Cifti2Image)
        else nifti_timeseries(input_data, seg_file)
    )

    fig = fMRIPlot(
        dataset,
        segments=segments,
        spikes_files=([in_spikes_bg] if (in_spikes_bg is not attrs.NOTHING) else None),
        tr=(tr if (tr is not attrs.NOTHING) else get_tr(input_data)),
        confounds=dataframe,
        units={"outliers": "%", "FD": "mm"},
        vlines={"FD": [fd_thres]},
        nskip=drop_trs,
    ).plot()
    fig.savefig(out_file, bbox_inches="tight")

    return out_file


# Nipype methods converted into functions
