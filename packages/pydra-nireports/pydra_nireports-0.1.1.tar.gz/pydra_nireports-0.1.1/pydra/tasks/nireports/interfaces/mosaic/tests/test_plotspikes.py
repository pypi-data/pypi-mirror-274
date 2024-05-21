from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.mosaic.plot_spikes import PlotSpikes
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_plotspikes_1():
    task = PlotSpikes()
    task.inputs.in_spikes = File.sample(seed=0)
    task.inputs.in_fft = File.sample(seed=1)
    task.inputs.in_file = File.sample(seed=2)
    task.inputs.annotate = True
    task.inputs.figsize = [11.69, 8.27]
    task.inputs.dpi = 300
    task.inputs.out_file = "mosaic.svg"
    task.inputs.cmap = "Greys_r"
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
