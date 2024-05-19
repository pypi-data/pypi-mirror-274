from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.threshold import Threshold
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_threshold_1():
    task = Threshold()
    task.inputs.direction = "below"
    task.inputs.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
