from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.preprocess.apply_warp import ApplyWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applywarp_1():
    task = ApplyWarp()
    task.inputs.in_file = NiftiGz.sample(seed=0)
    task.inputs.ref_file = NiftiGz.sample(seed=2)
    task.inputs.field_file = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
