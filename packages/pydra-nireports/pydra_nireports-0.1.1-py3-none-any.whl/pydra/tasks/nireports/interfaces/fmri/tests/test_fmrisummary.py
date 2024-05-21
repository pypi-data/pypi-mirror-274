from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.fmri.fmri_summary import FMRISummary
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fmrisummary_1():
    task = FMRISummary()
    task.inputs.in_func = File.sample(seed=0)
    task.inputs.in_spikes_bg = File.sample(seed=1)
    task.inputs.fd = File.sample(seed=2)
    task.inputs.dvars = File.sample(seed=3)
    task.inputs.outliers = File.sample(seed=4)
    task.inputs.in_segm = File.sample(seed=5)
    task.inputs.fd_thres = 0.2
    task.inputs.drop_trs = 0
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
