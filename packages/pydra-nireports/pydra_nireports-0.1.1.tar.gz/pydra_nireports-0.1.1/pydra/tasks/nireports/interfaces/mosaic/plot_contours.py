import attrs
from fileformats.generic import File
import logging
from pydra.tasks.nireports.reportlets.mosaic import plot_segmentation
import os
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def PlotContours(
    in_file: File,
    in_contours: File,
    cut_coords: int,
    levels: list,
    colors: list,
    display_mode: ty.Any,
    saturate: bool,
    out_file: Path,
    vmin: float,
    vmax: float,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.mosaic.plot_contours import PlotContours

    """
    in_file_ref = Path(in_file)

    if out_file is not attrs.NOTHING:
        in_file_ref = Path(out_file)

    fname = in_file_ref.name.rstrip("".join(in_file_ref.suffixes))
    out_file = (Path(os.getcwd()) / ("plot_%s_contours.svg" % fname)).resolve()
    out_file = str(out_file)

    vmax = None if (vmax is attrs.NOTHING) else vmax
    vmin = None if (vmin is attrs.NOTHING) else vmin

    plot_segmentation(
        in_file,
        in_contours,
        out_file=str(out_file),
        cut_coords=cut_coords,
        display_mode=display_mode,
        levels=levels,
        colors=colors,
        saturate=saturate,
        vmin=vmin,
        vmax=vmax,
    )

    return out_file


# Nipype methods converted into functions
