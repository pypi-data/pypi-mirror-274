import attrs
from fileformats.generic import File
import logging
from pydra.tasks.nireports.reportlets.mosaic import plot_mosaic
import os
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def PlotMosaic(
    bbox_mask_file: File,
    only_noise: bool,
    view: list,
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
    >>> from pydra.tasks.nireports.interfaces.mosaic.plot_mosaic import PlotMosaic

    """
    mask = bbox_mask_file if (bbox_mask_file is not attrs.NOTHING) else None

    title = title if (title is not attrs.NOTHING) else None

    plot_mosaic(
        in_file,
        out_file=out_file,
        title=title,
        only_plot_noise=only_noise,
        bbox_mask_file=mask,
        cmap=cmap,
        annotate=annotate,
        views=view,
    )
    out_file = str((Path(os.getcwd()) / out_file).resolve())

    return out_file


# Nipype methods converted into functions
