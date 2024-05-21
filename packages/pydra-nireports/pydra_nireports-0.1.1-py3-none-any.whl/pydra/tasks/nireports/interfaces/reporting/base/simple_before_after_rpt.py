from fileformats.generic import File
import logging
from pathlib import Path
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)


@pydra.mark.task
@pydra.mark.annotate({"return": {"out_report": File}})
def SimpleBeforeAfterRPT(
    before: File,
    after: File,
    wm_seg: File,
    before_label: str,
    after_label: str,
    dismiss_affine: bool,
    fixed_params: dict,
    moving_params: dict,
    out_report: Path,
    compress_report: ty.Any,
) -> File:
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.nireports.interfaces.reporting.base.simple_before_after_rpt import SimpleBeforeAfterRPT

    """

    try:
        outputs = super(ReportCapableInterface, self)._list_outputs()
    except NotImplementedError:
        outputs = {}
    if self._out_report is not None:
        out_report = self._out_report

    return out_report


# Nipype methods converted into functions
