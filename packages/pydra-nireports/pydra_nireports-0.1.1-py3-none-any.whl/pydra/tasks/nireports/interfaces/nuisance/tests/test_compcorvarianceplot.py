from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.nuisance.comp_cor_variance_plot import (
    CompCorVariancePlot,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_compcorvarianceplot_1():
    task = CompCorVariancePlot()
    task.inputs.metadata_files = [File.sample(seed=0)]
    task.inputs.variance_thresholds = [0.5, 0.7, 0.9]
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
