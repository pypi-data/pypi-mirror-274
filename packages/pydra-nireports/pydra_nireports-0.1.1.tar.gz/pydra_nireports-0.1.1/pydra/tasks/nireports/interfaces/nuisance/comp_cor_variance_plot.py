from fileformats.generic import File
import logging
from pydra.tasks.nireports.nipype_ports.utils.filemanip import fname_presuffix
from pydra.tasks.nireports.reportlets.xca import compcor_variance_plot
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def CompCorVariancePlot(
    metadata_files: ty.List[File],
    metadata_sources: list,
    variance_thresholds: ty.Any,
    out_file: ty.Any,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.nuisance.comp_cor_variance_plot import CompCorVariancePlot

    """
    if out_file is None:
        out_file = fname_presuffix(
            metadata_files[0],
            suffix="_compcor.svg",
            use_ext=False,
            newpath=os.getcwd(),
        )
    else:
        out_file = out_file
    compcor_variance_plot(
        metadata_files=metadata_files,
        metadata_sources=metadata_sources,
        output_file=out_file,
        varexp_thresh=variance_thresholds,
    )

    return out_file


# Nipype methods converted into functions
