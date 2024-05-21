from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.nireports.interfaces.reporting.base.simple_before_after_rpt import (
    SimpleBeforeAfterRPT,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_simplebeforeafterrpt_1():
    task = SimpleBeforeAfterRPT()
    task.inputs.before = File.sample(seed=0)
    task.inputs.after = File.sample(seed=1)
    task.inputs.wm_seg = File.sample(seed=2)
    task.inputs.before_label = "before"
    task.inputs.after_label = "after"
    task.inputs.dismiss_affine = False
    task.inputs.fixed_params = {}
    task.inputs.moving_params = {}
    task.inputs.out_report = "report.svg"
    task.inputs.compress_report = "auto"
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
