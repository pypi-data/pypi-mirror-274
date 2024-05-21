from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.mosaic.plot_mosaic import PlotMosaic
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_plotmosaic_1():
    task = PlotMosaic()
    task.inputs.bbox_mask_file = File.sample(seed=0)
    task.inputs.only_noise = False
    task.inputs.view = ["axial", "sagittal"]
    task.inputs.in_file = File.sample(seed=3)
    task.inputs.annotate = True
    task.inputs.figsize = [11.69, 8.27]
    task.inputs.dpi = 300
    task.inputs.out_file = "mosaic.svg"
    task.inputs.cmap = "Greys_r"
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
