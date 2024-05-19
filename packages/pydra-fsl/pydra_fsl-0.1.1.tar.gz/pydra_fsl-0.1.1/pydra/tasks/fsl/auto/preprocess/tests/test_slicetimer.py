from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.preprocess.slice_timer import SliceTimer
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_slicetimer_1():
    task = SliceTimer()
    task.inputs.in_file = File.sample(seed=0)
    task.inputs.custom_timings = File.sample(seed=6)
    task.inputs.custom_order = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
