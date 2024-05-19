from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.maths.apply_mask import ApplyMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applymask_1():
    task = ApplyMask()
    task.inputs.mask_file = Mask__NiftiGz.sample(seed=0)
    task.inputs.in_file = NiftiGz.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
