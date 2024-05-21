from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.nuisance.confounds_correlation_plot import (
    ConfoundsCorrelationPlot,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_confoundscorrelationplot_1():
    task = ConfoundsCorrelationPlot()
    task.inputs.confounds_file = File.sample(seed=0)
    task.inputs.reference_column = "global_signal"
    task.inputs.max_dim = 20
    task.inputs.ignore_initial_volumes = 0
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
