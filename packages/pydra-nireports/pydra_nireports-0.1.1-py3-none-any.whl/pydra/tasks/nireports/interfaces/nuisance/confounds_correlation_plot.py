import attrs
from fileformats.generic import File
import logging
from pydra.tasks.nireports.nipype_ports.utils.filemanip import fname_presuffix
from pydra.tasks.nireports.reportlets.nuisance import confounds_correlation_plot
import os
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_file": File}})
def ConfoundsCorrelationPlot(
    confounds_file: File,
    out_file: ty.Any,
    reference_column: str,
    columns: list,
    max_dim: int,
    ignore_initial_volumes: int,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.nuisance.confounds_correlation_plot import ConfoundsCorrelationPlot

    """
    if out_file is None:
        out_file = fname_presuffix(
            confounds_file,
            suffix="_confoundCorrelation.svg",
            use_ext=False,
            newpath=os.getcwd(),
        )
    else:
        out_file = out_file
    confounds_correlation_plot(
        confounds_file=confounds_file,
        columns=columns if (columns is not attrs.NOTHING) else None,
        max_dim=max_dim,
        output_file=out_file,
        reference=reference_column,
        ignore_initial_volumes=ignore_initial_volumes,
    )

    return out_file


# Nipype methods converted into functions
