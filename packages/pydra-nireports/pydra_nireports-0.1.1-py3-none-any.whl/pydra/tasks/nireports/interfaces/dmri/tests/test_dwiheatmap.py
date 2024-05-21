from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.dmri.dwi_heatmap import DWIHeatmap
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dwiheatmap_1():
    task = DWIHeatmap()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.scalarmap = File.sample(seed=1)
    task.inputs.mask_file = File.sample(seed=2)
    task.inputs.colormap = "YlGn"
    task.inputs.bins = [150, 11]
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
