from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.auto.utils.inv_warp import InvWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_invwarp_1():
    task = InvWarp()
    task.inputs.warp = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_invwarp_2():
    task = InvWarp()
    task.inputs.warp = Nifti1.sample(seed=0)
    task.inputs.reference = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(plugin=PassAfterTimeoutWorker)
    print("RESULT: ", res)
