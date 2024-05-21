from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.mosaic.plot_contours import PlotContours
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_plotcontours_1():
    task = PlotContours()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.in_contours = File.sample(seed=1)
    task.inputs.cut_coords = 8
    task.inputs.levels = [0.5]
    task.inputs.colors = ["r"]
    task.inputs.display_mode = "ortho"
    task.inputs.saturate = False
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
