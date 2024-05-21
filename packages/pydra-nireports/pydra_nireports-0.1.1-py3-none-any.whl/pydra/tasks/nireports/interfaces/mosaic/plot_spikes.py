from fileformats.generic import File
import logging
from pydra.tasks.nireports.reportlets.mosaic import plot_spikes
import numpy as np
import os
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def PlotSpikes(
    in_spikes: File,
    in_fft: File,
    in_file: File,
    title: str,
    annotate: bool,
    figsize: ty.Any,
    dpi: int,
    out_file: Path,
    cmap: str,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.mosaic.plot_spikes import PlotSpikes

    """
    out_file = str((Path(os.getcwd()) / out_file).resolve())
    out_file = out_file

    spikes_list = np.loadtxt(in_spikes, dtype=int).tolist()
    # No spikes
    if not spikes_list:
        Path(out_file).write_text(
            "<p>No high-frequency spikes were found in this dataset</p>"
        )
        return runtime

    spikes_list = [tuple(i) for i in np.atleast_2d(spikes_list).tolist()]
    plot_spikes(
        in_file,
        in_fft,
        spikes_list,
        out_file=out_file,
    )

    return out_file


# Nipype methods converted into functions
