from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.av_scale import AvScale
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_avscale_1():
    task = AvScale()
    task.inputs.mat_file = File.sample(seed=1)
    task.inputs.ref_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
